#ifndef ANOMALYPREDICTOR_H
#define ANOMALYPREDICTOR_H

#include <QObject>
#include "icardata.h"

class AnomalyPredictor : public QObject {
  Q_OBJECT  // Необходимо для корректной работы MOC

 public:
  explicit AnomalyPredictor(QObject* parent = nullptr) : QObject(parent) {}
  virtual void getNewDataToPredict(CarState carstate) = 0;
  virtual ~AnomalyPredictor();
};

#endif  // ANOMALYPREDICTOR_H
