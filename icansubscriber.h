#ifndef ICANSUBSCRIBER_H
#define ICANSUBSCRIBER_H

#include <QObject>
#include "icardata.h"

class ICanSubscriber {
public:
    virtual ~ICanSubscriber() {}
    virtual void onCarStateUpdate(const CarState& state) = 0;
};

class IAnomalySubscriber {
public:
    virtual ~IAnomalySubscriber() {}
    virtual void onAnomalyDetected(const CarState& state) = 0;
};

#endif // ICANSUBSCRIBER_H
