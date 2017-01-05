import quandl
import pandas as pd

api_key = '3Xa54miougXruYt_HGaZ'

# df = quandl.get('FMAC/HPI_AK', authtoken=api_key)
#
# print(df.head)

fifty_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')

# # Prints entire list
# print(fifty_states)
#
# # Prints very first data frame
# print(fifty_states[0])

# Prints very first column of first data frame
print(fifty_states[0][0])

for abbv in fifty_states[0][0][1:]:
    print("FMAC/HPI_" + str(abbv))
