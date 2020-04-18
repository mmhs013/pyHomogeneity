"""
Created on 13 April 2020
Last Update on 17 April 2020
@author: Md. Manjurul Hussain Shourov
version: 1.0
Approach: Vectorisation
"""

from __future__ import division
import numpy as np
from scipy.stats import rankdata
from collections import namedtuple


# Supporting Functions
# Data Preprocessing
def __preprocessing(x):
    try:
        if x.index.dtype != 'int64':
            idx = x.index.date.astype('str')
        else:
            idx = np.asarray(range(1, len(x)+1))
    except:
        idx = np.asarray(range(1, len(x)+1))
        
    x = np.asarray(x)
    dim = x.ndim
    
    if dim == 1:
        c = 1
        
    elif dim == 2:
        (n, c) = x.shape
        
        if c == 1:
            dim = 1
            x = x.flatten()
            
    else:
        print('Please check your dataset.')
        
    return x, c, idx


# Missing Values Analysis
def __missing_values_analysis(x, idx, method = 'skip'):
    if method.lower() == 'skip':
        if x.ndim == 1:
            idx = idx[~np.isnan(x)]
            x = x[~np.isnan(x)]
            
        else:
            idx = idx[~np.isnan(x).any(axis=1)]
            x = x[~np.isnan(x).any(axis=1)]
            
    n = len(x)
    
    return x, n, idx


# Pettitt test
def __pettitt(x):
    n = len(x)
    r = rankdata(x)
    
    k = np.arange(n-1)
    s = r.cumsum()[:-1]
    
    U = 2 * s - (k + 1) * (n + 1)
    
    return U.max(), U.argmax() + 1


# SNHT test
def __snht(x):
    n = len(x)
    k = np.arange(1, n)
    s = x.cumsum()[:-1]
    rs = x[::-1].cumsum()[::-1][1:]

    z1 = ((s - k * x.mean()) / x.std(ddof=1)) / k
    z2 = ((rs - k[::-1] * x.mean()) / x.std(ddof=1)) / (n - k)
    T = (k) * z1 ** 2 + (n - k) * z2 ** 2 
    
    return T.max() , T.argmax() + 1


# Buishad Q statistics test
def __buishand_q(x, alpha=0.05):
    n = len(x)
    
    k = np.arange(1, n+1)
    S = x.cumsum() - k * x.mean()
        
    S_std = S  / x.std()  # sample std
    Q = abs(S_std).max() / np.sqrt(n)
    
    return Q, abs(S).argmax() + 1


# Buishad range test
def __buishand_range(x, alpha=0.05):
    n = len(x)
    
    k = np.arange(1, n+1)
    S = x.cumsum() - k * x.mean()
        
    S_std = S  / x.std() # should use sample std -> x.std()
    R = (S_std.max() - S_std.min()) / np.sqrt(n)
    
    return R, abs(S).argmax() + 1


# Buishad likelihood ratio test
def __buishand_lr(x, alpha=0.05):
    n = len(x)
    
    k = np.arange(1, n+1)
    S = x.cumsum() - k * x.mean()
    
    V = S[:-1] / (x.std() * k[:-1] *(n-k[:-1]))
    
    return V.max(), abs(S).argmax() + 1


# Buishad U statistics test
def __buishand_u(x):
    n = len(x)
    
    k = np.arange(1, n+1)
    S = x.cumsum() - k * x.mean()
        
    S_std = S  / x.std() # should use sample std -> x.std()
    U = (S_std[:n-1]**2).sum() / (n * (n + 1))
    
    return U, abs(S).argmax() + 1


# Monte carlo simulation for p-value calculation
def __mc_p_value(func, stat, n, sim): 
    rand_data = np.random.normal(0, 1, [sim, n])
    res = np.asarray(list(map(func, rand_data)))
    p_val = (res[:,0] > stat).sum() / sim
    
    return p_val


# Mean calculation
def __mean(x, loc):
    mu = namedtuple('mean',['mu1', 'mu2'])
    mu1 = x[:loc].mean()
    mu2 = x[loc:].mean()
    
    return mu(mu1, mu2)


# Homogeneity test
def __test(func, x, alpha, sim):
    x, c, idx = __preprocessing(x)
    x, n, idx = __missing_values_analysis(x, idx, method = 'skip')
    
    stat, loc = func(x)
    
    if sim:
        p = __mc_p_value(func, stat, n, sim)
        h = alpha > p
    else:
        p = None
        h = None
    
    mu = __mean(x, loc)
    
    return h, idx[loc-1], p, stat, mu


def pettitt_test(x, alpha = 0.05, sim = 20000):
    """
    This function checks homogeneity test using A. N. Pettitt's (1979) method.
    Input:
        x: a vector (list, numpy array or pandas series) data
        alpha: significance level (0.05 default)
        sim: No. of monte carlo simulation for p-value calculation (default 20000)
    Output:
        h: True (if data is nonhomogeneous) or False (if data is homogeneous)
        cp: probable change point location index
        p: p-value of the significance test
        U: Maximum of Pettitt's U Statistics
        avg: mean values at before and after change point
    Examples
    --------
      >>> import pyhomogeneity as hg
      >>> x = np.random.rand(1000)
      >>> h, cp, p, U, mu = hg.pettitt_test(x, 0.05)
    """
    res = namedtuple('Pettitt_Test', ['h', 'cp', 'p', 'U', 'avg'])
    h, cp, p, U, mu = __test(__pettitt, x, alpha, sim)
    
    if not sim:
        x, c, idx = __preprocessing(x)
        x, n, idx = __missing_values_analysis(x, idx, method = 'skip')
        p = 2 * np.exp((- 6 * np.max(U)**2) / (n**3 + n**2))
        h = alpha > p
    
    return res(h, cp, p, U, mu)


