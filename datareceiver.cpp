#include "datareceiver.h"
#include <iostream>

void DataReceiver::enqueueData(const CanData& newData) {
    std::lock_guard<std::mutex> lock(queueMutex);
    dataQueue.push_back(newData);
    std::cout << "[DataReceiver] Data enqueued. Queue size: " << dataQueue.size() << std::endl;
}

CanData DataReceiver::askForNewData() {
    std::lock_guard<std::mutex> lock(queueMutex);

    if (dataQueue.empty()) {
        return CanData();  // Возвращаем пустой объект
    }

    CanData newData = dataQueue.front();
    dataQueue.pop_front();
    std::cout << "[DataReceiver] Data dequeued. Queue size: " << dataQueue.size() << std::endl;

    return newData;
}
