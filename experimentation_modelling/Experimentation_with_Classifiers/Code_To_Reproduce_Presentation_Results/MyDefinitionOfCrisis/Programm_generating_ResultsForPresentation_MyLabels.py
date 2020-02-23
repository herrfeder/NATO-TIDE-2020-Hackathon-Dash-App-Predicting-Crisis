# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 14:54:45 2020

@author: T510
"""

import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix



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




df = pd.read_csv('acled_social_iso3.csv')# imports prepared data from acled database
#cleaning Dataframe
df = df [~( df [ ['GDP (current US$)', ] ] == 0).all(axis=1) ] # for some rows there are no GDP availabe. => we filtered them out


# generating training set
help_df = pd.DataFrame()
country_list = df['COUNTRY'].unique()
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


rnd_forest = RandomForestClassifier(max_depth=16, max_features=7, min_samples_leaf=3, n_estimators=190)


print('rnd_forest')

rnd_forest.fit(X_train, y_train)
y_perdict = rnd_forest.predict(X_test)
a = confusion_matrix(y_test, y_perdict)
ConfusionMatrix = pd.DataFrame(a, index = ['as usual', 'actual battle case', 'actual protest case'], columns = ['predicted as usual', 'predicted battle case', 'predicted protest case'])
ConfusionMatrix.to_csv('ConfusionMatrix_MyLabels_rndForest.csv', sep=',')
from sklearn.metrics import classification_report
classifig_report = classification_report(y_test, y_perdict, output_dict = True)
print('classification report: ', classifig_report)
print('score:', rnd_forest.score(X_test, y_test))

# training on whole trainingset in oder to make prediction

rnd_forest.fit(x,y)

# seperating the data for december 2019 in oder to be able
x_present = help_df.loc[help_df['EVENT_DATE_MONTH'] == '2019-12'].drop(columns = ['label', 'COUNTRY', 'iso3', 'EVENT_DATE_MONTH', 'YEAR'])
x_present_with_ios3COUNTRY = help_df.loc[help_df['EVENT_DATE_MONTH'] == '2019-12'].drop(columns = ['label', 'EVENT_DATE_MONTH', 'YEAR'])
x_present = x_present.drop(columns = ['Unnamed: 0', 'Unnamed: 0.1'])
x_present = my_scaler.transform(x_present)




# ------ Random forest ----------------------------------------------
#make prediction
y_future = rnd_forest.predict(x_present)
y_future = pd.DataFrame(y_future)
        
#hackathon_crisis_future =  pd.DataFrame(np.array([]), columns=['month'])
hackathon_crisis_future = pd.DataFrame()

hackathon_crisis_future['iso3'] = x_present_with_ios3COUNTRY['iso3']
hackathon_crisis_future['month'] = '2020-01-01'
hackathon_crisis_future['country'] = x_present_with_ios3COUNTRY['COUNTRY']
hackathon_crisis_future['battle_case'] = 0
hackathon_crisis_future['protest_riots_case'] = 0
for index, row in y_future.iterrows():
    if y_future.loc[index,0] == 2:
        hackathon_crisis_future.iloc[index, 3] = 1        
    if y_future.loc[index,0] == 3:
        hackathon_crisis_future.iloc[index, 4] = 1
    if y_future.loc[index,0] == 4:
        hackathon_crisis_future.iloc[index, 4] = 1
        hackathon_crisis_future.iloc[index, 3] = 1

hackathon_crisis_future.to_csv('Future_MyDefinitionOfCrisis_rnd_forest.csv', sep=',', index=False)
