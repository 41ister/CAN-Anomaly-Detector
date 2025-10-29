#ifndef MAZDA6CARDATA_H
#define MAZDA6CARDATA_H

#include "icardata.h"

class Mazda6CarData : public ICarData {
public:
    Mazda6CarData(AnomalyPredictor* pred = nullptr);

    int currentRPM() override;
    double currentSpeed() override;
    double currentEngineTemp() override;
    int currentGear() override;

    void onNewDataAvailable(CarState state) override;

    bool tempProcessor(CanData data);
    bool rpmAndSpeedProcessor(CanData data);

    bool rpmValid = false;
    bool speedValid = false;
    bool tempValid = false;
    void maybeEmitCarState();

private:
    int motorRPM = 0;
    double speed = 0.0;
    double engineTemp = 0.0;
    int gear = 0;
};

#endif // MAZDA6CARDATA_H
