Automated OCR Text Extraction for Shipping Labels


for better view drive link: https://drive.google.com/file/d/17Ggj5WUHd9bnZo3_7xfo9A6GVeYedAgS/view?usp=sharing

Project Title

Automated OCR Text Extraction for Shipping Labels

Objective / Purpose

The primary objective of this project is to develop an automated Optical Character Recognition (OCR) system capable of extracting specific Waybill/Order IDs from shipping label images with high accuracy (>75%). The goal is to eliminate manual data entry by reliably processing real-world "dirty data" that suffers from noise, blur, rotation, and complex layouts.

Project Description

This project implements a robust computer vision pipeline designed to parse complex shipping labels. It moves beyond simple text recognition by integrating advanced image preprocessing techniques (such as CLAHE and Morphological Erosion) to make faint text visible. The system utilizes EasyOCR for deep learning-based text detection and applies intelligent, context-aware logic to reconstruct split IDs and distinguish target data from barcodes. The solution is deployed as an interactive Streamlit web application, allowing users to upload images, adjust orientation, and extract data in real-time.

Key Features

High Accuracy: Achieves >84% accuracy on noisy datasets by using advanced image enhancement to restore faint characters.

Robust Extraction: Successfully handles edge cases such as rotated text, missing underscores, and IDs split across multiple lines.

Context-Aware Logic: Distinguishes between target IDs and random numbers (like barcodes) by prioritizing text found near keywords like "Order ID".

Interactive UI: A user-friendly interface that provides manual rotation controls and a "Debug View" to visualize how the AI sees the image.

Tech Stack

Programming Language: Python 3.8+

OCR Engine: EasyOCR (Deep Learning-based)

Image Processing: OpenCV (cv2), NumPy

Web Framework: Streamlit

Data Analysis: Pandas





Installation Instructions

Prerequisites

Python 3.8 or higher installed on your system.

pip (Python package installer).

Git (optional, for cloning the repository).

Step-by-Step Setup Guide

Clone the Repository
Open your terminal or command prompt and run:

git clone https://github.com/drshtijivani/OCR
cd ocr


(Alternatively, download the project ZIP file and extract it.)

Create a Virtual Environment (Recommended)
It is best practice to use a virtual environment to avoid conflicts with other projects.

Windows:

python -m venv venv
venv\Scripts\activate


Mac/Linux:

python3 -m venv venv
source venv/bin/activate


Install Dependencies
Install all required libraries using pip:

pip install -r requirements.txt


Note: This may take a few minutes as it downloads the EasyOCR models.

Run the Application
Launch the Streamlit web interface:

streamlit run app.py


The application should automatically open in your default web browser at http://localhost:8501.

1. OCR Method / Model Used
Model: We used EasyOCR.

Why?

It is a deep-learning-based OCR engine (unlike older tools like Tesseract).

It uses a two-stage pipeline:

CRAFT (Character Region Awareness for Text Detection): This neural network finds where the text is in the image (the bounding boxes).

CRNN (Convolutional Recurrent Neural Network): This network reads the characters inside those boxes.

This combination makes it very robust for "scene text" (text in the wild, on messy papers) compared to simple document scanners.

2. Preprocessing Techniques
We applied a custom "High-Definition" pipeline in src/preprocessing.py to handle the specific challenges of shipping labels (glare, noise, faint ink).

Grayscale Conversion: We convert the image to black and white (grayscale) to remove color distractions. The AI only cares about light vs. dark patterns.

CLAHE (Contrast Limited Adaptive Histogram Equalization):

Problem: Shipping labels often have "hot spots" (shiny glare) where text washes out.

Solution: CLAHE boosts contrast locally. It looks at small tiles of the image and fixes the contrast in just that tile. This makes faint underscores (_) pop out even in bright areas.

Lanczos4 Upscaling:

Problem: The ID number is often printed very small.

Solution: We resize the image to 2x its original size using Lanczos interpolation (a high-quality resizing math). This gives the OCR engine more pixels to analyze for each letter.

Morphological Erosion (Thickening):

Problem: The critical underscore (_) is often just 1 pixel thick and gets lost.

Solution: We apply "Erosion". In image processing terms (assuming black text on white paper), eroding the white background makes the black text thicker. This physically expands the lines so the AI cannot miss them.

3. Text Extraction Logic
Regex (Regular Expressions) alone wasn't enough because OCR makes mistakes (like reading 1 as I or l, or missing the _). We used a multi-layered logic in src/text_extraction.py:

Context-Aware Search (The "Smart" Layer):

Instead of blindly scanning the whole page, the code first searches for keywords like "Order ID", "Waybill", "FTPL", or "RVP".

It only validates 18-digit numbers found immediately after these keywords. This prevents the system from accidentally picking up a barcode number.

Robust Regex Pattern:

We designed a regex that is "forgiving".

It looks for 18 digits (\d{18}).

It allows the separator to be a dash, underscore, or even a space ([_\-\s]).

It accepts common OCR typos for the digit '1' (like l, I, i, |).

Auto-Correction/Reconstruction:

If the OCR engine splits the ID into two lines (e.g., 1621... on line 1 and ...vrw on line 2), our code detects the 18-digit "anchor" and automatically looks at the next line to find the suffix.

It then reconstructs the ID into the standard format: 18Digits_1_Suffix.

Performance Metrics

An extensive evaluation was conducted on a test set of 27 shipping label images, representing diverse conditions (blur, rotation, noise).

Summary Results

Total Images: 27

Passed (Valid Extraction): 20

Success Rate (on legible images): ~85%


Challenges & Solutions

Challenge

Solution

Rotated Images

OCR fails on vertical text. Added Manual Rotation UI to allow users to correct orientation before processing.

Invisible Underscores

Faint separators (_) were lost. Implemented CLAHE and Morphological Erosion to physically thicken lines in the image data.

Split IDs

Long IDs were broken into two lines. Created a Fallback Strategy to merge adjacent text lines and search for ID patterns across breaks.

Barcode Confusion

Barcode numbers look like IDs. Implemented Context-Aware Logic to prioritize text near specific keywords ("Order ID", "FTPL") over random numbers.

Future Improvements

Auto-Rotation: Integrate a model (like Tesseract OSD) to automatically detect and correct image orientation.

Fine-Tuning: Train a custom CRNN model specifically on shipping label fonts to improve recognition of specific characters (like 1 vs I).


