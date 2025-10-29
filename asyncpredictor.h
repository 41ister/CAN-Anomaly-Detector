#ifndef ASYNCPREDICTOR_H
#define ASYNCPREDICTOR_H

#include <thread>
#include <mutex>
#include <queue>
#include <condition_variable>
#include "anomalypredictorlstm.h"
#include "csvanomalylogger.h"
#include "icardata.h"

class AsyncPredictionController : public ICanSubscriber {
public:
    AsyncPredictionController(AnomalyPredictorLSTM* predictor, CsvAnomalyLogger* logger);
    ~AsyncPredictionController() { stop(); }

    void start();
    void stop();

    void enqueueData(const CarState& data);

    // Реализация интерфейса ICanSubscriber
    void onCarStateUpdate(const CarState& state) override;
private:
    void predictionLoop();
    void loggingLoop();

    AnomalyPredictorLSTM* predictor;
    CsvAnomalyLogger* logger;

    std::thread predThread;
    std::thread logThread;
    std::mutex queueMutex;
    std::condition_variable queueCond;

    std::queue<CarState> inputQueue;
    std::queue<CarState> confirmedAnomalies;

    bool running;
};

#endif // ASYNCPREDICTOR_H
