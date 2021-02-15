from typing import List

from pydantic import BaseModel


class EmbeddingResponse(BaseModel):
    embedding_type: str
    embedding: List[float]


class Prediction(BaseModel):
    probability: float
    label: str


class ImageClassifcationResponse(BaseModel):
    predictions: List[Prediction]
