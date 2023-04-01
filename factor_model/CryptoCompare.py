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

        # header['fsym'] = fsym
        # header['tsym'] = tsym
        # header['e'] = e
        # header['limit'] = limit


        # let's add tsym, e in get
        return requests.get(
           f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={fsym}&tsym=USD&limit={limit}",
           headers=self.key)

    # get rid of this if not needed
    def order_book_l1(self):
        return requests.get(
            "https://min-api.cryptocompare.com/data/ob/l1/top?fsyms=BTC,"
            "ETH&tsyms=USD,EUR&e=coinbase",
            headers=self.key)

    def order_book_l2(self):
        return requests.get(
            "https://min-api.cryptocompare.com/data/v2/ob/l2/snapshot",
            headers=self.key)

    # do self.key
    def fetch_all(self):
        return requests.get(f"https://min-api.cryptocompare.com/data/blockchain/list?api_key={self.KEY}")

    # do self.key
    def get_latest(self,fsym: str):
        return requests.get(f"https://min-api.cryptocompare.com/data/blockchain/latest?fsym={fsym}&api_key={self.KEY}")

