# -*- coding: utf-8 -*-
"""pyannote_segmentation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GmWchtDpS6o6NYUX20CVm2AtyvPJ3knp
"""

pip install pyannote.audio

pip install torch

pip install torchaudio

pip install pyannote.audio==3.1

pip show torch

from pyannote.audio import Pipeline
pipeline = Pipeline.from_pretrained(
  "pyannote/speaker-diarization-3.1",
  use_auth_token="replace your token")

# run the pipeline on an audio file
diarization = pipeline("audio.wav")

# dump the diarization output to disk using RTTM format
with open("audio.rttm", "w") as rttm:
    diarization.write_rttm(rttm)

"""**Without rttm**"""

import torchaudio
import torch
from pyannote.audio.pipelines.utils.hook import ProgressHook
from pyannote.audio import Pipeline


pipeline = Pipeline.from_pretrained(
  "pyannote/speaker-diarization-3.1",
  use_auth_token="replace your token")

pipeline.to(torch.device("cuda"))

waveform, sample_rate = torchaudio.load("audio.wav")
diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate})


with ProgressHook() as hook:
    diarization = pipeline("audio.wav", hook=hook)

diarization = pipeline("audio.wav", num_speakers=2)

diarization = pipeline("audio.wav", min_speakers=2, max_speakers=5)

print(diarization)

!apt-get install -y locales

"""**For Text**"""

!pip install openai-whisper

import torchaudio
import torch
from pyannote.audio import Pipeline
from pyannote.core import Segment
from whisper import load_model  # Using OpenAI's Whisper for transcription

# Load diarization pipeline
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="replace your token"
)

# Move pipeline to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
pipeline.to(device)

# Load the audio file
waveform, sample_rate = torchaudio.load("audio.wav")

# Perform diarization
diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate})

# Initialize Whisper for transcription
asr_model = load_model("base")  # Choose a Whisper model size: tiny, base, small, medium, large

# Extract speaker-wise text
speaker_text = {}
for turn, _, speaker in diarization.itertracks(yield_label=True):
    # Extract the audio segment for the speaker
    segment = waveform[:, int(turn.start * sample_rate): int(turn.end * sample_rate)]

    # Save segment temporarily (Whisper requires a file as input)
    temp_file = "temp_segment.wav"
    torchaudio.save(temp_file, segment, sample_rate)

    # Transcribe the segment
    result = asr_model.transcribe(temp_file)
    transcription = result["text"]

    # Append transcription to the speaker's text
    if speaker not in speaker_text:
        speaker_text[speaker] = ""
    speaker_text[speaker] += f" {transcription}"

# Output speaker-wise transcriptions and number of speakers
num_speakers = len(speaker_text)
print(f"Number of speakers: {num_speakers}")
for speaker, text in speaker_text.items():
    print(f"{speaker}: {text}")