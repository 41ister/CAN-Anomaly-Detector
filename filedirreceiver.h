#ifndef FILEDIRRECEIVER_H
#define FILEDIRRECEIVER_H

#include <QString>
#include "datareceiver.h"

class FileDirReceiver : public DataReceiver {
 public:
  FileDirReceiver(QString &path) {
    this->path = path;
    setup();
  };
  virtual CanData askForNewData();
  ~FileDirReceiver();

 private:
  void setup();
  QString path;
};

#endif  // FILEDIRRECEIVER_H
