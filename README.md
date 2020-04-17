# pyHomogeneity
A python package for homogeneity test.


## What is the Homogeneity Test ?
Currently, this package has 6 Homogeneity Tests functions. Brief description of functions are below:

1. **Pettitt test (*pettitt_test*):** 

2. **Standard Normal Homogeinity Test (SNHT) Test (*snht_test*):** 

3. **Buishand Q Test (*buishand_q_test*):**

4. **Buishand's Range Test (*buishand_range_test*):**

5. **Buishand's Likelihood Ration Test (*buishand_likelihood_ratio_test*):**

6. **Buishand U Test (*buishand_u_test*):** 

## Function details:

All Homogeneity test functions have almost similar input parameters. Those are:

- **x**:   a vector of data
- **alpha**: significance level (0.05 default)
- **sim**: No. of monte carlo simulation for p-value calculation.

And all Homogeneity tests return a named tuple which contained:

- **h**: True (if trend is present) or False (if trend is absence)
- **cp**: probable change point location index
- **p**: p value of the significance test
- **U/T/Q/R/V**: Test Statistics depand of test methods
- **avg**: mean values at before and after change point


## Dependencies

For the installation of `pyHomogeneity`, the following packages are required:
- [numpy](https://www.numpy.org/)
- [scipy](https://www.scipy.org/)

## Installation

You can install `pyHomogeneity` using pip. For Linux users

```python
sudo pip install pyhomogeneity
```

or, for Windows user

```python
pip install pyhomogeneity
```

Or you can clone the repo and install it:

```bash
git clone https://github.com/mmhs013/pyhomogeneity
cd pyhomogeneity
python setup.py install
```

## Tests

`pyHomogeneity` is automatically tested using `pytest` package on each commit [here](https://travis-ci.org/mmhs013/pyHomogeneity/), but the tests can be manually run:

```
pytest -v
```

## Usage

A quick example of `pyHomogeneity` usage is given below. Several more examples are provided [here]().

```python
import numpy as np
import pyhomogeneity as hg

# Data generation for analysis
data = np.random.rand(360,1)

result = hg.pettitt_test(data)
print(result)
```
Output are like this:
```python
Pettitt_Test(h=False, cp=89, p=0.1428, U=3811.0, avg=mean(mu1=0.5487521427805625, mu2=0.46884198890609463))
```
Whereas, the output is a named tuple, so you can call by name for specific result:
```python
print(result.cp)
print(result.avg.mu1)
```
or, you can directly unpack your results like this:
```python
h, cp, p, U, mu = hg.pettitt_test(x, 0.05)
```

## Contributions

`pyHomogeneity` is a community project and welcomes contributions. Additional information can be found in the [contribution guidelines](https://github.com/mmhs013/pyHomogeneity/blob/master/CONTRIBUTING.md)


## Code of Conduct

`pyHomogeneity` wishes to maintain a positive community. Additional details can be found in the [Code of Conduct](https://github.com/mmhs013/pyHomogeneity/blob/master/CODE_OF_CONDUCT.md)


## References

1. Alexandersson, H., 1986. A homogeneity test applied to precipitation data. Journal of climatology, 6(6), pp.661-675. doi:[10.1002/joc.3370060607](https://doi.org/10.1002/joc.3370060607)

2. Buishand, T.A., 1982. Some methods for testing the homogeneity of rainfall records. Journal of hydrology, 58(1-2), pp.11-27. doi:[10.1016/0022-1694(82)90066-X](https://doi.org/10.1016/0022-1694(82)90066-X)

3. Pettitt, A.N., 1979. A non‐parametric approach to the change‐point problem. Journal of the Royal Statistical Society: Series C (Applied Statistics), 28(2), pp.126-135. doi:[10.2307/2346729](https://doi.org/10.2307/2346729)

4. Pohlert, T., 2016. Package ‘trend’. Title Non-Parametric Trend Tests and Change-Point Detection.

5. Verstraeten, G., Poesen, J., Demarée, G. and Salles, C., 2006. Long‐term (105 years) variability in rain erosivity as derived from 10‐min rainfall depth data for Ukkel (Brussels, Belgium): Implications for assessing soil erosion rates. Journal of Geophysical Research: Atmospheres, 111(D22). doi:[10.1029/2006JD007169](https://doi.org/10.1029/2006JD007169)