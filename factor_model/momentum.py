import pandas as pd
from CryptoCompare import CryptoCompare
import json
import numpy as np


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
        self.dfvolume = pd.DataFrame(columns = coins_list)
        self.dfmomentum = pd.DataFrame(columns = coins_list)
        self.dfreturns= pd.DataFrame(columns = coins_list)
       

        for coin in coins_list: 
            i=0
    

            fetch = cc.daily_pair_ohlc(coin, 'USD', '150')
            historical = cc.get_historical(coin, '150')
            data = json.loads((fetch.content).decode('utf-8'))
            data2 = json.loads((historical.content).decode('utf-8'))
            dict = ((data.get('Data')).get('Data'))
            dict2 = ((data2.get('Data')).get('Data'))
            total_supply = []
            
            
            total_supply = [x.get('current_supply') if x.get('current_supply') is not None else 0  for x in dict2]
           
            if ((dict is not None) and (len(dict2)== len(dict)-1)):
                dict = dict[1:]
                close_prices = [float(x.get("close")) if float(x.get("close")) > 0.01 else np.nan  for x in dict]
                market_caps=[]
                for x in dict :
                  
                    if i < len(total_supply):
                        close = float(x.get("close"))
                        supply = float(total_supply[i])
                        cap = close * supply
                        market_caps.append(cap)
                        i+=1
                        
                volume = [float(x.get("volumeto"))  if x.get("volumeto") is not None else 0 for x in dict ]
                self.dfvolume[str(coin)] = volume
                self.dfprices[str(coin)] = close_prices
                self.dfmarket_caps[str(coin)] = market_caps

        
        self.dfprices.replace(0, np.nan, inplace=True)
        self.dfreturns = (self.dfprices - self.dfprices.shift(1))/ self.dfprices.shift(1)
        self.dfmomentum = (self.dfreturns - self.dfreturns.shift(21))/self.dfreturns.shift(21)

        self.dfmomentum.to_csv('data/dfmoms.csv', sep =',', index = False)
        self.dfmarket_caps.to_csv('data/dfmkcaps.csv',sep =',', index = False)
        self.dfreturns.to_csv('data/dfreturns.csv',sep =',', index = False)
        self.dfvolume.to_csv('data/dfvolume.csv',sep =',', index = False)
        self.dfreturns.to_csv('data/dfreturns.csv',sep =',', index = False)
        

           
