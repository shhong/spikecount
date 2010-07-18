import sys
sys.path.append('..')

import unittest
import spikecount.utils as utils

class TestUtils(unittest.TestCase):
  def test_read_table(self):
    testfile = 'test_data/statid_correlation_mu_sigma2_urate.dat'
    self.assertEqual(str(utils.read_table(testfile)), "{0: {'mu': 0.0, 'c': 0.5, 'urate': 0.00068666666666699998, 'sigma2': 0.01}, 1: {'mu': 0.0, 'c': 0.5, 'urate': 0.0045558333333300003, 'sigma2': 0.020864197530899999}, 2: {'mu': 0.0, 'c': 0.5, 'urate': 0.00867638888889, 'sigma2': 0.035679012345699999}, 3: {'mu': 0.0, 'c': 0.5, 'urate': 0.0126605555556, 'sigma2': 0.054444444444399998}, 4: {'mu': 0.0, 'c': 0.5, 'urate': 0.016584722222200001, 'sigma2': 0.0771604938272}, 5: {'mu': 0.0, 'c': 0.5, 'urate': 0.0205044444444, 'sigma2': 0.103827160494}, 6: {'mu': 0.0, 'c': 0.5, 'urate': 0.024421666666699999, 'sigma2': 0.134444444444}, 7: {'mu': 0.0, 'c': 0.5, 'urate': 0.028336666666700001, 'sigma2': 0.169012345679}, 8: {'mu': 0.0, 'c': 0.5, 'urate': 0.032223888888900001, 'sigma2': 0.20753086419799999}, 9: {'mu': 0.0, 'c': 0.5, 'urate': 0.036155555555600002, 'sigma2': 0.25}}")
  
  def test_read_pairs(self):
    import os.path
    testdir = os.path.join('50','cgm')
    pairs = utils.read_pairs(testdir)
    self.assertEqual(pairs[0], (0,0))
  
  def test_triangle_window(self):
    import matplotlib.pyplot as pl
    c = utils.TimeWindow(width=200, wsize=200, kind='triangle')
    pl.plot(c.window,'.-')
    pl.show()
    self.assertEqual(c.window.size, 401)
    self.assertEqual(c.kind, 'triangle')
  
  def test_square_window(self):
    import matplotlib.pyplot as pl
    c = utils.TimeWindow(width=200, wsize=200, kind='square')
    pl.plot(c.window,'.-')
    pl.show()
    self.assertEqual(c.window.size, 401)
    self.assertEqual(c.kind, 'square')


if __name__ == '__main__':
  unittest.main()