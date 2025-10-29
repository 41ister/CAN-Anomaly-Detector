#include "datareceiverthread.h"
#include <QThread>
#include <QtConcurrent>
#include "icardata.h"
#include "lockers.h"

void DataReceiverThread::run() {
  while (true) {
    CanData can = receiver->askForNewData();
    Lockers::monitor.lock();
    this->dataToProcess->push_back(can);
    Lockers::monitor.unlock();
    // notify
    Lockers::notifier = true;
    Lockers::cond_var.notify_one();
  }
}

DataReceiverThread::DataReceiverThread(DataReceiver *receiver,
                                       CanQueue *dataToProcess) {
  this->receiver = receiver;
  this->dataToProcess = dataToProcess;
  qDebug() << "creating a thread to handle data...\n";
}
