from pathlib import Path

from dotenv import load_dotenv
from google import genai

from backend.schema import Invoice


load_dotenv()

client = genai.Client()


def extract_invoice_with_ai(text):

    prompt = f"""
    Extract invoice information from the document text below.

    Return the result according to the provided Invoice schema.

    Rules:
    - Extract only information supported by the document.
    - Do not guess missing values.
    - Return null when a value cannot be reliably found.
    - Preserve invoice table items.

    Document text:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": Invoice
        }
    )

    return response.parsed


def extract_invoice_from_image(file_path):

    from google.genai import types

    extension = Path(file_path).suffix.lower()

    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg"
    }

    mime_type = mime_types.get(
        extension,
        "image/png"
    )

    with open(file_path, "rb") as file:
        image_data = file.read()

    prompt = """
    Extract invoice information from this document image.

    Return the result according to the provided Invoice schema.

    Rules:
    - Read the original document image directly.
    - Use the document layout to identify fields and table rows.
    - Extract only information visible in the document.
    - Do not guess missing values.
    - Return null when a value cannot be reliably found.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[
            types.Part.from_bytes(
                data=image_data,
                mime_type=mime_type
            ),
            prompt
        ],
        config={
            "response_mime_type": "application/json",
            "response_schema": Invoice
        }
    )

    return response.parsed