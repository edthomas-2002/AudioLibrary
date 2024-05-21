import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import time
import sys

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024 * 2

# Create the figure and axis
fig, ax = plt.subplots()
x = np.arange(0, 2 * CHUNK, 2)
line, = ax.plot(x, np.random.rand(CHUNK))

ax.set_ylim(0,255)

data = np.zeros(CHUNK)
is_running = False

def audio_processing():
    global data
    # Open the audio stream in the audio thread
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        output=False,
        input=True,
        frames_per_buffer=CHUNK,
    )

    # Continuously read and process audio data in the background
    while is_running:
        in_data = stream.read(CHUNK)
        audio_data = np.frombuffer(in_data, dtype=np.int16)

        data = np.concatenate((data, audio_data))
        data = data[-CHUNK:]

        time.sleep(0.01)  # Adjust as needed based on your application's requirements

    # Close the stream when done
    plt.close()
    stream.stop_stream()
    stream.close()
    p.terminate()

def update_plot(self):
    line.set_ydata(data)

    # if time.time() - start_time > duration:
    #     close_app()

def close_app(self):
    is_running = False
    audio_thread.join()  # Wait for the audio thread to finish
    sys.exit()

audio_thread = threading.Thread(target=audio_processing)
audio_thread.start()
is_running = True

# Set up the animation
ani = FuncAnimation(fig, update_plot, frames=data, interval=1)

# Show the plot
plt.show()

