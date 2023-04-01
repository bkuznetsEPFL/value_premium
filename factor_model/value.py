import pandas as pd
from defillama import Llama
from datetime import datetime as dt
import json
import pandas as pd

class Value:
    def __init__(self, protocol_list):
        llama = Llama()
        self.tvls = pd.DataFrame(columns=protocol_list)
        self.tvls['date']=pd.date_range(start='2019-01-04', end='2023-03-31').strftime('%Y-%m-%d')
        self.tvls.set_index('date', inplace=True)
        for protocol in protocol_list:
            fetch = llama.getTvl(protocol)
            fetch = json.loads(fetch.content.decode('utf-8'))
            tvls = fetch.get('chainTvls')
            if (tvls is not None):
                tvls = list(tvls.values())[0]
                if (tvls is not None):
                    tvls = tvls.get('tvl')
                    for pair in tvls:
                        date = pair.get('date')
                        date = pd.to_datetime(date, unit='s').date()
                        print (date)
                        tvl = pair.get('totalLiquidityUSD')
                        self.tvls.at[str(date), str(protocol)] = tvl
                        

                        
            #self.tvls[str(protocol)] = tvl
        self.tvls = self.tvls.fillna(0)
        self.tvls.to_csv('tvls.csv', sep=',', index=True)
        
    def print(self):
        print(self.tvls)