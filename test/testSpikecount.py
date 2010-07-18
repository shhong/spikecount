import sys
sys.path.append('..')

import unittest
import spikecount

import os
testdata = 'test_data/50'
d = spikecount.Data(testdata, 0.5)

class TestUtils(unittest.TestCase):
  def test_Data_init(self):
    self.assertEqual(os.listdir('.').count('result'), 1)
    self.assertEqual(os.listdir('result').count('50'), 1)
    self.assertEqual(str(d.single_data), "{0: {'mu': 0.0, 'c': 0.5, 'urate': 0.00068666666666699998, 'sigma2': 0.01}, 1: {'mu': 0.0, 'c': 0.5, 'urate': 0.0045558333333300003, 'sigma2': 0.020864197530899999}, 2: {'mu': 0.0, 'c': 0.5, 'urate': 0.00867638888889, 'sigma2': 0.035679012345699999}, 3: {'mu': 0.0, 'c': 0.5, 'urate': 0.0126605555556, 'sigma2': 0.054444444444399998}, 4: {'mu': 0.0, 'c': 0.5, 'urate': 0.016584722222200001, 'sigma2': 0.0771604938272}, 5: {'mu': 0.0, 'c': 0.5, 'urate': 0.0205044444444, 'sigma2': 0.103827160494}, 6: {'mu': 0.0, 'c': 0.5, 'urate': 0.024421666666699999, 'sigma2': 0.134444444444}, 7: {'mu': 0.0, 'c': 0.5, 'urate': 0.028336666666700001, 'sigma2': 0.169012345679}, 8: {'mu': 0.0, 'c': 0.5, 'urate': 0.032223888888900001, 'sigma2': 0.20753086419799999}, 9: {'mu': 0.0, 'c': 0.5, 'urate': 0.036155555555600002, 'sigma2': 0.25}}")
    self.assertEqual(d.pairs[0], (0, 0))
  
  def test_create_pair_data(self):
    self.assertEqual(d.pair_data[0]['id'], (0, 0))
    self.assertEqual(d.pair_data[0]['rate'], 0.68666666666699994)
  
  def test_Data_mean_rate(self):
    p = d.compute_mean_rate()
    self.assertEqual(p[2], {'rate': 8.6763888888899992, 'id': (2, 2)})
  
  def test_write_pairs(self):
    d.write_pairs()
    self.assertEqual(os.listdir('result/50').count('pairs.txt'), 1)
  
  def test_compute_agm(self):
    import spikecount.utils as utils
    w = utils.TimeWindow(width=200, wsize=200, kind='triangle')
    x = d.compute_agm(w)
    self.assertEqual(os.listdir('result/50').count('a-triangle200.dat'), 1)
    for k in x: print k
  
  def test_compute_cgm(self):
    import spikecount.utils as utils
    w = utils.TimeWindow(width=200, wsize=200, kind='triangle')
    x = d.compute_cgm(w)
    self.assertEqual(os.listdir('result/50').count('triangle200.dat'), 1)
    for k in x: print k
  
  def test_savetxt(self):
    import spikecount.utils as utils
    w = utils.TimeWindow(width=200, wsize=200, kind='triangle')
    temp = d.compute_agm(w)
    temp = d.compute_cgm(w)
    d.savetxt()
    self.assertEqual(os.listdir('result/50').count('all_triangle_triangle_200.dat'), 1)
    x = open('result/50/all_triangle_triangle_200.dat','r').read().split('\n')
    self.assertEqual(len(x), 11)
      
if __name__ == '__main__':
  unittest.main()
