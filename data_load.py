from binance import AsyncClient
import pandas as pd
import asyncio
import json
import talib


async def create_api_client(
    key: str,
    secret: str,
    is_test: bool,
):
    client = await AsyncClient.create(
        api_key=key,
        api_secret=secret,
        testnet=is_test,
    )
    return client


async def fetch_info(
    client: AsyncClient,
    symbol: str,
    interval: str,
):
    result = await client.get_historical_klines(
        symbol=symbol,
        interval=interval,
        start_str="2019-09-29 11:57:54 UTC",
        end_str="2023-10-29 11:57:54 UTC",
    )
    await client.close_connection()
    return result


async def main(
    api_key: str,
    api_secret: str,
    is_test: bool,
    symbol: str,
    interval: str,
    period: int,
):
    client = await create_api_client(
        api_key,
        api_secret,
        is_test,
    )
    data = await fetch_info(
        client,
        symbol=symbol,
        interval=interval,
    )
    df = pd.DataFrame(
        data=data,
        columns=[
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume",
            "ignore",
        ],
    )
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        unit="ms",
    )

    df["cci"] = talib.CCI(
        df["high"].astype(float),
        df["low"].astype(float),
        df["close"].astype(float),
        timeperiod=period,
    )

    df.to_csv(
        "binance_data_cci.csv",
        index=False,
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        main(
            api_key="API_KEY",
            api_secret="API_SECRET",
            is_test=False,
            symbol="BTCUSDT",
            interval=AsyncClient.KLINE_INTERVAL_1MINUTE,
            period=30,
        )
    )
