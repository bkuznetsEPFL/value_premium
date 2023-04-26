# Import necessary libraries
from momentum import MOM
from CryptoCompare import CryptoCompare
from portfolio_plot  import plotter
import json
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Fetch all symbols from CryptoCompare API
all_symbols = []
cc = CryptoCompare()
request = cc.fetch_all()
data = json.loads((request.content).decode('utf-8'))
#all_symbols = ['BTC','ETH']
all_symbols = [str(s) for s in data.get('Data')]

# Compute momentum factor using MOM function from rendu_momentum module

# UNCOMMENT NEXT LINES TO RUN THE CODE WITH LATEST DATA
# mom_factor = MOM(all_symbols)
# mkcap = mom_factor.dfmarket_caps
# momt = mom_factor.dfmomentum
# dfreturns = mom_factor.dfreturns
# dfvolume = mom_factor.dfvolume    

# UNCOMMENT NEXT LINES TO RUN THE CODE WITH SAVED DATA
mkcap = pd.read_csv ('data/dfmkcaps.csv')
momt =  pd.read_csv ('data/dfmoms.csv')
dfreturns = pd.read_csv ('data/dfreturns.csv')
dfvolume = pd.read_csv ('data/dfvolume.csv') 

# Create an empty dataframe to store market portfolio weights
mkt_data_portfolio = pd.DataFrame()

size_portfolio = pd.DataFrame()

momentum_big_portfolio = pd.DataFrame()


# Loop through each date in the momentum factor dataframe
for index, row in momt.iterrows():
    # Create a new dataframe to store coin data for the current date
    data = pd.DataFrame(columns = ['Coin','Market-Cap','Momentum','VolumeTo'])
    
    # Get market cap and volume data for current date
    mkcap_r = mkcap.iloc[index]
    volume_r = dfvolume.iloc[index]
    
    # If data is available 21 days ago, get market cap, momentum, and volume data for that date
    if index > 21:
        data21 = pd.DataFrame(columns = ['Coin','Market-Cap','Momentum','VolumeTo'])
        mkcap21 = mkcap.iloc[index - 21]
        volume21 = dfvolume.iloc[index - 21]
        momentum21 = momt.iloc[index - 21]
        
    # Loop through each coin in the momentum factor dataframe
    for j,col in enumerate(momt.columns):
        # Create a new row with coin data
        new_row = {'Coin': col, 'Market-Cap':mkcap_r[j], 'Momentum': row[j],'VolumeTo': volume_r[j]}
        # Append the new row to the data dataframe
        data = data.append(new_row, ignore_index = True)
        # If data is available 21 days ago, create a new row with coin data for that date and append it to the data21 dataframe
        if index > 21:
            new_row21 = {'Coin': col, 'Market-Cap':mkcap21[j], 'Momentum': momentum21[j],'VolumeTo': volume21[j]}
            data21 = data21.append(new_row21, ignore_index = True)
    
    # Define a condition for removing coins from the portfolio
    condition  = (data['Market-Cap'] < 1000000) | (pd.isna(data['Market-Cap'])) | (data['VolumeTo'] < 10000 )| (pd.isna(data['VolumeTo']))
    # Create a copy of the data dataframe to use for momentum calculations
    data_for_momentum = data.copy()
    # Remove coins that meet the condition and store them in the removed_data dataframe
    removed_data = data[condition]
    removed_data['Weights'] = np.nan
    # Keep coins that meet the inverse condition in  the data dataframe
    data = data[~condition]
    # Sort the remaining coins in the data dataframe by market cap in descending order
    data = data.sort_values(by = ['Market-Cap'],ascending= False)
    # Create a copy of the data dataframe to use for market portfolio calculations
    market_portfolio = data.copy()

    # Calculate the weights of each coin in the market portfolio based on market cap
    sum_mc = sum(market_portfolio['Market-Cap'])
    market_portfolio['Weights'] = market_portfolio['Market-Cap']/sum_mc
    market_portfolio.drop('Momentum',axis=1,inplace=True)
    market_portfolio.drop('Market-Cap',axis= 1,inplace= True)
    market_portfolio = market_portfolio.sort_values('Coin')

    # Concatenate the market portfolio with the weights of all coins, and reset the index
    mdf = pd.concat([removed_data[['Coin','Weights']],market_portfolio[['Coin','Weights']]])
    mkt_data_portfolio  = mkt_data_portfolio.reset_index(drop=True)
    mdf = mdf.sort_values('Coin')
    weights = mdf['Weights'].T
    mkt_data_portfolio = mkt_data_portfolio.append(weights, ignore_index=False)

    # Split the coins into three size groups based on market cap, and calculate the weights of each group
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

    # Assign the weights to each coin based on size and momentum, multiplied by the investment strategy (sign)
    data_up['Weights'] = -1*weights_up # SHORT BIG COMPANIES
    data_middle['Weights'] = 0
    data_down['Weights'] = weights_down # LONG SMALL COMPANIES 

    # Concatenate the size portfolio with the weights of all coins
    size_p = pd.concat([removed_data[['Coin','Weights']],data_up[['Coin','Weights']],data_middle[['Coin','Weights']],data_down[['Coin','Weights']]])
    size_p['Coin'] = size_p['Coin'].astype(str)
    # Sort on 'Coin', to become consistent with the other dates
    size_p = size_p.sort_values('Coin')
    size_portfolio = size_portfolio.reset_index(drop=True)
    weights = size_p['Weights'].T
    size_portfolio = size_portfolio.append(weights, ignore_index=False)

    # Remove coins with market cap less than a million, and Volume less than 10000, and assign them NaN weights
    data_for_momentum.replace([np.inf, -np.inf], np.nan, inplace=True)
    #Ensure that the conditions also hold, at  time t-21
    condition21 = (data21['Market-Cap'] < 1000000) | (pd.isna(data21['Market-Cap'])) | (data21['VolumeTo'] < 10000 )| (pd.isna(data21['VolumeTo']))     if index > 21 else False
    condition = (data_for_momentum['Market-Cap'] < 1000000) | (pd.isna(data_for_momentum['Market-Cap'])) | (data_for_momentum['VolumeTo'] < 10000 )| (pd.isna(data_for_momentum['VolumeTo'])) | (pd.isna(data_for_momentum['Momentum']))
    condition = condition | condition21
    removed_data = data_for_momentum[condition]
    removed_data['Weights'] = np.nan


    # Keep data based on the opposite condition and sort the remaining data by market capitalization in descending order.
    data_for_momentum = data_for_momentum[~condition]
    data_for_momentum = data_for_momentum.sort_values(by=['Market-Cap'], ascending=False)

    # Split data into two groups - those with market capitalization above the 50th percentile and those with market capitalization below or equal to the 50th percentile.
    colmk = data_for_momentum['Market-Cap']
    small = data_for_momentum.loc[colmk <= colmk.quantile(0.5)]
    big = data_for_momentum.loc[colmk > colmk.quantile(0.5)]

    # For the big group, split into three subgroups based on momentum -
    # those with momentum above the 70th percentile, those with momentum between the 30th and 70th percentile,
    #  and those with momentum below or equal to the 30th percentile.
    colmom = big['Momentum']
    q1 = colmom.quantile(0.3)
    q2 = colmom.quantile(0.7)
    big_up = big.loc[colmom > q2]
    big_middle = big.loc[(q1 < colmom) & (colmom <= q2)]
    big_down = big.loc[colmom <= q1]

    # Calculate weights based on market capitalization and assign a value of 1 for the subgroup with the highest momentum,
    #  0 for the subgroup with medium momentum, and -1 for the subgroup with the lowest momentum.
    #  Multiply weights with the investment strategy sign for each subgroup.
    big_up['Weights'] = big_up['Market-Cap'] / sum(big_up['Market-Cap'])  # LONG
    big_middle['Weights'] = 0
    big_down['Weights'] = -1 * big_down['Market-Cap'] / sum(big_down['Market-Cap'])  # SHORT


    # For the small group, split into three subgroups based on momentum - 
    # those with momentum above the 70th percentile, those with momentum between the 30th and 70th percentile, 
    # and those with momentum below or equal to the 30th percentile.
    colmom = small['Momentum']
    q1 = colmom.quantile(0.3)
    q2 = colmom.quantile(0.7)
    small_up = small.loc[colmom > q2]
    small_middle = small.loc[(q1 < colmom) & (colmom <= q2)]
    small_down = small.loc[colmom <= q1]

    # Calculate weights based on market capitalization and assign a value of 1 for the subgroup with the highest momentum,
    #  0 for the subgroup with medium momentum, and -1 for the subgroup with the lowest momentum. 
    # Multiply weights with the investment strategy sign for each subgroup.
    small_up['Weights'] = small_up['Market-Cap'] / sum(small_up['Market-Cap'])  # LONG
    small_middle['Weights'] = 0
    small_down['Weights'] = -1 * small_down['Market-Cap'] / sum(small_down['Market-Cap'])  # SHORT


    
    #Reconcatenate all the coins, to be consistent with the columns of the data frame containing all dates
    momentum_conc = pd.concat([removed_data[['Coin','Weights']],big_up[['Coin','Weights']],big_middle[['Coin','Weights']],big_down[['Coin','Weights']],small_up[['Coin','Weights']],small_middle[['Coin','Weights']],small_down[['Coin','Weights']]])
    momentum_conc = momentum_conc.sort_values('Coin')
 
    momentum_conc = momentum_conc[['Coin','Weights']]
    momentum_conc['Coin'] = momentum_conc['Coin'].astype(str)


    momentum_big_portfolio = momentum_big_portfolio.reset_index(drop=True)
    momentum_conc = momentum_conc.sort_values(by = 'Coin')
    weights = momentum_conc['Weights'].T

  
    momentum_big_portfolio = momentum_big_portfolio.append(weights, ignore_index=False)


