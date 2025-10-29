#ifndef ISLTLPROPERTY_H
#define ISLTLPROPERTY_H

#include <icardata.h>
#include <QString>
class ISLTLProperty {
 public:
  ISLTLProperty() {}
  void setFormula(const QString &formula) { this->formula = formula; }
  virtual bool checkPropertyForCurrentData(CarState data) = 0;
  virtual ~ISLTLProperty();

 private:
  QString formula;
};

#endif  // ISLTLPROPERTY_H
