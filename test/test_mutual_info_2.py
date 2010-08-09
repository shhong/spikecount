import sys
sys.path.append('..')

import unittest
import spikecount
import os

import matplotlib.pyplot as pl
from numpy.random import randn

def generate_gaussian(N=10000, sigma = 75, offset=300):
  x = randn(N)*sigma + offset
  x[x<0] = 0.0
  x = x.astype(int)
  return x

def generate_correlated_gaussian(N=10000, sigma=75, offset=300, c = 0.3):
  from numpy import sqrt
  z = [randn(N)*sigma + offset for i in xrange(3)]
  cc = [z[i]*sqrt(1-c) + z[2]*sqrt(c) for i in xrange(2)]
  for x in cc:
    x[x<0] = 0.0
    x = x.astype(int)
  return cc

class TestUtils(unittest.TestCase):
  
  def test_count1(self):
    from spikecount.shannon import count1, count1p
    
    x  = generate_gaussian(sigma=5)
    c, delta = count1(x)
    cp, deltap = count1p(x)
    print c, delta
    print cp, deltap
#    pl.plot(c)
#    pl.show()

  def test_count2(self):
    from spikecount.shannon import count2, count2p

    x  = generate_gaussian(sigma=10)
    y = generate_gaussian(sigma=10)
    c, delta2 = count2(x, y)
    cp, delta2p = count2p(x, y)
    print c[:,10]
    print cp[:,10]
    print c[:,15]
    print cp[:,15]
    print delta2, delta2p
#    pl.figure()
#    pl.imshow(c)
#    pl.figure()
#    pl.imshow(cp)
#    pl.show()
  
  def test_entropy1(self):
    from spikecount.shannon import entropy1
    from numpy import pi, e, log2
    
    print
    print "Test 1d entroy."
    x = generate_gaussian(sigma = 5)
    print entropy1(x), entropy1(x)-log2(x.std()), log2(2*pi*e)/2
    
    x = generate_gaussian(sigma = 30)
    print entropy1(x), entropy1(x)-log2(x.std()), log2(2*pi*e)/2
    
    x = generate_gaussian(sigma = 75)
    print entropy1(x), entropy1(x)-log2(x.std()), log2(2*pi*e)/2

  def test_entropy2(self):
    from spikecount.shannon import entropy2
    from numpy import pi, e, log2

    print
    print "Test 2d entropy."
    x = generate_gaussian(sigma = 2)
    y = generate_gaussian(sigma = 2)
    print entropy2(x,y), entropy2(x,y)-log2(x.std())-log2(y.std()), log2(2*pi*e)

    x = generate_gaussian(sigma = 10)
    y = generate_gaussian(sigma = 10)
    print entropy2(x,y), entropy2(x,y)-log2(x.std())-log2(y.std()), log2(2*pi*e)

    x = generate_gaussian(sigma = 20)
    y = generate_gaussian(sigma = 20)
    print entropy2(x,y), entropy2(x,y)-log2(x.std())-log2(y.std()), log2(2*pi*e)
    
  def test_sampling_bias1(self):
    from spikecount.shannon import entropy1, bootstrap
    from numpy import pi, e, log2
    from numpy import array, polyfit

    print 
    print "Sampling bias 1d"
    x = generate_gaussian(sigma = 10, N=30000)
    N = x.size
    N = array([N/2**i for i in xrange(5)])
    print N, '\n'
    ss = []
    for i, n in enumerate(N):
      y = x[:n*(2**i)].reshape((2**i, n))
      smean = array([entropy1(z) for z in y]).mean()
      ss.append(smean)
      print n, smean, smean - log2(x.std()), log2(2*pi*e)/2
      
