#ifndef STREAMINGRECEIVER_H
#define STREAMINGRECEIVER_H

#include "datareceiver.h"

class StreamingReceiver : public DataReceiver {
 public:
  StreamingReceiver() {}
  virtual CanData askForNewData() = 0;
  virtual ~StreamingReceiver();
};

#endif  // STREAMINGRECEIVER_H
