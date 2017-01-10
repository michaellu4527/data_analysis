import quandl
import pandas as pd
import pickle
import matplotlib.pyplot
from matplotlib import pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

api_key = '3Xa54miougXruYt_HGaZ'

# Function to obtain list of states
def state_list():
    fifty_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return fifty_states[0][0][1:]

def grab_initial_state_data():
    states = state_list()       # Passing in state list
    main_df = pd.DataFrame()        # Creating an empty data frame

    for abbv in states:
        query = "FMAC/HPI_"+str(abbv)
        df = quandl.get(query, authtoken=api_key)
        df.rename(columns={"Value": abbv}, inplace=True)

        df[abbv] = (df[abbv] - df[abbv][0]) / df[abbv][0] * 100

        if main_df.empty:   # It's empty
            main_df = df    # Store the first data inside of it
        else:   # Not empty
            main_df = main_df.join(df, rsuffix=abbv)      # Add data to existing data frame

    print(main_df.head())
    print(df.head())

    pickle_out = open('fifty_states3.pickle', 'wb')  # wb is write back
    pickle.dump(main_df, pickle_out)
    pickle_out.close()

def HPI_Benchmark():
    abv2 = "United States"
    df = quandl.get("FMAC/HPI_USA", authtoken=api_key)
    df.rename(columns={"United States": abv2}, inplace=True)
    df["United States"] = (df[abv2] - df[abv2][0]) / df[abv2][0] * 100
    return df

#grab_initial_state_data()


fig = plt.figure()
ax1 = plt.subplot2grid((2,1),(0,0))     # (Size of plot, where you want it to start)
ax2 = plt.subplot2grid((2,1),(1,0), sharex=ax1)

HPI_data = pd.read_pickle('fifty_states3.pickle')     # Read in pickle

# HPI_data['OR12MA'] = pd.rolling_mean(HPI_data['OR'], 12)        # 12 month moving average
# HPI_data['OR12STD'] = pd.rolling_std(HPI_data['OR'], 12)
#
# print(HPI_data[['OR', 'OR12MA', 'OR12STD']].head())
#
# HPI_data[['OR', 'OR12MA']].plot(ax=ax1)     # Plotting moving average and raw data
# HPI_data[['OR12STD']].plot(ax=ax2)      # Plotting std. deviation

OR_AK_12corr = pd.rolling_corr(HPI_data['OR'], HPI_data['AK'], 12)

HPI_data['OR'].plot(ax=ax1, label='OR HPI')
HPI_data['OR'].plot(ax=ax1, label='AK HPI')
ax1.legend(loc=4)

OR_AK_12corr.plot(ax=ax2, label='OR_AK_12corr')
plt.show()
