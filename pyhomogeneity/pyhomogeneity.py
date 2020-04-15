"""
Created on 13 April 2020
Last Update on 15 April 2020
@author: Md. Manjurul Hussain Shourov
version: 0.1
Approach: Vectorisation
"""

from __future__ import division
import numpy as np
from scipy.stats import rankdata
from collections import namedtuple


# Supporting Functions
# Data Preprocessing
def __preprocessing(x):
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
        
    return x, c


# Missing Values Analysis
def __missing_values_analysis(x, method = 'skip'):
    if method.lower() == 'skip':
        if x.ndim == 1:
            x = x[~np.isnan(x)]
            
        else:
            x = x[~np.isnan(x).any(axis=1)]
    
    n = len(x)
    
    return x, n


def __pettitt(x):
    n = len(x)
    r = rankdata(x)
    
    k = np.arange(n-1)
    s = r.cumsum()[:-1]
    
    U = 2 * s - (k + 1) * (n + 1)
    
    return U.max(), U.argmax() + 1


def __snht(x):
    n = len(x)
    k = np.arange(1, n)
    s = x.cumsum()[:-1]
    rs = x[::-1].cumsum()[::-1][1:]

    z1 = ((s - k * x.mean()) / x.std(ddof=1)) / k
    z2 = ((rs - k[::-1] * x.mean()) / x.std(ddof=1)) / (n - k)
    T = (k) * z1 ** 2 + (n - k) * z2 ** 2 
    
    return T.max() , T.argmax() + 1


def __buishand_q(x, alpha=0.05):
    n = len(x)
    
    k = np.arange(1, n+1)
    S = x.cumsum() - k * x.mean()
        
    S_std = S  / x.std()  # sample std
    Q = abs(S_std).max() / np.sqrt(n)
    
    return Q, abs(S).argmax() + 1


def __buishand_range(x, alpha=0.05):
    n = len(x)
    
    k = np.arange(1, n+1)
    S = x.cumsum() - k * x.mean()
        
    S_std = S  / x.std(ddof=1) # should use sample std -> x.std()
    R = (S_std.max() - S_std.min()) / np.sqrt(n)
    
    return R, abs(S).argmax() + 1


def __buishand_lr(x, alpha=0.05):
    n = len(x)
    
    k = np.arange(1, n+1)
    S = x.cumsum() - k * x.mean()
    
    V = S[:-1] / (x.std() * k[:-1] *(n-k[:-1]))
    
    return V.max(), abs(S).argmax() + 1


def __buishand_u(x):
    n = len(x)
    
    k = np.arange(1, n+1)
    S = x.cumsum() - k * x.mean()
        
    S_std = S  / x.std(ddof=1) # should use sample std -> x.std()
    U = (S_std[:n-1]**2).sum() / (n * (n + 1))
    
    return U, abs(S).argmax() + 1


def __mc_p_value(func, stat, n, sim): 
    rand_data = np.random.normal(0, 1, [sim, n])
    res = np.asarray(list(map(func, rand_data)))
    p_val = (res[:,0] > stat).sum() / sim
    
    return p_val


def __mean(x, loc):
    mu1 = x[:loc].mean()
    mu2 = x[loc:].mean()
    
    return mu1, mu2


def __test(func, x, alpha, sim):
    x, c = __preprocessing(x)
    x, n = __missing_values_analysis(x, method = 'skip')
    
    stat, loc = func(x)
    
    if sim:
        p = __mc_p_value(func, stat, n, sim)
        h = alpha > p
    else:
        p = None
        h = None
    
    mu1, mu2 = __mean(x, loc)
    
    return stat, loc, h, p, mu1, mu2


