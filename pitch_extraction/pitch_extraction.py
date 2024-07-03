from pitch_extractor import PitchExtractor

pe = PitchExtractor.start_audio_processing()

while True:
    print(pe.pitch_values[-1])