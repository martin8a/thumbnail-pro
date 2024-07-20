import streamlit as st

import numpy as np
import pandas as pd
import time
from PIL import Image
import os
import json
import base64
import io
import modelbit
from get_data_from_model import get_thumbnail_pro_model
from process_image import image_to_base64
from get_data_from_model import get_recommendations_llava

os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'
api_token = os.environ['HUGGINGFACEHUB_API_TOKEN']

from huggingface_hub.inference_api import InferenceApi


# URL del modelo
model_url = "https://api-inference.huggingface.co/models/llava-hf/llava-v1.6-mistral-7b-hf"

headers = {
    "Authorization": f"Bearer {api_token}"
}

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

            # Display the uploaded image
            st.image(thumbnail, caption='Uploaded Thumbnail', use_column_width=True)

            # Here you would add the code to process the data and give feedback
            st.success("Data submitted successfully! Analyzing the performance...")

            # Convertir la imagen a bytes
            img_base64 = image_to_base64(thumbnail)
            scoreData = get_thumbnail_pro_model(title, 'https://i.ytimg.com/vi/BEAm5lUn70M/mqdefault.jpg')
            st.write(scoreData['classification'])
            st.write(scoreData['score'])
            
            recommendations = get_recommendations_llava(title, 'https://i.ytimg.com/vi/BEAm5lUn70M/mqdefault.jpg')

            print('Modelo corriendo')
            st.write(recommendations)

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
