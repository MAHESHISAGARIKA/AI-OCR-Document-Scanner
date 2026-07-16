import os
from pathlib import Path

import pytesseract
from PIL import Image
from pytesseract import Output


def configure_tesseract() -> None:
    """
    Configure the Tesseract executable location on Windows.
    """

    environment_path = os.getenv("TESSERACT_CMD")

    default_windows_path = Path(
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

    if environment_path:
        pytesseract.pytesseract.tesseract_cmd = environment_path
    elif default_windows_path.exists():
        pytesseract.pytesseract.tesseract_cmd = str(
            default_windows_path
        )


configure_tesseract()


def extract_text_and_confidence(image_path: str) -> dict:
    """
    Extract text from the image and calculate the average
    confidence of the detected words.
    """

    image = Image.open(image_path)

    # OEM 3 lets Tesseract choose the available OCR engine.
    # PSM 6 assumes the image contains a uniform block of text.
    configuration = "--oem 3 --psm 6"

    extracted_text = pytesseract.image_to_string(
        image,
        config=configuration,
    ).strip()

    recognition_data = pytesseract.image_to_data(
        image,
        output_type=Output.DICT,
        config=configuration,
    )

    confidence_scores = []

    for word, confidence in zip(
        recognition_data["text"],
        recognition_data["conf"],
    ):
        if not word.strip():
            continue

        try:
            confidence_value = float(confidence)
        except (TypeError, ValueError):
            continue

        if confidence_value >= 0:
            confidence_scores.append(confidence_value)

    if confidence_scores:
        average_confidence = round(
            sum(confidence_scores) / len(confidence_scores),
            2,
        )
    else:
        average_confidence = 0.0

    if not extracted_text:
        extracted_text = "No readable text was detected."

    return {
        "text": extracted_text,
        "confidence": average_confidence,
        "passed": average_confidence >= 80,
        "detected_word_count": len(confidence_scores),
    }