def snht_test(x, alpha = 0.05, sim = 20000):
    """
    This function checks homogeneity test using H. Alexandersson (1986) method.
    Input:
        x: a vector (list, numpy array or pandas series) data
        alpha: significance level (0.05 default)
        sim: No. of monte carlo simulation for p-value calculation (default 20000)
    Output:
        h: True (if data is nonhomogeneous) or False (if data is homogeneous)
        cp: probable change point location index
        p: p-value of the significance test
        T: Maximum of SNHT T Statistics
        avg: mean values at before and after change point
    Examples
    --------
      >>> import pyhomogeneity as hg
      >>> x = np.random.rand(1000)
      >>> h, cp, p, T, mu = hg.snht_test(x, 0.05)
    """
    res = namedtuple('SNHT_Test', ['h', 'cp', 'p', 'T', 'avg'])
    h, cp, p, T, mu = __test(__snht, x, alpha, sim)

    return res(h, cp, p, T, mu)


def buishand_q_test(x, alpha = 0.05, sim = 20000):
    """
    This function checks homogeneity test using Buishand's Q statistics method proposed in T. A. Buishand (1982).
    Input:
        x: a vector (list, numpy array or pandas series) data
        alpha: significance level (0.05 default)
        sim: No. of monte carlo simulation for p-value calculation (default 20000)
    Output:
        h: True (if data is nonhomogeneous) or False (if data is homogeneous)
        cp: probable change point location index
        p: p-value of the significance test
        Q: Maximum of Buishand's Q Statistics divided by squire root of sample size [Q/sqrt(n)]
        avg: mean values at before and after change point
    Examples
    --------
      >>> import pyhomogeneity as hg
      >>> x = np.random.rand(1000)
      >>> h, cp, p, Q, mu = hg.buishand_q_test(x, 0.05)
    """
    res = namedtuple('Buishand_Q_Test', ['h', 'cp', 'p', 'Q', 'avg'])
    h, cp, p, Q, mu = __test(__buishand_q, x, alpha, sim)

    return res(h, cp, p, Q, mu)


def buishand_range_test(x, alpha = 0.05, sim = 20000):
    """
    This function checks homogeneity test using Buishand's range method proposed in T. A. Buishand (1982).
    Input:
        x: a vector (list, numpy array or pandas series) data
        alpha: significance level (0.05 default)
        sim: No. of monte carlo simulation for p-value calculation (default 20000)
    Output:
        h: True (if data is nonhomogeneous) or False (if data is homogeneous)
        cp: probable change point location index
        p: p-value of the significance test
        R: Buishand's Q Statistics range divided by squire root of sample size [R/sqrt(n)]
        avg: mean values at before and after change point
    Examples
    --------
      >>> import pyhomogeneity as hg
      >>> x = np.random.rand(1000)
      >>> h, cp, p, R, mu = hg.buishand_range_test(x, 0.05)
    """
    res = namedtuple('Buishand_Range_Test', ['h', 'cp', 'p', 'R', 'avg'])
    h, cp, p, R, mu = __test(__buishand_range, x, alpha, sim)

    return res(h, cp, p, R, mu)


def buishand_likelihood_ratio_test(x, alpha = 0.05, sim = 20000):
    """
    This function checks homogeneity test using Buishand's likelihood ration method proposed in T. A. Buishand (1982).
    Input:
        x: a vector (list, numpy array or pandas series) data
        alpha: significance level (0.05 default)
        sim: No. of monte carlo simulation for p-value calculation (default 20000)
    Output:
        h: True (if data is nonhomogeneous) or False (if data is homogeneous)
        cp: probable change point location index
        p: p-value of the significance test
        V: Maximum of Buishand's weighted adjusted partial sum Z
        avg: mean values at before and after change point
    Examples
    --------
      >>> import pyhomogeneity as hg
      >>> x = np.random.rand(1000)
      >>> h, cp, p, V, mu = hg.buishand_range_test(x, 0.05)
    """
    res = namedtuple('Buishand_Likelihood_Ratio_Test', ['h', 'cp', 'p', 'V', 'avg'])
    h, cp, p, V, mu = __test(__buishand_lr, x, alpha, sim)

    return res(h, cp, p, V, mu)


def buishand_u_test(x, alpha = 0.05, sim = 20000):
    """
    This function checks homogeneity test using Buishand's U statistics method method proposed in T. A. Buishand (1982).
    Input:
        x: a vector (list, numpy array or pandas series) data
        alpha: significance level (0.05 default)
        sim: No. of monte carlo simulation for p-value calculation (default 20000)
    Output:
        h: True (if data is nonhomogeneous) or False (if data is homogeneous)
        cp: probable change point location index
        p: p-value of the significance test
        U: Maximum of Buishand's U Statistics
        avg: mean values at before and after change point
    Examples
    --------
      >>> import pyhomogeneity as hg
      >>> x = np.random.rand(1000)
      >>> h, cp, p, U, mu = hg.buishand_u_test(x, 0.05)
    """
    res = namedtuple('Buishand_U_Test', ['h', 'cp', 'p', 'U', 'avg'])
    h, cp, p, U, mu = __test(__buishand_u, x, alpha, sim)

    return res(h, cp, p, U, mu)