import quandl
import pandas as pd
import matplotlib.pyplot
from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np
style.use('fivethirtyeight')

api_key = '3Xa54miougXruYt_HGaZ'

housing_data = pd.read_pickle("HPI.pickle")

housing_data = housing_data.pct_change()
print(housing_data.head())

housing_data.replace([np.inf, -np.inf], np.nan, inplace=True)       # inf is infinity
housing_data.dropna(inplace=True)
