from pydantic import BaseModel


class ImageEmbeddingRequest(BaseModel):
    image_b64_encoded: str


class ImageClassificationRequest(BaseModel):
    image_b64_encoded: str
