#include "autodetectingreceiver.h"
#include "arduinoproxyreceiver.h"
#include <QFile>
#include <iostream>
#include <filereceiver.h>

AutoDetectingReceiver::AutoDetectingReceiver(const QString& fallbackCsvPath, std::deque<CarState>* storage) {
    std::cout << "[AutoDetectingReceiver] Checking for /dev/ttyUSB0..." << std::endl;

    if (QFile::exists("/dev/ttyUSB0")) {
        std::cout << "[AutoDetectingReceiver] Arduino device detected, using ArduinoProxyReceiver" << std::endl;
        arduinoReceiver = new ArduinoProxyReceiver("/dev/ttyUSB0", nullptr);
        activeReceiver = arduinoReceiver;
        fileReceiver = nullptr;
    } else {
        std::cerr << "[AutoDetectingReceiver] No Arduino found, falling back to file: "
                  << fallbackCsvPath.toStdString() << std::endl;
        arduinoReceiver = nullptr;
        fileReceiver = new FileReceiver(fallbackCsvPath, storage);
        activeReceiver = fileReceiver;
    }
}

AutoDetectingReceiver::~AutoDetectingReceiver() {
    delete arduinoReceiver;
    delete fileReceiver;
}

void AutoDetectingReceiver::attachCarData(ICarData* car) {
    if (fileReceiver) fileReceiver->attachCarData(car);
    if (arduinoReceiver) arduinoReceiver->attachCarData(car);
}

CanData AutoDetectingReceiver::askForNewData() {
    return activeReceiver->askForNewData();
}

void AutoDetectingReceiver::enqueueData(const CanData& newData) {
    activeReceiver->enqueueData(newData);
}
