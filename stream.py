import streamlit as st
from openai import OpenAI

# Initialize the OpenAI client with your API key
client = OpenAI(api_key='')

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
        st.write(description)
