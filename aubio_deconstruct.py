import librosa
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import aubio

file_path = './samples/rolling-in-the-deep.wav'
sample_rate, data = wavfile.read(file_path)
print("sr:", sample_rate)
data = data[308700:] # because first 7 seconds are empty
data = data[:441000] # for testing
data = data.T

time = np.arange(0, len(data[1])) / sample_rate
plt.figure(figsize=(10, 4))
plt.plot(time, data[0], color='blue')  # You can set the color explicitly
plt.title('Audio Waveform')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.show()

min_freq = 40 
max_freq = 1000       
amplitude_threshold = 0.1 
energy_threshold = 50

win_s = 8192
hop_s = 4096
pitch_o = aubio.pitch("yin", win_s, hop_s, sample_rate)
audio_data = data[0].astype(np.float32) / 32768.0  # Assuming 16-bit PCM

pitches = []
for i in range(0, len(audio_data) - hop_s, hop_s):
     # Calculate FFT to determine if we should consider this signal a hum
    sample = audio_data[i:i+hop_s]
    fft_result = np.fft.fft(sample)
    frequency_bins = np.fft.fftfreq(len(sample), 1 / sample_rate)
    humming_energy = np.sum(np.abs(fft_result[(frequency_bins > min_freq) & (frequency_bins < max_freq)]))
    
    pitch = 0
    if np.max(np.abs(sample)) > amplitude_threshold:
        calc_pitch = pitch_o(sample)[0]
        if humming_energy > energy_threshold:
            pitch = calc_pitch
    pitches.append(pitch)

# Plot the pitches over time
time_axis = np.arange(len(pitches)) * hop_s / float(sample_rate)  # Convert sample index to time in seconds

plt.figure(figsize=(10, 4))
plt.plot(time_axis, pitches, label='Pitch (Hz)', color='blue')
plt.xlabel('Time (s)')
plt.ylabel('Pitch (Hz)')
plt.title('Pitch over Time')
plt.grid(True)
plt.legend()
plt.show()