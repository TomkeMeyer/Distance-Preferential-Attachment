import networkx as nx
import matplotlib.pyplot as plt
import collections
import numpy as np
import pandas as pd
import random
import math

def get_avg_triangles(Graph):
    triangles = nx.triangles(Graph)
    nodes = Graph.number_of_nodes()
    tri = 0
    for i in triangles.values():
        tri += i
    avg = tri/nodes
    return avg
    
def countDegree(Graph, b):
    plt.clf()
    degree = [Graph.degree(n) for n in Graph.nodes()]
    countDeg =collections.Counter(degree)
    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.plot(countDeg.keys(), countDeg.values(), 'bo')
    plt.savefig(f"DPA_distribution_log_PA_{b}.png")
    

def countHops(Graph, b):
    plt.clf()
    countHops = dict()
    hops  = dict(nx.all_pairs_shortest_path_length(Graph))
    
    for i in hops.values():
        countHops.update(collections.Counter(i))
        print(countHops)
    
    countHops = collections.Counter(countHops.values())
    print(countHops)
    plt.yscale("log")
    plt.xlabel("Hops, h")
    plt.ylabel("Number of edges")
    plt.plot(countHops.keys(), countHops.values(), 'bo')
    plt.savefig(f"hops_dpa_{b}.png")
  
def Betweenness():
    pi_k = nx.betweenness_centrality(DPA)
    pi_k = [pi_k[key] for key in pi_k.keys()]
    if np.sum(pi_k) == 0:
        chosen_node = np.random.choice(DPA.nodes())
    else:
        pi_k = pi_k / np.sum(pi_k)
        chosen_node = np.random.choice(DPA.nodes(), p=pi_k)
    return chosen_node
    
def PA():
    pi_k = []
    for i in DPA.nodes():
        deg = DPA.degree(i)
        probability = deg/(2*DPA.number_of_edges())
        pi_k.append(probability)
    chosen_node = np.random.choice(DPA.nodes(),p=pi_k)
    return chosen_node

def CalculateF():
    sum_dist = 0
    dist = 1
    if nx.is_connected(DPA):
        for i in DPA.nodes:
            deg = DPA.degree(i)
            maxdeg = np.max(DPA.degree())
            dist = nx.shortest_path_length(DPA, new_node, i)
            if dist > 1:            
                if nx.has_path(DPA, i, new_node) and nx.shortest_path_length(DPA, i, new_node) > 0:
                    sum_dist += (1/dist)*deg
    return sum_dist

def Distance_PA():
    CalculateF()
    pi_k = []
    sum_dist = 0
    dist = 1
    choices = []
    if nx.is_connected(DPA):
        for i in DPA.nodes():
            deg = DPA.degree(i)
            dist = nx.shortest_path_length(DPA, new_node, i)
            if dist > 1:
                choices.append(i)
                sum_dist = CalculateF()
                probability = ((1/dist)*deg)/sum_dist
                pi_k.append(probability)
                
        print(pi_k)
        chosen_node = np.random.choice(choices,p=pi_k)

    else:
        chosen_node = PA()
    return chosen_node

def CalculateF_beta(beta):
    sum_dist = 0
    dist = 1
    if nx.is_connected(DPA):
        for i in DPA.nodes:
            deg = DPA.degree(i)
            dist = nx.shortest_path_length(DPA, new_node, i)
            maxdeg = np.max(DPA.degree())
            maxdist = nx.diameter(DPA)
            if dist > 1:            
                if nx.has_path(DPA, i, new_node) and nx.shortest_path_length(DPA, i, new_node) > 0:
                    sum_dist += (beta*(1/dist))+((1-beta)*(deg/maxdeg))
    return sum_dist

def Distance_PA_beta(beta):
    #CalculateF()
    pi_k = []
    sum_dist = CalculateF_beta(beta)
    dist = 1
    choices = []
    if nx.is_connected(DPA):
        for i in DPA.nodes():
            deg = DPA.degree(i)
            dist = nx.shortest_path_length(DPA, new_node, i)
            maxdeg = np.max(DPA.degree())
            maxdist = nx.diameter(DPA)
            if dist > 1:
                choices.append(i)
                probability = ((beta*(1/dist))+((1-beta)*(deg/maxdeg)))/sum_dist
                pi_k.append(probability)
        pi_k = pi_k / np.sum(pi_k) 
        chosen_node = np.random.choice(choices,p=pi_k)

    else:
        chosen_node = PA()#Betweenness()#
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
        print("edge", chosen_node, new_node)

def add_random():
    random_node = np.random.choice(DPA.nodes())
    new_edge = (new_node, random_node)
    if new_edge in DPA.edges():
        add_random()
    else:
        DPA.add_edge(new_node, random_node)
        print("edge", new_node, random_node)

time = 250
beta = [0,0.25,0.5,0.75,1,2]
fig, ax = plt.subplots()
repetitions = 1
for r in range(repetitions):
    for b in range(len(beta)):
        print("beta", b)
        DPA = nx.Graph()
        DPA.add_edge(0,1)
        DPA.add_edge(0,2)
        DPA.add_edge(0,3)
        DPA.add_edge(0,4)
        DPA.add_edge(1,2)
        DPA.add_edge(1,3)
        DPA.add_edge(1,4)
        DPA.add_edge(2,3)
        DPA.add_edge(2,4)
        DPA.add_edge(3,4)
        m_0 = DPA.number_of_nodes() #2,5,10,25,50
        new_node = m_0
        largest_distances = []
        average_clustering = []
        avg_triangles = []
        for t in range(time):
            DPA.add_node(new_node)
            print("node", new_node)
            #m_0 = round(DPA.number_of_nodes()/5)
            for i in range(m_0):
                if beta[b] == 2:
                    add_random()
                else:
                    add_new_edge(beta[b])
            new_node+=1
            #largest_cc = DPA.subgraph(max(nx.connected_components(DPA), key=len))
            #print(largest_cc)
            #largest_distances.append(nx.average_shortest_path_length(largest_cc))
            #average_clustering.append(nx.average_clustering(largest_cc))
            #triangles = get_avg_triangles(largest_cc)
            #avg_triangles.append(triangles)
        #plt.plot(average_clustering, label=f'b={beta[b]}')
        #np.save(f"avg_dist_PA_t{time}_b{beta[b]}_r{r}.npy", largest_distances)
        countDegree(DPA, beta[b])
        #countHops(DPA, beta[b])
        
'''
plt.legend()
plt.xlabel("Timestep")
plt.ylabel("Average clustering Of Largest Component")
plt.savefig("avg_clust_dpa_t=100_m=5.png")
plt.clf()
'''
#Average Number Of Triangles Per Node
#plt.xlabel("Timestep")
#plt.ylabel("Average Distance Of Largest Component")
#plt.plot(range(len(largest_distances)), largest_distances, label="Average Distance Distribution over Time")
#plt.savefig("avg_dist_dpa.png")
#plt.clf()
#plt.xlabel("Timestep")
#plt.ylabel("Average Clustering Of Largest Component")
#plt.plot(range(len(average_clustering)), average_clustering, label="Average Clustering Distribution over Time")
#plt.savefig("avg_clust_dpa.png")
#countDegree(largest_cc)
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


