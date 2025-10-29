import numpy as np
import pandas as pd

class DataLoader:
    """Класс для загрузки и подготовки данных для LSTM модели"""

    def __init__(self, filename, filename_test, split, cols):
        # Загружаем обучающие данные
        df_train = pd.read_csv(filename)
        self.data_train = df_train[cols].values

        # Загружаем тестовые данные
        df_test = pd.read_csv(filename_test)
        self.data_test = df_test[cols].values

        self.len_train = len(self.data_train)
        self.len_test = len(self.data_test)
        self.len_train_windows = None

        # Вычисляем максимум по каждой колонке (на основе train + test)
        combined = np.vstack((self.data_train, self.data_test))
        self.mx = np.max(combined, axis=0)

    def get_test_data(self, seq_len, normalise):
        """Создание тестовых окон x/y"""
        data_windows = []
        for i in range(self.len_test - seq_len):
            data_windows.append(self.data_test[i:i + seq_len])

        data_windows = np.array(data_windows).astype(float)

        if normalise:
            data_windows = self.normalise_windows(data_windows, single_window=False)

        x = data_windows[:, :-1]
        y = data_windows[:, -1, [0]]  # Предсказываем первую колонку
        return x, y

    def get_train_data(self, seq_len, normalise):
        """Создание обучающих окон x/y"""
        data_x = []
        data_y = []
        for i in range(self.len_train - seq_len):
            x, y = self._next_window(i, seq_len, normalise)
            data_x.append(x)
            data_y.append(y)
        return np.array(data_x), np.array(data_y)

    def generate_train_batch(self, seq_len, batch_size, normalise):
        """Генератор батчей обучающих данных"""
        i = 0
        while i < (self.len_train - seq_len):
            x_batch = []
            y_batch = []
            for _ in range(batch_size):
                if i >= (self.len_train - seq_len):
                    yield np.array(x_batch), np.array(y_batch)
                    i = 0
                x, y = self._next_window(i, seq_len, normalise)
                x_batch.append(x)
                y_batch.append(y)
                i += 1
            yield np.array(x_batch), np.array(y_batch)

    def _next_window(self, i, seq_len, normalise):
        """Формирует одно окно данных"""
        window = self.data_train[i:i + seq_len]
        if normalise:
            window = self.normalise_windows(window, single_window=True)[0]
        x = window[:-1]
        y = window[-1, [0]]  # Предсказываем первую колонку
        return x, y

    def normalise_windows(self, window_data, single_window=False):
        """Нормализация данных относительно максимума"""
        if single_window:
            window_data = [window_data]

        normalised_data = []
        for window in window_data:
            normed = window / self.mx  # векторное деление
            normalised_data.append(normed)

        return np.array(normalised_data)

    def denormalise_series(self, series, col=0):
        """Обратное масштабирование ряда (одной колонки)"""
        return series * self.mx[col]
