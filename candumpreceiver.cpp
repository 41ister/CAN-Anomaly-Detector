#include "candumpreceiver.h"

#ifdef __linux__

#include <ctype.h>
#include <errno.h>
#include <libgen.h>
// needs to install can_utils package
#include <linux/can.h>
#include <linux/can/raw.h>

#include <net/if.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/uio.h>
#include <time.h>
#include <unistd.h>

#endif

void CanDumpReceiver::setup() {
  // ported from candump
#ifdef __linux__
  int maxdlen = 8;

  canfd_on = 1;
  running = true;
  ptr = "can0";  // fixme
  nbytes = strlen(ptr);
  s = socket(PF_CAN, SOCK_RAW, CAN_RAW);
  if (s < 0) {
    perror("socket");
    return;
  }
  addr.can_family = AF_CAN;
  memset(&ifr.ifr_name, 0, sizeof(ifr.ifr_name));
  strncpy(ifr.ifr_name, ptr, nbytes);
  if (strcmp(ANYDEV, ifr.ifr_name)) {
    if (ioctl(s, SIOCGIFINDEX, &ifr) < 0) {
      perror("SIOCGIFINDEX");
      exit(1);
    }
    addr.can_ifindex = ifr.ifr_ifindex;
  } else
    addr.can_ifindex = 0;
  setsockopt(s, SOL_CAN_RAW, CAN_RAW_FD_FRAMES, &canfd_on, sizeof(canfd_on));
  if (bind(s, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
    perror("bind");
    return;
  }
  iov.iov_base = &frame;
  msg.msg_name = &addr;
  msg.msg_iov = &iov;
  msg.msg_iovlen = 1;
  msg.msg_control = &ctrlmsg;
  len = (frame.len > maxdlen) ? maxdlen : frame.len;
#endif
}

CanData CanDumpReceiver::askForNewData() {
  CanData can;

#ifdef __linux__
  while (running) {
    FD_ZERO(&rdfs);
    FD_SET(s, &rdfs);
    if ((ret = select(s + 1, &rdfs, NULL, NULL, 0)) <= 0) {
      // perror("select");
      running = 0;
      continue;
    }
    if (FD_ISSET(s, &rdfs)) {
      iov.iov_len = sizeof(frame);
      msg.msg_namelen = sizeof(addr);
      msg.msg_controllen = sizeof(ctrlmsg);
      msg.msg_flags = 0;

      readWriteLock->lock();
      nbytes = recvmsg(s, &msg, 0);
      readWriteLock->unlock();

      if (nbytes < 0) {
        // if ((errno == ENETDOWN) && !down_causes_exit) {
        continue;
        //}
      }
      if ((size_t)nbytes == CAN_MTU)
        maxdlen = CAN_MAX_DLEN;
      else if ((size_t)nbytes == CANFD_MTU)
        maxdlen = CANFD_MAX_DLEN;

      if (frame.can_id & CAN_ERR_FLAG) continue;

      // check the RTD flag

      if (frame.can_id & CAN_RTR_FLAG) continue;

      // store the result frame
      //   printf("canid=%d\n", frame.can_id);
      can.push_back(frame.can_id);

      for (int i = 0; i < frame.len; i++) {
        can.push_back(frame.data[i]);
      }

      Lockers::monitor.lock();
      this->dataToProcess->push_back(can);
      Lockers::monitor.unlock();

      // break;
    }
#endif
    return can;
  }

  CanDumpReceiver::~CanDumpReceiver() = default;
