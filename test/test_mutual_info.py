import sys
sys.path.append('..')

import unittest
import spikecount

import os
testdata = 'test_data/50'
d = spikecount.Data(testdata, 0.5)

class TestUtils(unittest.TestCase):
  
  def test_load_spiketime(self):
    self.assertEqual(d.spiketime(5)[0], 1.04620000e+03)
  
  def test_rate_train(self):
    import matplotlib.pyplot as pl
    wsize = 2000
    r = d.rate_train(5, wsize=wsize)
#    pl.plot(r[:100000])
#    pl.show()
    t = d.spiketime(5)-1000
    self.assertEqual(r.size, 1800000-wsize)
    self.assertEqual(r[0],(t<=wsize).sum())
  
  def test_mutual_info(self):
    import matplotlib.pyplot as pl
    wsize = 2000
    r = d.rate_train(5, wsize=wsize)
    #pl.plot(r[:100000])
    #pl.hist(r,100)
    pl.show()
    print r.max()


if __name__ == '__main__':
  unittest.main()
