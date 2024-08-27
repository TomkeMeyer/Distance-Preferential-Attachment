import numpy as np
import matplotlib

import matplotlib.pyplot as plt

labels = []
label_values = [0,0.25,0.5,0.75,1,'random']
fig, ax = plt.subplots()
PA_clustering_ito = [0.4460057955679206, -0.2084715887461948, -0.11234599731898455, 0.4500249126473693, 0.6891622629291609, 0.26261903566551925]
Bet_clustering_ito = [-0.09811164067341115, -0.16240044889869468, -0.22842775394062018, -0.22318399373437076, -0.3856746607537928, 0.21882567121326182]
PA_distance_ito = [0.9796399519915656, 0.9690510259193216, 0.9852159369896902, 0.9723121365017282, 0.9796844935776546, 0.9348840034282202]
Bet_distance_ito = [0.9638901533362272, 0.9654042259257558, 0.9670089321291689, 0.9667051045851084, 0.9631704676262816, 0.8282629702919144]
PA_clustering_tarassov_m5 = [-0.528997861512911, -0.5296577516288499, -0.5615301728252718, -0.5677567112104694, -0.5719194838256068, -0.5401324197646253]
Bet_clustering_tarassov_m5 = [-0.6359874123940339, -0.6399461261203754, -0.583974419053616, -0.6498815022520957, -0.6617610253353258, -0.5562551382161445]
PA_clustering_tarassov_m3 = [-0.481957730176108, -0.5388947033045611, -0.454626055545358, -0.5155577736412663, -0.5611576525184807, -0.4893216584363559]
Bet_clustering_tarassov_m3 = [-0.5484264963589343, -0.5302239762429158, -0.5436623257041494, -0.5403049408246089, -0.563738243797642, -0.48708156309920475]
PA_clustering_lambert_m5 = [-0.8139826835790894, -0.9477673313779686, -0.9657127763395997, -0.9175822542122246, -0.8684962844693461, -0.9448883507592205]
Bet_clustering_lambert_m5 = [0.9576800767088244, 0.9385860088664633, 0.9531290043168335, 0.935291697852795, 0.9681309072294685, -0.9602341922092708]
PA_clustering_lambert_m3 = [-0.9502142557708435, -0.9757924624242583, -0.953274335505504, -0.9539125504516824, -0.9022871008101806, -0.9718152299916808]
Bet_clustering_lambert_m3 = [0.9751043995961602, 0.9331338187271582, 0.9442336556111036, 0.9686012480099763, 0.9026967909909203, -0.9647670077762077]
arrays_clust = [PA_clustering_ito, Bet_clustering_ito]
labels_clust = ['PA_clust', 'Bet_clust']
arrays_dist = [PA_distance_ito, Bet_distance_ito]
labels_dist = ['PA_dist', 'Bet_dist']
arrays_clust_t = [PA_clustering_tarassov_m5, Bet_clustering_tarassov_m5, PA_clustering_tarassov_m3, Bet_clustering_tarassov_m3]
labels_clust_t = ['PA_clust_m5', 'Bet_clust_m5', 'PA_clust_m3', 'Bet_clust_m3']
arrays_clust_l = [PA_clustering_lambert_m5, Bet_clustering_lambert_m5, PA_clustering_lambert_m3, Bet_clustering_lambert_m3]
labels_clust_l = ['PA_clust_m5', 'Bet_clust_m5', 'PA_clust_m3', 'Bet_clust_m3']
for a,l in zip(arrays_clust_l, labels_clust_l):
    a = [abs(i) for i in a]
    plt.plot(label_values, a, '-o', label = l)
plt.legend()
plt.xlabel("Beta")
plt.ylabel("Absolute Pearson Correlation")
plt.savefig("pearson_correlation_clust_lambert.png")
plt.clf()
