import aubio, pyaudio
import numpy as np
import threading

class PitchExtractor():

    def __init__(self):
        self.samplerate = 44100
        self.win_s = 4096
        self.hop_s = 2048
        self.pitch_o = aubio.pitch("yin", self.win_s, self.hop_s, self.samplerate)
        self.amplitude_threshold = 0.1  # Adjust this threshold based on your requirements
        self.min_humming_freq = 40 
        self.max_humming_freq = 175       
        self.energy_threshold = 0  
        self.pitch_window_size = 7
        self.raw_pitch = [0.0 for i in range(self.pitch_window_size)]
        self.pitch_values = [0.0]

    def audio_processing(self):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.samplerate,
            output=False,
            input=True,
            frames_per_buffer=self.hop_s,
        )

        while True:
            in_data = stream.read(self.hop_s, exception_on_overflow=False)
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            audio_data = audio_data.astype(np.float32) / 32768.0  # Assuming 16-bit PCM

            # Calculate FFT to determine if we should consider this signal a hum
            fft_result = np.fft.fft(audio_data)
            frequency_bins = np.fft.fftfreq(len(audio_data), 1 / self.samplerate)
            humming_energy = np.sum(np.abs(fft_result[(frequency_bins > self.min_humming_freq) & (frequency_bins < self.max_humming_freq)]))
        
            pitch = 0
            if np.max(np.abs(audio_data)) > self.amplitude_threshold:
                calc_pitch = self.pitch_o(audio_data)[0]
                if humming_energy > self.energy_threshold:
                    pitch = calc_pitch
            self.raw_pitch.append(pitch)
            averaged_pitch = np.mean(self.raw_pitch[-self.pitch_window_size:])
            self.pitch_values.append(averaged_pitch)
    
    @classmethod
    def start_audio_processing(cls):
        pe = cls()
        audio_thread = threading.Thread(target=pe.audio_processing)
        audio_thread.daemon = True
        audio_thread.start()
        return pe