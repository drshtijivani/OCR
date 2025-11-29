import cv2
import numpy as np

def preprocess_image(input_image):
    """
    Advanced Preprocessing with LINE THICKENING.
    
    Features:
    1. Grayscale Conversion.
    2. CLAHE: Boosts contrast so faint text pops against the background.
    3. Lanczos Upscaling: High-quality zoom (2x) to help OCR read small text.
    4. Morphological Erosion: Physically thickens dark lines (text/underscores) 
       so the OCR engine doesn't miss them.
    """
    # Convert file upload to OpenCV format
    if not isinstance(input_image, np.ndarray):
        file_bytes = np.asarray(bytearray(input_image.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    else:
        img = input_image

    # 1. Convert to Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. CLAHE (Contrast Limited Adaptive Histogram Equalization)
    # This is better than global thresholding for shiny/uneven lighting.
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)

    # 3. High-Quality Upscaling
    # resize 2x using Lanczos4 (best quality) to make text clearer.
    scaled = cv2.resize(enhanced, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_LANCZOS4)

    # 4. Morphological Thickening (Erosion)
    # In OpenCV grayscale, 'Erosion' eats away the white background, 
    # making the black text/lines THICKER.
    kernel = np.ones((2,2), np.uint8)
    thickened = cv2.erode(scaled, kernel, iterations=1)

    # Return the processed grayscale image
    return thickened