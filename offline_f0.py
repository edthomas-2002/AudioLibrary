import librosa
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import aubio

file_path = './samples/piano-C.wav'
sample_rate, data = wavfile.read(file_path)
print("sr:", sample_rate)
data = data.T

# time = np.arange(0, len(data[1])) / sample_rate
# plt.figure(figsize=(10, 4))
# plt.plot(time, data[0], color='blue')  # You can set the color explicitly
# plt.title('Audio Waveform')
# plt.xlabel('Time (seconds)')
# plt.ylabel('Amplitude')
# plt.show()

win_s = 8192
hop_s = 4096
pitch_o = aubio.pitch("yin", win_s, hop_s, sample_rate)
audio_data = data[0].astype(np.float32) / 32768.0  # Assuming 16-bit PCM

for i in range(0, len(audio_data) - hop_s, hop_s):
    pitch = pitch_o(audio_data[i:i+hop_s])[0]
    print(pitch)
## EXPECTED to be appx 529. SUCCESS