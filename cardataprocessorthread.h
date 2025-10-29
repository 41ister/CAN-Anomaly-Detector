#ifndef CARDATAPROCESSORTHREAD_H
#define CARDATAPROCESSORTHREAD_H

#include <QThread>
#include "icardata.h"

class carDataProcessorThread : public QThread {
    Q_OBJECT

public:
    carDataProcessorThread(ICarData *car, CanQueue *dataToProcess)
        : car(car), dataToProcess(dataToProcess) {}

protected:
    void run() override;

private:
    ICarData *car;
    CanQueue *dataToProcess;
};

#endif  // CARDATAPROCESSORTHREAD_H
