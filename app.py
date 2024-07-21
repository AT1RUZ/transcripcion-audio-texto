import streamlit as st
import pydub as pd

# Título de la aplicación
st.title("Mi Aplicación Web con Streamlit")

# Texto introductorio
st.write("Aplicación para transcribir audio a texto")

# Subir un archivo
st.write("Sube archivo archivo que se quiere transcribir:")
uploaded_file = st.file_uploader("Elige un archivo", ("mp3", "wav"))

if uploaded_file is not None:
    st.write("Nombre del archivo:", uploaded_file.name)
    st.write("Tipo de archivo:", uploaded_file.type)
    st.write("Tamaño del archivo:", uploaded_file.size)

if (True):
    formato = st.selectbox("Elija el formato con el que se quiere exportar el audio", ("PDF", "TXT", "WORD"))
