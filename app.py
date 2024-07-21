import streamlit as st
from pydub import *
#from pydub.playback import *


st.title("Mi Aplicación Web con Streamlit")

st.write("Aplicación para transcribir audio a texto")

# Subir un archivo
st.write("Sube el archivo que se quiere transcribir:")
archivo = st.file_uploader("Elige un archivo", ("mp3", "wav"))
archivo.
if archivo is not None:
    st.download_button("Descargar m'usica", archivo)
    extensionArchivo = archivo.type
    st.write(extensionArchivo)



if (True):
    formato = st.selectbox("Elija el formato con el que se quiere exportar el audio", ("PDF", "TXT", "WORD"))
