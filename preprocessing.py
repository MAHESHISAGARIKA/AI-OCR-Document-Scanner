from pathlib import Path

import cv2


def preprocess_image(input_path: str, output_path: str) -> str:
    """
    Convert the input image into a cleaner black-and-white image
    suitable for OCR.
    """

    image = cv2.imread(input_path)

    if image is None:
        raise ValueError("The uploaded file could not be read as an image.")

    # Step 1: Convert the RGB image into grayscale.
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 2: Reduce small noise using Gaussian blur.
    blurred_image = cv2.GaussianBlur(
        grayscale_image,
        (5, 5),
        0,
    )

    # Step 3: Convert the image into clear black and white.
    threshold_image = cv2.adaptiveThreshold(
        blurred_image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15,
    )

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    saved = cv2.imwrite(output_path, threshold_image)

    if not saved:
        raise IOError("The processed image could not be saved.")

    return output_path