from base64 import b64decode
import io

from PIL import Image

from src.api.schemas.request import ImageEmbeddingRequest


def decode_image(request: ImageEmbeddingRequest) -> Image:
    image = b64decode(request.image_b64_encoded)

    image_buffer = io.BytesIO()
    image_buffer.write(image)
    image = Image.open(image_buffer).convert("RGB")

    return image
