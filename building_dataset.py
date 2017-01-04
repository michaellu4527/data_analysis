import quandl
import pandas as pd

api_key = '3Xa54miougXruYt_HGaZ'

df = quandl.get('FMAC/HPI_AK', authtoken=api_key)

print(df.head)