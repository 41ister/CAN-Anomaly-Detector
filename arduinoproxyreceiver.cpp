#include "arduinoproxyreceiver.h"
#include <QCoreApplication>
#include <QDateTime>
#include <QDebug>
#include <QThread>

#include "lockers.h"

void ArduinoProxyReceiver::setup() {
  QThread::msleep(1000);

  qDebug() << "Opening serial...\n";
  serial = new QSerialPort();
  serial->setPortName(port);

  serial->setBaudRate(115200);
  serial->setDataBits(QSerialPort::Data8);
  serial->setParity(QSerialPort::NoParity);
  serial->setStopBits(QSerialPort::OneStop);
  serial->setFlowControl(QSerialPort::NoFlowControl);

  if (!serial->open(QIODevice::ReadWrite)) {
    qDebug() << "bad serial \n";
    QCoreApplication::quit();
  }

  // data to send magic configuration
  unsigned char sendData[4] = {0x19, 0x84, 0, 0};
  sendData[3] = 3;  // 500

  const char *sending = reinterpret_cast<char *>(sendData);

  QByteArray resp;

  qDebug() << "waiting Arduino to be ready...\n";

  QString outputMsg = "";
  do {
    QThread::msleep(100);

    QCoreApplication::processEvents();
    // qDebug() << serial->bytesAvailable() << "\n";

    if (serial->bytesAvailable() > 30) {
      QByteArray data = serial->readAll();
      if (data.length() > 0) {
        resp.append(data);
        outputMsg = QString::fromStdString(resp.toStdString());
        qDebug() << outputMsg << "\n";
      }
    }
  } while (outputMsg.indexOf("\n") < 0);

  QThread::msleep(1000);
  serial->readAll();
  serial->flush();
  // sending setup data buffer
  serial->write(QByteArray::fromRawData(sending, sizeof(sendData)));
  serial->waitForBytesWritten(1000);
  QCoreApplication::processEvents();
  serial->flush();
  serial->waitForReadyRead(100);

  qDebug() << "waiting the reply...\n";
  // waiting the reply
  QDateTime timeStart = QDateTime::currentDateTime();
  resp.clear();
  do {
    QCoreApplication::processEvents();
    // if (serial->bytesAvailable() > 0) {
    QByteArray data = serial->readAll();

    if (data.length() > 0) {
      resp.append(data);
      qDebug() << data;
    }
    outputMsg = QString::fromStdString(resp.toStdString());

    if (timeStart.secsTo(QDateTime::currentDateTime()) > 5) {
      outputMsg = "Init failed with timeout. Try again.";
      break;
    }

  } while ((outputMsg.indexOf("init ok") < 0) &&
           (outputMsg.indexOf("init fail") < 0));

  serial->flush();

  if (outputMsg.indexOf("init ok") > 0) {
    qDebug() << "Init COM port OK \n";
  } else {
    qDebug() << "Init COM port NOT OK \n";
    QCoreApplication::exit();
  }
}

/*
 *
 */
CanData ArduinoProxyReceiver::askForNewData() {
  bool isStopped = false;

  QByteArray data;
  QString dataRep;
  QString dataToProcess;

  // pass all data to /n
  int indexOf = -1;
  do {
    QByteArray data0 = serial->readAll();
    if (data0.length() > 0) {
      data.append(data0);
      dataRep = QString::fromStdString(data.toStdString());
      indexOf = dataRep.indexOf("\n");
    }
  } while (indexOf < 0);

  // we get from \n to end (start of new substring)
  dataToProcess = dataRep.mid(indexOf + 1);

  data.clear();

  do {
    QThread::msleep(1);

    indexOf = -1;

    do {
      QDateTime timeStartGetting = QDateTime::currentDateTime();
      QString sendMe = "";

      QByteArray data0 = serial->readAll();
      if (data0.length() > 0) {
        data.append(data0);
        dataRep = QString::fromStdString(data.toStdString());
        indexOf = dataRep.indexOf("\n");
      }
    } while (indexOf < 0);

    qDebug() << dataRep << "\n";
    // process data we collected in 100ms period
    // Process data from string like FF 11 22 33 44 55 66 77 88

    QStringList strings = dataRep.split("\n");
    for (int s = 0; s < strings.length() - 1; s++) {
      // second: get bytes in array from each line
      QStringList bytes = strings.at(s).split(" ");
      int count = (bytes.length() <= 9) ? bytes.length() : 9;

      unsigned short converted[9];
      CanData can;

      // convert to normal chars
      int realCount = 0;
      for (int i = 0; i < count; i++) {
        QString oneByteHex = bytes.at(i);

        bool bStatus = false;
        uint nHex = oneByteHex.toUInt(&bStatus, 16);
        if (!bStatus) continue;

        converted[realCount++] = (unsigned short)nHex;
        can.push_back((unsigned short)nHex);
      }
      count = realCount;

      if (count == 0) continue;  // skip ""

      Lockers::monitor.lock();
      this->dataToProcess->push_back(can);
      Lockers::monitor.unlock();
    }
    // notify
    Lockers::notifier = true;
    Lockers::cond_var.notify_one();
  } while (!isStopped);

  // stub
  CanData d;
  return d;
}

ArduinoProxyReceiver::~ArduinoProxyReceiver() = default;
