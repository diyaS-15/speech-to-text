import streamlit as st 
import whisper
import os 
from deep_translator import GoogleTranslator
from gtts import gTTS
import ffmpeg_static

os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_static.__file__)

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("small")

model = load_whisper_model()

st.title("Multilingual Transcriber")

#audiofile = st.file_uploader("upload audio file: ", type=["mp3", "wav", "m4a"])
audiofile = st.audio_input("record audio")
result = model.transcribe("testingaudio.m4a")

if audiofile is not None: 
    with open("tempaudio.m4a", "wb") as f: 
        f.write(audiofile.getbuffer())
    
    result = model.transcribe("tempaudio.m4a")

# ADD FEATURE: RECOGNIZE DIFFERENT SPEAKERS 




# END FEATURE
st.subheader("Transcription")
st.write(result["text"])

# LANGUAGE TRANSLATION FEATURE
st.subheader("Translate")
language_options = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese",
    "ja": "Japanese", 
    "ko": "Korean", 
    "hi": "Hindi"
}

selection = st.segmented_control(
    "select language",
    options=language_options.keys(),
    format_func=lambda option: language_options[option]
)

if selection:
    translated_text = GoogleTranslator(source='auto', target=selection).translate(result["text"])
    st.write(translated_text)

    translated_audio = gTTS(text=translated_text, lang=selection, slow=False)
    translated_audio.save("translatedaudio.mp3")
    st.audio("translatedaudio.mp3")

#print(result["text"])

if audiofile is not None: 
    os.remove("tempaudio.m4a")
    if selection is not None:
        os.remove("translatedaudio.mp3")