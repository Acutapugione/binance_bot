import pandas as pd
import json
import asyncio
from strategy import Strategy  # Підключіть вашу стратегію з правильним імпортом
import sys

class Backtester:
    def __init__(self, df: pd.DataFrame, strategy: Strategy):
        self.df = df
        self.strategy = strategy
        self.__signals = self.strategy.get_signals()
        self.balance = 1_000_000  # Початковий баланс у доларах
        self.position = None
        self.trades = []
        
    async def calculate_metrics(self):
        # Після завершення тестування розрахунок метрик
        total_trades = len(self.trades)
        profitable_trades = len([t for t in self.trades if t["entry_price"] < t["take_profit_price"]])
        winrate = (profitable_trades / total_trades) * 100 if total_trades > 0 else 0
        
        divider = sum([t["stop_loss_price"] - t["entry_price"] for t in self.trades if t["entry_price"] > t["stop_loss_price"]])
        if divider > 0:
            profit_factor = sum([t["take_profit_price"] - t["entry_price"] for t in self.trades if t["entry_price"] < t["take_profit_price"]]) / abs(divider)
            return {
                "balance": self.balance,
                "winrate": winrate,
                "profit_factor": profit_factor,
            }
        
        return {
            "balance": self.balance,
            "winrate": winrate,
            "profit_factor": 0,
        }

    async def process_row(self, row, index):
        # Ваш код для обробки сигналів

        if self.__signals:
            for signal in self.__signals:
                if signal["action"]:
                    # Перевірка доступності коштів для відкриття позиції
                    if self.balance >= 100:  # Розмір позиції $100
                        self.position = {
                            "entry_price": signal["entry price"],
                            "take_profit_price": signal["TP"],
                            "stop_loss_price": signal["SL"],
                        }
                        self.balance -= 100  # Віднімання від балансу розміру позиції
                        self.trades.append(self.position)

        # Перевірка наявних позицій і закриття, якщо досягнуто TP або SL
        closed_positions = []
        for trade in self.trades:
            entry_price = trade["entry_price"]
            take_profit_price = trade["take_profit_price"]
            stop_loss_price = trade["stop_loss_price"]

            if row["close"] >= take_profit_price or row["close"] <= stop_loss_price:
                # Розрахунок прибутку або збитку
                if row["close"] >= take_profit_price:
                    profit_loss = 100 * (take_profit_price - entry_price) / entry_price
                else:
                    profit_loss = -100 * (entry_price - stop_loss_price) / entry_price

                # Додавання прибутку/збитку до балансу
                self.balance += profit_loss
                closed_positions.append(trade)

        # Видалення закритих позицій зі списку
        for trade in closed_positions:
            self.trades.remove(trade)
        
        sys.stdout.write(f"\rProcessed row {index}/{len(self.df)}")
        sys.stdout.flush()

    async def backtest(self):
        tasks = [self.process_row(row, index) for index, row in self.df.iterrows()]
        await asyncio.gather(*tasks)

        # Розрахунок метрик після завершення тестування
        results = await self.calculate_metrics()
        return results

async def main():
    # Зчитати історичні дані з CSV файлу (або замість цього використовуйте своє джерело даних)
    df = pd.read_csv("binance_data_cci.csv")
    strategy = Strategy(df)  # Ініціалізуйте вашу стратегію з правильним імпортом

    # Створення об'єкту бектестера і запуск бектесту
    backtester = Backtester(df, strategy=strategy)
    results = await backtester.backtest()

    # Виведення результатів бектесту
    print("\nBalance:", results["balance"])
    print("Winrate:", results["winrate"], "%")
    print("Profit Factor:", results["profit_factor"])

    with open("back_tester_results.json", "w") as _:
        json.dump(
            results,
            _,
            indent=4,
        )


if __name__ == "__main__":
    asyncio.run(main())
