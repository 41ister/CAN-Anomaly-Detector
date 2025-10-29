#include "asyncpredictor.h"

AsyncPredictionController::AsyncPredictionController(AnomalyPredictorLSTM* predictor, CsvAnomalyLogger* logger)
    : predictor(predictor), logger(logger), running(false) {}

void AsyncPredictionController::start() {
    running = true;
    predThread = std::thread([this]() { predictionLoop(); });
    logThread = std::thread([this]() { loggingLoop(); });
}

void AsyncPredictionController::stop() {
    running = false;
    queueCond.notify_all();
    if (predThread.joinable()) predThread.join();
    if (logThread.joinable()) logThread.join();
}

void AsyncPredictionController::enqueueData(const CarState& data) {
    std::unique_lock<std::mutex> lock(queueMutex);
    inputQueue.push(data);
    queueCond.notify_one();
}

void AsyncPredictionController::onCarStateUpdate(const CarState& state) {
    enqueueData(state);
}

void AsyncPredictionController::predictionLoop() {
    while (running) {
        CarState data;
        {
            std::unique_lock<std::mutex> lock(queueMutex);
            queueCond.wait(lock, [this] { return !inputQueue.empty() || !running; });
            if (!running) break;
            data = inputQueue.front();
            inputQueue.pop();
        }

        predictor->getNewDataToPredict(data);
        if (predictor->wasLastPredictionAnomaly()) {
            std::unique_lock<std::mutex> lock(queueMutex);
            confirmedAnomalies.push(data);
        }
    }
}

void AsyncPredictionController::loggingLoop() {
    while (running) {
        CarState anomaly;
        {
            std::unique_lock<std::mutex> lock(queueMutex);
            if (confirmedAnomalies.empty()) {
                queueCond.wait_for(lock, std::chrono::milliseconds(100));
                continue;
            }
            anomaly = confirmedAnomalies.front();
            confirmedAnomalies.pop();
        }
        logger->onAnomalyDetected(anomaly);

    }
}
