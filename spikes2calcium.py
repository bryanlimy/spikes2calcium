import warnings
import numpy as np

warnings.filterwarnings("ignore", category=RuntimeWarning)


def _times2calcium(spike_times: np.ndarray, duration: float, frame_rate: float,
                   tau_onset: float, amp1: float, tau1: float, amp2: float,
                   tau2: float):
  """ Convert spike time to calcium signal
  Reference: https://github.com/HelmchenLab/CalciumSim/blob/master/modelCalcium/etc/spkTimes2Calcium.m
  Args:
    spike_times: np.ndarray, 1D array of spike times in second
    duration: int, duration of the trial in second
    frame_rate: float, the frame rate of the recordings
  """
  if len(spike_times.shape) == 1:
    spike_times = np.expand_dims(spike_times, axis=-1)
  tau = np.arange(start=0, stop=duration, step=1 / frame_rate)
  diff = -(tau - spike_times)
  trace = np.multiply(1 - np.exp(diff / tau_onset),
                      amp1 * np.exp(diff / tau1) + amp2 * np.exp(diff / tau2))
  trace = np.nan_to_num(np.where(tau < spike_times, 0, trace))
  return np.sum(trace, axis=0)


def spikes2calcium(spike_trains: np.ndarray,
                   frame_rate: float,
                   tau_onset: float = 0.01,
                   amp1: float = 2.0,
                   tau1: float = 0.5,
                   amp2: float = 0,
                   tau2: float = 0,
                   snr: float = 10.0):
  """ Convolve spike trains to calcium-like traces
  Args:
    spike_trains: np.ndarray, spike trains in shape (num. neurons, time-steps)
    frame_rate: float, the frame rate of the recording
    tau_onset: float,
    amp1: float, single AP amplitude dF/F
    tau1: float, indicator decay time in s
    amp2: float, second amplitude for double-exp decay
    tau2: float, indicator decay time in s for second exponential
    snr: float, signal-to-noise ratio
  Returns:
    traces: np.ndarray, calcium-like traces in shape (num. neurons, time-steps)
  """
  assert len(spike_trains.shape) == 2, \
    f'spike_trains should have format (num. neurons, time-steps)'
  traces = np.zeros(shape=spike_trains.shape, dtype=np.float32)
  for i in range(spike_trains.shape[0]):
    spike_times = np.nonzero(spike_trains[i])[0] / frame_rate
    traces[i] = _times2calcium(spike_times=spike_times,
                               duration=spike_trains.shape[1] / frame_rate,
                               frame_rate=frame_rate,
                               tau_onset=tau_onset,
                               amp1=amp1,
                               tau1=tau1,
                               amp2=amp2,
                               tau2=tau2)
  # add noise to signals
  peak = amp1 * ((tau1 / tau_onset) * np.power(
      (tau1 / tau_onset) + 1, -((tau_onset / tau1) + 1)))
  noise = (peak / snr) * np.random.randn(*traces.shape)
  traces += noise
  return traces
