# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:54:59 2020

@author: T510
"""

import pandas as pd
import numpy as np
df = pd.read_csv('acled_social_iso3.csv')# imports prepared data from acled database

df = df [~( df [ ['GDP (current US$)', ] ] == 0).all(axis=1) ] # for some rows there are no GDP availabe. => we filtered them out


# generating training set
help_df = pd.DataFrame()
country_list = df['COUNTRY'].unique()
#country_list = ['Algeria', 'Angola', 'Mali']
for countryname in country_list: # creates the labled training Data of all countrys
    help_df = pd.concat([help_df, CreateAndLableDATA(countryname, df)]) # labeling the data concering a sudden increase in battle events or demonstraions
    #help_df = pd.concat([help_df, CreateAndLableDATA_2(countryname, df)]) #labeling the data concering an increase of events in contrast to the averag
    
help_df.reset_index(drop=True, inplace = True)
help_df = help_df.loc[help_df['EVENT_DATE_MONTH'] != '2020-02'] # for some countrys there all already informations for februr available

# seperates the features from the labels
x = help_df.drop(columns = ['label', 'COUNTRY', 'iso3', 'EVENT_DATE_MONTH', 'YEAR'])# drops features that are noth helpfull for training
# here you have the option to continou with just the information of the present month
#x = x.drop(columns = ['Battles_1_month_ago','Protests_1_month_ago','Explosions/Remote violence_1_month_ago','Strategic developments_1_month_ago','Violence against civilians_1_month_ago','FATALITIES_1_month_ago','Battles_2_month_ago','Protests_2_month_ago','Explosions/Remote violence_2_month_ago','Strategic developments_2_month_ago','Violence against civilians_2_month_ago','FATALITIES_2_month_ago','Battles_3_month_ago','Protests_3_month_ago','Explosions/Remote violence_3_month_ago','Strategic developments_3_month_ago','Violence against civilians_3_month_ago','FATALITIES_3_month_ago','Battles_4_month_ago','Protests_4_month_ago','Explosions/Remote violence_4_month_ago','Strategic developments_4_month_ago','Violence against civilians_4_month_ago','FATALITIES_4_month_ago','Battles_5_month_ago','Protests_5_month_ago','Explosions/Remote violence_5_month_ago','Strategic developments_5_month_ago','Violence against civilians_5_month_ago','FATALITIES_5_month_ago'])# x_without last 6 month
x = x.drop(columns = ['Unnamed: 0', 'Unnamed: 0.1'])
y = help_df['label']# seperates the labels

# fits StandardScaler and scales features
from sklearn.preprocessing import StandardScaler
my_scaler = StandardScaler()
my_scaler.fit(x)
x = my_scaler.transform(x)

# seperates training and test data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


