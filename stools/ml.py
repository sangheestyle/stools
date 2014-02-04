from sklearn.cluster import KMeans as sk_KMeans

def KMeans(vectors, n_clusters, max_iter):
    km = sk_KMeans(n_clusters=n_clusters, precompute_distances=False,
                           init='k-means++', max_iter=max_iter, n_init=1)
    predict = km.fit_predict(vectors)
    return predict