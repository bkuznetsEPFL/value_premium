from momentum import MOM
from CryptoCompare import CryptoCompare
import json


all_symbols = []
cc = CryptoCompare()
request = cc.fetch_all()
data = json.loads((request.content).decode('utf-8'))
for s in data.get('Data'):
    all_symbols.append(s)

mom_factor = MOM(all_symbols)
mom_factor.print_caps()

