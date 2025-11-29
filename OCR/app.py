import streamlit as st
import numpy as np
import cv2
from src.preprocessing import preprocess_image
from src.ocr_engine import get_text_from_image
from src.text_extraction import extract_target_line

# Page Config
st.set_page_config(page_title="OCR Assessment", layout="wide")

# --- SESSION STATE ---
if 'rotation' not in st.session_state:
    st.session_state['rotation'] = 0

def rotate_image_by_angle(image, angle):
    if angle == 0: return image
    elif angle == 90: return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180: return cv2.rotate(image, cv2.ROTATE_180)
    elif angle == 270: return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return image

# --- UI ---
st.title("Shipping Label OCR Tool")
st.markdown("1. Upload -> 2. Rotate -> 3. Extract")

uploaded_file = st.file_uploader("Upload Label", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Load
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    original_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Rotate
    current_angle = st.session_state['rotation'] % 360
    rotated_image = rotate_image_by_angle(original_image, current_angle)

    # Layout
    col_left, col_right = st.columns([1, 1], gap="medium")

    with col_left:
        st.subheader("1. Setup Image")
        st.image(cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB), caption=f'Rotation: {current_angle}°', use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("↺ Left"):
                st.session_state['rotation'] -= 90
                st.rerun()
        with c2:
            if st.button("↻ Right"):
                st.session_state['rotation'] += 90
                st.rerun()

    with col_right:
        st.subheader("2. Extraction Results")
        if st.button("Extract Data", type="primary", use_container_width=True):
            with st.spinner('Extracting the id...'):
                
                # A. Preprocess (CLAHE + Upscale)
                processed_img = preprocess_image(rotated_image)
                
                # --- NEW: Display Processed Image Side-by-Side (in Right Column) ---
                st.image(processed_img, caption='Processed Image (Enhanced)', use_container_width=True, channels='GRAY')
                
                # B. OCR
                ocr_results = get_text_from_image(processed_img)
                
                # C. Extract
                found_text, found_conf = extract_target_line(ocr_results)

                # D. Results
                st.divider()
                if found_text:
                    st.success("Target ID Found!")
                    st.metric("Extracted ID", found_text)
                    st.caption(f"Confidence: {found_conf:.2%}")
                else:
                    st.error("Pattern not found.")
                    st.info("Ensure text is horizontal.")

                
                # DEBUG SECTION
                with st.expander("🔍 Debug: Raw OCR Output"):
                    st.write("Raw Text Detected:")
                    for item in ocr_results:
                        st.text(item[1])