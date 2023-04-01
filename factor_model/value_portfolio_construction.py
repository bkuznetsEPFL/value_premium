from value import Value
from defillama import Llama
import json


llama = Llama()
fetch = llama.getAllProtocols()
fetch = json.loads(fetch.content.decode('utf-8'))
all_protocols = []
for protocol in fetch:
    all_protocols.append(protocol.get('name'))
all_protocols=all_protocols[0:10]
value = Value(all_protocols)
value.print()
