from numpy import sqrt, dot, convolve, array

def normalized(x):
  return x/sqrt(dot(x,x))

class FTModel(object):
  def __init__(self, model_data):
    super(FTModel, self).__init__()
    self.params = model_data
    self.dt = self.params['dt']
    
    print "model parameters = ", self.params
  
  def spiketime(self, stim):
    import addahp
    v_linear = convolve(self.params['filter'], stim)[:stim.size]
    print "v_linear calculated."
    v = addahp.addahp(v_linear,
                      self.params['tau'], 
                      self.params['threshold'],
                      self.params['vpeak'],
                      self.params['peakahp'],
                      self.params['dt'])
    print "ahp added to v_linear."
    return array([i for i in range(1, v.size) if v[i]>=self.params['vpeak']])*self.dt
  


def main():
  from numpy import fromfile, blackman, diff
  from numpy import exp, arange
  import os
  
  print "initializing.."
  steps_per_ms = 5
  tstop = 1801000
  Dt = 1.0/steps_per_ms
  N = steps_per_ms*tstop
  twait = 1000
  tcorr = 5
  
  gain = sqrt(2.0*steps_per_ms/tcorr)
  mu = 0.0
  sigma = sqrt(0.169012345679)
  correlation = 0.5
  
  z = fromfile(os.path.join('stimulus', '3.stim.bin'))
  ztot = sigma*z
  print "stimulus loaded."
  
  prefilter = normalized(exp(-arange(0,200,Dt)/tcorr))
  filtered_stim = mu + convolve(prefilter, ztot)[:ztot.size]
  print "stimulus filtered and added mu"
  
  diffr = FTModel({'filter': normalized(diff(blackman(15*steps_per_ms+1))),
                   'threshold': 1.0,
                   'vpeak': 20,
                   'tau': 50.0,
                   'peakahp': 1.0,
                   'dt': Dt})
  
  tspikes = diffr.spiketime(filtered_stim)
  tspikes = tspikes[tspikes>twait]
  print tspikes
  tspikes.tofile("spiketime/16.spiketime.bin")


if __name__ == '__main__':
  main()
