from numpy import zeros, log2, array, histogram, histogram2d, bincount

def plog2p(p, epsilon):
  x = zeros(p.shape)
  ind = (p>=epsilon)
  q = p[ind]
  x[ind] = q * log2(q)
  return x

def count1(u):
  umin = u.min()
  r = (u-u.min()).astype(int)
  N = r.max()
  p = bincount(r)
  return (p, (umin, umin+N))

def count1p(u):
  umin, umax = u.min(), u.max()
  p, b = histogram(u,umax-umin+1)
  return (p, (umin, umax))

def merge1(x):
  bmin = array([y[1][0] for y in x]).min()
  bmax = array([y[1][1] for y in x]).max()
  N = int(bmax-bmin)
  p = zeros(N+1)
  for y in x:
    i1 = y[1][0]-bmin
    i2 = y[1][1]-bmin+1
    p[i1:i2] = p[i1:i2] + y[0]
  return (p, (bmin, bmax))

def count2(u1, u2):
  umin1, umin2 = u1.min(), u2.min()
  r1, r2 = (u1-umin1).astype(int), (u2-umin2).astype(int)
  N1, N2 = r1.max(), r2.max()
  
  p12 = zeros((N1+1, N2+1))
  
  for i, re1 in enumerate(r1):
    j1 = re1
    j2 = r2[i]
    p12[j1,j2] = p12[j1,j2] + 1
  
  return (p12, ((umin1,umin1+N1),(umin2,umin2+N2)))

def count2p(u1, u2):
  umin1, umin2 = u1.min(), u2.min()
  umax1, umax2 = u1.max(), u2.max()
  p12, x, y = histogram2d(u1, u2, (umax1-umin1+1, umax2-umin2+1)) 
  
  return (p12, ((umin1,umax1),(umin2,umax2)))

def merge2(x):
  bmin1 = array([y[1][0][0] for y in x]).min()
  bmin2 = array([y[1][1][0] for y in x]).min()
  bmax1 = array([y[1][0][1] for y in x]).max()
  bmax2 = array([y[1][1][1] for y in x]).max()
  N1 = int(bmax1-bmin1)
  N2 = int(bmax2-bmin2)
  p = zeros((N1+1, N2+1))
  for y in x:
    imin1 = y[1][0][0]-bmin1
    imax1 = y[1][0][1]-bmin1+1
    imin2 = y[1][1][0]-bmin2
    imax2 = y[1][1][1]-bmin2+1
    p[imin1:imax1,imin2:imax2] = p[imin1:imax1,imin2:imax2] + y[0]
  return (p, ((bmin1, bmax1),(bmin2,bmax2)))

def entropy_from_count(p):
  N = float(p[0].sum())
  q = p[0]/N
  epsilon = 1.0/N
  return -plog2p(q, epsilon).sum()
  
def entropy1(r):
  p = count1(r)
  return entropy_from_count(p)

def entropy2(*r):
  if len(r) is 1:
    r1, r2 = r[0]
  else:
    r1, r2 = r
  p12 = count2p(r1, r2)
  return entropy_from_count(p12)

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

def mix_samples(p):
  from numpy import vstack, array
  N, L = len(p[0]), len(p)
  return vstack(p).T.reshape(N*L)
