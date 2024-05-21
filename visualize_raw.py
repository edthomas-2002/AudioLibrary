import pyaudio
import aubio
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg
import threading
import time
import mne

class AudioPlotter(QMainWindow):
    def __init__(self, chunk_size=2048, sample_rate=44100, duration=15):
        super().__init__()

        self.chunk_size = chunk_size
        self.sample_rate = sample_rate
        self.duration = duration
        self.start_time = time.time()
        self.data = np.zeros(self.chunk_size * 2)
        self.is_running = True
        self.psd_data, self.freqs = mne.time_frequency.psd_array_welch(
                self.data, self.sample_rate, n_fft=1024
            )

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Live Audio Plotter")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.plot_widget = pg.PlotWidget()
        self.plot = self.plot_widget.plot(pen='y')
        self.layout.addWidget(self.plot_widget)

        self.timer = pg.QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(0)

        # Create a separate thread for audio processing
        self.audio_thread = threading.Thread(target=self.audio_processing)
        self.psd_thread = threading.Thread(target=self.calculate_psd)

        # Start both threads
        self.audio_thread.start()
        self.psd_thread.start()

    def audio_processing(self):
        # Open the audio stream in the audio thread
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            output=False,
            input=True,
            frames_per_buffer=self.chunk_size,
        )

        # Continuously read and process audio data in the background
        while self.is_running:
            in_data = stream.read(self.chunk_size)
            audio_data = np.frombuffer(in_data, dtype=np.int16)

            self.data = np.concatenate((self.data, audio_data))
            self.data = self.data[-self.chunk_size * 2:]

            time.sleep(0.01)  # Adjust as needed based on your application's requirements

        # Close the stream when done
        stream.stop_stream()
        stream.close()
        p.terminate()

    def calculate_psd(self):
        while self.is_running:
            # Adjust the sleep duration based on your application's requirements
            time.sleep(0.01)
            # Calculate PSD in a separate thread
            psd, freqs = mne.time_frequency.psd_array_welch(
                self.data, self.sample_rate, n_fft=1024
            )
            self.psd_data = psd
           
    def update_plot(self):
        self.plot.setData(y=self.data)
        # self.plot.setData(x=self.freqs, y=np.log10(self.psd_data))

        if time.time() - self.start_time > self.duration:
            self.close_app()

    def close_app(self):
        self.is_running = False
        self.audio_thread.join()
        self.psd_thread.join()
        sys.exit()


def main():
    app = QApplication(sys.argv)
    plotter = AudioPlotter()
    plotter.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
