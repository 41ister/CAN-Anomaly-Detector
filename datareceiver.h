#ifndef DATARECEIVER_H
#define DATARECEIVER_H

#include <deque>
#include <mutex>
#include "icardata.h"

class DataReceiver {
public:
    virtual void attachCarData(ICarData* /*car*/) {}
    virtual ~DataReceiver() = default;
    virtual void enqueueData(const CanData& newData) = 0;
    virtual CanData askForNewData() = 0;

private:
    std::deque<CanData> dataQueue;
    std::mutex queueMutex;
};

#endif // DATARECEIVER_H
