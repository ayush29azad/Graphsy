from fastapi import FastAPI
import librosa, numpy as np

app = FastAPI()

@app.get("/analyze_sound")
def analyze_sound(speed: int):
    y, sr = librosa.load("sample.wav", sr=None)
    energy = float(np.mean(librosa.feature.rms(y=y)))

    if speed < 30:
        baseline = 20
    elif speed < 80:
        baseline = 40
    else:
        baseline = 70

    sound_level = energy*100 + (speed/10)
    anomaly = (sound_level > baseline + 20)

    return {"speed": speed, "sound_level": round(sound_level, 2), "anomaly": anomaly}
