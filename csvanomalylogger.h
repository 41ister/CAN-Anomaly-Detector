#ifndef CSVANOMALYLOGGER_H
#define CSVANOMALYLOGGER_H

#pragma once
#include "icansubscriber.h"
#include <QFile>
#include <QTextStream>
#include <QObject>
#include <QSet>

class CsvAnomalyLogger : public QObject, public IAnomalySubscriber {
    Q_OBJECT
public:
    explicit CsvAnomalyLogger(const QString& filename);
    ~CsvAnomalyLogger();

    void onAnomalyDetected(const CarState& state) override;

private:
    QFile file;
    QTextStream* stream;
    QSet<QString> seenAnomalies;
    QSet<QString> seenEntries;
};

#endif // CSVANOMALYLOGGER_H
