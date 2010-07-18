from numpy import zeros, log

def plogp(p, epsilon):
  x = zeros(p.shape)
  ind = (p>=epsilon)
  q = p[ind]
  x[ind] = q * log(q)
  return x

def count1(u):
  r = u-u.min()
  N = int(r.max())
  p = zeros(N+1)
  
  for i in r:
    j = int(float(i))
    p[j] = p[j] + 1
  return (p, 1.0)

def count2(u1, u2):
  r1, r2 = u1-u1.min(), u2-u2.min()
  N1, N2 = int(r1.max()), int(r2.max())
  
  p12 = zeros((N1+1, N2+1))
  
  for i, re1 in enumerate(r1):
    j1 = int(re1)
    j2 = int(r2[i])
    p12[j1,j2] = p12[j1,j2] + 1
  
  return (p12, 1.0)
  
def entropy1(r):
  L = r.size
  p, delta = count1(r)
  p = p/L
  epsilon = 1.0/L
  return -plogp(p, epsilon).sum()

def entropy2(*r):
  if len(r) is 1:
    r1, r2 = r[0]
  else:
    r1, r2 = r
  L = r1.size
  p12, delta2 = count2(r1, r2)
  p12 = p12/L
  epsilon = 1.0/L
  return -plogp(p12, epsilon).sum()

def bootstrap(*args, **kwargs):
  from numpy import array, polyfit
  default = {'factors': (1, 0.5, 0.25, 0.125), 'debug':False}
  for k in kwargs: default[k] = kwargs[k]
  sfunc = args[0]
  data = args[1:]
  N = data[0].size
  block_sizes = array([int(N*f) for f in default['factors']])
  if default['debug']: print block_sizes
  ss = []
  for n in block_sizes:
    nblocks = N/n
    blocked_data = [[d[i*n:(i+1)*n] for d in data] for i in xrange(nblocks)]  
    smean = array([sfunc(*bd) for bd in blocked_data]).mean()
    ss.append(smean)
  if default['debug']: print ss
  sr = polyfit(1.0/array(block_sizes), array(ss), 2)
  return {'predict':sr[-1], 'samples':ss}
