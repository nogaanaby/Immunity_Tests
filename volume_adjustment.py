import librosa
import soundfile as sf
import numpy as np

def calculate_rms(audio_file):
    y, sr = librosa.load(audio_file, sr=None)
    rms = np.sqrt(np.mean(y**2))
    return rms, y, sr


original_rms, original_audio, sr = calculate_rms("original.wav")
recorded_rms, recorded_audio, _ = calculate_rms("recorded.wav")

# Calculate the gain factor needed to match the recorded song's volume to the original song's volume
gain = original_rms / recorded_rms

adjusted_audio = recorded_audio * gain

sf.write("recorded_adjusted.wav", adjusted_audio, sr)

# Print relevant information for tracking
print(f"Original RMS level: {original_rms}")
print(f"Recorded RMS level: {recorded_rms}")
print(f"Gain factor: {gain}")
print("The adjusted recorded song has been saved as recorded_adjusted.wav")
