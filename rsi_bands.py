import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


overbought_level = 70
oversold_level = 30
rsi_length = 14

df = pd.read_csv("binance_data_cci.csv")

closing_prices = df["close"]
ema_period = 2 * rsi_length - 1
positive_momentum = (
    closing_prices.diff().clip(lower=0).ewm(span=ema_period, adjust=False).mean()
)
negative_momentum = (
    (-closing_prices.diff(-1)).clip(lower=0).ewm(span=ema_period, adjust=False).mean()
)

upper_band_multiplier = (rsi_length - 1) * (
    negative_momentum * overbought_level / (100 - overbought_level) - positive_momentum
)
upper_band = np.where(
    upper_band_multiplier >= 0,
    closing_prices + upper_band_multiplier,
    closing_prices
    + upper_band_multiplier * (100 - overbought_level) / overbought_level,
)

lower_band_multiplier = (rsi_length - 1) * (
    negative_momentum * oversold_level / (100 - oversold_level) - positive_momentum
)
lower_band = np.where(
    lower_band_multiplier >= 0,
    closing_prices + lower_band_multiplier,
    closing_prices + lower_band_multiplier * (100 - oversold_level) / oversold_level,
)

plt.plot(upper_band, label="Опір", color="red", linewidth=2)
plt.plot(lower_band, label="Підтримка", color="green", linewidth=2)
plt.plot(
    (upper_band + lower_band) / 2, label="Середня лінія RSI", color="gray", linewidth=1
)

plt.title("RSI Bands [LazyBear]")
plt.legend()
plt.show()
