from momentum import MOM
from CryptoCompare import CryptoCompare
import json
import math
import pandas as pd
import random

all_symbols = []
cc = CryptoCompare()
request = cc.fetch_all()
data = json.loads((request.content).decode('utf-8'))

# avoid for loop
for s in data.get('Data'):
    all_symbols.append(s)

mom_factor = MOM(all_symbols)
mom_factor.print_caps()






data = pd.DataFrame(columns = ['Coin','Market-Cap','Momentum'])
#for i in  range(20):#####JUST USING RANDOM VALUES FOR TESTING PURPOSES
for coin in mom_factor.market_caps:
    mom_list = mom_factor.market_caps.get(coin)
    new_row = {'Coin': coin, 'Market-Cap': mom_list[len(mom_list)-1], 'Momentum': mom_factor.momentum.get(coin)}
    data = data.append(new_row, ignore_index = True)
#print(data)

data = data[data['Market-Cap'] >= 1000000]
print(data)

data = data.sort_values(by = ['Market-Cap'],ascending= False)
print("After sorting by Market Capitalization")
print(data)

# better quantiles here
index_up = math.floor(len(data)*0.3)
index_down = math.floor(len(data)*0.7)

# quantiles, not efficient
data_up = data.iloc[:index_up+1]
data_middle = data.iloc[index_up+1: index_down+1]
data_down = data.iloc[index_down+1:]

#print("Index Up " + str(index_up))
print("Size  Portfolio UP")
print(data_up)
print("\n")
#print("Index Middle " + str(index_down))
print("Size Portfolio Middle")
print(data_middle)
print("\n")
#print("DOWN")
print("Size Portfolio  Down")
print(data_down)
print("\n")


mkcap_up = data_up['Market-Cap']
mkcap_middle = data_middle['Market-Cap']
mkcap_down = data_down['Market-Cap']

# print(data_up)
# print(mkcap_up)

sum_up = sum(mkcap_up)
sum_middle = sum(mkcap_middle)
sum_down = sum(mkcap_down)


weights_up = mkcap_up/sum_up
weights_middle = mkcap_middle/sum_middle
weights_down = mkcap_down/sum_down
# print(data_up)
# print(sum_up)
# print(weights_up)

data_up['Weights'] = weights_up
data_middle['Weights'] = weights_middle
data_down['Weights'] = weights_down

print("After computing the weights for the Size portfolio")
print(data_up)
print(data_middle)
print(data_down)
print("\n")



#### AFTER constructing THE SIZE Portfolio and the  WEIGHTS WE WILL FIND THE MOMENTUM Portfolio and its WEIGHTS ####

# better np I think
index_half = math.floor(len(data)*0.5)

big = data.iloc[:index_half+1]
small = data.iloc[index_half+1:]
print("Data  Before constructing momentum portfolio")
print(data)
print("\n")
# print("#######################################################")
# print(index_half)
# print(big)
# print("#######################################################")
#print(small)



big = big.sort_values(by = ['Momentum'],ascending= False)

print("After sorting Momentum big")

# better np here
index_big_up = math.floor(len(big)*0.3)
index_big_down = math.floor(len(big)*0.7)

big_up = big.iloc[:index_big_up+1]
big_middle = big.iloc[index_big_up+1: index_big_down+1]
big_down = big.iloc[index_big_down+1:]

print(big_up)
print(big_middle)
print(big_down)
print("\n")

small = small.sort_values(by = ['Momentum'],ascending= False)

print("After sorting Momentum small")
index_small_up = math.floor(len(small)*0.3)
index_small_down = math.floor(len(small)*0.7)

small_up = small.iloc[:index_small_up+1]
small_middle = small.iloc[index_small_up +1: index_small_down +1]
small_down = small.iloc[index_small_down +1:]

print(small_up)
print(small_middle)
print(small_down)





