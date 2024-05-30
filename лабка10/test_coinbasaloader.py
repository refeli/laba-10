import pytest
from dataloader.coinbaseloader import CoinbaseLoader

class TestClass:
    @pytest.fixture
    async def loader(self):
        return CoinbaseLoader()

    async def test_get_pairs(self, loader: CoinbaseLoader):
        data = await loader.get_pairs()
        assert data is not None and len(data) != 0, "Empty pairs list received"

    async def test_get_stats(self, loader: CoinbaseLoader):
        data = await loader.get_stats("btc-usdt")
        assert data is not None, "Failed to retrieve stats for btc-usdt"