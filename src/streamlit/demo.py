from base64 import b64encode

import requests
from PIL import Image
from src.api.schemas.request import ImageClassificationRequest

import streamlit as st

API_ENDPOINT = "http://localhost:8000/recognize-exercise"
API_KEY = "exercise-recognition"
headers = {"API-Token": API_KEY}

st.set_page_config(page_title="Recognize Exercise via CLIP Model")
st.title("Exercise Recognition")
st.header("Recognize Exercise in Image")
st.markdown(
    """
Here we serve sample results for exercise recognition using [OpenAI's "zero-shot"
CLIP model](https://github.com/openai/CLIP). Current supported exercises:

1. "a person standing"
2. "a person repeating a squat"
3. "a person repeating a jumping jack"
4. "a person performing a plank"

The goal is to show off the API used to generate the demos in the gif below.
"""
)

# Display sample video result.
file_ = open("src/streamlit/assets/burpee.gif", "rb")
contents = file_.read()
data_url = b64encode(contents).decode("utf-8")
file_.close()
st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
    unsafe_allow_html=True,
)

image_file = st.file_uploader("Upload Image", type=["png", "jpeg", "jpg"])

if image_file:
    image = Image.open(image_file)
    st.image(image, use_column_width=True)

    encoded_image = b64encode(image_file.getvalue())

    request_data = ImageClassificationRequest(image_b64_encoded=encoded_image)
    response = requests.post(
        f"{API_ENDPOINT}", headers=headers, data=request_data.json()
    )

    if response.status_code == 200:
        out = response.json()
        out
    else:
        st.error("Exercise recognition service failed - likely a bug. Please submit")
