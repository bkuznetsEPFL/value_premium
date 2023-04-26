import requests


class CryptoCompare:
    """
    CryptoCompare API with enterprise subscription.
    See https://min-api.cryptocompare.com/documentation
    for documentation, to check if API key is valid and
    to try various endpoints.
    """
    # Java's enterprise API key (see Skype chat)
    # Key 1: 944903d112f984bfb475209cfa6e802c44dfa72f582a7f14f50961fca1a31d6e 
    # Key 2 (Thomas) : 7d9161a5c19464276f169286ae5a8d9a716de6dacecf825e14167c6783dc4348
    KEY = '944903d112f984bfb475209cfa6e802c44dfa72f582a7f14f50961fca1a31d6e'

    def __init__(self):
        self.key = {"Apikey": CryptoCompare.KEY}

    def daily_pair_ohlc(self,
                        fsym: str,
                        tsym: str,
                        limit: str,
                        e: str = 'CCCAGG',
                        ):

        # let's add tsym, e in get
        return requests.get(
           f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={fsym}&tsym={tsym}&limit={limit}",
           headers=self.key)

    def fetch_all(self):
        """
        Fetch names of all available coins.
        """
        return requests.get(f"https://min-api.cryptocompare.com/data/blockchain/list?api_key={self.KEY}")

    def get_latest(self,fsym: str):
        """
        Fetch latest data for a given coin.
        """
        return requests.get(f"https://min-api.cryptocompare.com/data/blockchain/latest?fsym={fsym}&api_key={self.KEY}")

    def get_historical(self,fsym: str,limit: str):
        """
        Fetch historical data for a given coin.
        """
        return requests.get(f"https://min-api.cryptocompare.com/data/blockchain/histo/day?fsym={fsym}&limit={limit}&api_key={self.KEY}")

