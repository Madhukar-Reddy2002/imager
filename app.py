import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import streamlit as st

def get_unsplash_images(search_term):
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

def get_adobe_stock_images(search_term):
    url = f'https://stock.adobe.com/in/search?k={search_term}&search_type=usertyped'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html')
    imgs = soup.find_all('img', class_='img')
    src = []
    for i in imgs[:]:
        item = i.get('src')
        if item.startswith('https://'):
            src.append(item)
    return list(set(src))

def display_images(image_urls):
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
                    st.markdown(
                        f"""
                        <div class="image-container">
                            <a href="{image_url}"><img src="{image_url}" class="image"></a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                print("Image dimensions are less than 200x200. Skipping display.")
        except (requests.exceptions.RequestException, OSError, Image.UnidentifiedImageError):
            print("Error processing the image. Skipping display.")

def main():
    st.set_page_config(page_title="Image Viewer", layout="wide")
    st.title("Image Viewer")

    st.markdown("""
        <style>
        .stApp {
            background-color: #000;
            font-family: 'Poppins', sans-serif;
        }
        .image-container {
            position: relative;
            display: inline-block;
            width: 100%;
            transition: transform 0.3s ease;
        }
        .image-container:hover {
            transform: scale(1.05);
        }
        .image {
            width: 100%;
            height: auto;
            display: block;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            animation: fade-in linear forwords;
            animation-timeline: view();
            animation-range : 250px 500px;
        }
                
        @keyframe  fade-in { from {scale:.8,  opacity: 0.5; } to   { scale:1, opacity: 1; }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    search_term = st.text_input("What photos do you want?", '')
    if search_term:
        unsplash_urls = get_unsplash_images(search_term)
        adobe_stock_urls = get_adobe_stock_images(search_term)
        all_urls = unsplash_urls + adobe_stock_urls
        display_images(all_urls)

if __name__ == "__main__":
    main()
