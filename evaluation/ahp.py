import numpy as np
from functools import reduce

# Function: AHP
def ahp_method(dataset, wd = 'm'):
    # 初始化RI值，用于进行一致性检验
    inc_rat  = np.array([0, 0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45])
    X        = np.copy(dataset)
    weights  = np.zeros(X.shape[1])
    if (wd == 'm' or wd == 'mean'):
        weights  = np.mean(X/np.sum(X, axis = 0), axis = 1)
    elif (wd == 'g' or wd == 'geometric'):
        for i in range (0, X.shape[1]):
            weights[i] = reduce( (lambda x, y: x * y), X[i,:])**(1/X.shape[1])
        weights = weights/np.sum(weights)
    vector   = np.sum(X*weights, axis = 1)/weights      # 权重向量
    lamb_max = np.mean(vector)
    cons_ind = (lamb_max - X.shape[1])/(X.shape[1] - 1) # CI值
    rc       = cons_ind/inc_rat[X.shape[1]]
    return weights, rc