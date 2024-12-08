import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mne.io import read_raw_edf
from scipy.signal import welch

from fft_func import compute_frequency_analysis

file_path = "01IS-1-ADP.edf"
raw = read_raw_edf(file_path, preload=True)
print(raw.info)
sfreq = int(raw.info['sfreq'])
signal = raw.get_data(picks="eeg")[0]  # Tout le signal

window_size = sfreq * 10  # secondes
start = 0

def update_graph(start):
    end = start + window_size
    current_signal = signal[start:end]

    ax_time.clear()
    time = [i / sfreq for i in range(start, end)]
    ax_time.plot(time, current_signal, color="blue")
    ax_time.set_title("Signal EEG - Fenêtre temporelle")
    ax_time.set_xlabel("Temps (s)")
    ax_time.set_ylabel("Amplitude")

    frequencies, power = compute_frequency_analysis(current_signal, sfreq)

    ax_fft.clear()
    ax_fft.plot(frequencies, power, color="red")
    ax_fft.set_title("Spectre de puissance (FFT)")
    ax_fft.set_xlabel("Fréquence (Hz)")
    ax_fft.set_ylabel("Amplitude")
    ax_fft.grid()

    fig.canvas.draw_idle()

def update(val):
    global start
    start = int(slider.val) * sfreq
    update_graph(start)

def on_key(event):
    global start
    step = sfreq
    if event.key == "right":
        start = min(start + step, len(signal) - window_size)
    elif event.key == "left":
        start = max(start - step, 0)
    slider.set_val(start / sfreq)
    update_graph(start)

fig, (ax_time, ax_fft) = plt.subplots(2, 1, figsize=(12, 8))
plt.subplots_adjust(bottom=0.2)

current_signal = signal[start:start + window_size]
time = [i / sfreq for i in range(start, start + window_size)]
ax_time.plot(time, current_signal, color="blue")
ax_time.set_title("Signal EEG - Fenêtre temporelle")
ax_time.set_xlabel("Temps (s)")
ax_time.set_ylabel("Amplitude")

frequencies, power = compute_frequency_analysis(current_signal, sfreq)

ax_fft.plot(frequencies, power, color="red")
ax_fft.set_title("Spectre de puissance (FFT)")
ax_fft.set_xlabel("Fréquence (Hz)")
ax_fft.set_ylabel("Amplitude")
ax_fft.grid()

ax_slider = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor="lightgoldenrodyellow")
slider = Slider(ax_slider, "Début (s)", 0, len(signal) / sfreq - 5, valinit=0, valstep=5)
slider.on_changed(update)

fig.canvas.mpl_connect("key_press_event", on_key)

plt.show()
