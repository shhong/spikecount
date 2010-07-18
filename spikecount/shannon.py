from numpy import zeros, log

def plogp(p, epsilon):
  x = zeros(p.shape)
  q = p[p>=epsilon]
  x[p>=epsilon] = q * log(q)
  return x

def count1(r):
  N = int(r.max())
  p = zeros(N+1)
  
  for i in r:
    p[i] = p[i] + 1
  return p

def count2(r1, r2):
  L = r1.size
  N1, N2 = int(r1.max()), int(r2.max())
  p12 = zeros((N1+1, N2+1))

  for i in xrange(L):
    p12[r1[i],r2[i]] = p12[r1[i],r2[i]] + 1
  
  return p12
  
def entropy1(r):
  L = r.size
  p = count1(r)
  p = p/L
  epsilon = 1.0/L
  return -plogp(p, epsilon).sum()

def entropy2(r1, r2):
  L = r1.size
  p12 = count2(r1, r2)
  p12 = p12/L
  epsilon = 1.0/L
  return -plogp(p12, epsilon).sum()