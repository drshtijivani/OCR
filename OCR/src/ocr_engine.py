import easyocr

# Initialize reader
reader = easyocr.Reader(['en'], gpu=False)

def get_text_from_image(processed_image):
    """
    Runs EasyOCR.
    Returns: List of tuples -> [(bbox, text, confidence), ...]
    """
    try:
        # detail=1 gives us coordinates, text, and confidence level
        results = reader.readtext(processed_image, detail=1)
        return results
    except Exception as e:
        print(f"Error in OCR Engine: {e}")
        return []