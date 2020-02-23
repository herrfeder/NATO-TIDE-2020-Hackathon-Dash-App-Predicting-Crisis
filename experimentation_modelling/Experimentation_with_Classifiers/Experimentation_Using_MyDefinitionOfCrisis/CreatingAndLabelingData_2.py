# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 15:12:34 2020

@author: T510
"""



# returns the labled training data of one country
def CreateAndLableDATA_2 (NameOfCountry, df):
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

    
    
#----labeling the data concering an increase of events in contrast to the average
    example_Battles_mean = df_example['Battles'].mean()
    example_Explosions_mean = df_example['Explosions/Remote violence'].mean()
    example_Violance_mean = df_example['Violence against civilians'].mean()
    example_Riots_mean = df_example['Riots'].mean()
    example_Protests_mean = df_example['Protests'].mean()
    df_example.reset_index(drop=True, inplace = True)
    for index, row in df_example.iterrows():
        if row['Battles'] > 1.3*example_Battles_mean and row['Explosions/Remote violence'] > 1.3*example_Explosions_mean and row['Violence against civilians'] > 1.3*example_Violance_mean: # increase of violent events => definition for battle case
            df_example.loc[index-1, 'label'] = 2 # battle case is going to come
            if row['Protests'] > 1.3*example_Protests_mean and row['Riots'] > 1.3*example_Riots_mean: # increase of demonstations => definition for protest riot case
                df_example.loc[index-1, 'label'] = 3 # protest Riot case is going to come
                if (row['Battles'] > 1.3*example_Battles_mean and row['Explosions/Remote violence'] > 1.3*example_Explosions_mean and row['Violence against civilians'] > 1.3*example_Violance_mean) and (row['Protests'] > 1.5*example_Protests_mean and row['Riots'] > 1.5*example_Riots_mean): # both condition for battle case and protest_riot_case
                    df_example.loc[index-1, 'label'] = 4 # battle case and Riot case is going to come
        else:
            df_example.loc[index-1, 'label'] = 1 # it will go on as usual



           
    df_example = df_example.dropna() # case of the forloop there are some NaNs i the last row, which are droped here
    return df_example

