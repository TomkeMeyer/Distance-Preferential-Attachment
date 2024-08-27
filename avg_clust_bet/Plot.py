import numpy as np
import matplotlib

import matplotlib.pyplot as plt
import torch
from scipy.signal import savgol_filter


labels = []
label_values = [0,0.25,0.5,0.75,1,2]

fig, ax = plt.subplots()
multi_results = []
for i,l in zip(['avg_clust_bet_t250_b0_', 'avg_clust_bet_t250_b0.25_', 'avg_clust_bet_t250_b0.5_', 'avg_clust_bet_t250_b0.75_', 'avg_clust_bet_t250_b1_', 'avg_clust_bet_t250_b2_'], range(6)):
    values = np.zeros(250)
    for j in range(10):
        values += np.load(f'{i}r{j}.npy')  
        multi_results.append(np.load(f'{i}r{j}.npy'))
    
    std_dev_array = np.std(multi_results, axis=0)       
        
    values = values / 10
    print(label_values[l])
    plt.plot(values, label=f'b={label_values[l]}')
    print(label_values[l],np.mean(std_dev_array)) 
    
plt.legend()
plt.xlabel("Timestep")
plt.ylabel("Average Clustering Of Largest Component")
plt.savefig("avg_clust_bet.png")
plt.clf()

