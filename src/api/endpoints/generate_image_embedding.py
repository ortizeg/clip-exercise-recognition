import clip
import numpy as np
import torch
from fastapi import APIRouter
from src.api.schemas.request import ImageEmbeddingRequest
from src.api.schemas.response import EmbeddingResponse
from src.api.utils.image import decode_image

router = APIRouter()

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)


@router.post("")
def generage_image_embedding(
    request: ImageEmbeddingRequest,
) -> EmbeddingResponse:
    """
    Pre-process and run image through CLIP embedding model. This is a lower-level API.
    """
    # load and preprocess image
    image = decode_image(request)
    image = preprocess(image).unsqueeze(0).to(device)

    # run image through clip model
    with torch.no_grad():
        embedding = model.encode_image(image).cpu().numpy().flatten().tolist()

    # generate response
    response = EmbeddingResponse(embedding=embedding, embedding_type="visual")

    return response
