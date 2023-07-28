#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "reader.h"
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <fstream> 
#include <lsl_cpp.h>

MainWindow::MainWindow(QWidget *parent, const std::string &config_file, const bool linkOnStart)
	: QMainWindow(parent), ui(new Ui::MainWindow) {
	ui->setupUi(this);
	connect(ui->actionLoad_Configuration, &QAction::triggered, [this]() {
		load_config(QFileDialog::getOpenFileName(
			this, "Load Configuration File", "", "Configuration Files (*.cfg)"));
	});
	connect(ui->actionSave_Configuration, &QAction::triggered, [this]() {
		save_config(QFileDialog::getSaveFileName(
			this, "Save Configuration File", "", "Configuration Files (*.cfg)"));
	});
	connect(ui->btn_dll, &QPushButton::clicked, [this]() {
		auto dllpath = QFileDialog::getOpenFileName(this, "Select eego-SDK.dll",
			QCoreApplication::applicationDirPath(), "SDK dll (eego-SDK.dll)");
		this->ui->input_dll->setText(dllpath);
	});
	connect(ui->actionQuit, &QAction::triggered, this, &MainWindow::close);
	connect(ui->linkButton, &QPushButton::clicked, this, &MainWindow::link);
	if(!config_file.empty()) load_config(QString::fromStdString(config_file));
	if(linkOnStart) link();
}

void MainWindow::load_config(const QString &filename) {
	using boost::property_tree::ptree;
	ptree pt;

	// parse file
	try {
		read_xml(filename.toStdString(), pt);
	}
	catch (std::exception &e) {
		QMessageBox::information(this, "Error", (std::string("Cannot read config file: ") += e.what()).c_str(), QMessageBox::Ok);
		return;
	}

	// get config values
	try {
		ui->samplingRate->setCurrentIndex(pt.get<int>("settings.samplingrate", 3));
	}
	catch (std::exception &) {
		QMessageBox::information(this, "Error in Config File", "Could not read out config parameters.", QMessageBox::Ok);
		return;
	}
}

void MainWindow::save_config(const QString &filename) {
	using boost::property_tree::ptree;
	ptree pt;

	// transfer UI content into property tree
	try {
		pt.put("settings.samplingrate", ui->samplingRate->currentIndex());
	}
	catch (std::exception &e) {
		QMessageBox::critical(this, "Error", (std::string("Could not prepare settings for saving: ") += e.what()).c_str(), QMessageBox::Ok);
	}

	// write to disk
	try {
		write_xml(filename.toStdString(), pt);
	}
	catch (std::exception &e) {
		QMessageBox::critical(this, "Error", (std::string("Could not write to config file: ") += e.what()).c_str(), QMessageBox::Ok);
	}
}

void MainWindow::closeEvent(QCloseEvent *ev) {
	if (reader) {
		QMessageBox::warning(this, "Recording still running", "Can't quit while recording");
		ev->ignore();
	}
}


void MainWindow::link() {
	if (reader != nullptr) {
		reader->setStop(true);
		ui->linkButton->setText("Link");
	}
	else {
		// === perform link action ===
		try {
			// get the UI parameters...
			QString sr = ui->samplingRate->currentText();
			int samplingRate = sr.toInt();// boost::lexical_cast<int>(sr);
			
			auto dllpath = ui->input_dll->text();
			if(!QFile::exists(dllpath)) throw std::runtime_error("eego-SDK.dll wasn't found.");
			thread = new QThread;
			reader = new Reader(dllpath.toStdString());

			reader->setParams(samplingRate);

			reader->moveToThread(thread);
			connect(thread, &QThread::started, reader, &Reader::read);
			connect(reader, &Reader::finished, thread, &QThread::quit);
			connect(thread, &QThread::finished, this, &MainWindow::threadFinished);
			connect(reader, &Reader::finished, reader, &Reader::deleteLater);
			connect(thread, &QThread::finished, thread, &QThread::deleteLater);
			connect(reader, &Reader::timeout, this, &MainWindow::threadTimeout);
			connect(reader, &Reader::connectionLost, this, &MainWindow::connectionLost);
			connect(reader, &Reader::ampNotFound, this, &MainWindow::ampNotFound);
			thread->start();
		}
		catch (std::exception &e) {
			// try to decode the error message
			std::string msg = "Could not query driver message because the device is not open";
			QMessageBox::critical(this, "Error", ("Could not initialize the eego Sport interface: " + (e.what() + (" (driver message: " + msg + ")"))).c_str(), QMessageBox::Ok);
			return;
		}

		// done, all successful
		ui->linkButton->setText("Unlink");
	}
}

void MainWindow::threadFinished() {
	reader = nullptr;
	delete thread;
	thread = nullptr;
	ui->linkButton->setText("Link");
}

void MainWindow::threadTimeout() {
	QMessageBox::critical(this, "Error", (std::string("Error: eego Sport Conncetion timed out")).c_str(), QMessageBox::Ok);
}

void MainWindow::ampNotFound() {
	QMessageBox::critical(this, "Error", (std::string("Error: Amp not found or license file not present.Please connect the amplifier and make sure that the amp is turned on and a license file is present in 'My Documents/eego/")).c_str(), QMessageBox::Ok);
}

void MainWindow::connectionLost() {
	QMessageBox::critical(this, "Error", (std::string("Error: Amp connection lost")).c_str(), QMessageBox::Ok);
}

MainWindow::~MainWindow() noexcept = default;
