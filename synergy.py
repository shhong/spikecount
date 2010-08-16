#!/usr/bin/env python
import spikecount
from spikecount.shannon import mix_samples

WSIZE = 200

def h2(x):
  from spikecount.shannon import bootstrap, entropy2
  scompare = bootstrap(entropy2, x[0], x[1], debug=False)['predict']
  return scompare

def h1(x):
  from spikecount.shannon import bootstrap, entropy1
  from numpy import array
  sx = bootstrap(entropy1, x[0])['predict']
  sy = bootstrap(entropy1, x[1])['predict']
  return array([sx, sy])

def shuffle1(r):
  from numpy import hstack
  N2 = r.size/2
  return hstack((r[N2:],r[:N2]))

def shuffle(r):
  return [r[0], shuffle1(r[1])]

def main(d, indlist):
  i1, i2 = indlist[0]
  j1, j2 = indlist[1]
  r_s1 = [d.rate_train(i, WSIZE) for i in [i1, i2]]
  r_s2 = [d.rate_train(j, WSIZE) for j in [j1, j2]]
  r_all = [mix_samples([r_s1[i], r_s2[i]]) for i in range(2)]
  
  ai_12, bi_12 = h2(r_all), (h2(r_s1) + h2(r_s2))/2.0
  ai_i, bi_i  = h1(r_all), (h1(r_s1) + h1(r_s2))/2.0
  mi_12 = ai_12 - bi_12
  mi_i = ai_i - bi_i
  
  r_s1_shuffled = shuffle(r_s1)
  r_s2_shuffled = shuffle(r_s2)
  r_all_shuffled = [mix_samples([r_s1_shuffled[i], r_s2_shuffled[i]]) for i in range(2)]
  mi_shuffle = h2(r_all_shuffled) - (h2(r_s1_shuffled) + h2(r_s2_shuffled))/2.0
  
  print i2, j2, mi_i[0], mi_i[1], mi_12, mi_shuffle, mi_12-mi_shuffle, mi_i.sum() - mi_shuffle, sum(bi_i)-bi_12, sum(ai_i)-ai_12
  
if __name__ == '__main__':
  import sys
  from numpy import loadtxt
  
  d = spikecount.Data(sys.argv[1], 0.5)
  inds = loadtxt(sys.argv[2], int)
  for i in xrange(inds.shape[0]-1):
    main(d, inds[i:i+2,])