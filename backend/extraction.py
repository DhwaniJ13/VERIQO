import fitz
from PIL import Image
import pytesseract
from pathlib import Path

# telling pytesseract where Tesseract OCR is installed
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# extracting text from a document
def extract_text(file_path):
    file_extension = Path(file_path).suffix.lower()

    if file_extension == ".pdf":
        document = fitz.open(file_path)
        text = "\n".join(page.get_text() for page in document)
        document.close()

        if text.strip():
            return text

        return extract_pdf_with_ocr(file_path)

    if file_extension in {".png", ".jpg", ".jpeg"}:
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)

    if file_extension == ".txt":
        return Path(file_path).read_text(encoding="utf-8")

    raise ValueError("Unsupported document format")


# extracting text from scanned PDF using OCR
def extract_pdf_with_ocr(file_path):
    document = fitz.open(file_path)
    text = ""

    for page in document:
        pixmap = page.get_pixmap()

        image = Image.frombytes(
            "RGB",
            [pixmap.width, pixmap.height],
            pixmap.samples
        )

        text += pytesseract.image_to_string(image) + "\n"

    document.close()

    return text


# extracting OCR text together with confidence information
def extract_text_with_confidence(file_path):

    file_extension = Path(file_path).suffix.lower()

    # image document
    if file_extension in {".png", ".jpg", ".jpeg"}:

        image = Image.open(file_path)

        # getting OCR word-level information
        ocr_data = pytesseract.image_to_data(
            image,
            output_type=pytesseract.Output.DICT
        )

        words = []
        confidences = []

        for i in range(len(ocr_data["text"])):

            word = ocr_data["text"][i].strip()

            try:
                confidence = float(
                    ocr_data["conf"][i]
                )
            except ValueError:
                confidence = -1

            if word and confidence >= 0:
                words.append(word)
                confidences.append(confidence)

        text = " ".join(words)

        if confidences:
            average_confidence = sum(confidences) / len(confidences)
        else:
            average_confidence = 0

        return {
            "text": text,
            "ocr_confidence": round(average_confidence, 2)
        }

    # PDF document
    if file_extension == ".pdf":

        document = fitz.open(file_path)

        text = "\n".join(
            page.get_text()
            for page in document
        )

        document.close()

        # normal PDF with selectable text
        if text.strip():

            return {
                "text": text,
                "ocr_confidence": None
            }

        # scanned PDF
        document = fitz.open(file_path)

        all_words = []
        all_confidences = []

        for page in document:

            pixmap = page.get_pixmap()

            image = Image.frombytes(
                "RGB",
                [pixmap.width, pixmap.height],
                pixmap.samples
            )

            ocr_data = pytesseract.image_to_data(
                image,
                output_type=pytesseract.Output.DICT
            )

            for i in range(len(ocr_data["text"])):

                word = ocr_data["text"][i].strip()

                try:
                    confidence = float(
                        ocr_data["conf"][i]
                    )
                except ValueError:
                    confidence = -1

                if word and confidence >= 0:
                    all_words.append(word)
                    all_confidences.append(confidence)

        document.close()

        text = " ".join(all_words)

        if all_confidences:
            average_confidence = (
                sum(all_confidences) /
                len(all_confidences)
            )
        else:
            average_confidence = 0

        return {
            "text": text,
            "ocr_confidence": round(
                average_confidence,
                2
            )
        }

    # TXT document
    if file_extension == ".txt":

        text = Path(file_path).read_text(
            encoding="utf-8"
        )

        return {
            "text": text,
            "ocr_confidence": None
        }

    raise ValueError("Unsupported document format")