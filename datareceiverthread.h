#ifndef DATARECEIVERTHREAD_H
#define DATARECEIVERTHREAD_H

#include <QThread>
#include "datareceiver.h"

class DataReceiverThread : public QThread {
 private:
  // std::thread *impl;
  DataReceiver *receiver;
  CanQueue *dataToProcess;

  void run();

 public:
  DataReceiverThread(DataReceiver *receiver, CanQueue *dataToProcess);
};

#endif  // DATARECEIVERTHREAD_H
