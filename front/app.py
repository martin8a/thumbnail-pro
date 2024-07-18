import streamlit as st

import numpy as np
import pandas as pd
import time
from PIL import Image
import os
import json
import base64
import io
from transformers import AutoTokenizer, pipeline
# Load model directly
from transformers import AutoModelForCausalLM
from transformers import AutoProcessor, AutoModelForPreTraining
## #model = AutoModelForCausalLM.from_pretrained("Ridealist/llava-v1.6-mistral-7b-chess-finetuned")
## processor = AutoProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")
## model = AutoModelForPreTraining.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")

import requests

#def query(payload, title, keywords, thumbnail):
#    API_URL = "https://api-inference.huggingface.co/models/llava-v1.6-mistral-7b-chess-finetuned"
#    headers = {"Authorization": f"Bearer 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"}
#    response = requests.post(API_URL, headers=headers, json=payload)
#    return response.json()
# from archivo del modelo import *

##Constants
#saved_model_path =
#
## Load model (Cached)
#@st.cache_resource
#def load_model():
#    return load(saved_model_path)

os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'
api_token = os.environ['HUGGINGFACEHUB_API_TOKEN']

from huggingface_hub.inference_api import InferenceApi

#model_api = InferenceApi(
#    repo_id = "llava-hf/llava-v1.6-mistral-7b-hf",
#    token = api_token
#)

# URL del modelo
model_url = "https://api-inference.huggingface.co/models/llava-hf/llava-v1.6-mistral-7b-hf"

headers = {
    "Authorization": f"Bearer {api_token}"
}

#def results(title, keywords, thumbnail):
    #thmb = model.load('llava')
#    return model_api(inputs = [title, keywords, thumbnail])
    #return query({"title": title, "keywords": keywords, "thumbnail": thumbnail})

def main():
    # Caracteristicas basicas de la pagina
    st.set_page_config(page_icon='', page_title = 'Thumbnail-Pro')
    st.markdown('# Thumbnail-Pro')
    st.markdown('## Make your videos **stand out!**')
    st.image('https://i.ytimg.com/vi/BEAm5lUn70M/maxresdefault.jpg', width=600)

    ## Instrucciones
    st.markdown('### - Instrucciones:')

    left_column, mid_column, right_column = st.columns(3, vertical_alignment = 'top')
    # You can use a column just like st.sidebar:

    with left_column:
        with st.container(height= 285, border=True):
            st.markdown('**1.** Seleccionar Thumbnail:\n')
            st.markdown('- Escoge la imagen del thumbnail que quieres analizar.\n')
            st.markdown('- Asegúrate de que la imagen esté en formato JPG, JPEG, o PNG.')

    with mid_column:
        with st.container(height= 285, border=True):
            st.markdown('**2.** Escribir Título:\n')
            st.markdown('- Escribe el título del video.\n')
            st.markdown('- Asegúrate de que el título sea claro y atractivo.')

    with right_column:
        with st.container(height= 285, border=True):
            st.markdown('**3.** Añadir Palabras Clave (Opcional):\n')
            st.markdown('- Incluye palabras clave relevantes para tu video.\n')
            st.markdown('- Estas palabras ayudarán a mejorar la precisión de las predicciones.')


    # Create a form
    with st.form(key='thumbnail_form'):
        # Title input
        title = st.text_input("Enter the video title:")

        # Keywords input
        keywords = st.text_input("Enter the keywords (comma-separated):")

        # Image upload
        thumbnail = st.file_uploader("Upload the thumbnail image (JPEG or PNG):", type=["jpg", "jpeg", "png"])

        # Boton para imprimir resultados del modelo
        submit_button = st.form_submit_button(label='Submit')

    # Process the form data
    if submit_button:
        if not title:
            st.error("Please enter a video title.")
        if not thumbnail:
            st.error("Please upload a thumbnail image.")
        if not keywords:
            st.error("Please enter keywords.")

        if title and thumbnail and keywords:
            # Display the inputs
            st.write("### Submitted Data")
            st.write(f"**Title:** {title}")
            st.write(f"**Keywords:** {keywords.split(',')}")

            # Display the uploaded image
            st.image(thumbnail, caption='Uploaded Thumbnail', use_column_width=True)

            # Here you would add the code to process the data and give feedback
            st.success("Data submitted successfully! Analyzing the performance...")

    #Mandar los resultados de la foto, texto, titulo
    # Leer la imagen
    image = Image.open(thumbnail)

    # Convertir la imagen a bytes
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()

    # Codificar la imagen en base64 (opcional)
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        # Preparar los datos para la API
    inputs = {
        "title": title,
        "keywords": keywords,
        "image": img_base64
    }

    ##AQUI PONER EL MODELO!!!!!!!
    #response = model_api(inputs = inputs)
    response = requests.get(model_url, headers=headers, json=inputs, timeout=3600).json()
    print('Modelo corriendo')
    st.write(response)

    ### Barra de carga del progreso
    #'Starting a long computation...'
    ## Add a placeholder
    #latest_iteration = st.empty()
    #bar = st.progress(0)
    #for i in range(100):
    #    # Update the progress bar with each iteration.
    #    latest_iteration.text(f'Iteration {i+1}')
    #    bar.progress(i + 1)
    #    time.sleep(0.1)
    #'...and now we\'re done!'
## Cuando se aplaste el boton enviar el input al modelo
# (procesar imagen y subir a algun lado) y despues pasarle al modelo
# Cuando se pase al modelo, el modelo me va a retornar un score que lo debo presentar en algun tipo de chart

if __name__=='__main__':
    main()
