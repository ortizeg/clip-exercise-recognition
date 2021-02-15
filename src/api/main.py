from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.security.api_key import APIKeyHeader, APIKeyQuery
from src.api.endpoints import generate_image_embedding, recognize_exercise
from starlette_prometheus import PrometheusMiddleware, metrics

API_KEY = "exercise-recognition"
API_KEY_NAME = "access_token"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_token_header(api_token: str = Header(...)):
    if api_token != API_KEY:
        raise HTTPException(status_code=400, detail="API-Token header invalid")


app = FastAPI(
    title="Still-Image based Exercise Recognition",
    description="""API for testing CLIP model against several exercise categories.""",
)

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", metrics)

app.include_router(
    recognize_exercise.router,
    prefix="/recognize-exercise",
    tags=["inference"],
    dependencies=[Depends(get_token_header)],
)

app.include_router(
    generate_image_embedding.router,
    prefix="/generate-image-embedding",
    tags=["inference"],
    dependencies=[Depends(get_token_header)],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8004)
