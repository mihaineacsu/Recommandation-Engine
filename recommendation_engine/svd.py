__author__ = 'alexei'

import recsys.algorithm
from recsys.algorithm.factorize import SVD
from recsys.datamodel.data import Data
from recsys.evaluation.prediction import RMSE, MAE
from recsys.algorithm.factorize import SVDNeighbourhood

recsys.algorithm.VERBOSE = True

def svd_neighbourhood(data, K=100):

    svd = SVDNeighbourhood()
    svd.set_data(data)

    svd.compute(k=K,
                min_values=5,
                pre_normalize=None,
                mean_center=True,
                post_normalize=True)
    return svd


def svd_instance(data, K=100):

    svd = SVD()
    svd.set_data(data)

    svd.compute(k=K,
                min_values=5,
                pre_normalize=None,
                mean_center=True,
                post_normalize=True,
                savefile=None)
    return svd


def svd_test_accuracy(svd, test):

    rmse = RMSE()
    mae  = MAE()

    for rating, item_id, user_id in test.get():

        try:
            pred_rating = svd.predict(item_id, user_id)
            rmse.add(rating, pred_rating)
            mae.add(rating, pred_rating)
        except KeyError:
            continue

    print 'RMSE=%s' % rmse.compute()
    print 'MAE=%s' % mae.compute()


def sample_data():

    path = "../temp/ml-1m/ratings.dat"
    data = Data()

    # userId :: productId :: rating
    format = {'col': 0, 'row': 1, 'value': 2, 'ids': 'int'}

    data.load(path, sep='::', format=format)
    return data.split_train_test(percent=80) # 80% train, 20% test


def _test():

    train, test = sample_data()
    svd = svd_instance(train)
    svd_test_accuracy(svd, test)

    # Print similiar items
    print svd.similar(1)

    # Print similiar users
    print svd.recommend(1)

    # svdn = svd_neighbourhood(train)
    # svd_test_accuracy(svdn, test)


if __name__ == "__main__":
    _test()

