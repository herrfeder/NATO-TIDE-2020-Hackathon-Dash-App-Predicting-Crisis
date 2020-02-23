# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 17:09:20 2020

@author: T510
"""

from sklearn.metrics import confusion_matrix
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model
from sklearn.svm import SVC
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

#-------------- finding best parameters and initialising instance models with good parameters
# random forest
param_distribs = {
        'n_estimators': randint(low=1, high=200),
        'max_features': randint(low=1, high=8),
        'max_depth'   : randint(low=1, high=20),
        'min_samples_leaf' : randint(low=1, high=4),
    }
my_model = RandomForestClassifier()
rnd_search = RandomizedSearchCV(my_model, param_distributions=param_distribs, n_iter=5, cv=3, scoring='balanced_accuracy', random_state=42)
rnd_search.fit(X_train,y_train)
print(rnd_search.best_params_)

rnd_forest = RandomForestClassifier(max_depth=11, max_features=5, min_samples_leaf=1, n_estimators=103)


# sgdc cclassifier
sgdclassifier = linear_model.SGDClassifier()


# svc poly
param_distribs = {
        'degree': randint(low=1, high=10),
        'coef0': randint(low=1, high=3),
        'C'   : randint(low=1, high=8),
    }
my_model = SVC(kernel = 'poly')
rnd_search = RandomizedSearchCV(my_model, param_distributions=param_distribs, n_iter=4, cv=3, scoring='balanced_accuracy', random_state=42)
rnd_search.fit(X_train,y_train)
print(rnd_search.best_params_)

svc_poly = SVC(kernel = 'poly', degree = 7, coef0= 1, C=2)





# svc_rbf_low_gamma
param_distribs = {
        'C'   : randint(low=500, high=1500),
    }
my_model = SVC(kernel = 'rbf', gamma=0.01)
rnd_search = RandomizedSearchCV(my_model, param_distributions=param_distribs, n_iter=5, cv=3, scoring='balanced_accuracy', random_state=42)
rnd_search.fit(X_train,y_train)
print(rnd_search.best_params_)
svc_rbf_low_gamma = SVC(kernel = 'rbf', gamma=0.1, C=1360)



# svc_rbf_high_gamma
param_distribs = {
        'C'   : randint(low=1, high=1500),
    }
my_model = SVC(kernel = 'rbf', gamma=5)
rnd_search = RandomizedSearchCV(my_model, param_distributions=param_distribs, n_iter=5, cv=3, scoring='balanced_accuracy', random_state=42)
rnd_search.fit(X_train,y_train)
print(rnd_search.best_params_)
svc_rbf_high_gamma = SVC(kernel = 'rbf', gamma=5, C=1127)


print('\n')
print('rnd_forest')
my_model = rnd_forest
my_model.fit(X_train, y_train)
y_perdict = my_model.predict(X_test)
print(confusion_matrix(y_test, y_perdict))
my_model_mse = mean_squared_error(y_test, y_perdict)
print('mean_squared_error', my_model_mse)
print('score:', my_model.score(X_test, y_test))
#my_model_rmse = np.sqrt(my_model_mse)
#print(my_model_rmse)

print('\n')
print(' sgdclassifier')
my_model = sgdclassifier
my_model.fit(X_train, y_train)
y_perdict = my_model.predict(X_test)
print(confusion_matrix(y_test, y_perdict))
my_model_mse = mean_squared_error(y_test, y_perdict)
print('mean_squared_error', my_model_mse)
print('score:',my_model.score(X_test, y_test))
#my_model_rmse = np.sqrt(my_model_mse)
#print(my_model_rmse)

print('\n')
print('svc_poly')
my_model = svc_poly
my_model.fit(X_train, y_train)
y_perdict = my_model.predict(X_test)
print(confusion_matrix(y_test, y_perdict))
my_model_mse = mean_squared_error(y_test, y_perdict)
print('mean_squared_error', my_model_mse)
print('score:',my_model.score(X_test, y_test))
#my_model_rmse = np.sqrt(my_model_mse)
#print(my_model_rmse)

print('\n')
print(' svc_rbf_low_gamma')
my_model = svc_rbf_low_gamma
my_model.fit(X_train, y_train)
y_perdict = my_model.predict(X_test)
print(confusion_matrix(y_test, y_perdict))
my_model_mse = mean_squared_error(y_test, y_perdict)
print('mean_squared_error', my_model_mse)
print('score:',my_model.score(X_test, y_test))
#my_model_rmse = np.sqrt(my_model_mse)
#print(my_model_rmse)

print('\n')
print('svc_rbf_high_gamma')
my_model = svc_rbf_high_gamma
my_model.fit(X_train, y_train)
y_perdict = my_model.predict(X_test)
print(confusion_matrix(y_test, y_perdict))
my_model_mse = mean_squared_error(y_test, y_perdict)
print('mean_squared_error', my_model_mse)
print('score:',my_model.score(X_test, y_test))
my_model_rmse = np.sqrt(my_model_mse)
print(my_model_rmse)

