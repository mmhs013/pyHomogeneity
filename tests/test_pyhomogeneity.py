"""In this unit test file, we check the accuracy of all functions with generated data and compare the results with known results.
"""


import os
import pytest
import numpy as np
import pyhomogeneity as hg

@pytest.fixture
def sample_data():
    # Generate arbitrary 360 data
    sample_data = np.array([ 32.,  20.,  25., 189., 240., 193., 379., 278., 301.,   0.,   0.,
        82.,   0.,   4.,  np.nan,  np.nan, 121., 234., 360., 262., 120.,  30.,
        11.,   1.,   7.,   3.,  31.,  31., 355., 102., 248., 274., 308.,
        np.nan,   5.,  26.,  11.,  16.,   6.,  48., 388., 539., 431., 272.,
       404., 186.,   0.,   2.,   0.,   4.,   1.,  54., 272., 459., 235.,
       164., 365., 135.,   2.,  np.nan,  np.nan,   4.,   0., 128., 210., 163.,
       446., 225., 462., 467.,  19.,  13.,   0.,   3.,  17., 132., 178.,
       338., 525., 623., 145.,  31.,  19.,   3.,   0.,  29.,  25.,  87.,
       259., 756., 486., 180., 292.,  43.,  92.,   1.,   0.,  16.,   2.,
         0., 130., 253., 594., 111., 273.,  30.,   0.,   4.,   0.,  27.,
        24.,  41., 292., 378., 499., 265., 320., 227.,   4.,   0.,   4.,
        14.,   8.,  48., 416., 240., 404., 207., 733., 105.,   0., 112.,
         0.,  14.,   0.,  30., 140., 202., 289., 159., 424., 106.,   3.,
         0.,  65.,   3.,  14.,  58., 268., 466., 432., 266., 240.,  95.,
         1.,   0.,  10.,  26.,   4., 114.,  94., 289., 173., 208., 263.,
       156.,   5.,   0.,  16.,  16.,  14.,   0., 111., 475., 534., 432.,
       471., 117.,  70.,   1.,   3.,  28.,   7., 401., 184., 283., 338.,
       171., 335., 176.,   0.,   0.,  10.,  11.,   9., 140., 102., 208.,
       298., 245., 220.,  29.,   2.,  27.,  10.,  13.,  26.,  84., 143.,
       367., 749., 563., 283., 353.,  10.,   0.,   0.,   0.,   0.,   9.,
       246., 265., 343., 429., 168., 133.,  17.,   0.,  18.,  35.,  76.,
       158., 272., 250., 190., 289., 466.,  84.,   0.,   0.,   0.,   0.,
         0.,  22., 217., 299., 185., 115., 344., 203.,   8.,  np.nan,  np.nan,
         0.,   5., 284., 123., 254., 476., 496., 326.,  27.,  20.,   0.,
         4.,  53.,  72., 113., 214., 364., 219., 220., 156., 264.,   0.,
        13.,   0.,   0.,  45.,  90., 137., 638., 529., 261., 206., 251.,
         0.,   0.,   5.,   9.,  58.,  72., 138., 130., 471., 328., 356.,
       523.,   0.,   1.,   0.,   0.,  12., 143., 193., 184., 192., 138.,
       174.,  69.,   1.,   0.,   0.,  18.,  25.,  28.,  92., 732., 320.,
       256., 302., 131.,  15.,   0.,  27.,   0.,  22.,  20., 213., 393.,
       474., 374., 109., 159.,   0.,   0.,   0.,   3.,   3.,  49., 205.,
       128., 194., 570., 169.,  89.,   0.,   0.,   0.,   0.,   0.,  26.,
       185., 286.,  92., 225., 244., 190.,   3.,  20.])
    return sample_data


def test_pettitt_test(sample_data):
    res = hg.pettitt_test(sample_data)
#    assert res.h == False
    assert res.cp == 298
#    assert res.p == 0.7332886357063501
    assert res.U == 2716.0
    assert res.avg.mu1 == 157.87285223367698
    assert res.avg.mu2 == 120.93548387096774
    

def test_snht_test(sample_data):
    res = hg.snht_test(sample_data, sim=None)
    assert res.h == None
    assert res.cp == 298
    assert res.p == None
    assert res.T == 2.4426594259172947
    assert res.avg.mu1 == 157.87285223367698
    assert res.avg.mu2 == 120.93548387096774
    

def test_buishand_q_test(sample_data):
    res = hg.buishand_q_test(sample_data, sim=None)
    assert res.h == None
    assert res.cp == 298
    assert res.p == None
    assert res.Q == 0.5955457285563376
    assert res.avg.mu1 == 157.87285223367698
    assert res.avg.mu2 == 120.93548387096774
    
    
def test_buishand_range_test(sample_data):
    res = hg.buishand_range_test(sample_data, sim=None)
    assert res.h == None
    assert res.cp == 298
    assert res.p == None
    assert res.R == 0.9893156056266303
    assert res.avg.mu1 == 157.87285223367698
    assert res.avg.mu2 == 120.93548387096774
    
    
def test_buishand_likelihood_ratio_test(sample_data):
    res = hg.buishand_likelihood_ratio_test(sample_data, sim=None)
    assert res.h == None
    assert res.cp == 298c
    assert res.p == None
    assert res.V == 0.08330290132452312
    assert res.avg.mu1 == 157.87285223367698
    assert res.avg.mu2 == 120.93548387096774
    
    
def test_buishand_u_test(sample_data):
    res = hg.buishand_u_test(sample_data, sim=None)
    assert res.h == None
    assert res.cp == 298
    assert res.p == None
    assert res.U == 0.0644043126990563
    assert res.avg.mu1 == 157.87285223367698
    assert res.avg.mu2 == 120.93548387096774