#include "reader.h"
#include <lsl_cpp.h>
#include <string>
// eegoSports
#define WIN32_LEAN_AND_MEAN
#define EEGO_SDK_BIND_DYNAMIC
#define _UNICODE
//#include <windows.h>
#include "eemagine/sdk/factory.h"

using namespace eemagine::sdk;

// --- DECONSTRUCTOR ---
Reader::~Reader() { }

void Reader::setParams(int sampling_rate) {
	this->samplingRate = sampling_rate;
}

// --- PROCESS ---
// Start processing data.
void Reader::read() {
	bool ampFound = true;
	try {
		factory fact(dllpath);
		amp = fact.getAmplifier();
		eegStream = amp->OpenEegStream(samplingRate);

		std::vector<channel> channelList = eegStream->getChannelList();

		// create data streaminfo and append some meta-data
		lsl::stream_info data_info("eegoSports " + amp->getSerialNumber(), "EEG", channelList.size() - 2, samplingRate, lsl::cf_float32, "eegoSports_" + amp->getSerialNumber());
		lsl::xml_element channels = data_info.desc().append_child("channels");

		for (int k = 0; k < channelList.size() - 2; k++) {
			channels.append_child("channel")
				.append_child_value("label", "Ch" + std::to_string(k))
				.append_child_value("type", "EEG")
				.append_child_value("unit", "microvolts");
		}
		data_info.desc().append_child("acquisition")
			.append_child_value("manufacturer", "antneuro")
			.append_child_value("serial_number", amp->getSerialNumber());

		// make a data outlet
		lsl::stream_outlet data_outlet(data_info);

		// create marker streaminfo and outlet
		lsl::stream_info marker_info("eegoSports-" + amp->getSerialNumber() + "_markers" + "Markers", "Markers", 1, 0, lsl::cf_string, "eegoSports_" + amp->getSerialNumber() + "_markers");
		lsl::stream_outlet marker_outlet(marker_info);

		std::vector<channel> eegChannelList = eegStream->getChannelList();

		int timeout_count = 0;
		while (!stop) {
			buffer buffer = eegStream->getData();
			auto channelCount = buffer.getChannelCount();
			auto sampleCount = buffer.size() / channelCount;
			std::vector<std::vector<float>> send_buffer(sampleCount, std::vector<float>(channelCount - 2));
			for (unsigned int s = 0; s < sampleCount; s++) {
				for (unsigned int c = 0; c < channelCount - 2; c++) {
					send_buffer[s][c] = buffer.getSample(c, s);
				}
			}
			double now = lsl::local_clock();
			data_outlet.push_chunk(send_buffer, now);

			unsigned int last_mrk = 0;
			for (unsigned int s = 0; s < sampleCount; s++) {
				//if (int mrk = src_buffer[channelCount + s*(channelCount + 1)]) {
				unsigned int mrk = buffer.getSample(channelCount - 2, s);
				if (mrk != last_mrk) {
					std::string mrk_string = std::to_string(mrk);
					marker_outlet.push_sample(&mrk_string, now + (s + 1 - sampleCount) / samplingRate);
					last_mrk = mrk;
				}
			}
		}
	}
	catch (exceptions::notFound) {
		ampFound = false;
		emit ampNotFound();
	}
	catch (exceptions::notConnected) {
		emit connectionLost();
	}
	catch (std::exception &e) {
	}
	if (ampFound) {
		delete eegStream;
		delete amp;
	}
	emit finished();
}
