# Resumen del Código y Flujo de Trabajo

Este código implementa una aplicación web utilizando Streamlit que permite a los usuarios cargar archivos de audio en formato MP3 y transcribir su contenido a texto. A continuación, se describe el flujo de trabajo de la aplicación:

## 1. Inicialización del Estado
Al iniciar la aplicación, se establecen variables de estado en `st.session_state` para manejar la transcripción y el permiso para procesar audio.

## 2. Interfaz de Usuario
Se presenta un título y se solicita al usuario que seleccione el idioma del audio y cargue un archivo MP3. Si el archivo es válido y el usuario hace clic en "Procesar", se inicia el proceso de transcripción.

## 3. Transcripción del Audio
- Se convierte el archivo MP3 cargado en un objeto `AudioSegment`.
- Dependiendo del idioma seleccionado, se configura el asistente (`Asistente`) con el archivo y el idioma.
- Se llama al método `trabajar()` del asistente, que divide el audio en segmentos y los envía a una API de transcripción (Whisper de OpenAI) para su procesamiento.

## 4. Manejo de Errores
Si ocurre un error durante la transcripción, se muestra un mensaje de advertencia. Si la transcripción es exitosa, se marca el estado como transcrito.

## 5. Exportación de Resultados
Una vez que el audio ha sido transcrito, se ofrece al usuario la opción de exportar el texto transcrito en formatos TXT o PDF. Al seleccionar un formato, se genera el archivo correspondiente y se proporciona un botón para descargarlo.

## 6. Clase `Asistente`
Esta clase maneja la lógica de transcripción, incluyendo la división del audio en segmentos, la llamada a la API para la transcripción y la exportación de los resultados en diferentes formatos.
