import math
import numpy as np
from statistics import *


def find_clusters(X: np):
    clusters = {}
    min_clusters = {}
    for i in range(2,11):
        clusters[i] = {}
        index = np.random.randint(0, X.shape[0], i)
        cluster = index.tolist()
        for j in cluster:
            k = cluster.index(j)
            clusters[i][k+1] = X[j]
    final_clusters = {}
    min_clusters[0] = {}
    for size in clusters:
        final_clusters[size]={}
        for iteration in range(1, 100):
            min_clusters[iteration] = {}
            if iteration < 2 or min_clusters[iteration-2] != min_clusters[iteration-1]:
                distance = {}
                min_distance = []
                for cluster in clusters[size]:
                    value = 0
                    distance[cluster] = {}
                    for values in X:
                        value = value+1
                        sub = np.sum(np.square(clusters[size][cluster]-values))
                        distance[cluster][value] = math.sqrt(sub)
                        if cluster == 1:
                            min_distance.append(distance[cluster][value])
                            min_clusters[iteration][value] = cluster
                        else:
                            if min_distance[value-1] > distance[cluster][value]:
                                min_distance[value-1] = distance[cluster][value]
                                min_clusters[iteration][value] = cluster
                k_cluster = {}
                for n in range(1, size+1):
                    k_cluster[n] = {}
                    for val in min_clusters[iteration]:
                        if min_clusters[iteration][val] == n:
                            k_cluster[n][val] = min_clusters[iteration][val]
                clusters[size] = {}
                array = {}
                final_array = {}
                for clust in k_cluster:
                    array[clust] = []
                    if k_cluster[clust] != {}:
                        for items in k_cluster[clust]:
                            array[clust].append(X[items-1])
                        final_array[clust] = np.asarray(array[clust])
                        clusters[size][clust] = np.mean(final_array[clust], axis=0)
                    else:
                        continue
            elif iter == 99 or min_clusters[iteration-2] == min_clusters[iteration-1]:
                final_clusters[size] = min_clusters[iteration-1]
                # print(iteration)
                break
    return final_clusters


def elbow_method(X: np, final_clusters):
    ss = {}
    sse = {}
    for num in final_clusters:
        ss[num] = {}
        sse[num] = [0]
        for cluster in final_clusters[num]:
            value = 0
            ss[num][cluster] = {}
            for values in X:
                value = value + 1
                ss[num][cluster][value] = np.sum(np.square(final_clusters[num][cluster] - values))
                sse[num] = sse[num] + ss[num][cluster][value]
    return find_k(sse)


def find_k(sse):
    sse_final = []
    for n in sse:
        for val in sse[n]:
            sse_final.append(val / n)
    last_sse = []
    for value in sse_final:
        last_sse.append(abs(value - mean(sse_final)))
    k = last_sse.index(min(last_sse)) + 1
    return k