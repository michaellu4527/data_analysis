import quandl
import pandas as pd
import pickle
import matplotlib.pyplot
from matplotlib import pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

api_key = '3Xa54miougXruYt_HGaZ'

def mortgage_30y():
    abv2 = "Value"
    df = quandl.get("FMAC/MORTG", trim_start="1975-01-01", authtoken=api_key)   # Specify a different starting value
    df.rename(columns={"Value": abv2}, inplace=True)

    df["Value"] = (df[abv2] - df[abv2][0]) / df[abv2][0] * 100
    df = df.resample('1D').mean()   # Need to supersample first in order for Python to know there
                                    # are values for resampling later date
    df = df.resample('M').mean()
    df.columns = ['M30']
    return df

def sp500_data():
    df = quandl.get("YAHOO/INDEX_GSPC", trim_start="1975-01-01", authtoken=api_key)
    df["Adjusted Close"] = (df["Adjusted Close"]-df["Adjusted Close"][0]) / df["Adjusted Close"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Adjusted Close':'S&P 500'}, inplace=True)     # Rename to S&P 500
    df = df['S&P 500']
    return df

def gdp_data():
    df = quandl.get("BCB/4385", trim_start="1975-01-01", authtoken=api_key)
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Value':'GDP'}, inplace=True)    # Rename to GDP
    df = df['GDP']
    return df

def us_unemployment():
    df = quandl.get("ECPI/JOB_G", trim_start="1975-01-01", authtoken=api_key)
    df["Unemployment Rate"] = (df["Unemployment Rate"]-df["Unemployment Rate"][0]) / df["Unemployment Rate"][0] * 100.0
    df=df.resample('1D').mean()
    df=df.resample('M').mean()
    return df


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
    df.rename(columns={"Value": abv2}, inplace=True)    # Renames columns since everything is "Value" right now
    df["United States"] = (df[abv2] - df[abv2][0]) / df[abv2][0] * 100
    return df

#grab_initial_state_data()

sp500 = sp500_data()
US_GDP = gdp_data()
US_unemployment = us_unemployment()
m30 = mortgage_30y()

HPI_data = pd.read_pickle('fifty_states3.pickle')     # Read in pickle
HPI_bench = HPI_Benchmark()

HPI = HPI_data.join([HPI_bench, m30, sp500, US_GDP, US_unemployment])
HPI.dropna(inplace="True")

print(HPI)
print(HPI.corr())

HPI.to_pickle("HPI.pickle")

#print (state_HPI_M30.corr()['M30'].describe())


#
# HPI_data['OR1yr'] = HPI_data['OR'].resample('A', how='mean')    # A is annually. Check documentation for resampling options#
#
# # Option 2
# print(HPI_data[['OR', 'OR1yr']].head())
# HPI_data.fillna(method='ffill', inplace=True)   # Takes previous value and fills it in up until the next y value.
#                                                 # Will result in step function
# #HPI_data.fillna(method='bfill', inplace=True)   # Takes future value and fill it backwards to next y value.
# print(HPI_data[['OR', 'OR1yr']].head())
#
# HPI_data[['OR', 'OR1yr']].plot(ax=ax1)     # Plotting raw data
#
#
# plt.legend(loc=4)
# plt.show()
