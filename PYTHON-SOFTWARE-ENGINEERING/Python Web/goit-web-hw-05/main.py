import aiohttp
import asyncio
from datetime import datetime, timedelta
import sys

# Інтерфейс для роботи з API
class ExchangeRateAPI:
    async def fetch_exchange_rate(self, date: str):
        pass

# Реалізація роботи з API ПриватБанку
class PrivatBankAPI(ExchangeRateAPI):
    BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date={}"

    async def fetch_exchange_rate(self, date: str):
        url = self.BASE_URL.format(date)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"Помилка при отриманні даних: {response.status}")
                        return None
        except aiohttp.ClientError as e:
            print(f"Помилка мережі: {e}")
            return None

# Клас для обробки даних
class ExchangeRateService:
    def __init__(self, api: ExchangeRateAPI):
        self.api = api

    async def get_exchange_rates(self, days: int):
        if days > 10 or days < 1:
            raise ValueError("Кількість днів повинна бути від 1 до 10.")

        rates = []
        today = datetime.now()

        for i in range(days):
            date = (today - timedelta(days=i)).strftime("%d.%m.%Y")
            data = await self.api.fetch_exchange_rate(date)
            if data:
                rate_info = self._extract_rate_info(data)
                if rate_info:
                    rates.append({date: rate_info})

        return rates

    def _extract_rate_info(self, data):
        rate_info = {}
        if 'exchangeRate' in data:
            for rate in data['exchangeRate']:
                if rate['currency'] in ['USD', 'EUR']:
                    rate_info[rate['currency']] = {
                        'sale': rate.get('saleRate', rate.get('saleRateNB')),
                        'purchase': rate.get('purchaseRate', rate.get('purchaseRateNB'))
                    }
        return rate_info

# Клас для виведення результату
class ExchangeRateDisplay:
    def display(self, rates):
        print("Курс валют за останні дні:")
        for rate in rates:
            for date, info in rate.items():
                print(f"Дата: {date}")
                for currency, values in info.items():
                    print(f" {currency}: Продаж: {values['sale']} Покупка: {values['purchase']}")

# Головна функція
async def main(days):
    try:
        privat_api = PrivatBankAPI()
        service = ExchangeRateService(privat_api)
        display = ExchangeRateDisplay()

        rates = await service.get_exchange_rates(days)
        display.display(rates)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Використання: python main.py <кількість_днів>")
        sys.exit(1)

    try:
        days = int(sys.argv[1])
        asyncio.run(main(days))
    except ValueError:
        print("Помилка: Кількість днів повинна бути цілим числом.")
        sys.exit(1)
