# download images from csv file and upload images to google cloud.

!pip install google-cloud-storage

import os
import pandas as pd
import requests
from google.cloud import storage


os.getcwd()

# Read the CSV file
file_path = 'data/videos_by_channel.csv'
df = pd.read_csv(file_path)



# Function to download and upload images to GCS
def download_and_upload_images_to_gcs(dataframe, bucket_name):

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    for index, row in dataframe.iterrows():
        image_url = row['thumbnailUrl']
        video_id = row['videoId']

        # Download image from URL
        try:
            image_content = requests.get(image_url).content
        except Exception as e:
            print(f"Failed to download image from {image_url}: {str(e)}")
            continue

        # Upload image to GCS
        try:
            image_name = f"{video_id}.jpg"  # Assuming the image format is JPG
            blob = bucket.blob(image_name)
            blob.upload_from_string(image_content, content_type='image/jpeg')
            print(f"Uploaded {image_name} to {bucket_name}/{image_name}")
        except Exception as e:
            print(f"Failed to upload {image_name} to {bucket_name}: {str(e)}")


# Replace 'lewagon_bootcamp_jc' with your actual GCS bucket name
download_and_upload_images_to_gcs(df, 'lewagon_bootcamp_jc')



# process text from images already storaged in google cloud

!pip install google-cloud-vision pandas

from google.cloud import vision
from google.cloud.vision_v1 import types
from google.cloud import storage

# Initialize Google Cloud Vision client
client = vision.ImageAnnotatorClient()

# Function to process images using Vision API for OCR
def detect_text_in_image(image_uri):
    image = types.Image()
    image.source.image_uri = image_uri

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    else:
        return "No text found"

# Specify your bucket name
bucket_name = 'lewagon_bootcamp_jc'

# Initialize Google Cloud Storage client
storage_client = storage.Client()

# Get the bucket
bucket = storage_client.bucket(bucket_name)

# List all blobs (objects/images) in the bucket
blobs = bucket.list_blobs()

# Iterate over each image blob and process for text detection
for blob in blobs:
    image_uri = f"gs://{bucket_name}/{blob.name}"
    text = detect_text_in_image(image_uri)

    print(f"Image {blob.name}:")
    print(text)
    print("="*30)
