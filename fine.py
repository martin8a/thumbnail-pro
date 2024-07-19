import streamlit as st
from openai import OpenAI
from transformers import CLIPProcessor, CLIPModel
import torch
from PIL import Image
import requests
from sklearn.metrics.pairwise import cosine_similarity

# Initialize the OpenAI client with your API key
client = OpenAI(api_key='')

# Initialize the CLIP model and processor
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def get_image_features(image_url):
    image = Image.open(requests.get(image_url, stream=True).raw)
    inputs = clip_processor(images=image, return_tensors="pt")
    return clip_model.get_image_features(**inputs).detach()

def score_description(image_features, generated_description):
    inputs = clip_processor(text=generated_description, return_tensors="pt")
    description_features = clip_model.get_text_features(**inputs).detach()
    return cosine_similarity(image_features, description_features).item()

# Streamlit app
st.title("Image Description with OpenAI GPT-4")

st.write("Enter the URL of an image, and the model will describe it for you.")

image_url = st.text_input("Image URL")

if image_url:
    with st.spinner('Generating description...'):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What’s in this image?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        description = response.choices[0].message.content
        st.write("Generated Description:", description)

        # Get image features and score the description
        image_features = get_image_features(image_url)
        score = score_description(image_features, description)
        st.write("Score:", score)
