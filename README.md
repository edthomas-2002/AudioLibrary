All the most important code is in the pitch_extraction directory. OUTSIDE of the pitch_extraction directory, visualize_raw just displays the raw audio signal, and the other two py files are just to play around. Inside the pitch_extraction directory, if you want the demo then run pitch_visualizer. pitch_extractor shares much code with this file, but provides a standalone class that extracts pitch, and we demonstrate how to use it in pitch_extraction.
Preferable to use conda env / venv. Need to install aubio, pyaudio, numpy, and pygame (possibly among others) to run pitch_visualizer.