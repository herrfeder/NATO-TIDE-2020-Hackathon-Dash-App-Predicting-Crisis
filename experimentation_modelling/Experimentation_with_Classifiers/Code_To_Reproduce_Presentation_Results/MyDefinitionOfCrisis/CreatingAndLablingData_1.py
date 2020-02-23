# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 12:29:03 2020

@author: T510
"""


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

