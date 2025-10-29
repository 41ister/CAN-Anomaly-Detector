#ifndef PREDICTWORKER_H
#define PREDICTWORKER_H

#ifdef slots
#undef slots
#endif

#include <QObject>

class PredictWorker : public QObject {
    Q_OBJECT

public:
    explicit PredictWorker(void* instance);

public Q_SLOTS:
    void run();

Q_SIGNALS:
    void finished(int result);

private:
    void* pInstance;
};

#endif // PREDICTWORKER_H
