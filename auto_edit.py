import streamlit as st
from PIL import Image
import numpy as np
import cv2
from io import BytesIO
import time
import requests 

# Function to apply HDR enhancement
def enhance_image_hdr(image):
    try:
        # Convert to numpy array for OpenCV processing
        image_np = np.array(image)

        # Ensure the image is in RGB format for OpenCV processing
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Apply HDR enhancement
        hdr_image_np = cv2.detailEnhance(image_np, sigma_s=10, sigma_r=0.15)

        # Convert back to RGB format for displaying
        hdr_image_np = cv2.cvtColor(hdr_image_np, cv2.COLOR_BGR2RGB)

        # Convert back to PIL Image for displaying
        hdr_image = Image.fromarray(hdr_image_np)

        return hdr_image
    except Exception as e:
        st.error(f"Error during HDR enhancement: {e}")
        return image

# Initialize session state for image storage
if 'original_image' not in st.session_state:
    st.session_state['original_image'] = None
if 'enhanced_image' not in st.session_state:
    st.session_state['enhanced_image'] = None

# Streamlit app
st.title('HDR Image Enhancer')
st.header('Upload an image to apply HDR enhancement!')

# Sidebar

# Fetch and display image from GitHub in sidebar
try:
    response = requests.get('https://github.com/KirtanTankRed/image_auto_edit/blob/main/source/Red_logo_transparent.png?raw=true')
    response.raise_for_status()  # Check if the request was successful
    image_data = BytesIO(response.content)
    sidebar_image = Image.open(image_data)
    st.sidebar.image(sidebar_image, caption='Sample Image from GitHub', use_column_width=True)
except (requests.exceptions.RequestException, UnidentifiedImageError) as e:
    st.sidebar.error(f"Failed to load image from GitHub: {e}")

st.sidebar.title('🎛️ Side Panel')
st.sidebar.header('🗑️ Click the below button to clear images')
if st.sidebar.button('Clear Images'):
    st.session_state['original_image'] = None
    st.session_state['enhanced_image'] = None
    st.sidebar.success('Images cleared successfully.')

# File upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the original image
    original_image = Image.open(uploaded_file)
    st.session_state['original_image'] = original_image

    # Show a spinner while processing
    with st.spinner('Applying HDR enhancement to your image 🪄'):
        # Simulate processing time
        time.sleep(2)
        # Enhance the image
        enhanced_image = enhance_image_hdr(original_image)
        st.session_state['enhanced_image'] = enhanced_image

# Display the original and enhanced images side by side
if st.session_state['original_image'] and st.session_state['enhanced_image']:
    col1, col2 = st.columns(2)

    with col1:
        st.image(st.session_state['original_image'], caption='Original Image 🖼️', use_column_width=True)

    with col2:
        st.image(st.session_state['enhanced_image'], caption='HDR Enhanced Image ✨', use_column_width=True)

    # Popup reminder to clear images
    st.sidebar.warning('ℹ️ Remember to clear the images after reviewing to manage memory!')
st.sidebar.warning("""⚠️ This is a prototype for demonstration purposes and is not at production capacity which offers limited trials.          
🔧 In case of breakdown, please reboot the app or contact the developer.""")
