from CryptoCompare import CryptoCompare
from datetime import datetime
import json

if __name__ == '__main__':
    cc = CryptoCompare()
    BTC = cc.daily_pair_ohlc('BTC', 'USD', '20')
    data = json.loads((BTC.content).decode('utf-8'))
    dict =  ((data.get('Data')).get('Data'))
    for x in dict:
        ts = int(x.get('time'))
        formatted = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')[:10]
        x['time_formatted'] = formatted
        print (x)
    
        



