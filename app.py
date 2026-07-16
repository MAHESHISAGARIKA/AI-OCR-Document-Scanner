from pathlib import Path
import uuid

from flask import Flask, flash, render_template, request
from werkzeug.utils import secure_filename

from ocr_engine import extract_text_and_confidence
from preprocessing import preprocess_image


BASE_DIRECTORY = Path(__file__).resolve().parent

UPLOAD_FOLDER = BASE_DIRECTORY / "static" / "uploads"
OUTPUT_FOLDER = BASE_DIRECTORY / "static" / "outputs"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


app = Flask(__name__)

# Used by Flask to display flash messages.
app.secret_key = "ai-ocr-document-scanner-secret-key"

# Maximum upload size: 10 MB.
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


def allowed_file(filename: str) -> bool:
    """
    Check whether the uploaded file has an allowed extension.
    """

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        uploaded_file = request.files.get("image")

        if uploaded_file is None:
            flash("Please choose an image before submitting.")
            return render_template("index.html", result=None)

        if uploaded_file.filename == "":
            flash("No image was selected.")
            return render_template("index.html", result=None)

        if not allowed_file(uploaded_file.filename):
            flash(
                "Invalid file type. Please upload a PNG, JPG "
                "or JPEG image."
            )
            return render_template("index.html", result=None)

        try:
            safe_original_name = secure_filename(
                uploaded_file.filename
            )

            extension = safe_original_name.rsplit(".", 1)[1].lower()

            unique_identifier = uuid.uuid4().hex

            uploaded_filename = (
                f"{unique_identifier}.{extension}"
            )

            processed_filename = (
                f"processed_{unique_identifier}.png"
            )

            text_filename = (
                f"extracted_text_{unique_identifier}.txt"
            )

            uploaded_path = UPLOAD_FOLDER / uploaded_filename
            processed_path = OUTPUT_FOLDER / processed_filename
            text_path = OUTPUT_FOLDER / text_filename

            uploaded_file.save(uploaded_path)

            preprocess_image(
                str(uploaded_path),
                str(processed_path),
            )

            ocr_result = extract_text_and_confidence(
                str(processed_path)
            )

            text_path.write_text(
                ocr_result["text"],
                encoding="utf-8",
            )

            result = {
                "original_image": (
                    f"uploads/{uploaded_filename}"
                ),
                "processed_image": (
                    f"outputs/{processed_filename}"
                ),
                "text_file": (
                    f"outputs/{text_filename}"
                ),
                "text": ocr_result["text"],
                "confidence": ocr_result["confidence"],
                "passed": ocr_result["passed"],
                "detected_word_count": (
                    ocr_result["detected_word_count"]
                ),
            }

        except Exception as error:
            flash(f"Processing failed: {error}")

    return render_template(
        "index.html",
        result=result,
    )


@app.errorhandler(413)
def file_too_large(_error):
    flash("The uploaded image is too large. Maximum size is 10 MB.")

    return render_template(
        "index.html",
        result=None,
    ), 413


if __name__ == "__main__":
    app.run(debug=True)