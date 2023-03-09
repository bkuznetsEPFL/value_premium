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
    prices = {}
    market_caps = {}
    momentum = {}
    def __init__(self, coins_list):
        cc = CryptoCompare()
        for coin in coins_list:
                # I would set limit=2000 and fetch everything, then
                # compute momentum values for all dates at once, e.g.
                # not dict but dataframe and without for loop below
                fetch = cc.daily_pair_ohlc(coin, 'USD', '21')
                latest = cc.get_latest(coin)
                data = json.loads((fetch.content).decode('utf-8'))
                data2 = json.loads((latest.content).decode('utf-8'))
                dict =  ((data.get('Data')).get('Data'))
                total_supply = ((data2.get('Data').get('current_supply')))
                if (dict is not None):
                    self.prices[coin]=[]
                    self.market_caps[coin]=[]
                    for x in dict:
                        close = x.get("close")
                        self.prices[coin].append(float(close))
                        cap = float(close)*float(total_supply)
                        self.market_caps[coin].append(cap)
                    
                    self.compute_mom(coin)


    def compute_mom(self,coin_name):
         
         
                close_today =self.prices[coin_name][len(self.prices[coin_name])-1]
                close_three_weeks_ago = self.prices[coin_name][0]
                # this is not 3-week return though
                self.momentum[coin_name] = close_today-close_three_weeks_ago
           

    def print_mom(self):
        print(self.momentum)
    
    def print_prices(self):
        print(self.prices)
    
    def print_caps(self):
        print(self.market_caps)      
    

                    



       



