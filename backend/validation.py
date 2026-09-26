def validate_invoice(invoice):

    results = []

    if (
        invoice.subtotal is not None
        and invoice.tax is not None
        and invoice.total is not None
    ):

        calculated_total = (
            invoice.subtotal + invoice.tax
        )

        if abs(
            calculated_total - invoice.total
        ) < 0.01:

            results.append({
                "check": "total_calculation",
                "status": "passed",
                "message": "Subtotal + tax matches the total."
            })

        else:

            results.append({
                "check": "total_calculation",
                "status": "failed",
                "message": "Subtotal + tax does not match the total."
            })

    else:

        results.append({
            "check": "total_calculation",
            "status": "unable_to_verify",
            "message": "Required financial fields are missing."
        })

    if invoice.vendor:

        results.append({
            "check": "vendor",
            "status": "passed",
            "message": "Vendor information is available."
        })

    else:

        results.append({
            "check": "vendor",
            "status": "failed",
            "message": "Vendor information is missing."
        })

    return results