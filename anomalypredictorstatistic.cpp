#include "anomalypredictorstatistic.h"
#include <QDateTime>
#include <QDebug>

AnomalyPredictorStatistic::~AnomalyPredictorStatistic() = default;

AnomalyPredictorStatistic::AnomalyPredictorStatistic() {
  numPointsToPredict = 11000;
  curentPoints = 0;
  decay = 0.5;
  ema = 0;
  mseError = 0;
}

void AnomalyPredictorStatistic::getNewDataToPredict(CarState carstate) {
  curentPoints++;

  if (curentPoints == 1) carstateOld = carstate;

  // todo: include not only speed
  ema = ema * decay + (1.0 - decay) * carstateOld.speed;

  mseError += (ema - carstate.speed) * (ema - carstate.speed);

  carstateOld = carstate;

  if (curentPoints >= numPointsToPredict) {
    if (mseError > maxAnomalyScore) {
      qDebug() << "Statistical anomaly for last " << numPointsToPredict
               << " points detected at "
               << QDateTime::fromMSecsSinceEpoch(carstate.timestamp).toString();
    }

    ema = 0;
    curentPoints = 0;
    mseError = 0;
  }
}
