#include "cardataprocessorthread.h"
#include "lockers.h"
#include <iostream>
#include <QDateTime>

void carDataProcessorThread::run() {
    std::mutex mut;
    std::unique_lock<std::mutex> lock(mut);

    while (true) {
        while (!Lockers::notifier) {
            Lockers::cond_var.wait(lock);
        }

        if (!dataToProcess || dataToProcess->empty()) {
            std::cerr << "[carDataProcessorThread] Error: No data to process!" << std::endl;
            Lockers::notifier = false;
            continue;
        }

        try {
            //std::cout << "[carDataProcessorThread] Processing " << dataToProcess->size() << " elements" << std::endl;

            car->processData(*dataToProcess);

            // После обработки извлекаем новое состояние
            CarState state;
            state.timestamp = QDateTime::currentMSecsSinceEpoch();
            state.speed = car->currentSpeed();
            state.rpm = car->currentRPM();
            state.gear = car->currentGear();

            car->onNewDataAvailable(state);

        } catch (const std::exception &e) {
            std::cerr << "[carDataProcessorThread] Exception: " << e.what() << std::endl;
        } catch (...) {
            std::cerr << "[carDataProcessorThread] Unknown error occurred!" << std::endl;
        }

        Lockers::notifier = false;
    }
}
