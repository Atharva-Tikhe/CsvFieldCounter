import pandas as pd
import numpy as np
from pandas_profiling import ProfileReport  

df = pd.read_csv('dummy_data.csv')

profile = ProfileReport(df)
# profile

diff_val = list(pd.unique(df["number(num)"]))

sub_frame_list = []

for new_val in diff_val:
    sub_frame_list.append(df[df["number(num)"] == new_val])

# sub_frame_list[0]
# sub_frame_list[1]
# sub_frame_list[2]
sub_df = sub_frame_list[2]

## Find Duplicate Rows

sub_df[sub_df.duplicated(subset = ['property_numeric_value','property_val_units','property_value'], keep = False)]

def append_text(elem):
    return elem + 791

def add_q_if_p(elem):
    if elem == 'p':
        return elem + 'q'
    else:
        return elem
    
def apply_nan(elem):
    if elem == r'/N':
        return np.nan
    else:
        return elem
    

df[df["species"] == "cxdw"]

## Apply a function to a column

# sub_df.iat[0,2] = 2314
# sub_df["inchi(num)"] = sub_df["inchi(num)"].apply(append_text)
# sub_df["property_name"] = sub_df["property_name"].apply(add_q_if_p)

df.iat[15, 8] = r'/N'
df.iat[16, 8] = r'/N'
df.iat[17, 8] = r'/N'
df

df["property_name"] = df["property_name"].apply(add_q_if_p)


# if inchi is even -> add 100
def change_inchi(elem):
    if elem % 2 == 0:
        return elem + 100
    else:
        return elem
    
df["inchi(num)"] = df["inchi(num)"].apply(change_inchi)

df["property_numeric_value"] = df["property_numeric_value"].apply(apply_nan)

df

"Atharva \"Tikhe\",mit"

# find and take out special chars using regex

df.iat[17,13] = "Atharva \"Tikhe\",mit"

df

## Regular expression for finding special characters

df["property_condition_units"].str.match(r'^[a-zA-Z0-9]*$')

df["mode of delivery"].str.match(r'^[a-zA-Z0-9 ,]*$')

df.iat[7,12]
df["mode of delivery"]

def find_newline(elem):
    if r'\n' in elem:
        return 

cols = df.columns
last_col = cols[len(cols)-1]

string = "something\n"
string[-1]

