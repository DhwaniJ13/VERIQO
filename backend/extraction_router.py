from pathlib import Path

from fastapi import APIRouter, HTTPException

from backend.extraction import extract_text_with_confidence
from backend.ai_extraction import (
    extract_invoice_with_ai,
    extract_invoice_from_image
)
from backend.validation import validate_invoice
from backend.trust_engine import calculate_trust


router = APIRouter()


@router.post("/extract/{document_id}")
def extract_document(document_id: str):

    file_path = Path("data/uploads") / document_id

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    is_image = file_path.suffix.lower() in {
        ".png",
        ".jpg",
        ".jpeg"
    }

    try:

        extraction_result = extract_text_with_confidence(
            file_path
        )

        text = extraction_result["text"]
        ocr_confidence = extraction_result[
            "ocr_confidence"
        ]

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Document extraction failed: {str(error)}"
        )

    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="Could not extract readable text from this document."
        )

    try:

        if is_image:

            # Keep the original image for layout-aware extraction.
            invoice = extract_invoice_from_image(
                file_path
            )

            visual_extraction = True

        else:

            invoice = extract_invoice_with_ai(
                text
            )

            visual_extraction = False

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"AI extraction failed: {str(error)}"
        )

    validation_results = validate_invoice(
        invoice
    )

    trust_result = calculate_trust(
        validation_results,
        ocr_confidence,
        visual_extraction
    )

    return {
        "document_id": document_id,
        "extracted_data": invoice.model_dump(),
        "validation": validation_results,
        "trust": trust_result,
        "ocr_confidence": ocr_confidence,
        "visual_extraction": visual_extraction,
        "status": "processed"
    }