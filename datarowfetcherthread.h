#ifndef DATAROWFETCHERTHREAD_H
#define DATAROWFETCHERTHREAD_H

#include <QThread>
#include <deque>
#include "icardata.h"
#include <QMutex>
#include <QMutexLocker>

class DataRowFetcherThread : public QThread {
public:
    DataRowFetcherThread(unsigned latency, unsigned capacity);

    void setCarAndStorage(ICarData* car, std::deque<CarState>* dataRows);
    void run() override;

private:
    unsigned latency;
    unsigned capacity;
    ICarData* car = nullptr;
    std::deque<CarState>* dataRows = nullptr;
    QMutex accessLock;
};

#endif  // DATAROWFETCHERTHREAD_H
