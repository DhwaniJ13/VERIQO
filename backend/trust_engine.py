def calculate_trust(
    validation_results,
    ocr_confidence=None,
    visual_extraction=False
):

    verification_score = 100

    failed_checks = [
        result
        for result in validation_results
        if result["status"] == "failed"
    ]

    uncertain_checks = [
        result
        for result in validation_results
        if result["status"] == "unable_to_verify"
    ]

    verification_score -= (
        len(failed_checks) * 30
    )

    verification_score -= (
        len(uncertain_checks) * 15
    )

    # OCR affects the score only when OCR is the
    # primary extraction method.
    if (
        ocr_confidence is not None
        and not visual_extraction
    ):

        if ocr_confidence < 60:
            verification_score -= 25

        elif ocr_confidence < 75:
            verification_score -= 15

        elif ocr_confidence < 85:
            verification_score -= 5

    verification_score = max(
        0,
        min(100, verification_score)
    )

    if failed_checks:

        decision = "REVIEW"
        reason = "One or more validation checks failed."

    elif uncertain_checks:

        decision = "REVIEW"
        reason = "Some information could not be verified."

    elif (
        ocr_confidence is not None
        and ocr_confidence < 75
        and not visual_extraction
    ):

        decision = "REVIEW"
        reason = (
            "OCR confidence is low. "
            "Manual review is recommended."
        )

    else:

        decision = "SAFE"
        reason = "All available validation checks passed."

    field_reliability = {}

    vendor_check = next(
        (
            result
            for result in validation_results
            if result["check"] == "vendor"
        ),
        None
    )

    if not vendor_check or vendor_check["status"] != "passed":

        field_reliability["vendor"] = {
            "reliability": "REVIEW",
            "reason": "Vendor information could not be verified."
        }

    elif (
        ocr_confidence is not None
        and ocr_confidence < 75
        and not visual_extraction
    ):

        field_reliability["vendor"] = {
            "reliability": "REVIEW",
            "reason": "Vendor was extracted, but OCR confidence is low."
        }

    else:

        field_reliability["vendor"] = {
            "reliability": "HIGH",
            "reason": (
                "Vendor information was successfully "
                "extracted and validated."
            )
        }

    if (
        ocr_confidence is not None
        and ocr_confidence < 75
        and not visual_extraction
    ):

        field_reliability["invoice_number"] = {
            "reliability": "REVIEW",
            "reason": (
                "Invoice number may contain OCR "
                "recognition errors."
            )
        }

    else:

        field_reliability["invoice_number"] = {
            "reliability": "HIGH",
            "reason": (
                "Invoice number was extracted using "
                "the available document information."
            )
        }

    if (
        ocr_confidence is not None
        and ocr_confidence < 75
        and not visual_extraction
    ):

        field_reliability["invoice_date"] = {
            "reliability": "REVIEW",
            "reason": "Date may contain OCR recognition errors."
        }

    else:

        field_reliability["invoice_date"] = {
            "reliability": "HIGH",
            "reason": (
                "Invoice date was extracted using "
                "the available document information."
            )
        }

    total_check = next(
        (
            result
            for result in validation_results
            if result["check"] == "total_calculation"
        ),
        None
    )

    if not total_check:

        field_reliability["total"] = {
            "reliability": "REVIEW",
            "reason": "Total could not be independently verified."
        }

    elif total_check["status"] != "passed":

        field_reliability["total"] = {
            "reliability": "REVIEW",
            "reason": (
                "Subtotal + tax does not match "
                "the extracted total."
            )
        }

    elif (
        ocr_confidence is not None
        and ocr_confidence < 75
        and not visual_extraction
    ):

        field_reliability["total"] = {
            "reliability": "REVIEW",
            "reason": (
                "Total calculation passed, "
                "but OCR confidence is low."
            )
        }

    else:

        field_reliability["total"] = {
            "reliability": "HIGH",
            "reason": (
                "Total calculation passed "
                "independent validation."
            )
        }

    if ocr_confidence is not None:

        if visual_extraction:

            ocr_reliability = "SECONDARY"

            ocr_reason = (
                f"Average OCR confidence: "
                f"{ocr_confidence}%. "
                "Used as a secondary signal because "
                "Gemini Vision handled the primary extraction."
            )

        else:

            if ocr_confidence >= 85:
                ocr_reliability = "HIGH"

            elif ocr_confidence >= 75:
                ocr_reliability = "MEDIUM"

            else:
                ocr_reliability = "REVIEW"

            ocr_reason = (
                f"Average OCR confidence: "
                f"{ocr_confidence}%."
            )

        field_reliability["ocr"] = {
            "reliability": ocr_reliability,
            "reason": ocr_reason
        }

    return {
        "decision": decision,
        "reason": reason,
        "verification_score": verification_score,
        "field_reliability": field_reliability
    }