#Save portolio weights*investment strategy in csv files
momentum_big_portfolio.to_csv('data/Portfolio-Momentum.csv', sep =',', index = False)
mkt_data_portfolio.to_csv('data/Portfolio-Market.csv',sep =',', index = False)
size_portfolio.to_csv('data/Portfolio-Size.csv',sep =',', index = False)

#Returns are shifted and then multiplied by the weights
returns_shifted = dfreturns.shift(-1)
return_cols = dfreturns.columns.tolist()

rename_dict = dict(zip(momentum_big_portfolio.columns.tolist(), return_cols))

momentum_big_portfolio = momentum_big_portfolio.rename(columns=rename_dict)
mom_mul = momentum_big_portfolio.mul(returns_shifted)

mom_ret = mom_mul.sum(axis = 1)
mom_ret.to_csv('data/Momentum-returns.csv',sep =',', index = False)


mkt_data_portfolio = mkt_data_portfolio.rename(columns=rename_dict)
mkt_mul = mkt_data_portfolio.mul(returns_shifted)
mkt_ret = mkt_mul.sum(axis = 1)
mkt_ret.to_csv('data/Market-returns.csv',sep =',', index = False)

size_portfolio = size_portfolio.rename(columns=rename_dict)

size_mul = size_portfolio.mul(returns_shifted)
size_ret = size_mul.sum(axis = 1)
size_ret.to_csv('data/Size-returns.csv',sep =',', index = False)

#Plot the portfolios
plotter('data/Market-returns.csv','data/Size-returns.csv','data/Momentum-returns.csv')