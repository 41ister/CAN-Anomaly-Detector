#include "filedirreceiver.h"
#include <QDir>

void FileDirReceiver::setup() {
  QDir directory(this->path);
  QStringList files = directory.entryList(QStringList() << "*.csv"
                                                        << "*.CSV",
                                          QDir::Files);
  foreach (QString filename, files) {
    // read all cvs in arrays...
  }
}

CanData FileDirReceiver::askForNewData() {
  CanData can;

  while (true) {
    // tbd
  }

  return can;
}

FileDirReceiver::~FileDirReceiver() = default;
