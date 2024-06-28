from io import BytesIO
from google.cloud import vision
from PIL import Image
import requests
import pandas as pd


df = pd.read_csv('../data/videos_by_channel.csv')
texts = []
imagenes = []

# Función para extraer texto de una imagen usando Vertex AI OCR
def extract_text_from_image(image):
    try:
        #buffer de memoria para almacenar datos binarios (de la imagen)
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        content = buffered.getvalue()

        vision_image = vision.Image(content=content)
        #deteccion de texto en la imagen
        response = vision_client.text_detection(image=vision_image)
        #anotaciones de texto de la deteccion
        texts = response.text_annotations

        if response.error.message:
            raise Exception(response.error.message)

        return texts[0].description if texts else None
    except Exception as e:
        print(f"Error al extraer texto: {e}")
        return None


for url in df['thumbnailUrl']:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    imagenes.append(img)

    extracted_text = extract_text_from_image(img)
    texts.append(extracted_text)
