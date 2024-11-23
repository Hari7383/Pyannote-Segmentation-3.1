# -*- coding: utf-8 -*-
"""pyannote_segmentation _3.1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GmWchtDpS6o6NYUX20CVm2AtyvPJ3knp
"""

pip install pyannote.audio

pip install pyannote.audio==3.1

# instantiate the pipeline
from pyannote.audio import Pipeline
pipeline = Pipeline.from_pretrained(
  "pyannote/speaker-diarization-3.1",
  use_auth_token="replace your token")

# run the pipeline on an audio file
diarization = pipeline("audio.wav")

# dump the diarization output to disk using RTTM format
with open("audio.rttm", "w") as rttm:
    diarization.write_rttm(rttm)

pip install torch

import torch
pipeline.to(torch.device("cuda"))

pip install torchaudio

import torchaudio
waveform, sample_rate = torchaudio.load("audio.wav")
diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate})

from pyannote.audio.pipelines.utils.hook import ProgressHook
with ProgressHook() as hook:
    diarization = pipeline("audio.wav", hook=hook)

diarization = pipeline("audio.wav", num_speakers=2)

diarization = pipeline("audio.wav", min_speakers=2, max_speakers=5)

print(diarization)