def pettitt_test(x, alpha = 0.05, sim = None):
    """
    This function checks homogeneity test using Pettitt, A. N. (1979) method.
    Input:
        x: a vector (list, numpy array or pandas series) data
        alpha: significance level (0.05 default)
        sim: no. of monte carlo simulation for p-value calculation
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p-value of the significance test
        z: normalized test statistics
        Tau: Kendall Tau
        s: Mann-Kendal's score
        var_s: Variance S
        slope: sen's slope
    Examples
    --------
      >>> import pyhomogeneity as hg
      >>> x = np.random.rand(1000)
      >>> trend,h,p,z,tau,s,var_s,slope = hm.pettitt_test(x, 0.05)
    """
    res = namedtuple('Pettitt_Test', ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope'])
    U, loc, h, p, mu1, mu2 = __test(__pettitt, x, alpha = 0.05, sim = sim)
    
    if not sim:
        x, c = __preprocessing(x)
        x, n = __missing_values_analysis(x, method = 'skip')
        p = 2 * np.exp((- 6 * np.max(U)**2) / (n**3 + n**2))
        h = alpha > p
    
    return U, loc, h, p, mu1, mu2


def snht_test(x, alpha = 0.05, sim = 20000):
    """
    This function checks homogeneity test using Pettitt, A. N. (1979) method.
    Input:
        x: a vector (list, numpy array or pandas series) data
        alpha: significance level (0.05 default)
        sim: no. of monte carlo simulation for p-value calculation
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p-value of the significance test
        z: normalized test statistics
        Tau: Kendall Tau
        s: Mann-Kendal's score
        var_s: Variance S
        slope: sen's slope
    Examples
    --------
      >>> import pyhomogeneity as hg
      >>> x = np.random.rand(1000)
      >>> trend,h,p,z,tau,s,var_s,slope = hm.pettitt_test(x, 0.05)
    """
    res = namedtuple('Pettitt_Test', ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope'])
    T, loc, h, p, mu1, mu2 = __test(__snht, x, alpha = 0.05, sim = sim)

    return T, loc, h, p, mu1, mu2


def buishand_q_test(x, alpha = 0.05, sim = 20000):
    """
    This function checks homogeneity test using Pettitt, A. N. (1979) method.
    Input:
        x: a vector (list, numpy array or pandas series) data
        alpha: significance level (0.05 default)
        sim: no. of monte carlo simulation for p-value calculation
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p-value of the significance test
        z: normalized test statistics
        Tau: Kendall Tau
        s: Mann-Kendal's score
        var_s: Variance S
        slope: sen's slope
    Examples
    --------
      >>> import pyhomogeneity as hg
      >>> x = np.random.rand(1000)
      >>> trend,h,p,z,tau,s,var_s,slope = hm.pettitt_test(x, 0.05)
    """
    res = namedtuple('Buishand_Q_Test', ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope'])
    Q, loc, h, p, mu1, mu2 = __test(__buishand_q, x, alpha = 0.05, sim = sim)

    return Q, loc, h, p, mu1, mu2


def buishand_range_test(x, alpha = 0.05, sim = 20000):
    """
    This function checks homogeneity test using Pettitt, A. N. (1979) method.
    Input:
        x: a vector (list, numpy array or pandas series) data
        alpha: significance level (0.05 default)
        sim: no. of monte carlo simulation for p-value calculation
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p-value of the significance test
        z: normalized test statistics
        Tau: Kendall Tau
        s: Mann-Kendal's score
        var_s: Variance S
        slope: sen's slope
    Examples
    --------
      >>> import pyhomogeneity as hg
      >>> x = np.random.rand(1000)
      >>> trend,h,p,z,tau,s,var_s,slope = hm.pettitt_test(x, 0.05)
    """
    res = namedtuple('Buishand_Range_Test', ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope'])
    R, loc, h, p, mu1, mu22 = __test(__buishand_range, x, alpha = 0.05, sim = sim)

    return R, loc, h, p, mu1, mu2


def buishand_likelihood_ratio_test(x, alpha = 0.05, sim = 20000):
    """
    This function checks homogeneity test using Pettitt, A. N. (1979) method.
    Input:
        x: a vector (list, numpy array or pandas series) data
        alpha: significance level (0.05 default)
        sim: no. of monte carlo simulation for p-value calculation
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p-value of the significance test
        z: normalized test statistics
        Tau: Kendall Tau
        s: Mann-Kendal's score
        var_s: Variance S
        slope: sen's slope
    Examples
    --------
      >>> import pyhomogeneity as hg
      >>> x = np.random.rand(1000)
      >>> trend,h,p,z,tau,s,var_s,slope = hm.pettitt_test(x, 0.05)
    """
    res = namedtuple('Buishand_Likelihood_Ratio_Test', ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope'])
    V, loc, h, p, mu1, mu22 = __test(__buishand_lr, x, alpha = 0.05, sim = sim)

    return V, loc, h, p, mu1, mu2


def buishand_u_test(x, alpha = 0.05, sim = 20000):
    """
    This function checks homogeneity test using Pettitt, A. N. (1979) method.
    Input:
        x: a vector (list, numpy array or pandas series) data
        alpha: significance level (0.05 default)
        sim: no. of monte carlo simulation for p-value calculation
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p-value of the significance test
        z: normalized test statistics
        Tau: Kendall Tau
        s: Mann-Kendal's score
        var_s: Variance S
        slope: sen's slope
    Examples
    --------
      >>> import pyhomogeneity as hg
      >>> x = np.random.rand(1000)
      >>> trend,h,p,z,tau,s,var_s,slope = hm.pettitt_test(x, 0.05)
    """
    res = namedtuple('Buishand_U_Test', ['trend', 'h', 'p', 'z', 'Tau', 's', 'var_s', 'slope'])
    U, loc, h, p, mu1, mu2 = __test(__buishand_u, x, alpha = 0.05, sim = sim)

    return U, loc, h, p, mu1, mu2