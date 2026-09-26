# VERIQO

### Extract less. Verify more.

VERIQO is an AI-powered document trust and verification system for business documents such as invoices.

Instead of only extracting information from a document, VERIQO checks whether the extracted information can be trusted before it enters a business workflow.

## What VERIQO Does

- Extracts structured information from invoices
- Supports image and text-based documents
- Uses Gemini for structured document extraction
- Uses Tesseract for OCR and OCR confidence
- Validates extracted financial values
- Calculates a verification score
- Shows field-level reliability
- Flags documents that need human review

## How It Works

```text
Document
    |
    v
Upload
    |
    +----------------------+
    |                      |
    v                      v
OCR / Text             Gemini Vision
Extraction             for images
    |                      |
    +----------+-----------+
               |
               v
        Structured Invoice
               |
               v
          Validation
               |
               v
         Trust Engine
               |
          +----+----+
          |         |
         SAFE     REVIEW