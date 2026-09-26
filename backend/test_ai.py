#sample testing

# importing our Gemini extraction function
from backend.ai_extraction import extract_invoice_with_ai

# sample invoice text for testing Gemini
sample_text = """
ABC Technologies Pvt Ltd

Invoice Number: INV-1042
Invoice Date: 25/09/2026

Laptop    2    50000    100000
Mouse     5     1000      5000

Subtotal: 105000
GST: 18900
Total: 123900
"""

# sending sample text to Gemini
result = extract_invoice_with_ai(sample_text)

# displaying the structured result
print(result)