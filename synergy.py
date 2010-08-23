#!/usr/bin/env python
import spikecount
from spikecount.shannon import mix_samples

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

def print_header():
  print 'index1', 'index2', 'mi1', 'mi2', 'miall', 'mishuffle', 'minoise', 'misignal', 'micondition', 'minocondition'
  

def main(d, indlist, wsize=200):
  i1, i2 = indlist[0]
  j1, j2 = indlist[1]
  r_s1 = [d.rate_train(i, wsize) for i in [i1, i2]] # R1, R2 for stim 1
  r_s2 = [d.rate_train(j, wsize) for j in [j1, j2]] # R1, R2 for stim 2
  r_all = [mix_samples([r_s1[i], r_s2[i]]) for i in range(2)] # R1, R2 for all the stim
  
  ai_12, bi_12 = h2(r_all), (h2(r_s1) + h2(r_s2))/2.0 # H(R1,R2), {H(R1, R2|s1) + H(R1, R2|s2)}/2
  ai_i, bi_i  = h1(r_all), (h1(r_s1) + h1(r_s2))/2.0 # H(Ri), {H(Ri|s1) + H(Ri|s2)}/2
  mi_12 = ai_12 - bi_12 # H(R1,R2) - <H(R1,R2|s)>_s = I(S; R1,R2)
  mi_i = ai_i - bi_i # H(Ri) - <H(Ri|s)>_s = I(S; Ri)
  
  r_s1_shuffled = shuffle(r_s1) # R1, Rs for stim1
  r_s2_shuffled = shuffle(r_s2) # R1, Rs for stim2
  r_all_shuffled = [mix_samples([r_s1_shuffled[i], r_s2_shuffled[i]]) for i in range(2)] # R1, Rs for all the stim
  mi_shuffle = h2(r_all_shuffled) - (h2(r_s1_shuffled) + h2(r_s2_shuffled))/2.0 # H(R1,Rs) - <H(R1, Rs|si)>_i = I(S; R1,Rs) = I_shuffle(S; R1,R2)
  
  # First, index 1 and 2
  # I(S; R1), I(S; R2)
  # I(S; R1,R2), I_shuffle(S; R1,R2)
  # I(S; R1,R2) - I_shuffle(S; R1,R2) = I_noise
  # I(S; R1) + I(S; R2) - I_shuffle(S; R1,R2) = I_signal
  # <H(R1|s)>_s + <H(R2|s)>_s - <H(R1,R2|s)>_s = <I(R1;R2|s)>_s
  # H(R1) + H(R2) - H(R1,R2) = I(R1;R2)
  print i2 , j2, mi_i[0], mi_i[1], mi_12, mi_shuffle, mi_12-mi_shuffle, mi_i.sum() - mi_shuffle, bi_i.sum()-bi_12, ai_i.sum()-ai_12
  
if __name__ == '__main__':
  import sys
  from numpy import loadtxt
  
  d = spikecount.Data(sys.argv[1], 0.3)
  inds = loadtxt(sys.argv[2], int)
  if len(sys.argv)>3:
    WSIZE = int(sys.argv[3])
  else:
    WSIZE = 200
  print_header()
  for i in xrange(inds.shape[0]-1):
    main(d, inds[i:i+2,], wsize=WSIZE)