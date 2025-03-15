import serial
import numpy as np
from scipy.signal import find_peaks, butter, filtfilt, welch
import matplotlib.pyplot as plt
import time

PORT = "COM3"
BAUD_RATE = 9600
SAMPLE_RATE = 2000
DURATION = 10

def bandpass_filter(signal, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, signal)

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {PORT}")
except Exception as e:
    print(f"Error: {e}")
    exit()

data = []
start_time = time.time()

while time.time() - start_time < DURATION:
    try:
        line = ser.readline().decode('utf-8').strip()
        if line.isdigit():
            data.append(int(line))
    except:
        continue

ser.close()
print("Data collection complete.")

data = np.array(data)
time_vector = np.linspace(0, DURATION, len(data))
filtered_signal = bandpass_filter(data, 20, 150, SAMPLE_RATE)
threshold_s1 = np.max(filtered_signal) * 0.5
threshold_s2 = np.max(-filtered_signal) * 0.5
peaks_s1, _ = find_peaks(filtered_signal, height=threshold_s1, distance=SAMPLE_RATE / 4)
peaks_s2, _ = find_peaks(-filtered_signal, height=threshold_s2, distance=SAMPLE_RATE / 4)
frequencies = np.fft.rfftfreq(len(filtered_signal), d=1 / SAMPLE_RATE)
fft_magnitude = np.abs(np.fft.rfft(filtered_signal))
frequencies_psd, psd_values = welch(filtered_signal, fs=SAMPLE_RATE, nperseg=1024)
heart_rate = len(peaks_s1 + peaks_s2) * (60 / DURATION)
dominant_freqs = frequencies[np.argsort(fft_magnitude)[-5:][::-1]]

plt.figure(figsize=(14, 10))
plt.subplot(3, 1, 1)
plt.plot(time_vector, data, label="Raw Signal")
plt.plot(time_vector, filtered_signal, label="Filtered Signal", color="orange")
plt.scatter(time_vector[peaks_s1], filtered_signal[peaks_s1], color="blue", label="S1 (Lub)", marker='o')
plt.scatter(time_vector[peaks_s2], filtered_signal[peaks_s2], color="green", label="S2 (Dub)", marker='x')
plt.title("Heart Sound Signal with S1 and S2 Peaks")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()

for peak in peaks_s1:
    plt.annotate("S1", (time_vector[peak], filtered_signal[peak]), textcoords="offset points", xytext=(0, 10), ha='center', color='blue')
for peak in peaks_s2:
    plt.annotate("S2", (time_vector[peak], filtered_signal[peak]), textcoords="offset points", xytext=(0, 10), ha='center', color='green')

plt.subplot(3, 1, 2)
plt.plot(frequencies, fft_magnitude, label="Frequency Spectrum")
plt.scatter(dominant_freqs, fft_magnitude[np.argsort(fft_magnitude)[-5:][::-1]], color='red', label="Dominant Frequencies")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("Frequency Spectrum with Dominant Frequencies")
plt.xlim(0, 200)
plt.legend()
plt.grid()

for i, freq in enumerate(dominant_freqs):
    plt.text(freq, fft_magnitude[np.argsort(fft_magnitude)[-5:][::-1]][i] * 1.1, f"{freq:.2f} Hz", color='red', fontsize=10, ha='center')

plt.subplot(3, 1, 3)
plt.semilogy(frequencies_psd, psd_values, label="PSD")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power/Frequency (dB/Hz)")
plt.title("Power Spectral Density")
plt.xlim(0, 200)
plt.grid()

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.figtext(0.5, 0.01, f"Heart Rate: {heart_rate:.2f} BPM", wrap=True, horizontalalignment='center', fontsize=12, weight='bold')

plt.show()

print(f"Heart Rate: {heart_rate:.2f} BPM")
print("Dominant Frequencies (Top 5):", dominant_freqs)
