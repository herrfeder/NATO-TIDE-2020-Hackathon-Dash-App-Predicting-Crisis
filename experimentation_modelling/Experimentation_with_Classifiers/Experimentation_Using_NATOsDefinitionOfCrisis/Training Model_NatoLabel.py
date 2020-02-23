# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:11:47 2020

@author: T510
"""



# finally trains on all training datas in order to be perfectly trained to make perdictions for future
rnd_forest.fit(x,y)
sgdclassifier.fit(x,y)
svc_poly.fit(x,y)
svc_rbf_low_gamma.fit(x,y)
svc_rbf_high_gamma.fit(x,y)








