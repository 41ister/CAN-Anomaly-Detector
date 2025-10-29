#ifndef ANOMALYPREDICTORSLTL_H
#define ANOMALYPREDICTORSLTL_H

#include <vector>
#include "anomalypredictor.h"
#include "icardata.h"
#include "isltlproperty.h"

class AnomalyPredictorSLTL : public AnomalyPredictor {
 public:
  AnomalyPredictorSLTL();
  void attachProperty(ISLTLProperty *property) {
    properties.push_back(property);
  }
  virtual void getNewDataToPredict(CarState carstate);
  virtual ~AnomalyPredictorSLTL();

 private:
  std::vector<ISLTLProperty *> properties;
};

#endif  // ANOMALYPREDICTORSLTL_H
