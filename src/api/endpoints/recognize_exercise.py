import clip
import fastapi
import torch
from fastapi import APIRouter
from src.api.endpoints.generate_image_embedding import (
    device,
    generage_image_embedding,
    model,
)
from src.api.schemas.request import ImageClassificationRequest
from src.api.schemas.response import ImageClassifcationResponse, Prediction

router = fastapi.APIRouter()

# load pre computed text embeddings and labels
labels = [
    "a person standing",
    "a person repeating a squat",
    "a person repeating a jumping jack",
    "a person performing a plank",
]
texts = [f"This is {label}" for label in labels]
tokenized_text = clip.tokenize(texts).to(device)
text_features = model.encode_text(tokenized_text).type(torch.float32)
text_features /= text_features.norm(dim=-1, keepdim=True)


@router.post("")
def recognize_exercise(
    request: ImageClassificationRequest,
) -> ImageClassifcationResponse:
    """"""
    image_embedding = generage_image_embedding(request)
    image_features = torch.tensor(image_embedding.embedding).unsqueeze(0).to(device)
    image_features /= image_features.norm(dim=-1, keepdim=True)

    probabilities = (
        (100.0 * image_features @ text_features.T)
        .softmax(dim=-1)
        .detach()
        .cpu()
        .numpy()
        .flatten()
    )

    predictions = [
        Prediction(probability=prob, label=label)
        for prob, label in zip(probabilities, labels)
    ]

    response = ImageClassifcationResponse(predictions=predictions)

    return response
