import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
import cv2
from io import BytesIO
import time

# Function to measure parameters
def measure_parameters(image_np):
    image_gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(image_gray)
    contrast = image_gray.std()
    sharpness = cv2.Laplacian(image_gray, cv2.CV_64F).var()
    blurness = cv2.Laplacian(image_gray, cv2.CV_64F).var()
    return blurness, brightness, contrast, sharpness

def get_image_category(brightness):
    if brightness < 50:
        return 'dark'
    elif brightness < 100:
        return 'normal'
    else:
        return 'bright'

def enhance_image_adaptive(image):
    # Convert to numpy array for measurement
    image_np = np.array(image)

    # Ensure the image is in RGB format for OpenCV processing
    image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Calculate original measurements
    blurness, brightness, contrast, sharpness = measure_parameters(image_np)

    # Determine image category
    category = get_image_category(brightness)

    # Defining ratios
    dark_ratios = {'brightness': 0.9411223551057959, 'contrast': 1.0227920227920229, 'sharpness': 0.01367602640116344}
    regular_ratios = {'brightness': 1.00420511622474, 'contrast': 1.0076833138466679, 'sharpness': 0.7218255991840898}
    bright_ratios = {'brightness': 0.9857360365413895, 'contrast': 1.0073332140940798, 'sharpness': 0.4813268137967491}

    if category == 'dark':
        ratios = dark_ratios
    elif category == 'normal':
        ratios = regular_ratios
    else:
        ratios = bright_ratios

    # Calculate dynamic enhancement parameters
    brightness_factor = ratios['brightness']
    contrast_factor = ratios['contrast']
    sharpness_factor = ratios['sharpness']

    # Enhance the brightness
    enhancer_brightness = ImageEnhance.Brightness(image)
    bright_image = enhancer_brightness.enhance(brightness_factor)

    # Enhance the contrast
    enhancer_contrast = ImageEnhance.Contrast(bright_image)
    contrast_image = enhancer_contrast.enhance(contrast_factor)

    # Enhance the sharpness
    enhancer_sharpness = ImageEnhance.Sharpness(contrast_image)
    sharp_image = enhancer_sharpness.enhance(sharpness_factor)

    # Convert the enhanced image back to NumPy array for further processing
    sharp_image_np = np.array(sharp_image)

    # Ensure the image is in BGR format for OpenCV processing
    sharp_image_np = cv2.cvtColor(sharp_image_np, cv2.COLOR_RGB2BGR)

    # Apply HDR enhancement
    hdr_image_np = cv2.detailEnhance(sharp_image_np, sigma_s=10, sigma_r=0.15)

    # Apply slight denoising for a smooth overall image
    denoised_image_np = cv2.fastNlMeansDenoisingColored(hdr_image_np, None, 10, 10, 7, 21)

    # Convert back to RGB format for displaying
    denoised_image_np = cv2.cvtColor(denoised_image_np, cv2.COLOR_BGR2RGB)

    # Convert back to PIL Image for displaying
    denoised_image = Image.fromarray(denoised_image_np)

    return denoised_image

# Initialize session state for image storage
if 'original_image' not in st.session_state:
    st.session_state['original_image'] = None
if 'enhanced_image' not in st.session_state:
    st.session_state['enhanced_image'] = None

# Streamlit app
st.title('Smart Adaptive Image Enhancer')
st.write('Upload an image to start enhancing!')

# Sidebar for clearing images
st.sidebar.title('Side Panel')
st.sidebar.header('Click the below button to clear images')
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
    with st.spinner('Enhancing image...'):
        # Simulate processing time
        time.sleep(2)
        # Enhance the image
        enhanced_image = enhance_image_adaptive(original_image)
        st.session_state['enhanced_image'] = enhanced_image

# Display the original and enhanced images side by side
if st.session_state['original_image'] and st.session_state['enhanced_image']:
    col1, col2 = st.columns(2)

    with col1:
        st.image(st.session_state['original_image'], caption='Original Image', use_column_width=True)

    with col2:
        st.image(st.session_state['enhanced_image'], caption='Enhanced Image with HDR and Denoising', use_column_width=True)

    # Popup reminder to clear images
    st.sidebar.warning('Remember to clear the images after reviewing to manage memory, failing to do so can risk to insufficient memory!')
