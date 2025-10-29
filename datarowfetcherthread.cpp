#include "datarowfetcherthread.h"
#include <QDebug>
#include <QMutex>
#include <QMutexLocker>
#include <QDateTime>

DataRowFetcherThread::DataRowFetcherThread(unsigned latency, unsigned capacity)
    : latency(latency), capacity(capacity) {}

void DataRowFetcherThread::setCarAndStorage(ICarData* car, std::deque<CarState>* dataRows) {
    QMutexLocker locker(&accessLock);
    this->car = car;
    this->dataRows = dataRows;
}

void DataRowFetcherThread::run() {
    while (true) {
        QThread::msleep(latency);

        accessLock.lock();
        ICarData* localCar = this->car;
        std::deque<CarState>* localStorage = this->dataRows;
        accessLock.unlock();

        if (!localCar || !localStorage) {
            qWarning() << "[DataRowFetcherThread] car is null!";
            continue;
        }

        CarState state;
        state.timestamp = QDateTime::currentMSecsSinceEpoch();
        state.rpm = localCar->currentRPM();
        state.speed = localCar->currentSpeed();
        state.temp = localCar->currentEngineTemp();

        if (state.speed == 0 && state.rpm == 0 && state.temp == 0)
            continue;

        qDebug() << "Car state vector: <speed: " << state.speed
                 << " rpm: " << state.rpm
                 << " temp: " << state.temp << ">";

        QMutexLocker locker(&accessLock);
        if (localStorage->size() >= capacity)
            localStorage->pop_front();
        localStorage->push_back(state);
    }
}
