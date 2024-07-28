import streamlit as st
import requests
import json
import base64
from pydub import AudioSegment
import os

from Asistente import Asistente

transcrito = False

st.title("Aplicacion para transcribir audio a texto")

idioma = st.selectbox("Seleccione el idioma del texto", ( " " ,"Español", "Ingles"))

if idioma != " ":
    archivo = st.file_uploader("Elige un archivo", ("mp3"))
    procesar = st.button("Procesar")

    if archivo is not None and procesar :
        print(archivo)
        archivo2 = AudioSegment.from_mp3(archivo)
        asistente = Asistente()
        exito = False

        if idioma == "Español":
            asistente.idioma = "es"
            asistente.archivo = archivo2
            exito = asistente.trabajar()
            transcrito = True
        elif idioma == "Ingles":
            asistente.idioma = "en"
            asistente.archivo = archivo2
            exito = asistente.trabajar()
        if exito:
            transcrito = True
        else:
            st.warning("Vaya, ha ocurrido un error. Inténtelo de nuevo")


if transcrito == True:
    asistente.exportar_transcripcion()
    opcion_exportar = st.selectbox("Seleccione formato a exportar", ("TXT", "PDF"))
    if opcion_exportar == "TXT":
        archivo_descargar = ""
        asistente.exportar_transcripcion()
        with open("candela.txt", "rb") as file:
            st.download_button("Descargar archivo txt", file, file_name="Transcripcion.txt" )
    elif opcion_exportar == "PDF":
        archivo_descargar = ""
        st.download_button("Descargar archivo pdf", "candela.txt", file_name="Transcripcion.txt" )