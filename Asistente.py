import json
import base64
import os.path
import  time
import requests
from pydub import AudioSegment

class Asistente():


    def __init__(self):
        self.transcripcion = None
        self.url = "https://api-inference.huggingface.co/models/openai/whisper-large"
        self.token = "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"
        self.idioma = None
        self.tamaño_segmento = 30000
        self.archivo = None
        #Atributo temporal
        self.i = 0



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
        return True

    def exportar_transcripcion(self):
        with open("candela.txt", "w",encoding="utf-8") as file:
            file.write(self.transcripcion)
        if os.path.exists("temp_segment.mp3"):
            os.remove("temp_segment.mp3")


    def transcribe_segment(self, segment, api_token, idioma, api_url):
        print("EJECUTANDO TRANSCRIBE SERVERS PARA EL SEGMENTO " + str(self.i))
        inicio  =  time.time()
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

        while True and intentos  > 1:
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
                if intentos == 0:
                    return None
                print(f"Error {response.status_code}: {response.text}")
                print("reintentando")





