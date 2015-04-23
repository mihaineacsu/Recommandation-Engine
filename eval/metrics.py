__author__ = 'alexei'

from recsys.evaluation.prediction import MAE, RMSE
import sys


def mean_absolute_error(train_values, predicted_values):

    if len(train_values) != len(predicted_values):
        sys.stderr.write("mean_absolute_error: Invalid list lengths")
        exit(1)

    mae = MAE()
    mae.load_ground_truth(train_values)
    mae.load_test(predicted_values)
    return mae.compute()

def root_mean_square_error(train_values, predicted_values):

    if len(train_values) != len(predicted_values):
        sys.stderr.write("mean_absolute_error: Invalid list lengths")
        exit(1)

    rmse = RMSE()
    rmse.load_ground_truth(train_values)
    rmse.load_test(predicted_values)
    return rmse.compute()

def test_metrics(train, predicted):

    print "MAE... ", mean_absolute_error(train, predicted)
    print "RMSE... ", root_mean_square_error(train, predicted)

def _test():

    train_values = [3.0, 1.0, 5.0, 2.0, 3.0]
    predicted_values = [2.3, 0.9, 4.9, 1.9, 3.0]
    test_metrics(train_values, predicted_values)


if __name__ == "__main__":
    _test()
