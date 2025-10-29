#ifndef FILERECEIVER_H
#define FILERECEIVER_H

#pragma once

#include "icardata.h"
#include "datareceiver.h"
#include <QString>
#include <QFile>
#include <QMap>
#include <QObject>
#include <deque>
#include <QTimer>


class ICanSubscriber;

class FileReceiver : public QObject, public DataReceiver {
    Q_OBJECT

public:
    FileReceiver(const QString& path, std::deque<CarState>* rows = nullptr);

    void start();
    void enqueueData(const CanData& newData) override { Q_UNUSED(newData); }
    CanData askForNewData() override { return {}; }
    void attachCarData(ICarData* carData) override;
    void addSubscriber(ICanSubscriber* subscriber);
    void parseFile();
    void notifySubscribers(const CarState& state);

private Q_SLOTS:
    void tick();

Q_SIGNALS:
    void finishedReading();

private:
    QFile file;
    QTimer* timer;
    std::deque<CarState>* storage;
    QVector<CarState> states;
    QMap<QString, int> columnMap;
    QList<ICanSubscriber*> subscribers;
    int currentIndex;
    ICarData* car = nullptr;
    QVector<CarState> buffer;


    CarState parseLine(const QString& line);

};

#endif // FILERECEIVER_H
