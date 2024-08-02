import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
import cv2
from io import BytesIO

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

    # Convert the enhanced image back to NumPy array for HDR enhancement
    sharp_image_np = np.array(sharp_image)

    # Apply HDR enhancement
    hdr_image_np = cv2.detailEnhance(sharp_image_np, sigma_s=10, sigma_r=0.15)

    # Convert back to PIL Image for displaying
    hdr_image = Image.fromarray(cv2.cvtColor(hdr_image_np, cv2.COLOR_BGR2RGB))

    return hdr_image

# Streamlit app
st.title('Adaptive Image Enhancement with HDR')
st.write('Upload an image to enhance it dynamically with HDR.')

# File upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the original image
    original_image = Image.open(uploaded_file)
    st.image(original_image, caption='Original Image', use_column_width=True)

    # Enhance the image
    enhanced_image = enhance_image_adaptive(original_image)

    # Display the enhanced image
    st.image(enhanced_image, caption='Enhanced Image with HDR', use_column_width=True)
