#ifndef ARDUINOPROXYRECEIVER_H
#define ARDUINOPROXYRECEIVER_H

#include <QSerialPort>
#include <QString>

#include "streamingreceiver.h"

class ArduinoProxyReceiver : public StreamingReceiver {
 public:
  ArduinoProxyReceiver(const QString &port, CanQueue *dataToProcess) {
    this->port = port;
    this->dataToProcess = dataToProcess;
    setup();
  }
  void setup();
  CanData askForNewData() override;
  virtual ~ArduinoProxyReceiver();
  bool isConnected() const { return true; }
  void attachCarData(ICarData* /*car*/) override {}
  void enqueueData(const CanData&) override {}

 private:
  QString port;
  QSerialPort *serial;
  CanQueue *dataToProcess;
};

#endif  // ARDUINOPROXYRECEIVER_H
