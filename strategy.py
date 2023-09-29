import pandas as pd
import talib


LOWER_BAND_PRICE = 0.05
UPPER_BAND_PRICE = 1


class Strategy:
    def __init__(self, df):
        self.df = df
        self.commission = 0.005  # Комісія 0.5%
        self.position = None  # Зберігаємо поточну позицію

    def calculate_indicators(self):
        # Розрахунок CCI з періодом 30
        period = 30
        self.df["cci"] = talib.CCI(
            self.df["high"].astype(float),
            self.df["low"].astype(float),
            self.df["close"].astype(float),
            timeperiod=period,
        )

        # Додайте розрахунок RSIBANDS_LB (ваш RSIBANDS_LB логіку)

    def get_signals(self):
        signals = []

        for i in range(len(self.df)):
            if i == 0:
                continue

            close_price = float(self.df["close"].iloc[i])
            cci = float(self.df["cci"].iloc[i])

            # Перевірка умови LONG
            if close_price < LOWER_BAND_PRICE and cci < -100:
                entry_price = close_price
                take_profit_price = entry_price * 1.01  # TP 1%
                stop_loss_price = entry_price * 0.996  # SL 0.4%
                signals.append(
                    {
                        "action": True,
                        "entry price": entry_price,
                        "TP": take_profit_price,
                        "SL": stop_loss_price,
                    }
                )
            # Перевірка умови SHORT
            elif close_price > UPPER_BAND_PRICE and cci > 120:
                entry_price = close_price
                take_profit_price = entry_price * 0.989  # TP 1.1%
                stop_loss_price = entry_price * 1.005  # SL 0.5%
                signals.append(
                    {
                        "action": True,
                        "entry price": entry_price,
                        "TP": take_profit_price,
                        "SL": stop_loss_price,
                    }
                )
            else:
                signals.append({"action": False})

        return signals


if __name__ == "__main__":
    # Передайте ваш DataFrame із історією котирувань
    df = pd.read_csv('binance_data_cci.csv')
    strategy = Strategy(df)

    # Розрахуйте індикатори
    strategy.calculate_indicators()

    # Отримайте сигнали
    signals = strategy.get_signals()

    # Виведіть сигнали
    for signal in signals:
        print(signal)
