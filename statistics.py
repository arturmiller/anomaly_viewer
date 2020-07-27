
from sklearn.manifold import TSNE
from sklearn.neighbors import LocalOutlierFactor
from sklearn import preprocessing


def normalize(data):
    if 'url' in data:
        normal_data = data.drop(['url'], axis=1).to_numpy(copy=True)
    else:
        normal_data = data.to_numpy(copy=True)

    preprocessing.robust_scale(normal_data, copy=False)
    return normal_data

def calc_embeding(normal_data):
    tsne = TSNE()
    embeding = tsne.fit_transform(normal_data)
    return {'*embeding_x*': embeding[:, 0], '*embeding_y*': embeding[:, 1]}

def add_embeding(data, embeding):
    for column, values in embeding.items():
        data[column] = values

def calc_outlier_stats(normal_data):
    lof = LocalOutlierFactor(n_neighbors=10)
    lof.fit_predict(normal_data)
    return -lof.negative_outlier_factor_

def add_stats_to_data(data):
    normal_data = normalize(data)
    embeding = calc_embeding(normal_data)
    add_embeding(data, embeding)
    outlier_stats = calc_outlier_stats(normal_data)
    data['*lof*'] = outlier_stats
