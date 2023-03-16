import pandas as pd
from CryptoCompare import CryptoCompare
from datetime import datetime
import json


class MOM:
    """
    Momentum cryptocurrency factor as discussed
    in Y. Liu, A. Tsyvinski, Xi Wu, "Common Risk
    Factors in Cryptocurrency", pp. 20-21, see
    https://dx.doi.org/10.2139/ssrn.3379131
    """
    def __init__(self, coins_list):
        cc = CryptoCompare()
        self.dfprices = pd.DataFrame(columns = coins_list)
        self.dfmarket_caps = pd.DataFrame(columns = coins_list)
        self.dfmomentum = pd.DataFrame(columns = coins_list)
        self.dfreturns= pd.DataFrame(columns = coins_list)
        print("IN MOMENTUM RETURN")
        print(len(self.dfreturns.columns))
        for coin in coins_list:
            fetch = cc.daily_pair_ohlc(coin, 'USD', '168')
            latest = cc.get_latest(coin)
            data = json.loads((fetch.content).decode('utf-8'))
            print(data)
            data2 = json.loads((latest.content).decode('utf-8'))
            dict = ((data.get('Data')).get('Data'))
            total_supply = ((data2.get('Data').get('current_supply')))
            if dict is not None:
                close_prices = [float(x.get("close")) for x in dict]
                market_caps = [float(x.get("close")) * float(total_supply) for x in dict]
                self.dfprices[str(coin)] = close_prices
                self.dfmarket_caps[str(coin)] = market_caps

        self.dfmomentum = (self.dfprices - self.dfprices.shift(21))/self.dfprices
        self.dfreturns = self.dfreturns.fillna(0)
        self.dfprices = self.dfprices.fillna(0)
        self.dfreturns = (self.dfprices - self.dfprices.shift(1))/ self.dfprices.shift(1)
        self.dfreturns = self.dfreturns.fillna(0)
        self.dfreturns.to_csv('returns222.csv', sep =',', index = False)
        self.dfmomentum.to_csv('momentum222.csv', sep =',', index = False)
        self.dfmarket_caps.to_csv('mkcaps222.csv',sep =',', index = False)

           

    def print_mom(self):
        print(self.momentum)
    
    def print_prices(self):
        print(self.prices)
    
    def print_caps(self):
        print(self.market_caps)      
    