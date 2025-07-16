from PIL import Image
import io
import base64

def image_to_base64(image: Image.Image) -> str:
    """Convert a PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def base64_to_image(img_base64: str) -> Image.Image:
    """Convert a base64 string to PIL Image"""
    image_data = base64.b64decode(img_base64)
    return Image.open(io.BytesIO(image_data))