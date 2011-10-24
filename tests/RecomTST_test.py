# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 21:17:49 2011

@author: Nic

Test RecommendedTST algorithm
"""

import numpy as np
import numpy.linalg
import scipy.io
import unittest
from pyCSalgos.RecomTST.RecommendedTST import RecommendedTST

class RecomTSTresults(unittest.TestCase):
  def testResults(self):
    mdict = scipy.io.loadmat('RecomTSTtestdata.mat')
    
    # A = system matrix
    # Y = matrix with measurements (on columns)
    # X0 = matrix with initial solutions (on columns)
    # Eps = vector with epsilon
    # Xr = matrix with correct solutions (on columns)
    for A,Y,X0,Tol,Xr in zip(mdict['cellA'].squeeze(),mdict['cellY'].squeeze(),mdict['cellX0'].squeeze(),mdict['cellTol'].squeeze(),mdict['cellXr'].squeeze()):
      for i in np.arange(Y.shape[1]):
        xr = RecommendedTST(A, Y[:,i], nsweep=300, tol=Tol.squeeze()[i], xinitial=X0[:,i])
        
        # check if found solution is the same as the correct cslution
        diff = numpy.linalg.norm(xr - Xr[:,i])
        self.assertTrue(diff < 1e-12)
        #err1 = numpy.linalg.norm(Y[:,i] - np.dot(A,xr))
        #err2 = numpy.linalg.norm(Y[:,i] - np.dot(A,Xr[:,i]))
        #norm1 = numpy.linalg.norm(xr,1)
        #norm2 = numpy.linalg.norm(Xr[:,i],1)
        #print 'diff = ',diff
        #print 'err1 = ',err1
        #print 'err2 = ',err2
        #print 'norm1 = ',norm1
        #print 'norm2 = ',norm2
        #
        # It seems Matlab's linsolve and scipy solve are slightly different
        # Therefore make a more robust condition:
        #  OK;    if   solutions are close enough (diff < 1e-6)
        #              or
        #              (
        #               they fulfill the constraint close enough (differr < 1e-6)
        #                 and
        #               Python solution has l1 norm no more than 1e-6 larger as the reference solution
        #                 (i.e. either norm1 < norm2   or   norm1>norm2 not by more than 1e-6)
        #              )
        #        
        #  ERROR: else
        #differr  = abs((err1 - err2))
        #diffnorm = norm1 - norm2  # intentionately no abs(), since norm1 < norm2 is good
        #if diff < 1e-6 or (differr < 1e-6 and (diffnorm < 1e-6)):
        #  isok = True
        #else:
        #  isok = False
        #if not isok:
        #  print "should raise"
        #  #self.assertTrue(isok)
        #self.assertTrue(isok)
  
if __name__ == "__main__":
    unittest.main(verbosity=2)    
    #suite = unittest.TestLoader().loadTestsFromTestCase(CompareResults)
    #unittest.TextTestRunner(verbosity=2).run(suite)    