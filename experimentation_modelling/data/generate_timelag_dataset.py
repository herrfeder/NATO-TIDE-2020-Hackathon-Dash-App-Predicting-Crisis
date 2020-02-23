# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:54:59 2020

@author: Oliver Bornschlegl
"""

import pandas as pd
import numpy as np

# returns the labled training data of one country
def CreateAndLableDATA (NameOfCountry, df):
    
    df_example = df.loc[df['COUNTRY'] == NameOfCountry]
    
    # adding informations of past
    df_example.reset_index(drop=True, inplace = True)
    for index, row in df_example.iterrows():
        
        for i in range(1,6): # adds a column with the eventdata of the last half year to each row 
            name ='Battles_'+str(i)+'_month_ago'
            df_example.loc[index+i, name] = df_example.loc[index, 'Battles']
            'Riots_'+str(i)+'_month_ago'
            df_example.loc[index+i, name] = df_example.loc[index, 'Riots']
            name = 'Protests_'+str(i)+'_month_ago'
            df_example.loc[index+i, 'Protests_'+str(i)+'_month_ago'] = df_example.loc[index, 'Protests']
            name = 'Explosions/Remote violence_'+str(i)+'_month_ago'
            df_example.loc[index+i, name] = df_example.loc[index, 'Explosions/Remote violence']
            name = 'Strategic developments_'+str(i)+'_month_ago'
            df_example.loc[index+i, name] = df_example.loc[index, 'Strategic developments']
            name = 'Violence against civilians_'+str(i)+'_month_ago'
            df_example.loc[index+i, name] = df_example.loc[index, 'Violence against civilians']
            name = 'FATALITIES_'+str(i)+'_month_ago'
            df_example.loc[index+i, name] = df_example.loc[index, 'FATALITIES']
        
#----labeling the data concerning an sudden increase in battles or demonstrations

    df_example.reset_index(drop=True, inplace = True)
    for index, row in df_example.iterrows():
        if index < len(df_example)-1:
            if df_example.loc[index+1, 'Battles'] > 1.3*df_example.loc[index, 'Battles'] or df_example.loc[index+1, 'Explosions/Remote violence'] > 1.3*df_example.loc[index, 'Explosions/Remote violence'] or df_example.loc[index+1, 'Violence against civilians'] > 1.3*df_example.loc[index, 'Violence against civilians']: # sudden increase of violent events => definition for battle case
                df_example.loc[index, 'label'] = 2 # sudden battle case is going to come
                
            if df_example.loc[index+1, 'Protests'] > 1.3*df_example.loc[index, 'Protests'] or df_example.loc[index+1, 'Riots'] > 1.3*df_example.loc[index, 'Riots']: # sudden increase of demonstations => definition for protest riot case
                    df_example.loc[index, 'label'] = 3 # sudden protest Riot case is going to come
                    
                    if (df_example.loc[index+1, 'Battles'] > 1.3*df_example.loc[index, 'Battles'] or df_example.loc[index+1, 'Explosions/Remote violence'] > 1.3*df_example.loc[index, 'Explosions/Remote violence'] or df_example.loc[index+1, 'Violence against civilians'] > 1.3*df_example.loc[index, 'Violence against civilians']) and (df_example.loc[index+1, 'Protests'] > 1.3*df_example.loc[index, 'Protests'] or df_example.loc[index+1, 'Riots'] > 1.3*df_example.loc[index, 'Riots']): # both condition for battle case and protest_riot_case
                        df_example.loc[index, 'label'] = 4 # sudden battle case and sudden Riot case is going to come
            else:
                df_example.loc[index, 'label'] = 1 # it will go on as usual 
           
    df_example = df_example.dropna() # case of the forloop there are some NaNs i the last row, which are droped here
    return df_example

if __name__ == '__main__':
    
    df = pd.read_csv('acled_social_iso3.csv')# imports prepared data from acled database
    # generating training set
    help_df = pd.DataFrame()
    country_list = df['COUNTRY'].unique()
    #country_list = ['Algeria', 'Angola', 'Mali']
    for countryname in country_list: # creates the labled training Data of all countrys
        help_df = pd.concat([help_df, CreateAndLableDATA(countryname, df)])
        
    help_df.reset_index(drop=True, inplace = True)
    
    # seperates the features from the labels
    x = help_df.drop(columns = ['label', 'COUNTRY', 'iso3', 'EVENT_DATE_MONTH', 'YEAR'])# drops features that are noth helpfull for training
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