#    pl.plot(1.0/N, ss)
#    pl.show()
    
    sr = polyfit(1.0/N, ss, 1)
    s0 = sr[-1]
    print s0, s0-log2(x.std()), log2(2*pi*e)/2
    
    scompare = bootstrap(entropy1, x, debug=False)['predict']
    print scompare, scompare - log2(x.std()), log2(2*pi*e)/2

  def test_sampling_bias2(self):
    from spikecount.shannon import entropy2, bootstrap
    from numpy import pi, e, log2
    from numpy import array, polyfit

    print 
    print "Sampling bias 2d"
    x = generate_gaussian(sigma = 5, N=100000)
    y = generate_gaussian(sigma = 5, N=100000)
    
    print entropy2(x,y), entropy2(x,y)-log2(x.std())-log2(y.std()), log2(2*pi*e)
    
    scompare = bootstrap(entropy2, x, y, debug=False)['predict']
    print scompare, scompare - log2(x.std()) - log2(y.std()), log2(2*pi*e)

  def test_correlation(self):
    from spikecount.shannon import entropy1, entropy2, bootstrap
    from numpy import pi, e, log2
    from numpy import array, polyfit
    
    c = 0.3
    x, y = generate_correlated_gaussian(sigma=4, N=100000, c = c)
        
    scompare = bootstrap(entropy2, x, y, debug=False)['predict']
    sx = bootstrap(entropy1, x)['predict']
    sy = bootstrap(entropy1, y)['predict']
    
    print 'Test entropy'
    print scompare, scompare - log2(x.std()) - log2(y.std()), log2(2*pi*e)
    print sx, sx - log2(x.std()), log2(2*pi*e)/2
    print sy, sy - log2(y.std()), log2(2*pi*e)/2
    
    print 'Mutual info'
    print sx+sy-scompare, -log2(1-c**2)/2
    
  def test_real_data(self):
    from spikecount.shannon import bootstrap, entropy2, entropy1, log2

    print "\nTest with the real data."
    d = spikecount.Data('test_data/50', 0.5)
    r1 = d.rate_train(11, wsize=250)
    r2 = d.rate_train(12, wsize=250)
#    pl.subplot(2,1,1)
#    pl.plot(r1)
#    pl.subplot(2,1,2)
#    pl.plot(r2)
#    pl.show()
    print "The rate trains are ready."
    scompare = bootstrap(entropy2, r1, r2, debug=False)['predict']
    sx = bootstrap(entropy1, r1)['predict']
    sy = bootstrap(entropy1, r2)['predict']
    print "T = 250 ms"
    print sx+sy-scompare, -log2(1-0.5**2)/2

    print "T = 1000 ms"
    r1 = d.rate_train(11, wsize=1000)
    r2 = d.rate_train(12, wsize=1000)
    scompare = bootstrap(entropy2, r1, r2, debug=False)['predict']
    sx = bootstrap(entropy1, r1)['predict']
    sy = bootstrap(entropy1, r2)['predict']
    print sx+sy-scompare, -log2(1-0.5**2)/2

  def test_mix_samples(self):
    from spikecount.shannon import mix_samples, entropy2, entropy1, log2, bootstrap
    from numpy import hstack
    print "\nTest mixing samples."
    c = 0.3
    x1, y1 = generate_correlated_gaussian(sigma=5, N=100000, c = c)
    x2, y2 = generate_correlated_gaussian(sigma=10, N=100000, c = c)
    print "Well mixed samples"
    z1 = mix_samples([x1,x2])
    z2 = mix_samples([y1,y2])
    print entropy1(z1) + entropy1(z2) - entropy2(z1, z2), -log2(1-c**2)/2
    print "Datasets pasted side by side"
    z1 = hstack((x1, x2))
    z2 = hstack((y1, y2))
    print entropy1(z1) + entropy1(z2) - entropy2(z1, z2), -log2(1-c**2)/2    
    
    print "Now testing shifting and mixing samples"
    x1, y1 = generate_correlated_gaussian(sigma=4, N=100000, c = c)
    x2, y2 = generate_correlated_gaussian(sigma=4, N=100000, c = c)
    z1 = mix_samples((x1,x2+1000))
    z2 = mix_samples((y1,y2+1000))
    print bootstrap(entropy1, z1)['predict'] + bootstrap(entropy1, z2)['predict'] - bootstrap(entropy2, z1, z2)['predict'], -log2(1-c**2)/2    
    print bootstrap(entropy1, x2)['predict'] + bootstrap(entropy1, y2)['predict'] - bootstrap(entropy2, x2, y2)['predict'], -log2(1-c**2)/2    
    
if __name__ == '__main__':
  unittest.main()
