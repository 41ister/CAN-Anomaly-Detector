#include "speedincreasesafterrpmincreasesproperty.h"
#include <QDateTime>
#include <QDebug>

SpeedIncreasesAfterRPMIncreasesProperty::
    SpeedIncreasesAfterRPMIncreasesProperty() {
  t = 0;
  currentState = start;
}

bool SpeedIncreasesAfterRPMIncreasesProperty::checkPropertyForCurrentData(
    CarState carstate) {
  bool RPMOk = (carstate.rpm > 1000) && (carstate.temp > 60);

  if (currentState == start) {
    if (RPMOk) {
      t = carstate.timestamp;
      once = false;
      currentState = rpm_greater_1000;
      return true;
    }
  }
  if (currentState == rpm_greater_1000) {
    if (!RPMOk) {
      currentState = start;
      return true;
    }
    if (carstate.rpmDot >= 0 && (carstate.timestamp - t) > 1000) {
      currentState = rpm_dot_greater_0;

      return true;
    }
    if (carstate.rpmDot < 0) {
      currentState = start;
      return true;
    }
  }
  if (currentState == rpm_dot_greater_0) {
    if (!RPMOk) {
      currentState = start;
      return true;
    }
    if (carstate.rpmDot < 0) {
      currentState = start;
      return true;
    }
    if (carstate.speedDot >= 0 && once && (carstate.timestamp - t) > 2000) {
      qDebug() << "Property holds!\n";
      currentState = start;
      return true;
    }
    if (carstate.speedDot > 0) {
      once = true;
      return true;
    }
    if (carstate.speedDot < 0 ||
        (carstate.speedDot == 0 && !once && (carstate.timestamp - t) > 2000)) {
      qDebug() << "!!!Property violation at "
               << QDateTime::fromMSecsSinceEpoch(carstate.timestamp).toString();

      currentState = start;
      return false;
    }
  }
  return true;
}

SpeedIncreasesAfterRPMIncreasesProperty::
    ~SpeedIncreasesAfterRPMIncreasesProperty() = default;

/*

digraph finite_state_machine {
        rankdir=LR;
        size="8,5"
        node [shape = circle]; start rpm_greater_1000[label = "rpm>1000"]
rpm_dot_greater_0 [label="rpm'>0"]; node [shape = doublecircle]; fin anomaly;

    start -> rpm_greater_1000 [label = "[rpm > 1000 & temp > 60] t =
timestamp"]; rpm_greater_1000 -> start [label = "[!(rpm > 1000 & temp > 60)]"];
    rpm_greater_1000 -> rpm_greater_1000 [label = "[rpm' >= 0] timestamp++"];
    rpm_greater_1000 -> rpm_dot_greater_0 [label = "[rpm' >= 0 & timestamp - t >
1000]"]; rpm_greater_1000 -> start [label = "[rpm' < 0]"];

    rpm_dot_greater_0 -> start [label="[!(rpm > 1000 & temp > 60]"];
    rpm_dot_greater_0 -> start [label = "[rpm' < 0]"];

    rpm_dot_greater_0 -> anomaly[label = "[v' < 0]"];
    rpm_dot_greater_0 -> rpm_dot_greater_0 [label = "[v' >=0] timestamp++"];
    rpm_dot_greater_0 -> fin [label = "[v' >= 0  & timestamp - t > 2000]"]
}
*/
