import streamlit as st
from pydub import AudioSegment
import os

from Asistente import Asistente

# Inicializar el estado de la sesión
if 'transcrito' not in st.session_state:
    st.session_state.transcrito = False
if 'permiso_procesar' not in st.session_state:
    st.session_state.permiso_procesar = True
if 'asistente' not in st.session_state:
    st.session_state.asistente = Asistente()

st.title("Aplicacion para transcribir audio a texto")
if not st.session_state.transcrito:
    idioma = st.selectbox("Seleccione el idioma del texto", (" ", "Español", "Ingles"))
    procesar = False
    if idioma != " ":
        archivo = st.file_uploader("Elige un archivo", ("mp3"))

        if st.session_state.permiso_procesar:
            procesar = st.button("Procesar")

        if archivo is not None and procesar:
            archivo2 = AudioSegment.from_mp3(archivo)
            print(archivo)
            st.session_state.permiso_procesar = False
            exito = False
            st.session_state.asistente.i = 0
            if idioma == "Español":
                st.session_state.asistente.transcripcion = None
                st.session_state.asistente.idioma = "es"
                st.session_state.asistente.archivo = archivo2
                exito = st.session_state.asistente.trabajar()
            elif idioma == "Ingles":
                st.session_state.asistente.transcripcion = None
                st.session_state.asistente.idioma = "en"
                st.session_state.asistente.archivo = archivo2
                exito = st.session_state.asistente.trabajar()
            if not exito:
                st.session_state.transcrito = False
                st.session_state.permiso_procesar = True
                st.warning("Vaya, ha ocurrido un error. Inténtelo de nuevo.")
            else:
                procesar = False
                st.session_state.transcrito = True

if st.session_state.asistente.transcrito:
    opcion_exportar = st.selectbox("Seleccione formato a exportar", (" ", "TXT", "PDF"))
    if opcion_exportar == "TXT":
        st.session_state.asistente.exportar_transcripcion_txt()
        with open("tt.txt", "rb") as file:
            descargar = st.download_button("Descargar archivo txt", file, file_name="Transcripcion.txt")
            if descargar:
                if os.path.exists("tt.txt"):
                    os.remove("tt.txt")
    elif opcion_exportar == "PDF":
        st.session_state.asistente.exportar_transcripcion_pdf()
        with open("tt.pdf", "rb") as file:
            descargar = st.download_button("Descargar archivo pdf", file, file_name="Transcripcion.pdf")
            if descargar:
                if os.path.exists("tt.pdf"):
                    os.remove("tt.pdf")
