import os.path as _p
import utils
from numpy import sqrt, fromfile, array, savetxt
from numpy import ones, zeros, convolve

import shannon

class Data(object):
  def __init__(self, data_path, c):
    import shutil
    
    self.data_path = data_path
    self.c = c
    self.output_path = _p.join('result', self.data_path)
    utils.mkdir_p(self.output_path)
    self.cgmdir = _p.join(self.data_path, 'cgm')
    self.spiketime_dir = _p.join(self.data_path, 'spiketime')
    
    self.single_data = utils.read_table(_p.join(self.data_path,'statid_correlation_mu_sigma2_urate.dat'))
    shutil.copyfile(_p.join(self.data_path,'statid_correlation_mu_sigma2_urate.dat'),
                    _p.join(self.output_path,'statid_correlation_mu_sigma2_urate.dat'))
    
    self.zero_firing = [i for i in self.single_data if self.single_data[i]['urate']<1e-8]
    self.pairs = utils.read_pairs(self.cgmdir)
    self.pair_data = [{'id': p} for p in self.pairs]
  
  def spiketime(self, i):
    return fromfile(_p.join(self.spiketime_dir, str(i)+'.spiketime.bin'))
  
  def rate_train(self, i, twait=1000.0, wsize=200.0, tstop = 1801000):    
    t = self.spiketime(i)-twait
    t = t[t>0]
    r = zeros(tstop-twait)
    r[t.astype(int)] = 1.0
    r = convolve(ones(wsize), r)[-r.size:-wsize]
    return r
  
  def compute_mean_rate(self):
    for d in self.pair_data:
      id1, id2 = d['id']
      d['rate'] = sqrt(self.single_data[id1]['urate']*self.single_data[id2]['urate'])*1e3 # in Hz
    return self.pair_data
  
  def write_pairs(self):
    stream = '\n'.join(' '.join(str(i) for i in p) for p in self.pairs)
    open(_p.join(self.output_path, 'pairs.txt'),'w').write(stream)
   
  def compute_agm(self, window):
    from scipy.signal import resample
    
    self.agm_window_shape = window.kind
    self.window_size = window.wsize
    
    filename='a-' + window.kind + str(window.wsize) + '.dat'
    print '\nAutocorrelation calculation'
    z = []
    for d in self.pair_data:
      p = d['id']
      acgm1 = fromfile(_p.join(self.cgmdir, str(p[0])+'.acgm.bin'))
      acgm2 = fromfile(_p.join(self.cgmdir, str(p[1])+'.acgm.bin'))
      print p[0], p[1]
      d['var'] = [(acgm1*window.window).sum(), (acgm2*window.window).sum()]
      z.append(d['var'])
    savetxt(_p.join(self.output_path,filename), array(z))
    return self.pair_data
    
  def compute_cgm(self, window):
    from scipy.signal import resample
    
    self.cgm_window_shape = window.kind
    
    filename= window.kind + str(window.wsize) + '.dat'
    print '\nCross-covariance calculation'
    z = []
    for d in self.pair_data:
      p = d['id']
      cgm    = fromfile(_p.join(self.cgmdir, '_'.join(str(i) for i in p) + '.cgm.bin'))/self.c
      cgmsta = fromfile(_p.join(self.cgmdir, '_'.join(str(i) for i in p) + '.cgmsta.bin'))
      cgmsta = resample(cgmsta, cgm.size)
      
      print p[0], p[1]
      d['cov']  = (cgm*window.window).sum()
      d['pred'] = (cgmsta*window.window).sum()
      z.append([d['cov'], d['pred']])
    savetxt(_p.join(self.output_path, filename), array(z))
    return self.pair_data
  
  def savetxt(self, sep=' '):
    z = []
    keys = ['id1', 'id2', 'c', 'rate', 'var1', 'var2', 'cov', 'pred']
    z.append(sep.join(keys))
    filename = '_'.join(['all',
                         self.agm_window_shape,
                         self.cgm_window_shape,
                         str(self.window_size)]) + '.dat'
    
    for d in self.pair_data:
      this_z = [d['id'][0],
                d['id'][1],
                self.c,
                d['rate'],
                d['var'][0],
                d['var'][1],
                d['cov'],
                d['pred']]
      this_z = sep.join([str(x) for x in this_z])
      z.append(this_z)
    
    open(_p.join(self.output_path, filename), 'w').write('\n'.join(z))
    
    
