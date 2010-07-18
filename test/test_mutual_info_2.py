import sys
sys.path.append('..')

import unittest
import spikecount

import os
testdata = 'test_data/50'
d = spikecount.Data(testdata, 0.5)

import matplotlib.pyplot as pl
from numpy.random import randn

def generate_gaussian(N=10000, sigma = 75, offset=300):
  x = randn(N)*sigma + offset
  x[x<0] = 0.0
  x = x.astype(int)
  return x

class TestUtils(unittest.TestCase):
  
  def test_count1(self):
    from spikecount.shannon import count1
    
    x  = generate_gaussian()
    c = count1(x)
    pl.plot(c)
    pl.show()

  def test_count2(self):
    from spikecount.shannon import count2

    x  = generate_gaussian()
    y = generate_gaussian()
    c = count2(x, y)
    pl.imshow(c)
    pl.show()
  
  def test_entropy1(self):
    from spikecount.shannon import entropy1
    from numpy import pi, e, log
    
    print
    x = generate_gaussian(sigma = 5)
    print entropy1(x), entropy1(x)-log(x.std()), log(2*pi*e)/2
    
    x = generate_gaussian(sigma = 30)
    print entropy1(x), entropy1(x)-log(x.std()), log(2*pi*e)/2
    
    x = generate_gaussian(sigma = 75)
    print entropy1(x), entropy1(x)-log(x.std()), log(2*pi*e)/2

  def test_entropy2(self):
    from spikecount.shannon import entropy2
    from numpy import pi, e, log

    print
    x = generate_gaussian(sigma = 2)
    y = generate_gaussian(sigma = 2)
    print entropy2(x,y), entropy2(x,y)-log(x.std())-log(y.std()), log(2*pi*e)

    x = generate_gaussian(sigma = 10)
    y = generate_gaussian(sigma = 10)
    print entropy2(x,y), entropy2(x,y)-log(x.std())-log(y.std()), log(2*pi*e)

    x = generate_gaussian(sigma = 20)
    y = generate_gaussian(sigma = 20)
    print entropy2(x,y), entropy2(x,y)-log(x.std())-log(y.std()), log(2*pi*e)



if __name__ == '__main__':
  unittest.main()
