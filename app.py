import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import streamlit as st

def get_image_urls(search_term):
    url = f'https://unsplash.com/s/photos/{search_term}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html')
    imgs = soup.find_all('img')
    src = []
    for i in imgs[:]:
        item = i.get('src')
        h = i.get('height')
        if not item.endswith('.svg'):
            if item.startswith("https://"):
                if (h != '16') and (h != '32'):
                    src.append(item)
    return list(set(src))

def display_images(image_urls):
    with st.container():
        st.title(f"Images for '{st.session_state.search_term}'")
        cols = st.columns(3)
        for i, image_url in enumerate(image_urls):
            try:
                response = requests.get(image_url, stream=True)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
                width, height = img.size
                print(f"Image dimensions: {width}x{height}")

                if width >= 200 and height >= 200:
                    with cols[i % 3]:
                        st.image(img, use_column_width=True)
                        st.markdown(f"<a href='{image_url}' download>Download</a>", unsafe_allow_html=True)
                else:
                    print("Image dimensions are less than 200x200. Skipping display.")
            except (requests.exceptions.RequestException, OSError, Image.UnidentifiedImageError):
                print("Error processing the image. Skipping display.")

def main():
    st.set_page_config(page_title="Image Viewer", layout="wide")
    st.title("Unsplash Image Viewer")

    if 'search_term' not in st.session_state:
        st.session_state.search_term = ''

    search_term = st.text_input("What photos do you want?", st.session_state.search_term)
    if search_term:
        st.session_state.search_term = search_term
        image_urls = get_image_urls(search_term)
        display_images(image_urls)

    st.markdown("""
        <style>
        .stApp {
            font-family: 'Poppins', sans-serif;
        }
        .stImage {
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        .stDownloadLink {
            font-size: 0.8rem;
            color: #666;
            text-decoration: none;
        }
        .stDownloadLink:hover {
            color: #333;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()