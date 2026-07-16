# AI OCR Document Scanner

## Project Overview

AI OCR Document Scanner is a basic image recognition project
developed as part of Artificial Intelligence Project 4.

The application extracts readable text from document images using
OpenCV image preprocessing and the Tesseract OCR engine.

## Objective

The objective is to build a functional OCR pipeline that can:

- Accept document images
- Preprocess visual input
- Extract readable text
- Calculate recognition confidence
- Display results clearly

## Features

- PNG, JPG and JPEG upload
- Grayscale image conversion
- Gaussian noise reduction
- Adaptive thresholding
- OCR text extraction
- Average confidence calculation
- 80% confidence validation
- Original and processed image preview
- Extracted text download
- Error handling

## Technologies Used

- Python
- Flask
- OpenCV
- Pytesseract
- Tesseract OCR
- Pillow
- NumPy
- HTML
- CSS

## Project Structure

```text
AI-OCR-Document-Scanner/
├── app.py
├── preprocessing.py
├── ocr_engine.py
├── requirements.txt
├── templates/
├── static/
├── samples/
└── screenshots/