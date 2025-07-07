import streamlit as st 
import whisper
import os 
from deep_translator import GoogleTranslator
from gtts import gTTS

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("small")

model = load_whisper_model()

st.title("Multilingual Transcriber")
st.markdown("upload audio file or record directly to get transcription and translation.")

result_text="Record Audio - no input available"

#audiofile = st.file_uploader("upload audio file: ", type=["mp3", "wav", "m4a"])
audiofile = st.audio_input("record audio")

if audiofile is not None: 
    with open("tempaudio.m4a", "wb") as f: 
        f.write(audiofile.getbuffer())
    
    result = model.transcribe("tempaudio.m4a")
    result_text = result["text"]

st.subheader("Transcription")
st.write(result_text)

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