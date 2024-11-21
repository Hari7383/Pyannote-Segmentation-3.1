import sounddevice as sd
from scipy.io.wavfile import write

# Parameters
duration = 10  # seconds
sample_rate = 44100  # Hz

# Record audio
print("Recording...")
audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
sd.wait()  # Wait for the recording to finish
print("Recording completed!")

# Save as WAV file
output_file = "audio.wav"
write(output_file, sample_rate, audio)
print(f"Audio saved to {output_file}")
