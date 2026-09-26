#TESTING VALIDATION RESULTS

# importing our invoice structures
from backend.schema import Invoice, InvoiceItem

# importing our validation function
from backend.validation import validate_invoice

# creating a sample invoice for testing
invoice = Invoice(
    vendor="Apple Technologies Pvt Ltd",
    invoice_number="INV-1042",
    invoice_date="25/09/2026",

    items=[
        InvoiceItem(
            description="Laptop",
            quantity=2,
            unit_price=50000,
            amount=100000
        ),
        InvoiceItem(
            description="Mouse",
            quantity=5,
            unit_price=1000,
            amount=5000
        )
    ],

    subtotal=105000,
    tax=18900,
    total=123900
)
# sending the invoice to our validation engine
results = validate_invoice(invoice)

# displaying the validation results
for result in results:
    print(result)