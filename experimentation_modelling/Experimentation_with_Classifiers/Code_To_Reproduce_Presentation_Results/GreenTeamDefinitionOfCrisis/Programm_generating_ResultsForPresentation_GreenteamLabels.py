# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 14:09:30 2020

@author: T510
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix
df = pd.read_csv('acled_social_iso3_timelag_labeled.csv')# imports prepared data from acled database




for index, row in df.iterrows():
    if row['battle_case'] == 1:
        df.loc[index, 'oli_label'] = 2
    elif row['protest_riots_case'] == 1:
        df.loc[index, 'oli_label'] = 3
    elif row['battle_case'] == 1 and row['protest_riots_case'] == 1:
        df.loc[index, 'oli_label'] = 4
    else:
        df.loc[index, 'oli_label'] = 1
        
df = df [~( df [ ['GDP (current US$)', ] ] == 0).all(axis=1) ] # for some rows there are no GDP availabe. => we filtered them out
        
help_df = df      
# seperates the features from the labels
x = df.drop(columns = ['oli_label', 'COUNTRY', 'iso3', 'EVENT_DATE_MONTH', 'YEAR','battle_case', 'protest_riots_case'])# drops features that are noth helpfull for training
#x = x.drop(columns = ['Battles_1_month_ago','Protests_1_month_ago','Explosions/Remote violence_1_month_ago','Strategic developments_1_month_ago','Violence against civilians_1_month_ago','FATALITIES_1_month_ago','Battles_2_month_ago','Protests_2_month_ago','Explosions/Remote violence_2_month_ago','Strategic developments_2_month_ago','Violence against civilians_2_month_ago','FATALITIES_2_month_ago','Battles_3_month_ago','Protests_3_month_ago','Explosions/Remote violence_3_month_ago','Strategic developments_3_month_ago','Violence against civilians_3_month_ago','FATALITIES_3_month_ago','Battles_4_month_ago','Protests_4_month_ago','Explosions/Remote violence_4_month_ago','Strategic developments_4_month_ago','Violence against civilians_4_month_ago','FATALITIES_4_month_ago','Battles_5_month_ago','Protests_5_month_ago','Explosions/Remote violence_5_month_ago','Strategic developments_5_month_ago','Violence against civilians_5_month_ago','FATALITIES_5_month_ago'])# x_without last 6 month
x = x.drop(columns = ['Unnamed: 0'])
y = df['oli_label']# seperates the labels




# fits StandardScaler and scales features
from sklearn.preprocessing import StandardScaler
my_scaler = StandardScaler()
my_scaler.fit(x)
x = my_scaler.transform(x)

# seperates training and test data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


rnd_forest = RandomForestClassifier(max_depth=11, max_features=5, min_samples_leaf=1, n_estimators=103)



print('rnd_forest')
rnd_forest.fit(X_train, y_train)
y_perdict = rnd_forest.predict(X_test)
a = confusion_matrix(y_test, y_perdict)
ConfusionMatrix = pd.DataFrame(a, index = ['as usual', 'actual battle case', 'actual protest case'], columns = ['predicted as usual', 'predicted battle case', 'predicted protest case'])
ConfusionMatrix.to_csv('ConfusionMatrix_rndForest.csv', sep=',')
from sklearn.metrics import classification_report
classifig_report = classification_report(y_test, y_perdict, output_dict = True)
print('classification report. ', classifig_report)
print('score:', rnd_forest.score(X_test, y_test))

rnd_forest.fit(x,y)


# collects the current situation (jan 2020)
x_present = help_df.loc[help_df['EVENT_DATE_MONTH'] == '2019-12'].drop(columns = ['oli_label', 'COUNTRY', 'iso3', 'EVENT_DATE_MONTH', 'YEAR','battle_case', 'protest_riots_case'])
#x without last 6 month
#x_present = x_present.drop(columns = ['Battles_1_month_ago','Protests_1_month_ago','Explosions/Remote violence_1_month_ago','Strategic developments_1_month_ago','Violence against civilians_1_month_ago','FATALITIES_1_month_ago','Battles_2_month_ago','Protests_2_month_ago','Explosions/Remote violence_2_month_ago','Strategic developments_2_month_ago','Violence against civilians_2_month_ago','FATALITIES_2_month_ago','Battles_3_month_ago','Protests_3_month_ago','Explosions/Remote violence_3_month_ago','Strategic developments_3_month_ago','Violence against civilians_3_month_ago','FATALITIES_3_month_ago','Battles_4_month_ago','Protests_4_month_ago','Explosions/Remote violence_4_month_ago','Strategic developments_4_month_ago','Violence against civilians_4_month_ago','FATALITIES_4_month_ago','Battles_5_month_ago','Protests_5_month_ago','Explosions/Remote violence_5_month_ago','Strategic developments_5_month_ago','Violence against civilians_5_month_ago','FATALITIES_5_month_ago'])# x_without last 6 month
x_present_with_ios3COUNTRY = help_df.loc[help_df['EVENT_DATE_MONTH'] == '2019-12'].drop(columns = ['oli_label', 'EVENT_DATE_MONTH', 'YEAR','battle_case', 'protest_riots_case'])
x_present = x_present.drop(columns = ['Unnamed: 0'])
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

hackathon_crisis_future.to_csv('Future_NatoDefinitionCrisis_rnd_forest.csv', sep=',', index=False)