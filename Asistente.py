import json
import base64
import os.path
import time
import requests
from fpdf import FPDF


class Asistente:

    def __init__(self):
        self.transcripcion = None
        self.url = "https://api-inference.huggingface.co/models/openai/whisper-large"
        self.token = "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"
        self.idioma = None
        self.tamaño_segmento = 60000
        self.archivo = None
        # Atributo temporal
        self.i = 0
        self.transcrito = False

    def divide_audio(self, audio_a_separar, segment_length_ms):
        audio = audio_a_separar
        audio_segments = [audio[i:i + segment_length_ms] for i in range(0, len(audio), segment_length_ms)]
        return audio_segments

    def trabajar(self):
        segmentos = self.divide_audio(self.archivo, self.tamaño_segmento)
        self.transcripcion = ""
        for i, segment in enumerate(segmentos):
            transcripcion_temp = self.transcribe_segment(segment, self.token, self.idioma, self.url)
            if transcripcion_temp is not None:
                print(str(i) + ": " + transcripcion_temp)
                print("\n ")
                self.transcripcion += transcripcion_temp + ""
            else:
                return False
        self.transcrito = True
        return True

    def exportar_transcripcion_txt(self):
        if self.transcripcion is not None:
            with open("tt.txt", "w", encoding="utf-8") as file:
                file.write(self.transcripcion)
            if os.path.exists("temp_segment.mp3"):
                os.remove("temp_segment.mp3")
        else:
            return None

    def exportar_transcripcion_pdf(self):
        if self.transcripcion is not None:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Transcripcion", ln=1, align="C")
            pdf.multi_cell(200, 7, self.transcripcion, 0, 0, 'C')
            pdf.output("tt.pdf")
            if os.path.exists("temp_segment.mp3"):
                os.remove("temp_segment.mp3")
        else:
            return None

    def transcribe_segment(self, segment, api_token, idioma, api_url):
        print("EJECUTANDO TRANSCRIBE SERVERS PARA EL SEGMENTO " + str(self.i + 1))
        inicio = time.time()
        self.i += 1

        segment.export("temp_segment.mp3", format="mp3")
        with open("temp_segment.mp3", "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")

        # Encabezados de la solicitud
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

        # Datos de la solicitud
        data = json.dumps({
            "inputs": audio_base64,
            "options": {
                "language": idioma
            }
        })
        intentos = 3
        intento = 0

        while intentos > 0:

            print("Intento " + str(intento + 1))
            intento += 1
            print("Conectando...")
            # Realizar la solicitud a la API
            response = requests.post(api_url, headers=headers, data=data)

            if response.status_code == 200:
                result = response.json()
                transcription = result.get("text", "")
                final = time.time()
                print("...en talla")
                print(f"Demora {final - inicio} segundos")
                return transcription
            else:
                intentos -= 1
                print(f"Error {response.status_code}: {response.text}")
                print("reintentando")
        if intentos == 0:
            return None
