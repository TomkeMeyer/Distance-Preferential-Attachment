import networkx as nx
import matplotlib.pyplot as plt
import collections
import numpy as np
import pandas as pd
import pathpy as pp
import random
from scipy.integrate import quad
    
def countDegree(Graph):
    plt.clf()
    degree = [Graph.degree(n) for n in Graph.nodes()]
    countDeg =collections.Counter(degree)
    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.plot(countDeg.keys(), countDeg.values(), 'bo')
    plt.savefig("degree_distribution_ppin_uetz.png")
    
def countHops(Graph):
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
    plt.savefig("hops_ppin_ito.png")
    
def get_avg_triangles(Graph):
    triangles = nx.triangles(Graph)
    nodes = Graph.number_of_nodes()
    tri = 0
    for i in triangles.values():
        tri += i
    avg = tri/nodes
    avg = avg/3#???
    return avg
    

colors = plt.rcParams["axes.prop_cycle"]()
columns = ['node1', 'node2', 'timestamp', 'weight']
graph_list = pd.read_csv('Dynamic_PPIN_Lambert.txt', names = columns)
graph_list = graph_list.drop(columns=['weight'])
print(graph_list)
time = 0
max_time = graph_list['timestamp'].max()
print(max_time)
#graph = pp.TemporalNetwork()[graph.add_edge(graph_list['node1'][i],graph_list['node2'][i],int(graph_list['timestamp'][i])) for i in range(len(graph_list))]
graph = nx.Graph()
largest_cc = nx.Graph()
fig, ax = plt.subplots()
largest_distances = []
average_clustering = []
distances=[]
avg_triangles = []
pi_over_time = []
all_degrees = []
last_1 = graph_list['node1'].tail(1).values[0]
last_2 = graph_list['node2'].tail(1).values[0]
print("s;damb", last_1, last_2)
m=5
last_index=0
done = False
count = 0
while not done:
    if graph_list['timestamp'][last_index] == max_time:
        for i in range(m):
            if graph_list['node1'][last_index+i] == last_1 and graph_list['node2'][last_index+i] == last_2:
                #print(graph_list['node1'][last_index+i], graph_list['node2'][last_index+i], i)
                done = True
                distance=last_index
                for j in range(last_index, last_index+i):#dit moet anders
                    graph.add_edge(graph_list['node1'][j],graph_list['node2'][j])
                    last_index = graph_list.index[j]
                    #print(i, graph_list['timestamp'][j], graph_list['node1'][i], graph_list['node2'][j])
                average_clustering.append(nx.average_clustering(largest_cc))
                #largest_distances.append(nx.average_shortest_path_length(largest_cc))
                break
    if not done:
        if time <= 10:
            for i in range(1,len(graph_list)):
                if graph_list['timestamp'][i] == time:
                    graph.add_edge(graph_list['node1'][i],graph_list['node2'][i])
                    last_index = graph_list.index[i]
                    #print(last_index)
                    largest_cc = graph.subgraph(max(nx.connected_components(graph), key=len))
            print(graph, largest_cc)
            #average_clustering.append(nx.average_clustering(largest_cc))
        else:
            last_index+=1
            distance=last_index
            for i in range(last_index, last_index+m):#dit moet anders   
                new_edge = (graph_list['node1'][i],graph_list['node2'][i])
                if new_edge in graph.edges():
                    graph.add_edge(graph_list['node1'][i],graph_list['node2'][i])
                    last_index = graph_list.index[i]
                    #print(i, graph_list['timestamp'][i], graph_list['node1'][i], graph_list['node2'][i])
                else:
                    graph.add_edge(graph_list['node1'][i],graph_list['node2'][i])
                    last_index = graph_list.index[i]
                    #print(i, graph_list['timestamp'][i], graph_list['node1'][i], graph_list['node2'][i])
                    largest_cc = graph.subgraph(max(nx.connected_components(graph), key=len))
                    average_clustering.append(nx.average_clustering(largest_cc))
                    #largest_distances.append(nx.average_shortest_path_length(largest_cc))
        time += 1
        
        #triangles = get_avg_triangles(largest_cc)
        #avg_triangles.append(triangles)
        #len(avg_triangles)
    '''
    if(largest_cc.number_of_nodes() >= 150):
        print(largest_cc)
        degrees = [val for (node, val) in largest_cc.degree()]
        unique_deg = np.unique(degrees)
        for i in unique_deg:
            all_degrees.append(i)
        pi_k = []
        for i in unique_deg:
            probability = i/(2*largest_cc.number_of_edges())
            pi_k.append(probability)
        
        #c = next(colors)["color"]
        #ax.plot(unique_deg, pi_k, '-bo', label = t, color = c) 
    '''
print(graph)
print(largest_cc)
#countDegree(largest_cc)
#countHops(graph)
'''
columns = ['node1', 'node2', 'timestamp']
graph_list = pd.read_csv('edges.csv', names = columns, header=None)
graph_list = graph_list.iloc[1: , :]
print(graph_list)
timestamps = sorted(graph_list.timestamp.unique(), key=int)
#graph = pp.TemporalNetwork()[graph.add_edge(graph_list['node1'][i],graph_list['node2'][i],int(graph_list['timestamp'][i])) for i in range(len(graph_list))]
graph = nx.Graph()
largest_cc = 0
largest_distances = []
for t in timestamps:
    print(t)
    for i in range(1, len(graph_list)):
        if graph_list['timestamp'][i] == t:
            graph.add_edge(graph_list['node1'][i],graph_list['node2'][i])
    #distances = []
    #for c in sorted(nx.connected_components(graph)):
    #    sub = graph.subgraph(c)
    #    distances.append(nx.average_shortest_path_length(sub))
    largest_cc = graph.subgraph(max(nx.connected_components(graph), key=len))
    largest_distances.append(nx.average_shortest_path_length(largest_cc))
print(largest_distances)
'''
'''
plt.xlabel("Timestep")
plt.ylabel("Average Distance Of Largest Component")
plt.plot(range(len(largest_distances)), largest_distances, label="Average Distance Distribution over Time")
plt.savefig("avg_dist_ppin_ito.png")
plt.clf()

plt.xlabel("Timestep")
plt.ylabel("Average Clustering Of Largest Component")
plt.plot(range(len(average_clustering)), average_clustering, label="Average Clustering Distribution over Time")
plt.savefig("avg_clust_ppin_ito.png")
'''

np.save(f"avg_clust_lambert.npy", average_clustering)
#countDegree(largest_cc)

'''
plt.legend()
all_degrees= np.unique(all_degrees)
plt.xticks(all_degrees)
ax.set_xlabel("Degree")
ax.set_ylabel("Probability Distribution")
#plt.plot(range(len(pi_over_time)), pi_over_time, label="Average Distance Distribution over Time")
plt.savefig("test.png")

plt.clf()
plt.xlabel("Timestep")
plt.ylabel("Average Number Of Triangles In Largest Component")
plt.plot(range(len(avg_triangles)), avg_triangles, label="Average Number of Triangles over Time")
plt.savefig("tri_ppin_ito.png")
'''
#countDegree(largest_cc)
