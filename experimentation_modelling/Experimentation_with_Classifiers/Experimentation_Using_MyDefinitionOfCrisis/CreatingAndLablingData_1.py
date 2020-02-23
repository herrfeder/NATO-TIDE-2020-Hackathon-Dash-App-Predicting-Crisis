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
        
#for i in range(1,5):
#            name ='Battles_'+str(i)+'_month_ago'
 #           df_example.loc[index+i, name] = df_example.loc[index, 'Battles']
  #          df_example.loc[index+i, 'Riots_'+str(i)+'_month_ago'] = df_example.loc[index, 'Riots']
   #         df_example.loc[index+i, 'Protests_'+str(i)+'_month_ago'] = df_example.loc[index, 'Protests']
    #        df_example.loc[index+i, 'Explosions/Remote violence_'+str(i)+'_month_ago'] = df_example.loc[index, 'Explosions/Remote violence']
     #       df_example.loc[index+i, 'Strategic developments_'+str(i)+'_month_ago'] = df_example.loc[index, 'Strategic developments']
      #      df_example.loc[index+i, 'Violence against civilians_'+str(i)+'_month_ago'] = df_example.loc[index, 'Violence against civilians']
       #     df_example.loc[index+i, 'FATALITIES_'+str(i)+'_month_ago'] = df_example.loc[index, 'FATALITIES']
            
        #df_example.loc[index+1, 'Battles_one_month_ago'] = df_example.loc[index, 'Battles']
        #df_example.loc[index+2, 'Battles_two_month_ago'] = df_example.loc[index, 'Battles']
        #df_example.loc[index+3, 'Battles_three_month_ago'] = df_example.loc[index, 'Battles']
    
        #df_example.loc[index+1, 'Riots_one_month_ago'] = df_example.loc[index, 'Riots']
        #df_example.loc[index+2, 'Riots_two_month_ago'] = df_example.loc[index, 'Riots']
        #df_example.loc[index+3, 'Riots_three_month_ago'] = df_example.loc[index, 'Riots']
        
        #df_example.loc[index+1, 'Protests_one_month_ago'] = df_example.loc[index, 'Protests']
        #df_example.loc[index+2, 'Protests_two_month_ago'] = df_example.loc[index, 'Protests']
        #df_example.loc[index+3, 'Protests_three_month_ago'] = df_example.loc[index, 'Protests']
        
        #df_example.loc[index+1, 'Explosions/Remote violence_one_month_ago'] = df_example.loc[index, 'Explosions/Remote violence']
        #df_example.loc[index+2, 'Explosions/Remote violence_two_month_ago'] = df_example.loc[index, 'Explosions/Remote violence']
        #df_example.loc[index+3, 'Explosions/Remote violence_three_month_ago'] = df_example.loc[index, 'Explosions/Remote violence']
        
        #df_example.loc[index+1, 'Strategic developments_one_month_ago'] = df_example.loc[index, 'Strategic developments']
        #df_example.loc[index+2, 'Strategic developments_two_month_ago'] = df_example.loc[index, 'Strategic developments']
        #df_example.loc[index+3, 'Strategic developments_three_month_ago'] = df_example.loc[index, 'Strategic developments']
        
        #df_example.loc[index+1, 'Violence against civilians_one_month_ago'] = df_example.loc[index, 'Violence against civilians']
        #df_example.loc[index+2, 'Violence against civilians_two_month_ago'] = df_example.loc[index, 'Violence against civilians']
        #df_example.loc[index+3, 'Violence against civilians_three_month_ago'] = df_example.loc[index, 'Violence against civilians']
        
        #df_example.loc[index+1, 'FATALITIES_one_month_ago'] = df_example.loc[index, 'FATALITIES']
        #df_example.loc[index+2, 'FATALITIES_two_month_ago'] = df_example.loc[index, 'FATALITIES']
        #df_example.loc[index+3, 'FATALITIES_three_month_ago'] = df_example.loc[index, 'FATALITIES']
         
            
    
    
#----labeling the data concering the average
#    example_Battles_mean = df_example['Battles'].mean()
#    example_Explosions_mean = df_example['Explosions/Remote violence'].mean()
#    example_Violance_mean = df_example['Violence against civilians'].mean()
#    example_Riots_mean = df_example['Riots'].mean()
#    example_Protests_mean = df_example['Protests'].mean()
#    df_example.reset_index(drop=True, inplace = True)
#    for index, row in df_example.iterrows():
#        if row['Battles'] > 1.3*example_Battles_mean and row['Explosions/Remote violence'] > 1.3*example_Explosions_mean and row['Violence against civilians'] > 1.3*example_Violance_mean: # increase of violent events => definition for battle case
#            df_example.loc[index-1, 'label'] = 2 # battle case is going to come
#            if row['Protests'] > 1.3*example_Protests_mean and row['Riots'] > 1.3*example_Riots_mean: # increase of demonstations => definition for protest riot case
#                df_example.loc[index-1, 'label'] = 3 # protest Riot case is going to come
#                if (row['Battles'] > 1.3*example_Battles_mean and row['Explosions/Remote violence'] > 1.3*example_Explosions_mean and row['Violence against civilians'] > 1.3*example_Violance_mean) and (row['Protests'] > 1.5*example_Protests_mean and row['Riots'] > 1.5*example_Riots_mean): # both condition for battle case and protest_riot_case
#                    df_example.loc[index-1, 'label'] = 4 # battle case and Riot case is going to come
#        else:
#            df_example.loc[index-1, 'label'] = 1 # it will go on as usual

#----labeling the data concering an sudden increase in battles events or demonstraions

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

