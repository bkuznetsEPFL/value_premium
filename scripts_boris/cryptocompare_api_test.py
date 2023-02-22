from CryptoCompare import CryptoCompare

if __name__ == '__main__':
    cc = CryptoCompare()
    BTC = cc.daily_pair_ohlc('BTC', 'USD')
    breakpoint()

