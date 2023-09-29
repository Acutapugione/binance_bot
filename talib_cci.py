import pandas as pd
import numpy as np
import talib

# Зразок цінових даних (замініть своїми даними)
# Наприклад, df = pd.read_csv('your_data.csv')
df = pd.read_csv('binance_data.csv')

# Обчислити CCI з періодом 30
period = 30
cci = talib.CCI(df['high'], df['low'], df['close'], timeperiod=period)

# Додайте стовпець CCI до вашого DataFrame
df['cci'] = cci

# Вивести перші декілька рядків вашого DataFrame, включаючи значення CCI
print(df)
