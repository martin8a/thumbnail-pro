from io import BytesIO
from google.cloud import vision
from PIL import Image
import requests
import pandas as pd


df = pd.read_csv('../data/videos_by_channel.csv')
texts = []
imagenes = []

def text_from_image_in_df(df: pd.DataFrame):
    for video in df:
        image = download_image(video['thumbnailUrl'])
        text = extract_text_from_image(image)
        df['text'] = text

def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert("RGB")
        return img
    except Exception as e:
        print(f"Error al abrir {url}: {e}")
        return None

# Función para extraer texto de una imagen usando Vertex AI OCR
def extract_text_from_image(image):
    vision_client = vision.ImageAnnotatorClient()
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
