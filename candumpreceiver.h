#ifndef CANDUMPRECEIVER_H
#define CANDUMPRECEIVER_H

#include "streamingreceiver.h"

class CanDumpReceiver : public StreamingReceiver {
 public:
  CanDumpReceiver(){};
  void setup();
  virtual CanData askForNewData();
  virtual ~CanDumpReceiver();

 private:
  // needs to install can_utils package
#ifdef __linux__
  fd_set rdfs;
  char *ptr;
  struct sockaddr_can addr;
  int s;
  struct canfd_frame frame;
  struct iovec iov;
  struct msghdr msg;
  struct ifreq ifr;
  int nbytes;
  int maxdlen = 8;
  char ctrlmsg[CMSG_SPACE(sizeof(struct timeval) + 3 * sizeof(struct timespec) +
                          sizeof(__u32))];
  const int canfd_on;
  int ret;
  bool running;
  int len;
#endif
};

#endif  // CANDUMPRECEIVER_H
