import json
import asyncio
import logging
from datetime import datetime
from enum import Enum

import aiohttp


class Granularity(Enum):
    ONE_MINUTE = 60
    FIVE_MINUTES = 300
    FIFTEEN_MINUTES = 900
    ONE_HOUR = 3600
    SIX_HOURS = 21600
    ONE_DAY = 86400


class CoinbaseLoader:
    def __init__(self, endpoint="https://api.exchange.coinbase.com"):
        self.endpoint = endpoint
        self._logger = logging.getLogger("COINBASE")
        self._logger.info("created")

    async def _get_req(self, path, params=None, session=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.endpoint}{path}", params=params) as response:
                return await response.json()

    async def get_pairs(self) -> list[dict[str, any]]:
        self._logger.debug("get pairs")
        data = await self._get_req("/products")
        return data

    async def get_stats(self, pair: str) -> dict[str, any]:
        self._logger.debug(f"get pair {pair} stats")
        data = await self._get_req(f"/products/{pair}")
        return data

    async def get_historical_data(self, pair: str, begin: str, end: str, granularity: Granularity, session=None) -> list[dict[str, any]]:
        self._logger.debug(f"get pair {pair} history")
        params = {
            "start": begin,
            "end": end,
            "granularity": granularity.value
        }
        data = await self._get_req(f"/products/{pair}/candles", params, session)
        return data


async def get_data_history(loader, resources):
    session = aiohttp.ClientSession()
    results = []
    for i in range(0, len(resources), 10):
        group = resources[i:i+10]
        tasks = [loader.get_historical_data(resource, "2023-01-01", "2023-06-30", Granularity.ONE_DAY, session) for resource in group]
        results.extend(await asyncio.gather(*tasks))
    await session.close()
    return results


async def main(num_requests):
    logging.basicConfig(level=logging.INFO)
    loader = CoinbaseLoader()

    start_time = datetime.now()
    data = await loader.get_pairs()
    print(data[0:5])

    data = await loader.get_stats("btc-usdt")
    print(data)

    resources = ["btc-usdt", "eth-usdt", "ltc-usdt", "xrp-usdt"] * num_requests
    
    # Синхронний виклик
    sync_start_time = datetime.now()
    for resource in resources:
        await loader.get_historical_data(resource, "2023-01-01", "2023-06-30", Granularity.ONE_DAY)
    sync_end_time = datetime.now()
    print(f"Синхронний час: {sync_end_time - sync_start_time}")

    # Асинхронний виклик
    async_start_time = datetime.now()
    await get_data_history(loader, resources)
    async_end_time = datetime.now()
    print(f"Асинхронний час: {async_end_time - async_start_time}")


if __name__ == "__main__":
    while True:
        try:
            num_requests = int(input("Введіть кількість запитів: "))
            break
        except ValueError:
            print("Будь ласка, введіть ціле число.")
    asyncio.run(main(num_requests))
