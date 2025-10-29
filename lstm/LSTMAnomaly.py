import os
import json
import time
import math
import sys
import traceback
import numpy as np
import matplotlib.pyplot as plt
from core.data_processor import DataLoader
from core.model import Model

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def plot_results(predicted_data, true_data):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    ax.plot(predicted_data, label='Prediction')
    plt.legend()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    plt.savefig(timestr + '_series.png')
    plt.close()

def plot_results_multiple(predicted_data, true_data, prediction_len):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    # Pad the list of predictions to shift it in the graph to its correct start
    for i, data in enumerate(predicted_data):
        padding = [None for _ in range(i * prediction_len)]
        ax.plot(padding + data, label='Prediction')
    plt.legend()
    plt.close()

class LSTMAnomaly:
    def __init__(self):
        eprint("call INIT")

    def setup(self):
        print("call setup")

    def predict(self):
        print("call predict", flush=True)
        try:
            os.chdir('/home/qwerty/CAN-Anomaly-Detector-master/lstm')
            print(">> changed working directory", flush=True)
            configs = json.load(open('/home/qwerty/CAN-Anomaly-Detector-master/lstm/config_new.json', 'r'))
            print(">> loaded config", flush=True)
        except FileNotFoundError:
            eprint("Error: config_new.json not found.")
            return -1
        except json.JSONDecodeError:
            eprint("Error: Failed to decode JSON.")
            return -1

        try:
            if not os.path.exists(configs['model']['save_dir']):
                os.makedirs(configs['model']['save_dir'])
                print(f">> created save dir: {configs['model']['save_dir']}", flush=True)

            data = DataLoader(
                os.path.join('data', configs['data']['filename']),
                os.path.join('data', configs['data']['filename_test']),
                configs['data']['train_test_split'],
                configs['data']['columns']
            )
            print(">> data loaded", flush=True)

            model = Model()
            model.build_model(configs)
            model.load_model('longlong.h5')
            print(">> model loaded", flush=True)

            x_test, y_test = data.get_test_data(
                seq_len=configs['data']['sequence_length'],
                normalise=configs['data']['normalise']
            )
            print(">> got test data", flush=True)

            print(">> before model.predict_point_by_point", flush=True)
            predictions = model.predict_point_by_point(x_test)
            print(">> after model.predict_point_by_point", flush=True)
            print(">> got predictions", flush=True)
            std = np.std(y_test, ddof=1)
            diff0 = (predictions[0] - y_test[0])

            for i in range(len(predictions)):
                predictions[i] -= diff0

            anomaly_count = 0
            for i in range(len(predictions)):
                d = abs(predictions[i] - y_test[i])
                if d > 2 * std:
                    anomaly_count += 1
                    diff = (predictions[i] - y_test[i])
                    for j in range(i, len(predictions)):
                        predictions[j] -= diff

            plot_results(predictions, y_test)

            print(">>> Python: anomalies =", anomaly_count, flush=True)
            
            return int(anomaly_count)

        except Exception as e:
            eprint(f"Unhandled error in predict(): {e}")
            traceback.print_exc()
            return -1 

"""class LSTMAnomaly:
    def __init__(self):
        self.ano = None
        self.configs = None
        self.mx = None
        self.x_test = None
        self.y_test = None
        self.index = 0
        self.total = 0

    def setup(self):
        print(">> changed working directory", flush=True)
        os.chdir('/home/qwerty/CAN-Anomaly-Detector-master/lstm')
        print(">> loaded config", flush=True)
        self.configs = json.load(open('config_new.json'))

        data = DataLoader(
            os.path.join('data', self.configs['data']['filename']),
            os.path.join('data', self.configs['data']['filename_test']),
            self.configs['data']['train_test_split'],
            self.configs['data']['columns']
        )

        print(">> data loaded", flush=True)

        self.mx = data.mx
        self.model = Model()
        self.model.build_model(self.configs)
        self.model.load_model('longlong.h5')
        print(">> model loaded", flush=True)

        self.x_test, self.y_test = data.get_test_data(
            seq_len=self.configs['data']['sequence_length'],
            normalise=self.configs['data']['normalise']
        )
        self.total = len(self.x_test)
        print(f">> ready to stream predictions: total = {self.total}", flush=True)

    def stream(self, _):

        if self.index >= self.total:
            print(">>> Python: streaming finished")
            return 0

        try:
            x = self.x_test[self.index:self.index+1]
            y_true = self.y_test[self.index][0]
            pred = self.model.model.predict(x, verbose=0)[0][0]
            std = np.std(self.y_test)

            deviation = abs(pred - y_true)
            print(f"{self.index+1}/{self.total} - pred: {pred:.3f}, true: {y_true:.3f}, dev: {deviation:.3f}", flush=True)

            self.index += 1

            return 1 if deviation > 2 * std else 0
        except Exception as e:
            print(f"[Python] stream error: {e}")
            traceback.print_exc()
            return -1 """

    
def main():
    ano = LSTMAnomaly()
    ano.setup()
    ano.predict()
    """for _ in range(ano.total):
        ano.stream(None)
        time.sleep(0)  # симуляция стриминга"""

if __name__ == '__main__':
    main()