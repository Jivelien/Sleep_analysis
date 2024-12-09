import math

from scipy.signal import welch


def homebrew_fft(signal):
    N = len(signal)
    real = [0] * N
    imag = [0] * N
    for k in range(N):
        for n in range(N):
            angle = 2 * math.pi * k * n / N
            real[k] += signal[n] * math.cos(angle)
            imag[k] -= signal[n] * math.sin(angle)
    magnitude = [math.sqrt(r ** 2 + i ** 2) for r, i in zip(real, imag)]
    return magnitude[:N // 2]

def calculate_frequencies(N, sampling_rate):
    return [(sampling_rate * k) / N for k in range(N // 2)]

def compute_frequency_analysis(current_signal, sfreq):
    power = homebrew_fft(current_signal)
    frequencies = calculate_frequencies(len(current_signal), sfreq)

    return dict(zip(frequencies,power))


def compute_frequency_analysis_for_a_period(signal, windows_lenght,sampling_rate, period=0):
    start = windows_lenght * period
    end = start + windows_lenght

    current_signal = signal[start:end]
    return compute_welch(current_signal, sampling_rate)



def compute_welch(signal, sampling_rate):
    frequencies, power = welch(signal, fs=sampling_rate, nperseg=sampling_rate*5)
    return dict(zip(frequencies,power))