from PIL import Image
import io
import base64

def image_to_base64(uploadedImg) -> str:
    
    image = Image.open(uploadedImg)

    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()

    return base64.b64encode(img_bytes).decode('utf-8')