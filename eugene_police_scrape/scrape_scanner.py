#!/usr/bin/env python

# Scrape Police Scanner & Convert To Transcript


import time
import requests
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
# Whisper:
# choco install ffmpeg (as admin/sudo)
# pip install git+https://github.com/openai/whisper.git 
import whisper

# Find your broadcastify stream
BROADCAST_URL = "https://broadcastify.cdnstream1.com/20613"
view_melspec = True

if __name__=="__main__":

    fp = Path(__file__).parent / Path("stream.mp3")
    model = whisper.load_model("base")

    # Stream in audio from the broadcast and write to file
    r = requests.get(BROADCAST_URL, stream=True)

    print(f"Recording for 30s...")
    t0 = time.time()
    with open(fp, "wb") as f:
        try:

            for block in r.iter_content(1024):  
                f.write(block)
                if time.time() - t0 > 14: ##14 second loop -> 30 sec audio
                    break

        except Exception as e:
            print(e)

    # Transcribe via whisper
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = model.transcribe(str(fp), verbose=None)

    print("RESULT:")
    print(result["text"])
    if result["text"] == "":
        print("(Model returned 0 characters.)")

    if view_melspec:
        audio = whisper.load_audio(str(fp))
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio)
        plt.figure(figsize=(10, 8))
        plt.imshow(mel.unsqueeze(-1))
        plt.show()
