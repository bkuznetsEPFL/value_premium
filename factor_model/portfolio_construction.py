from momentumm import MOM
from CryptoCompare import CryptoCompare
import json
import math
import pandas as pd
import random
import numpy as np
import matplotlib as plt

all_symbols = []
cc = CryptoCompare()
request = cc.fetch_all()
data = json.loads((request.content).decode('utf-8'))

all_symbols = [str(s) for s in data.get('Data')]
print(len(all_symbols))

mom_factor = MOM(all_symbols)

mkcap = mom_factor.dfmarket_caps

momt = mom_factor.dfmomentum
dfreturns = mom_factor.dfreturns


# momt = pd.read_csv("momentum22.csv", sep=',')
# mkcap = pd.read_csv('mkcaps22.csv', sep=',')
# dfreturns = pd.read_csv('returns22.csv', sep=',')

dfreturns =dfreturns.fillna(0)
mkcap = mkcap.fillna(0)
momt = momt.fillna(0)
print(dfreturns.head())

# momentum_big_portfolio = pd.DataFrame(columns=all_symbols)
momentum_big_portfolio = pd.DataFrame()


print(momentum_big_portfolio.columns)

size_portfolio = pd.DataFrame()
mkt_data_portfolio = pd.DataFrame()
combined_data = mkcap.combine(momt,lambda v1,v2: np.array(zip(v1,v2)))

for index, row in combined_data.iterrows():#Each row is a date

    data = pd.DataFrame(columns = ['Coin','Market-Cap','Momentum'])
    for j,col in enumerate(combined_data.columns):
        new_row = {'Coin': col, 'Market-Cap':row[j][0], 'Momentum': row[j][1]}
        data = data.append(new_row, ignore_index = True)


    removed_data = data[data['Market-Cap'] < 1000000]#Coins with market cap less than a million
    removed_data['Weights'] = 0 
    
    data = data[data['Market-Cap'] >= 1000000]

    data = data.sort_values(by = ['Market-Cap'],ascending= False)


    market_portfolio = data.copy()


    sum_mc = sum(market_portfolio['Market-Cap'])

    market_portfolio['Weights'] = market_portfolio['Market-Cap']/sum_mc
    market_portfolio.drop('Momentum',axis=1,inplace=True)
    market_portfolio.drop('Market-Cap',axis= 1,inplace= True)

    market_portfolio = market_portfolio.sort_values('Coin')


    market_portfolio['Coin'] = market_portfolio['Coin'].astype(str)
    #Reconcatenate all the coins, to be consistent with the columns of the data frame containing all dates
    mdf = pd.concat([removed_data[['Coin','Weights']],market_portfolio[['Coin','Weights']]])

    mdf['Weights'] = mdf['Weights'].fillna(0)


    mkt_data_portfolio  = mkt_data_portfolio.reset_index(drop=True)

    mdf = mdf.sort_values('Coin')#The sorting is done so that the columns in the row match the columns of the dataframe
    weights = mdf['Weights'].T
    mkt_data_portfolio = mkt_data_portfolio.append(weights, ignore_index=False)#Append market portfolio for the processed date



    colmk = data['Market-Cap']
    q1 = colmk.quantile(0.3)
    q2 = colmk.quantile(0.7)
    data_up = data.loc[colmk > q2]
    data_middle = data.loc[(q1 < colmk) & (colmk <= q2)]
    data_down = data.loc[colmk <= q1]



    mkcap_up = data_up['Market-Cap']
    mkcap_middle = data_middle['Market-Cap']
    mkcap_down = data_down['Market-Cap']


    sum_up = sum(mkcap_up)
    sum_middle = sum(mkcap_middle)
    sum_down = sum(mkcap_down)


    weights_up = mkcap_up/sum_up
    weights_middle = mkcap_middle/sum_middle
    weights_down = mkcap_down/sum_down

    #Multiplying weights*investment strategy(sign)
    data_up['Weights'] = -1*weights_up#SHORT BIG COMPANIES
    data_middle['Weights'] = 0
    data_down['Weights'] = weights_down#LONG SMALL COMPANIES (SIZE)

    #Reconcatenate all the coins, to be consistent with the columns of the data frame containing all dates
    size_p = pd.concat([removed_data[['Coin','Weights']],data_up[['Coin','Weights']],data_middle[['Coin','Weights']],data_down[['Coin','Weights']]])


    size_p['Coin'] = size_p['Coin'].astype(str)
    size_p = size_p.sort_values('Coin')




    size_portfolio = size_portfolio.reset_index(drop=True)

    weights = size_p['Weights'].T
    size_portfolio = size_portfolio.append(weights, ignore_index=False)


    colmk = data['Market-Cap']
    small = data.loc[colmk <= colmk.quantile(0.5)]
    big = data.loc[colmk > colmk.quantile(0.5)]

    colmom = big['Momentum']
    q1 = colmom.quantile(0.3)
    q2 = colmom.quantile(0.7)
    big_up = big.loc[colmom > q2]
    big_middle = big.loc[(q1 < colmom) & (colmom <= q2)]
    big_down = big.loc[colmom <= q1]

    #Multiplying weights*investment strategy(sign)
    big_up['Weights'] = big_up['Momentum']/sum(big_up['Momentum'])#LONG
    big_middle['Weights'] = 0
    big_down['Weights'] = -1*big_down['Momentum']/sum(big_down['Momentum'])#SHORT  


    colmom = small['Momentum']
    q1 = colmom.quantile(0.3)
    q2 = colmom.quantile(0.7)
    small_up = small.loc[colmom > q2]
    small_middle = small.loc[(q1 < colmom) & (colmom <= q2)]
    small_down = small.loc[colmom <= q1]
    #Multiplying weights*investment strategy(sign)
    small_up['Weights'] = small_up['Momentum']/sum(small_up['Momentum'])#LONG
    small_middle['Weights'] = 0
    small_down['Weights'] = -1*small_down['Momentum']/sum(small_down['Momentum'])#SHORT

    #Reconcatenate all the coins, to be consistent with the columns of the data frame containing all dates
    momentum_conc = pd.concat([removed_data[['Coin','Weights']],big_up[['Coin','Weights']],big_middle[['Coin','Weights']],big_down[['Coin','Weights']],small_up[['Coin','Weights']],small_middle[['Coin','Weights']],small_down[['Coin','Weights']]])
    momentum_conc = momentum_conc.sort_values('Coin')
 
    momentum_conc = momentum_conc[['Coin','Weights']]
    momentum_conc['Coin'] = momentum_conc['Coin'].astype(str)


    momentum_conc['Weights'] = momentum_conc['Weights'].fillna(0)
    momentum_big_portfolio = momentum_big_portfolio.reset_index(drop=True)
    momentum_conc = momentum_conc.sort_values(by = 'Coin')
    weights = momentum_conc['Weights'].T
    momentum_big_portfolio = momentum_big_portfolio.append(weights, ignore_index=False)

    print(momentum_big_portfolio.head(40))

