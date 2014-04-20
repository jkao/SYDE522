from sklearn import preprocessing, metrics, neighbors
from sklearn.cross_validation import KFold, cross_val_score
from sklearn.decomposition import PCA
from sklearn.linear_model import LassoCV, LassoLarsCV, LassoLarsIC, LinearRegression, RidgeCV

import numpy as np


class LassoRegressor(object):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def evaluate(self):
        # K-Fold 90/10 split, shuffled for determining alpha and train/test
        train_test_cv = KFold(len(self.y), n_folds=10)#, shuffle=True)

        # Experiment 1
        print("Experiment 1: Lasso CV")
        model_1 = LassoCV(cv=10)
        r2_scores = \
            cross_val_score(model_1, self.X, self.y, cv=train_test_cv, scoring='r2')
        mse_scores = \
            cross_val_score(model_1, self.X, self.y, cv=train_test_cv, scoring='mean_squared_error')
        print "R2 ", r2_scores
        print "R2 ", np.mean(r2_scores)
        print "MSE: ", mse_scores
        print "MSE ", np.mean(mse_scores)

        # Experiment 2
        print("Experiment 2: LassoLarsCV")
        model_2 = LassoLarsCV(cv=10)
        r2_scores = \
            cross_val_score(model_2, self.X, self.y, cv=train_test_cv, scoring='r2')
        mse_scores = \
            cross_val_score(model_1, self.X, self.y, cv=train_test_cv, scoring='mean_squared_error')
        print "R2 ", r2_scores
        print "R2 ", np.mean(r2_scores)
        print "MSE: ", mse_scores
        print "MSE ", np.mean(mse_scores)

        # Experiment 3
        print("Experiment 3: LassoLarsIC using aic")
        model = LassoLarsIC(criterion='aic').fit(self.X, self.y)
        r2_scores = \
            cross_val_score(model, self.X, self.y, cv=train_test_cv, scoring='r2')
        mse_scores = \
            cross_val_score(model_1, self.X, self.y, cv=train_test_cv, scoring='mean_squared_error')
        print "R2 ", r2_scores
        print "R2 ", np.mean(r2_scores)
        print "MSE: ", mse_scores
        print "MSE ", np.mean(mse_scores)

        # Experiment 4
        print("Experiment 4: LassoLarsIC using aic")
        model = LassoLarsIC(criterion='bic').fit(self.X, self.y)
        r2_scores = \
            cross_val_score(model, self.X, self.y, cv=train_test_cv, scoring='r2')
        mse_scores = \
            cross_val_score(model_1, self.X, self.y, cv=train_test_cv, scoring='mean_squared_error')
        print "R2 ", r2_scores
        print "R2 ", np.mean(r2_scores)
        print "MSE: ", mse_scores
        print "MSE ", np.mean(mse_scores)

        # Experiment 5
        print("Experiment 5: Linear Regression")
        model = LinearRegression()
        r2_scores = \
            cross_val_score(model, self.X, self.y, cv=train_test_cv, scoring='r2')
        mse_scores = \
            cross_val_score(model_1, self.X, self.y, cv=train_test_cv, scoring='mean_squared_error')
        print "R2 ", r2_scores
        print "R2 ", np.mean(r2_scores)
        print "MSE: ", mse_scores
        print "MSE ", np.mean(mse_scores)

        # Experiment 6
        print("Experiment 6: Ridge Regression")
        model = RidgeCV(cv=10)
        r2_scores = \
            cross_val_score(model, self.X, self.y, cv=train_test_cv, scoring='r2')
        mse_scores = \
            cross_val_score(model_1, self.X, self.y, cv=train_test_cv, scoring='mean_squared_error')
        print "R2 ", r2_scores
        print "R2 ", np.mean(r2_scores)
        print "MSE: ", mse_scores
        print "MSE ", np.mean(mse_scores)

