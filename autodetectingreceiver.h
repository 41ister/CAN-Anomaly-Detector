#ifndef AUTODETECTINGRECEIVER_H
#define AUTODETECTINGRECEIVER_H

#include "datareceiver.h"
#include "arduinoproxyreceiver.h"
#include "filereceiver.h"
#include "icardata.h"

class AutoDetectingReceiver : public DataReceiver {
public:
    AutoDetectingReceiver(const QString& fallbackCsvPath, std::deque<CarState>* storage);
    ~AutoDetectingReceiver();

    void attachCarData(ICarData* car) override;
    CanData askForNewData() override;
    void enqueueData(const CanData& newData) override;

private:
    DataReceiver* activeReceiver;
    ArduinoProxyReceiver* arduinoReceiver;
    FileReceiver* fileReceiver;
};

#endif // AUTODETECTINGRECEIVER_H
