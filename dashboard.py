import streamlit as st
from pydub import AudioSegment
import tempfile

# CSS for dashboard cluster
st.markdown("""
    <style>
    .dashboard-cluster {
        background-color: #0b0f19;
        width: 800px;
        height: 350px;
        margin: 0 auto;
        border-radius: 20px;
        border: 2px solid #333;
        position: relative;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        color: white;
        overflow: hidden;
    }
    .speed-value { font-size: 120px; font-weight: bold; color: #ff9900; line-height: 1; }
    .footer-icons { position: absolute; bottom: 20px; left: 0; width: 100%; display: flex; justify-content: space-around; color: #555; font-size: 20px; }
    </style>
""", unsafe_allow_html=True)

# Slider
speed = st.sidebar.slider("Vehicle Speed", 0, 250, 52)

# Dashboard cluster UI
html_content = f"""
<div class='dashboard-cluster'>
    <div style='text-align: center; margin-top: 50px;'>
        <div class='speed-value'>{speed}</div>
        <div style='color: #777; font-size: 20px;'>km/h</div>
    </div>
    <div class='footer-icons'>
        <span>⚠️</span> <span>(i)</span> <span>ABS</span> <span>BRAKE</span> <span>0%</span>
    </div>
</div>
"""
st.markdown(html_content, unsafe_allow_html=True)

# Sound playback logic
sound = AudioSegment.from_wav("sample.wav")

if speed == 0:
    # Brake effect (extra screech sound if you have brake.wav)
    brake_sound = AudioSegment.from_wav("brake.wav")
    new_sound = brake_sound
elif speed < 30:
    factor = 0.8
    new_sound = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * factor)
    }).set_frame_rate(sound.frame_rate)
elif speed < 80:
    factor = 1.0
    new_sound = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * factor)
    }).set_frame_rate(sound.frame_rate)
else:
    factor = 1.3
    new_sound = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * factor)
    }).set_frame_rate(sound.frame_rate)

# Save temp file
tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
new_sound.export(tmpfile.name, format="wav")

# Auto playback in app
st.audio(tmpfile.name, format="audio/wav")
