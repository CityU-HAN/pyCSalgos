"""
Tests for generate.py
"""

# Author: Nicolae Cleju
# License: BSD 3 clause

import numpy
from numpy.testing import assert_equal
from numpy.testing import assert_array_equal
from numpy.testing import assert_array_almost_equal

from pyCSalgos.generate import make_sparse_coded_signal


def test_make_sparse_coded_signal():
    """ Tests make_sparse_coded_signal()"""

    n, N = 20, 30
    k = 5
    Ndata = 10
    # Parameterized test:
    for use_sklearn in [True,False]:
        yield subtest_make_sparse_coded_signal, n, N, k, Ndata, use_sklearn

def subtest_make_sparse_coded_signal(n,N,k,Ndata,use_sklearn):

    X, D, gamma, support = make_sparse_coded_signal(n, N, k, Ndata, use_sklearn)

    # check shapes
    print X.shape
    print (n, N)

    assert_equal(X.shape, (n, Ndata), "X shape mismatch")
    assert_equal(D.shape, (n, N), "D shape mismatch")
    assert_equal(gamma.shape, (N, Ndata), "gamma shape mismatch")
    assert_equal(support.shape, (k, Ndata), "support shape mismatch")

   # check multiplication
    assert_array_equal(X, numpy.dot(D, gamma))

    # check dictionary normalization
    assert_array_almost_equal(numpy.sqrt((D ** 2).sum(axis=0)),
                              numpy.ones(D.shape[1]))

    for i in range(Ndata):
        assert(numpy.all(gamma[support[:, i], i])) # check if all support is non-zero
        izero = numpy.setdiff1d(range(N), support[:, i])
        assert(not numpy.any(gamma[izero, i])) # check if all zeros are zero




