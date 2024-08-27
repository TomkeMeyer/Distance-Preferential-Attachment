import networkx as nx
import matplotlib.pyplot as plt
import collections
import numpy as np
import pandas as pd
import random
def Betweenness():
    pi_k = nx.betweenness_centrality(DPA)
    pi_k = [pi_k[key] for key in pi_k.keys()]
    if np.sum(pi_k) == 0:
        chosen_node = np.random.choice(DPA.nodes())
    else:
        pi_k = pi_k / np.sum(pi_k)
        chosen_node = np.random.choice(DPA.nodes(), p=pi_k)
    return chosen_node
  
def countDegree(Graph, time, m_0):
    plt.clf()
    degree = [Graph.degree(n) for n in Graph.nodes()]
    countDeg =collections.Counter(degree)
    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.plot(countDeg.keys(), countDeg.values(), 'bo')
    plt.savefig(f"DPA_distribution_log_ito:t={time},m={m_0}.png")
    
def PA():
    pi_k = []
    for i in DPA.nodes():
        deg = DPA.degree(i)
        probability = deg/(2*DPA.number_of_edges())
        pi_k.append(probability)
    chosen_node = np.random.choice(DPA.nodes(),p=pi_k)
    return chosen_node
    
def CalculateF_beta(beta):
    sum_dist = 0
    dist = 1
    if nx.is_connected(DPA):
        for i in DPA.nodes:
            deg = DPA.degree(i)
            dist = nx.shortest_path_length(DPA, new_node, i)
            maxdeg = np.max(DPA.degree())
            #maxdist = nx.diameter(DPA)
            if dist > 1:            
                if nx.has_path(DPA, i, new_node) and nx.shortest_path_length(DPA, i, new_node) > 0:
                    sum_dist += (beta*(1/dist))+((1-beta)*(deg/maxdeg))
    return sum_dist

def Distance_PA_beta(beta):
    pi_k = []
    sum_dist = CalculateF_beta(beta)
    dist = 1
    choices = []
    if nx.is_connected(DPA):
        for i in DPA.nodes():
            deg = DPA.degree(i)
            dist = nx.shortest_path_length(DPA, new_node, i)
            maxdeg = np.max(DPA.degree())
            #maxdist = nx.diameter(DPA)
            if dist > 1:
                choices.append(i)
                probability = ((beta*(1/dist))+((1-beta)*(deg/maxdeg)))/sum_dist
                pi_k.append(probability)
        pi_k = pi_k / np.sum(pi_k) 
        #print(pi_k)
        chosen_node = np.random.choice(choices,p=pi_k)

    else:
        chosen_node = Betweenness()#PA()#
    return chosen_node

def add_new_edge(beta):
    if DPA.number_of_nodes() != 0:
        chosen_node = Distance_PA_beta(beta)
    else:
        chosen_node = 0
    new_edge = (chosen_node, new_node)
    if new_edge in DPA.edges():
        add_new_edge(beta)
    else:
        DPA.add_edge(chosen_node, new_node)
        #print("edge", chosen_node, new_node)

def add_random():
    random_node = np.random.choice(DPA.nodes())
    new_edge = (new_node, random_node)
    if new_edge in DPA.edges():
        add_random()
    else:
        DPA.add_edge(new_node, random_node)
        print("edge", new_node, random_node)
       
       
time = [167]#[500,200,100]
DPA_list = open("DPA.in", "rb")
columns = ['node1', 'node2', 'timestamp', 'weight']
DPA_list = pd.read_csv('Dynamic_PPIN_Lambert.txt', names = columns)
DPA_list = DPA_list[DPA_list.timestamp <= 10]
DPA_list = DPA_list.drop(columns=['timestamp', 'weight'])
print(DPA_list)
#DPA = nx.Graph()
#DPA.add_edge(0,1)
#DPA.add_edge(0,2)
#DPA.add_edge(1,2)
m_0 = [5]#2,5,10,25,50]#DPA.number_of_nodes() 2,5,10,25,50
beta = [0, 0.25, 0.5, 0.75, 1, 2]#0.5 #0,0.25,0.5,0.75,1
pi_over_time = []
all_degrees = []
fig, ax = plt.subplots()
colors = plt.rcParams["axes.prop_cycle"]()
for i in range(len(time)):
    plt.clf()
    for j in range(len(beta)):
        DPA = nx.from_pandas_edgelist(DPA_list, "node1", "node2")
        print(DPA)
        new_node = DPA.number_of_nodes()#m_0
        largest_cc = nx.Graph()
        largest_distances = []
        average_clustering = []
        print(time[i], m_0[i],beta[j])
        for t in range(time[i]):
            #degrees = [val for (node, val) in DPA.degree()]
            #average = sum(degrees) / DPA.number_of_nodes()
            DPA.add_node(new_node)
            print("node", new_node)
            for m in range(m_0[i]):#round(average)):
                if beta[j] == 2:
                    add_random()
                else:
                    add_new_edge(beta[j])
                largest_cc = DPA.subgraph(max(  nx.connected_components(DPA), key=len))
                #largest_distances.append(nx.average_shortest_path_length(largest_cc))
                average_clustering.append(nx.average_clustering(largest_cc))
                print(largest_cc)
            new_node+=1
            #if(largest_cc.number_of_nodes() >= 1776):
        np.save(f"avg_clust_bet_lambert_t_{time}_m_{m_0}b{beta[j]}.npy", average_clustering)
        #plt.plot(average_clustering, label=f'b={beta[j]}')
    #plt.legend()
    #plt.xlabel("Timestep")
    #plt.ylabel("Average Clustering Of Largest Component")
    #plt.savefig(f'clustering_PA_ito:t={time[i]},m={m_0[i]}.png')
    #plt.clf()
    #countDegree(largest_cc, time[i], m_0[i])
'''
plt.xlabel("Timestep")
plt.ylabel("Average ance Of Largest Component")
plt.plot(range(len(largest_distances)), largest_distances, label="Average Distance Distribution over Time")
plt.savefig("avg_dist_ito_dpa.png")
plt.clf()
plt.xlabel("Timestep")
plt.ylabel("Average Clustering Of Largest Component")
plt.plot(range(len(average_clustering)), average_clustering, label="Average Clustering Distribution over Time")
plt.savefig("avg_clust_ito_dpa.png")
'''
#print(largest_cc)
#countDegree(DPA)
#nx.draw(DPA)
#plt.savefig("DPA.png")


'''
degrees = [val for (node, val) in largest_cc.degree()]
unique_deg = np.unique(degrees)
for i in unique_deg:
    all_degrees.append(i)
pi_k = []
for i in unique_deg:
    #deg = largest_cc.degree(i)
    probability = i/(2*largest_cc.number_of_edges())
    pi_k.append(probability)

c = next(colors)["color"]
ax.plot(unique_deg, pi_k, '-bo', label = t, color = c)   
'''


