import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from sklearn.decomposition import PCA
from mne.io import read_raw_edf

# 1. Charger le fichier EEG
file_path = "01IS-1-ADP.edf"
raw = read_raw_edf(file_path, preload=True)
print(raw.info)
sfreq = int(raw.info['sfreq'])  # Fréquence d'échantillonnage
signal = raw.get_data(picks="eeg")[0]  # Tout le signal


# 2. Calculer le spectre de puissance avec Welch
def compute_welch(signal, sampling_rate, nperseg=512):
    frequencies, power = welch(signal, fs=sampling_rate, nperseg=nperseg)
    return frequencies, power


# 3. Appliquer PCA sur le spectre de puissance
def apply_pca_to_spectrum(powers, n_components=10):
    pca = PCA(n_components=n_components)
    # Reshape powers to (n_windows, n_frequencies) for PCA
    powers = np.array(powers)
    pca.fit(powers)  # Fit PCA on the power spectra

    # Return all principal components
    return pca.components_


# 4. Split the signal into 10-second windows and compute power spectra
window_size = 10 * sfreq  # 10 seconds per window
n_windows = len(signal) // window_size  # Number of windows

powers = []
all_frequencies = None  # Frequencies will be the same for all windows, calculate once

# Compute the power spectrum for each window and collect them
for i in range(n_windows):
    start = i * window_size
    end = start + window_size
    current_signal = signal[start:end]

    # Compute the power spectrum using Welch
    frequencies, power = compute_welch(current_signal, sfreq, nperseg=sfreq*2)
    powers.append(power)

    if all_frequencies is None:
        all_frequencies = frequencies  # Set frequencies once

# # 5. Apply PCA to the power spectra across all windows and get all principal components
# principal_components = apply_pca_to_spectrum(powers, n_components=10)
#
# # 6. Plot all principal components
# plt.figure(figsize=(10, 6))
# for i, component in enumerate(principal_components):
#     plt.plot(all_frequencies[0:30], component[0:30], label=f'PC {i + 1}', linewidth=2)
#
# plt.title("Principal Components of Power Spectra")
# plt.xlabel("Frequency (Hz)")
# plt.ylabel("Principal Component Value")
# plt.grid(True)
# plt.legend()
# plt.show()

all_powers = np.array(powers)

freq_range = (all_frequencies >= 0) & (all_frequencies <= 30)
limited_frequencies = all_frequencies[freq_range]
limited_powers = all_powers[:, freq_range]  # Only take the rows corresponding to the 0-30 Hz range

# 5. Plot the Time-Frequency representation limited to 0-30 Hz
plt.figure(figsize=(12, 6))
plt.imshow(limited_powers.T, aspect='auto', origin='lower', cmap='jet',
           extent=[0, n_windows * window_size / sfreq, limited_frequencies[0], limited_frequencies[-1]])
plt.title("Time-Frequency Representation (0-30 Hz)")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.colorbar(label="Power (µV²/Hz)")
plt.grid(True)
plt.show()