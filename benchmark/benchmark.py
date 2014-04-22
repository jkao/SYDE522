import numpy as np
from sklearn.cross_validation import KFold, cross_val_score
from sklearn.decomposition import PCA
from sklearn.linear_model import LassoCV, LassoLarsCV, LassoLarsIC, LinearRegression, RidgeCV
from sklearn import preprocessing, metrics, neighbors

UCI_DATA = "housing.data"

d = np.genfromtxt(UCI_DATA)
X = d[:,0:13]
y = d[:,13]

train_test_cv = KFold(len(y), n_folds=10, shuffle=True)

# Try out lasso
model = LassoCV(cv=10)
r2_scores = \
    cross_val_score(model, X, y, cv=train_test_cv, scoring='r2')
mse_scores = \
    cross_val_score(model, X, y, cv=train_test_cv, scoring='mean_squared_error')

print r2_scores
print np.mean(r2_scores)
print mse_scores
print np.mean(mse_scores)

# standard scaling
model = LassoCV(cv=10)
r2_scores = \
    cross_val_score(model, preprocessing.scale(X), y, cv=train_test_cv, scoring='r2')
mse_scores = \
    cross_val_score(model, preprocessing.scale(X), y, cv=train_test_cv, scoring='mean_squared_error')

print r2_scores
print np.mean(r2_scores)
print mse_scores
print np.mean(mse_scores)

# Try out kNN
n_neighbors = 5
knn = neighbors.KNeighborsRegressor(n_neighbors, weights="distance")
r2_scores = \
    cross_val_score(knn, X, y, cv=train_test_cv, scoring='r2')
mse_scores = \
    cross_val_score(knn, X, y, cv=train_test_cv, scoring='mean_squared_error')

print r2_scores
print np.mean(r2_scores)
print mse_scores
print np.mean(mse_scores)

# standard scaling
knn = neighbors.KNeighborsRegressor(n_neighbors, weights="distance")
r2_scores = \
    cross_val_score(knn, preprocessing.scale(X), y, cv=train_test_cv, scoring='r2')
mse_scores = \
    cross_val_score(knn, preprocessing.scale(X), y, cv=train_test_cv, scoring='mean_squared_error')

print r2_scores
print np.mean(r2_scores)
print mse_scores
print np.mean(mse_scores)

# kNN with PCA
pca = PCA(n_components='mle')
X_pca = pca.fit_transform(X)

# standard scaling
knn = neighbors.KNeighborsRegressor(n_neighbors, weights="distance")
r2_scores = \
    cross_val_score(knn, X_pca, y, cv=train_test_cv, scoring='r2')
mse_scores = \
    cross_val_score(knn, X_pca, y, cv=train_test_cv, scoring='mean_squared_error')

print r2_scores
print np.mean(r2_scores)
print mse_scores
print np.mean(mse_scores)

# standard scaling
knn = neighbors.KNeighborsRegressor(n_neighbors, weights="distance")
r2_scores = \
    cross_val_score(knn, preprocessing.scale(X_pca), y, cv=train_test_cv, scoring='r2')
mse_scores = \
    cross_val_score(knn, preprocessing.scale(X_pca), y, cv=train_test_cv, scoring='mean_squared_error')

print r2_scores
print np.mean(r2_scores)
print mse_scores
print np.mean(mse_scores)

