#include <QCoreApplication>
#include <QString>
#include <iostream>

#include "anomalypredictorlstm.h"
#include "csvanomalylogger.h"
#include "asyncpredictor.h"
#include "filereceiver.h"
#include "mazda6cardata.h"
#include <QDebug>

int main(int argc, char *argv[]) {
    QCoreApplication app(argc, argv);

    setenv("PYTHONUNBUFFERED", "1", 1);
    QString inputCsv = "/home/qwerty/CAN-Anomaly-Detector-master/lstm/data/input.csv";
    QString outputCsv = "/home/qwerty/CAN-Anomaly-Detector-master/lstm/data/output.csv";
    QString pythonPath = "/home/qwerty/CAN-Anomaly-Detector-master/lstm:/home/qwerty/CAN-Anomaly-Detector-master/lstm/.venv310/lib/python3.10/site-packages";

    std::deque<CarState> dataRows;
    FileReceiver* dataReceiver = new FileReceiver(inputCsv, &dataRows);

    AnomalyPredictorLSTM* predictor = new AnomalyPredictorLSTM(outputCsv, pythonPath, "LSTMAnomaly", "/home/qwerty/CAN-Anomaly-Detector-master/lstm");
    CsvAnomalyLogger* logger = new CsvAnomalyLogger("/home/qwerty/CAN-Anomaly-Detector-master/lstm:/home/qwerty/CAN-Anomaly-Detector-master/anomalies.csv");
    predictor->addAnomalySubscriber(logger);

    ICarData* car = new Mazda6CarData();
    car->setPredictor(predictor);

    dataReceiver->attachCarData(car);
    dataReceiver->addSubscriber(predictor);

    QObject::connect(predictor, &AnomalyPredictorLSTM::predictionFinished, dataReceiver, [=]() {
        dataReceiver->start();
    });

    QObject::connect(dataReceiver, &FileReceiver::finishedReading, [&]() {
        QObject::connect(predictor, &AnomalyPredictorLSTM::predictionFinished, &app, [&]() {
            qDebug() << "[Main] Последний батч обработан. Завершение.";
            app.quit();
        });
    });

    dataReceiver->start();
    return app.exec();
}
