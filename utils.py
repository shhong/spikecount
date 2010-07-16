def mkdir_p(x):
  from os import mkdir
  import os.path as _p
  dirs = x.split(_p.sep)
  for i, d in enumerate(dirs):
    dd = _p.join(*dirs[:i+1])
    if not _p.exists(dd):
      mkdir(dd)

def read_table(filename, sep=' '): 
  f = open(filename, 'r')
  header = f.readline().strip()
  col_names = header.split(sep)
  data = {}
  for line in f.readlines():
    this_data = {}
    dd = line.strip().split(sep)
    for i, col in enumerate(col_names[1:]):
      this_data[col] = float(dd[i+1])
    data[int(dd[0])] = this_data
  return data

def read_pairs(path):
  import os
  pairs = [tuple(x[:-8].split('_')) for x in os.listdir(path) if x.endswith('.cgm.bin')]
  pairs = [(int(x[0]), int(x[1])) for x in pairs]
  return pairs

class TimeWindow(object):
  def __init__(self, **kwargs):
    self.wsize = kwargs['wsize']
    self.width = kwargs['width']
    self.kind = kwargs['kind']
    eval('self.make_'+ self.kind +'()')
  
  def make_triangle(self):
    from numpy import zeros, convolve
    thetaT = zeros(self.width+1)
    thetaT[:int(self.wsize)] = 1.0
    self.window = convolve(thetaT[::-1], thetaT)
  
  def make_square(self):
    from numpy import zeros
    self.window = zeros(2*self.width+1)
    self.window[self.width-self.wsize:self.width+self.wsize+1]=1.0
    