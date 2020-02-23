# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 10:28:18 2020

@author: T510
"""

# collects the current situation (jan 2020)
x_present = help_df.loc[help_df['EVENT_DATE_MONTH'] == '2019-12'].drop(columns = ['label', 'COUNTRY', 'iso3', 'EVENT_DATE_MONTH', 'YEAR'])
x_present_with_ios3COUNTRY = help_df.loc[help_df['EVENT_DATE_MONTH'] == '2019-12'].drop(columns = ['label', 'EVENT_DATE_MONTH', 'YEAR'])
x_present = x_present.drop(columns = ['Unnamed: 0', 'Unnamed: 0.1'])
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

hackathon_crisis_future.to_csv('Future_MyDefinitionOfCrisis_rnd_forest.csv', sep=',', index=False)



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

hackathon_crisis_future.to_csv('Future_MyDefinitionOfCrisis_sgdclassifier.csv', sep=',', index=False)


# ------ svc_poly ---------------------------------------------------
my_model = svc_poly
#make prediction
y_future = my_model.predict(x_present)
y_future = pd.DataFrame(y_future)

hackathon_crisis_future =  pd.DataFrame(np.array([]), columns=['month'])
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

hackathon_crisis_future.to_csv('Future_NatoDefinitionOfCrisis_svc_poly.csv', sep=',', index=False)


# ------ svc_rbf_1 ---------------------------------------------------
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

hackathon_crisis_future.to_csv('Future_MyDefinitionOfCrisis_svc_rbf_low_gamma.csv', sep=',', index=False)



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

hackathon_crisis_future.to_csv('Future_MyDefinitionOfCrisis_svc_rbf_high_gamma.csv', sep=',', index=False)


