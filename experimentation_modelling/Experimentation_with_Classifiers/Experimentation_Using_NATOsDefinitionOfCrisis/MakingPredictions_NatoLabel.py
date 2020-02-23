# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 10:28:18 2020

@author: T510
"""

# collects the current situation (jan 2020)
x_present = help_df.loc[help_df['EVENT_DATE_MONTH'] == '2019-12'].drop(columns = ['oli_label', 'COUNTRY', 'iso3', 'EVENT_DATE_MONTH', 'YEAR','battle_case', 'protest_riots_case'])
#x without last 6 month
#x_present = x_present.drop(columns = ['Battles_1_month_ago','Protests_1_month_ago','Explosions/Remote violence_1_month_ago','Strategic developments_1_month_ago','Violence against civilians_1_month_ago','FATALITIES_1_month_ago','Battles_2_month_ago','Protests_2_month_ago','Explosions/Remote violence_2_month_ago','Strategic developments_2_month_ago','Violence against civilians_2_month_ago','FATALITIES_2_month_ago','Battles_3_month_ago','Protests_3_month_ago','Explosions/Remote violence_3_month_ago','Strategic developments_3_month_ago','Violence against civilians_3_month_ago','FATALITIES_3_month_ago','Battles_4_month_ago','Protests_4_month_ago','Explosions/Remote violence_4_month_ago','Strategic developments_4_month_ago','Violence against civilians_4_month_ago','FATALITIES_4_month_ago','Battles_5_month_ago','Protests_5_month_ago','Explosions/Remote violence_5_month_ago','Strategic developments_5_month_ago','Violence against civilians_5_month_ago','FATALITIES_5_month_ago'])# x_without last 6 month
x_present_with_ios3COUNTRY = help_df.loc[help_df['EVENT_DATE_MONTH'] == '2019-12'].drop(columns = ['oli_label', 'EVENT_DATE_MONTH', 'YEAR','battle_case', 'protest_riots_case'])
x_present = x_present.drop(columns = ['Unnamed: 0'])
x_present = my_scaler.transform(x_present)




# ------ Random forest ----------------------------------------------
my_model = rnd_forest
#make prediction
y_future = my_model.predict(x_present)
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



# ------ sgdc_classifier ---------------------------------------------------
my_model = sgdclassifier
#make prediction
y_future = my_model.predict(x_present)
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

hackathon_crisis_future.to_csv('Future_NatoDefinitionCrisis_sgdclassifier.csv', sep=',', index=False)


# ------ svc_poly ---------------------------------------------------
my_model = svc_poly
#make prediction
y_future = my_model.predict(x_present)
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

hackathon_crisis_future.to_csv('Future_NatoDefinitionCrisis_svc_poly.csv', sep=',', index=False)


# ------ svc_rbf_low_gamma ---------------------------------------------------
my_model = svc_rbf_low_gamma
#make prediction
y_future = my_model.predict(x_present)
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

hackathon_crisis_future.to_csv('Future_NatoDefinitionCrisis_svc_rbf_low_gamma.csv', sep=',', index=False)



# ------ svc_rbf_2 ---------------------------------------------------
my_model = svc_rbf_high_gamma
#make prediction
y_future = my_model.predict(x_present)
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

hackathon_crisis_future.to_csv('Future_NatoDefinitionCrisis_svc_rbf_high_gamma.csv', sep=',', index=False)


