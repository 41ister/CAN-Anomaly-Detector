#include "anomalypredictorsltl.h"
#include <isltlproperty.h>
#include <QDateTime>
#include <QDebug>
#include "icardata.h"
AnomalyPredictorSLTL::AnomalyPredictorSLTL() {}

void AnomalyPredictorSLTL::getNewDataToPredict(CarState carstate) {
  for (ISLTLProperty *prop : this->properties) {
    if (!prop->checkPropertyForCurrentData(carstate)) {
      // property violation
      exit(1);
    }
  }
}

AnomalyPredictorSLTL::~AnomalyPredictorSLTL() = default;
