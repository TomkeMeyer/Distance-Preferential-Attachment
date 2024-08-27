import numpy as np
import matplotlib

import matplotlib.pyplot as plt
import torch
from scipy import stats
from scipy.signal import savgol_filter

def Pearson(x,y):
    res = stats.pearsonr(x, y)
    return res
    
labels = []
label_values = [0,0.25,0.5,0.75,1,'random','ito']
fig, ax = plt.subplots()
for i,l in zip(['avg_clust_bet_ito_t_[219]_b0', 'avg_clust_bet_ito_t_[219]_b0.25', 'avg_clust_bet_ito_t_[219]_b0.5', 'avg_clust_bet_ito_t_[219]_b0.75', 'avg_clust_bet_ito_t_[219]_b1', 'avg_clust_bet_ito_t_[219]_b2', 'avg_clust_ito_new_test'], range(7)):
    #values = np.zeros(250)
    values = np.load(f'{i}.npy')
    values = values[values!=0]
    print(i, values.shape, values)
    print(label_values[l])
    plt.plot(values, label=f'b={label_values[l]}')
    
for i in ['avg_clust_bet_ito_t_[219]_b0', 'avg_clust_bet_ito_t_[219]_b0.25', 'avg_clust_bet_ito_t_[219]_b0.5', 'avg_clust_bet_ito_t_[219]_b0.75', 'avg_clust_bet_ito_t_[219]_b1', 'avg_clust_bet_ito_t_[219]_b2']:
    x = np.load('avg_clust_ito_new_test.npy')
    values = np.load(f'{i}.npy')
    print(len(x), len(values))
    pearson = Pearson(x,values[:1084])
    print(i, pearson)
    
plt.legend()
plt.xlabel("Timestep")
plt.ylabel("Average Clustering Of Largest Component")
plt.savefig("avg_clust_bet_ito_new_test.png")
plt.clf()






