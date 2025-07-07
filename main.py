import streamlit as st 
import whisper
import os 

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("small")

model = load_whisper_model()

st.title("Speech To Text Transcriber")

audiofile = st.file_uploader("upload audio file: ", type=["mp3", "wav", "m4a"])
result = model.transcribe("testingaudio.m4a")

if audiofile is not None: 
    st.audio(audiofile)

    with open("tempaudio.m4a", "wb") as f: 
        f.write(audiofile.getbuffer())
    
    result = model.transcribe("tempaudio.m4a")

# ADD FEATURE: RECOGNIZE DIFFERENT SPEAKERS 

# TRANSLATE INTO DIFFERENT LANGUAGES 

#print(result["text"])
st.write(result["text"])

if audiofile is not None: 
    os.remove("tempaudio.m4a")