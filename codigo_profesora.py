import requests
import json
import base64
from pydub import AudioSegment
import os

def trans(name):
    NOMBRE = name
    # Función para dividir el audio en segmentos
    def divide_audio(audio_path, segment_length_ms):
        audio = AudioSegment.from_mp3(audio_path)
        audio_segments = [audio[i:i + segment_length_ms] for i in range(0, len(audio), segment_length_ms)]
        return audio_segments

    # Función para transcribir un segmento de audio
    def transcribe_segment(segment, api_token):
        segment.export("temp_segment.mp3", format="mp3")
        with open("temp_segment.mp3", "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")

        # URL de la API de Hugging Face para Whisper
        api_url = "https://api-inference.huggingface.co/models/openai/whisper-large"

        # Encabezados de la solicitud
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

        # Datos de la solicitud
        data = json.dumps({
            "inputs": audio_base64,
            "options": {
                "language": "es"
            }
        })

        # Realizar la solicitud a la API
        response = requests.post(api_url, headers=headers, data=data)

        # Procesar la respuesta
        if response.status_code == 200:
            result = response.json()
            transcription = result.get("text", "")
            return transcription
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    # Ruta al archivo de audio
    audio_file_path = f"{NOMBRE}.MP3"

    # Duración del segmento en milisegundos (p.ej., 60000 ms = 1 minuto)
    segment_length_ms = 60000

    # Token de API de Hugging Face
    api_token = "holajose"  # Reemplaza esto con tu token de API

    # Dividir el audio en segmentos
    audio_segments = divide_audio(audio_file_path, segment_length_ms)

    # Transcribir cada segmento
    full_transcription = ""
    for i, segment in enumerate(audio_segments):
        print(f"Transcribiendo segmento {i + 1}/{len(audio_segments)}...")
        transcription = transcribe_segment(segment, api_token)
        if transcription:
            full_transcription += transcription + " "

    print(full_transcription)
    # Guardar la transcripción completa en formato de diálogo en un archivo de texto
    output_file_path = f"{NOMBRE}.txt"
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(full_transcription)

    # Eliminar el archivo temporal
    if os.path.exists("temp_segment.wav"):
        os.remove("temp_segment.wav")

    print("Transcripción completa")


trans("musica")