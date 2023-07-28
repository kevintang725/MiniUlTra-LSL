#pragma once
#include <QObject>
#include <string>

namespace eemagine { namespace sdk { class amplifier; class stream; }}

class Reader : public QObject {
	Q_OBJECT
public:
	Reader(std::string dllpath): dllpath(std::move(dllpath)) {}
	virtual ~Reader() override;

	public slots:
	void read();
	void setStop(bool stop) {
		this->stop = stop;
	}
	void setParams(int samplingRate);

signals:
	void finished();
	void timeout();
	void ampNotFound();
	void connectionLost();

private:
	eemagine::sdk::amplifier* amp;
	eemagine::sdk::stream* eegStream;
	std::string dllpath;
	unsigned int samplingRate;
	bool stop{false};
};
