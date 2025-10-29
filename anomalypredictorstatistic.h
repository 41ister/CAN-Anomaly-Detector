#ifndef ANOMALYPREDICTORSTATISTIC_H
#define ANOMALYPREDICTORSTATISTIC_H
#include "anomalypredictor.h"

class AnomalyPredictorStatistic : public AnomalyPredictor {
 public:
  AnomalyPredictorStatistic();
  virtual void getNewDataToPredict(CarState carstate);
  void setNumPoints(unsigned numPointsToPredict) {
    this->numPointsToPredict = numPointsToPredict;
  }
  void setMaxAnomalyScore(double maxAnomalyScore) {
    this->maxAnomalyScore = maxAnomalyScore;
  }
  virtual ~AnomalyPredictorStatistic();

 private:
  unsigned numPointsToPredict;
  unsigned curentPoints;
  double ema;
  double decay;
  CarState carstateOld;
  double mseError;
  double maxAnomalyScore;
};

#endif  // ANOMALYPREDICTORSTATISTIC_H
