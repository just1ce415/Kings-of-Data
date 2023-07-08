import requests
import streamlit as st
import numpy as np
from PIL import Image


st.set_page_config(layout="wide")
api_endpoint = "http://api:8000/are_similar"

def resize_image(image, max_size=256):
    img = Image.fromarray(image)
    img.thumbnail((max_size, max_size))
    return np.array(img)

def are_similar(image1: np.ndarray, image2: np.ndarray):
    payload = {"image1": image1.tolist(), "image2": image2.tolist()}
    response = requests.post(api_endpoint, json=payload, verify=False)
    result = response.json()["response"]

    return result

def main():
    st.title("ЛУН – Image Similarity Checker")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Upload Image 1")
        uploaded_file1 = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"], key=1)
        image1 = None
        if uploaded_file1 is not None:
            image1 = np.array(Image.open(uploaded_file1))
            image1 = resize_image(image1, 512)

    with col2:
        st.subheader("Upload Image 2")
        uploaded_file2 = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"], key=2)
        image2 = None
        if uploaded_file2 is not None:
            image2 = np.array(Image.open(uploaded_file2))
            image2 = resize_image(image2, 512)

    if image1 is not None and image2 is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.image(image1, caption="Image 1", 
            )
        with col2:
            st.image(image2, caption="Image 2", 
            )

    if st.button("Check Similarity"):
        if image1 is None or image2 is None:
            st.error("Please upload both images.")
        else:
            result = are_similar(image1, image2)

            if result == 1:
                st.error("The images are similar.")
            else:
                st.success("The images are not similar.")

if __name__ == "__main__":
    main()
