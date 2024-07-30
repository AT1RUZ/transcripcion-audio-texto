import streamlit as st
from pydub import AudioSegment
import os

from Asistente import Asistente

# Inicializar el estado de la sesión Streamlit
if 'transcrito' not in st.session_state:
    st.session_state.transcrito = False  # Indica si el audio ha sido transcrito
if 'permiso_procesar' not in st.session_state:
    st.session_state.permiso_procesar = True  # Permite procesar el audio
if 'asistente' not in st.session_state:
    st.session_state.asistente = Asistente()  # Instancia del asistente para transcripción

st.title("Aplicacion para transcribir audio a texto")
if not st.session_state.transcrito:
    # Selección del idioma para la transcripción
    idioma = st.selectbox("Seleccione el idioma del texto", (" ", "Español", "Ingles"))
    procesar = False
    if idioma != " ":
        archivo = st.file_uploader("Elige un archivo", "mp3")# Carga del archivo de audio
        if st.session_state.permiso_procesar:
            procesar = st.button("Procesar") # Botón para iniciar el procesamiento
        if archivo is not None and procesar:
            archivo2 = AudioSegment.from_mp3(archivo) # Conversión del archivo de audio a un objeto AudioSegment
            print(archivo)
            st.session_state.permiso_procesar = False  # Desactiva el botón de procesar
            exito = False
            st.session_state.asistente.i = 0 # Inicializa el contador de segmentos
            # Configuración del asistente según el idioma seleccionado
            if idioma == "Español":
                st.session_state.asistente.transcripcion = None
                st.session_state.asistente.idioma = "es"
                st.session_state.asistente.archivo = archivo2
                exito = st.session_state.asistente.trabajar()  # Llama al método para transcribir
            elif idioma == "Ingles":
                st.session_state.asistente.transcripcion = None
                st.session_state.asistente.idioma = "en"
                st.session_state.asistente.archivo = archivo2
                exito = st.session_state.asistente.trabajar()  # Llama al método para transcribir
                # Manejo de errores en la transcripción
            if not exito: 
                st.session_state.transcrito = False
                st.session_state.permiso_procesar = True 
                st.warning("Vaya, ha ocurrido un error. Inténtelo de nuevo.") 
            else:
                procesar = False
                st.session_state.transcrito = True # Marca como transcrito
                
# Sección para exportar la transcripción
if st.session_state.asistente.transcrito:
    opcion_exportar = st.selectbox("Seleccione formato a exportar", (" ", "TXT", "PDF"))
    if opcion_exportar == "TXT":
        st.session_state.asistente.exportar_transcripcion_txt() # Exporta a TXT
        with open("tt.txt", "rb") as file:
            descargar = st.download_button("Descargar archivo txt", file, file_name="Transcripcion.txt")
            if descargar:
                if os.path.exists("tt.txt"):
                    os.remove("tt.txt")  # Elimina el archivo temporal
    elif opcion_exportar == "PDF":
        st.session_state.asistente.exportar_transcripcion_pdf() # Exporta a PDF
        with open("tt.pdf", "rb") as file:
            descargar = st.download_button("Descargar archivo pdf", file, file_name="Transcripcion.pdf")
            if descargar:
                if os.path.exists("tt.pdf"):
                    os.remove("tt.pdf")  # Elimina el archivo temporal