#Save portolio weights*investment strategy in csv files
momentum_big_portfolio.to_csv('MOM_PORTFOLIO_test.csv', sep =',', index = False)
mkt_data_portfolio.to_csv('MARKET_PORTFOLIO_test.csv',sep =',', index = False)
size_portfolio.to_csv('SIZE_PORTFOLIO_test.csv',sep =',', index = False)

return_cols = dfreturns.columns.tolist()
rename_dict = dict(zip(momentum_big_portfolio.columns.tolist(), return_cols))

momentum_big_portfolio = momentum_big_portfolio.rename(columns=rename_dict)
mom_mul = momentum_big_portfolio.mul(dfreturns)

mom_ret = mom_mul.sum(axis = 1)
mom_ret.to_csv('MOMENT_RETURNS_test.csv',sep =',', index = False)


mkt_data_portfolio = mkt_data_portfolio.rename(columns=rename_dict)

mkt_mul = mkt_data_portfolio.mul(dfreturns)
mkt_ret = mkt_mul.sum(axis = 1)
mkt_ret.to_csv('MARKET_RETURNS_test.csv',sep =',', index = False)

size_portfolio = size_portfolio.rename(columns=rename_dict)

size_mul = size_portfolio.mul(dfreturns)
size_ret = size_mul.sum(axis = 1)
size_ret.to_csv('SIZE_RETURNS_test.csv',sep =',', index = False)
################################################################################################

headers = ['Market Portfolio Returns']

df_market = pd.read_csv('MARKET_RETURNS_test.csv', names=headers)
df_market = df_market.replace([np.inf, -np.inf], np.nan).dropna(axis=0)
df_market = df_market.mask(df_market.eq('None')).dropna()

df_market['Market Portfolio Returns'] +=1
df_market = df_market.cumprod()

headers = ['Size Portfolio Returns']

df_size = pd.read_csv('SIZE_RETURNS_test.csv', names=headers)
df_size = df_size.replace([np.inf, -np.inf], np.nan).dropna(axis=0)
df_size = df_size.mask(df_size.eq('None')).dropna()

df_size['Size Portfolio Returns'] +=1
df_size = df_size.cumprod()

ax = df_market.plot()
df_size.plot(ax=ax)

plt.xlabel("Date")
plt.ylabel("Value of 1 dollar invested")
plt.show()



    

