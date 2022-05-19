import os
import platform
import matplotlib
import typing as t
import numpy as np
from math import ceil
import matplotlib.pyplot as plt

if platform.system() == 'Darwin':
  matplotlib.use('TkAgg')


def generate_spike_trains(firing_rate: float, duration: int, num_neuorns: int,
                          frame_rate: float) -> np.ndarray:
  spike_trains = np.random.rand(num_neuorns, ceil(duration * frame_rate))
  spike_trains = spike_trains < (firing_rate / frame_rate)
  return spike_trains.astype(np.float32)


def _plot_trace(axis: matplotlib.axes.Axes,
                signal: np.ndarray,
                spike: np.ndarray,
                color: str,
                linestyle: str = '-'):
  s_min, s_max = np.min(signal), np.max(signal)
  axis.plot(signal, color=color, linewidth=1, linestyle=linestyle)
  spike_times = np.nonzero(spike)[0]
  axis.scatter(spike_times,
               np.full(spike_times.shape, fill_value=s_min),
               marker='|',
               s=15,
               linewidths=1.5,
               color='#212529')
  yticks = np.linspace(s_min * 0.9, s_max, num=3)
  axis.set_yticks(yticks)
  axis.set_yticklabels(yticks.astype(int))
  axis.spines['top'].set_visible(False)
  axis.spines['right'].set_visible(False)


def plot_traces(traces: np.ndarray,
                spike_trains: np.ndarray,
                frame_rate: float,
                filename: str = '',
                dpi: int = 240,
                show: bool = True,
                close: bool = True):
  figure, axes = plt.subplots(nrows=4,
                              ncols=1,
                              gridspec_kw={
                                  'wspace': 0.1,
                                  'hspace': 0.1
                              },
                              sharex=True,
                              figsize=(6, 4),
                              dpi=dpi)

  _plot_trace(axis=axes[0],
              signal=traces[0],
              spike=spike_trains[0],
              color='orangered')
  _plot_trace(axis=axes[1],
              signal=traces[1],
              spike=spike_trains[1],
              color='orangered')
  _plot_trace(axis=axes[2],
              signal=traces[2],
              spike=spike_trains[2],
              color='orangered')
  _plot_trace(axis=axes[3],
              signal=traces[2],
              spike=spike_trains[2],
              color='orangered')

  xticks_loc = np.linspace(0, traces.shape[-1], 5)
  axes[-1].set_xticks(xticks_loc)
  axes[-1].set_xticklabels((xticks_loc / frame_rate).astype(int))
  axes[-1].set_xlabel('Time (s)')
  figure.supylabel(r'$\Delta F/F$', x=0.05)

  if filename:
    dirname = os.path.dirname(filename)
    if dirname and not os.path.exists(dirname):
      os.makedirs(dirname)
    figure.savefig(filename, dpi=dpi, bbox_inches='tight', pad_inches=0.01)
    print(f'plot saved to {filename}.')

  if show:
    plt.show()

  if close:
    plt.close(figure)
