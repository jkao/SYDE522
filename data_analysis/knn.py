from sklearn import preprocessing, metrics, neighbors
from sklearn.cross_validation import KFold, cross_val_score
from sklearn.decomposition import PCA
from sklearn.linear_model import LassoCV, LassoLarsCV, LassoLarsIC

import numpy as np


class KnnRegressor(object):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def evaluate(self):
        # K-Fold 90/10 split, shuffled for determining alpha and train/test
        train_test_cv = KFold(len(self.y), n_folds=10)#, shuffle=True)

        # Experiment 1 - kNN without PCA, varying neighbors
        print("Experiment 1 - kNN without PCA, vary neighbors")
        max_r2 = 0
        max_r2_neighbors = None
        min_mses = float("inf")
        min_mse_neighbors = None

        for n_neighbors in range(3, 50):
            r2s = []
            mses = []

            for train_idx, test_idx in train_test_cv:
                X_train, X_test = self.X[train_idx], self.X[test_idx]
                y_train, y_test = self.y[train_idx], self.y[test_idx]

                # model
                knn = neighbors.KNeighborsRegressor(n_neighbors, weights="distance")
                # train
                knn.fit(X_train, y_train)
                # evaluate
                y_pred = knn.predict(X_test)

                # Filter out nan output
                y_pred_nan = np.isnan(y_pred)
                y_pred = np.array([yy for idx, yy in enumerate(y_pred) if not y_pred_nan[idx]])
                y_test = np.array([yy for idx, yy in enumerate(y_test) if not y_pred_nan[idx]])

                # R^2 score
                r2 = metrics.r2_score(y_test, y_pred)
                r2s.append(r2)

                # MSE score
                mse = metrics.mean_squared_error(y_test, y_pred)
                mses.append(mse)

            avg_r2s = np.median(r2s)
            if avg_r2s > max_r2:
                max_r2 = avg_r2s
                max_r2_neighbors = n_neighbors
            avg_mses = np.median(mses)
            if avg_mses < min_mses:
                min_mses = avg_mses
                min_mse_neighbors = n_neighbors

            print("%d, %f, %f" % (n_neighbors, avg_r2s, avg_mses))

        print("DONE.")
        print("Max Neighbors: %d, R2: %f, MSE: %f" % (max_r2_neighbors, max_r2, min_mses))

        # Experiment 2 - kNN without PCA, varying neighbors
        print("Experiment 2 - kNN without PCA, varying neighbors")
        max_r2 = 0
        max_r2_components = 1
        n_neighbors = max_r2_neighbors

        for n_components in range(1, 9):
            r2s = []
            mses = []

            for train_idx, test_idx in train_test_cv:
                X_train, X_test = self.X[train_idx], self.X[test_idx]
                y_train, y_test = self.y[train_idx], self.y[test_idx]

                # run pca
                pca = PCA(n_components=n_components)
                X_train_pca = pca.fit_transform(X_train)
                X_test_pca = pca.transform(X_test)

                # model
                knn = neighbors.KNeighborsRegressor(n_neighbors, weights="distance")
                # train
                knn.fit(X_train_pca, y_train)
                # evaluate
                y_pred = knn.predict(X_test_pca)

                # Filter out nan output
                y_pred_nan = np.isnan(y_pred)
                y_pred = np.array([yy for idx, yy in enumerate(y_pred) if not y_pred_nan[idx]])
                y_test = np.array([yy for idx, yy in enumerate(y_test) if not y_pred_nan[idx]])

                # R^2 score
                r2 = metrics.r2_score(y_test, y_pred)
                r2s.append(r2)

                # MSE score
                mse = metrics.mean_squared_error(y_test, y_pred)
                mses.append(mse)

            avg_r2s = np.median(r2s)
            if avg_r2s > max_r2:
                max_r2 = avg_r2s
                max_r2_components = n_components
            avg_mses = np.median(mses)
            if avg_mses < min_mses:
                min_mses = avg_mses
                min_mse_neighbors = n_neighbors

            print("%d, %f, %f" % (n_neighbors, avg_r2s, avg_mses))

        print("DONE.")
        print("Max Components: %d, R2: %f, MSE: %f" % (max_r2_components, max_r2, min_mses))
