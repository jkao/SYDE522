from lasso import LassoRegressor
from knn import KnnRegressor
from sklearn import preprocessing, metrics
from util import Util


if __name__ == '__main__':
    # min/max norm'ed
    normalized_data_path = "cleaner/data/cleaned.json"
    # no normalization
    data_path = "cleaner/data/cleaned_no_normal.json"

    # min/max X,y
    X_mm, y_mm = Util.load_json_to_numpy_array(normalized_data_path)
    # X, y
    X, y = Util.load_json_to_numpy_array(data_path)
    # scaled X, y
    X_s = preprocessing.scale(X)

    # Run experiments on scaled X,y
    print("-------------Evaluate with Unnormalized Data-------------")
    knn = KnnRegressor(X, y)
    l = LassoRegressor(X, y)

    knn.evaluate()
    l.evaluate()
    print("-------------DONE-------------")

    # Run experiments on scaled X,y
    print("-------------Evaluate with Min/Max Normalized Data-------------")
    knn_mm = KnnRegressor(X_mm, y)
    l_mm = LassoRegressor(X_mm, y)

    knn_mm.evaluate()
    l_mm.evaluate()
    print("-------------DONE-------------")

    # Run experiments on scaled X,y
    print("-------------Evaluate with Scaled Data-------------")
    knn_s = KnnRegressor(X_s, y)
    l_s = LassoRegressor(X_s, y)

    knn_s.evaluate()
    l_s.evaluate()
    print("-------------DONE-------------")
