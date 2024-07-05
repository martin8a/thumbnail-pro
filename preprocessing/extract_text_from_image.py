from io import BytesIO
from google.cloud import vision
from PIL import Image
import requests
import pandas as pd
import os

dir_root = os.path.dirname(os.path.dirname(__file__))
dir_path = os.path.join(dir_root , 'data')
df = pd.read_csv(dir_path + '/prefinal_data.csv')
texts = []
imagenes = []

def text_from_image_in_df(df: pd.DataFrame):
    print('Leyendo archivo')
    for index, row in df.iterrows():
        image = download_image(row['thumbnailUrl'])
        text = extract_text_from_image(image)
        texts.append(text)
    df['text'] = text
    #df.iloc[:, 'text'] = text
    print('Sobreescribiendo archivo')

    df.to_csv(dir_path + '/prefinal_data.csv')
    print('Archivo almacenado con exito')

def download_image(url):
    print('Descargando imagen')
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert("RGB")
        print('Imagen descargada')
        return img
    except Exception as e:
        print(f"Error al abrir {url}: {e}")
        return None

# Función para extraer texto de una imagen usando Vertex AI OCR
def extract_text_from_image(image):
    vision_client = vision.ImageAnnotatorClient()
    try:
        print('Extrayendo texto')
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
        print('Texto extraido exitosamente')

        return texts[0].description if texts else None
    except Exception as e:
        print(f"Error al extraer texto: {e}")
        return None

if __name__ == '__main__':
    text_from_image_in_df(df)
