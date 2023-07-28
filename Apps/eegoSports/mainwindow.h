#ifndef MAINWINDOW_H
#define MAINWINDOW_H
#include <QMainWindow>
#include <QThread>
#include <QCloseEvent>
#include <QFileDialog>
#include <QMessageBox>
#include <memory> //for std::unique_ptr
#include <string>
#include <vector>

namespace Ui {
class MainWindow;
}

class Reader;

class MainWindow : public QMainWindow {
	Q_OBJECT

public:
	explicit MainWindow(QWidget *parent, const std::string &config_file, const bool linkOnStart);
	~MainWindow() noexcept override;

private slots:
	void threadFinished();
	void threadTimeout();
	void connectionLost();
	void ampNotFound();

	// start the eegosports connection
	void link();

	// close event (potentially disabled)
	void closeEvent(QCloseEvent *ev) override;
private:
	// background data reader thread
	void read_thread(std::string deviceNumber, int chunkSize, int samplingRate, bool isSlave, std::string serialNumber, int channelCount, std::vector<std::string> channelLabels);


	// raw config file IO
	void load_config(const QString &filename);
	void save_config(const QString &filename);

	Reader *reader{nullptr};
	std::unique_ptr<Ui::MainWindow> ui; // window pointer
	QThread *thread;
};

#endif // MAINWINDOW_H
