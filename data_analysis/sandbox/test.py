print(__doc__)

# Author: Olivier Grisel, Gael Varoquaux, Alexandre Gramfort
# License: BSD 3 clause

import time

import numpy as np
import pylab as pl

from sklearn.linear_model import LassoCV, LassoLarsCV, LassoLarsIC
from sklearn import datasets

diabetes = datasets.load_diabetes()
X = diabetes.data
y = diabetes.target

rng = np.random.RandomState(42)
X = np.c_[X, rng.randn(X.shape[0], 14)]  # add some bad features

# normalize data as done by Lars to allow for comparison
X /= np.sqrt(np.sum(X ** 2, axis=0))

##############################################################################
# LassoLarsIC: least angle regression with BIC/AIC criterion

model_bic = LassoLarsIC(criterion='bic')
t1 = time.time()
model_bic.fit(X, y)
t_bic = time.time() - t1
alpha_bic_ = model_bic.alpha_

model_aic = LassoLarsIC(criterion='aic')
model_aic.fit(X, y)
alpha_aic_ = model_aic.alpha_


def plot_ic_criterion(model, name, color):
    alpha_ = model.alpha_
    alphas_ = model.alphas_
    criterion_ = model.criterion_
    pl.plot(-np.log10(alphas_), criterion_, '--', color=color,
            linewidth=3, label='%s criterion' % name)
    pl.axvline(-np.log10(alpha_), color=color, linewidth=3,
               label='alpha: %s estimate' % name)
    pl.xlabel('-log(alpha)')
    pl.ylabel('criterion')

pl.figure()
plot_ic_criterion(model_aic, 'AIC', 'b')
plot_ic_criterion(model_bic, 'BIC', 'r')
pl.legend()
pl.title('Information-criterion for model selection (training time %.3fs)'
         % t_bic)

##############################################################################
# LassoCV: coordinate descent

# Compute paths
print("Computing regularization path using the coordinate descent lasso...")
t1 = time.time()
model = LassoCV(cv=20).fit(X, y)
t_lasso_cv = time.time() - t1

# Display results
m_log_alphas = -np.log10(model.alphas_)

pl.figure()
ymin, ymax = 2300, 3800
pl.plot(m_log_alphas, model.mse_path_, ':')
pl.plot(m_log_alphas, model.mse_path_.mean(axis=-1), 'k',
        label='Average across the folds', linewidth=2)
pl.axvline(-np.log10(model.alpha_), linestyle='--', color='k',
           label='alpha: CV estimate')

pl.legend()

pl.xlabel('-log(alpha)')
pl.ylabel('Mean square error')
pl.title('Mean square error on each fold: coordinate descent '
         '(train time: %.2fs)' % t_lasso_cv)
pl.axis('tight')
pl.ylim(ymin, ymax)

##############################################################################
# LassoLarsCV: least angle regression

# Compute paths
print("Computing regularization path using the Lars lasso...")
t1 = time.time()
model = LassoLarsCV(cv=20).fit(X, y)
t_lasso_lars_cv = time.time() - t1

# Display results
m_log_alphas = -np.log10(model.cv_alphas_)

pl.figure()
pl.plot(m_log_alphas, model.cv_mse_path_, ':')
pl.plot(m_log_alphas, model.cv_mse_path_.mean(axis=-1), 'k',
        label='Average across the folds', linewidth=2)
pl.axvline(-np.log10(model.alpha_), linestyle='--', color='k',
           label='alpha CV')
pl.legend()

pl.xlabel('-log(alpha)')
pl.ylabel('Mean square error')
pl.title('Mean square error on each fold: Lars (train time: %.2fs)'
         % t_lasso_lars_cv)
pl.axis('tight')
pl.ylim(ymin, ymax)

pl.show()
