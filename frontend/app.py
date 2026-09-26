# importing required libraries
import streamlit as st
import requests
import textwrap


# page configuration
st.set_page_config(
    page_title="VERIQO | Document Trust",
    page_icon="✓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# theme styling
st.markdown("""
<style>

    .stApp {
        background: #0b0f14;
        color: #f5f7fa;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"] {
        visibility: hidden;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .logo {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
        color: #ffffff;
        margin-bottom: 0;
    }

    .tagline {
        color: #8b949e;
        font-size: 17px;
        margin-top: -5px;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
        margin-top: 30px;
        margin-bottom: 12px;
    }

    [data-testid="stFileUploader"] {
        background: #111820;
        border: 1px solid #26313d;
        border-radius: 12px;
        padding: 8px;
        margin-bottom: 20px;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #151d27;
        border: 1px dashed #3b4857;
        border-radius: 10px;
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #3b82f6;
        background: #182230;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #c9d1d9;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] span {
        color: #8b949e;
    }

    [data-testid="stFileUploader"] button {
        background: #2563eb;
        color: #ffffff;
        border: 1px solid #3b82f6;
        border-radius: 8px;
    }

    [data-testid="stFileUploader"] button:hover {
        background: #1d4ed8;
        color: #ffffff;
    }

    .selected-file {
        background: #111820;
        border: 1px solid #26313d;
        border-radius: 10px;
        padding: 10px 14px;
        margin: 8px 0 14px 0;
        color: #c9d1d9;
        font-size: 14px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 9px;
        border: 1px solid #3b82f6;
        background: #2563eb;
        color: white;
        font-weight: 650;
        padding: 10px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: #1d4ed8;
        border-color: #60a5fa;
        transform: translateY(-1px);
    }

    .safe-box {
        background: #0d2118;
        border: 1px solid #1f8f5f;
        border-radius: 14px;
        padding: 22px;
        margin: 15px 0 25px 0;
    }

    .review-box {
        background: #241b0c;
        border: 1px solid #c58a28;
        border-radius: 14px;
        padding: 22px;
        margin: 15px 0 25px 0;
    }

    .score-card {
        background: #111820;
        border: 1px solid #26313d;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        transition: all 0.2s ease;
    }

    .score-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
    }

    .score-number {
        font-size: 38px;
        font-weight: 800;
        color: #ffffff;
    }

    .score-label {
        color: #8b949e;
        font-size: 13px;
    }

    .info-card {
        background: #111820;
        border: 1px solid #26313d;
        border-radius: 12px;
        padding: 18px;
        min-height: 105px;
        transition: all 0.2s ease;
    }

    .info-card:hover {
        border-color: #3b82f6;
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
    }

    .card-label {
        color: #8b949e;
        font-size: 13px;
        margin-bottom: 7px;
    }

    .card-value {
        color: #ffffff;
        font-size: 18px;
        font-weight: 650;
        word-wrap: break-word;
    }

    .reliability-card {
        background: #111820;
        border: 1px solid #26313d;
        border-radius: 12px;
        padding: 15px 18px;
        margin-bottom: 10px;
        transition: all 0.2s ease;
    }

    .reliability-card:hover {
        border-color: #3b82f6;
        background: #151e29;
        transform: translateX(3px);
    }

    .high {
        color: #43d17a;
        font-weight: 700;
    }

    .review {
        color: #e7ad45;
        font-weight: 700;
    }

    .secondary {
        color: #60a5fa;
        font-weight: 700;
    }

    .medium {
        color: #60a5fa;
        font-weight: 700;
    }

    .decision-guide {
        background: #111820;
        border: 1px solid #26313d;
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 20px;
        color: #c9d1d9;
        line-height: 1.6;
    }

    .validation-card {
        background: #111820;
        border: 1px solid #26313d;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
        transition: all 0.2s ease;
    }

    .validation-card:hover {
        border-color: #3b82f6;
        background: #151e29;
        transform: translateX(3px);
    }

    .validation-title {
        color: #ffffff;
        font-weight: 650;
        font-size: 15px;
    }

    .validation-message {
        color: #8b949e;
        font-size: 14px;
        margin-top: 4px;
    }

    .validation-passed {
        color: #43d17a;
        font-weight: 700;
    }

    .validation-failed {
        color: #f87171;
        font-weight: 700;
    }

    .validation-warning {
        color: #e7ad45;
        font-weight: 700;
    }

    .footer {
        text-align: center;
        color: #6b7280;
        margin-top: 35px;
        font-size: 13px;
        padding-bottom: 15px;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)


# HTML helper
# st.html is used so Streamlit renders the HTML instead of showing the tags
def render_html(html):
    st.html(textwrap.dedent(html))


# header
render_html("""
<div class="logo">
    VERIQO
</div>
""")

render_html("""
<div class="tagline">
    Extract less. Verify more.
</div>
""")


# short explanation
render_html("""
<div style="
    color:#c9d1d9;
    font-size:16px;
    line-height:1.6;
    max-width:850px;
    margin-bottom:25px;
">
    An AI-powered document trust layer that extracts business information,
    validates it against internal rules, and highlights information that
    requires human review.
</div>
""")


# upload section
render_html("""
<div class="section-title">
    Analyze Document
</div>
""")

uploaded_file = st.file_uploader(
    "Upload an invoice or business document",
    type=[
        "png",
        "jpg",
        "jpeg",
        "pdf",
        "txt"
    ],
    label_visibility="visible"
)


# document analysis
if uploaded_file:

    render_html(f"""
    <div class="selected-file">
        <strong>Selected document:</strong>
        {uploaded_file.name}
    </div>
    """)

    analyze_button = st.button(
        "Analyze & Verify Document"
    )

    if analyze_button:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }

        try:

            # upload document to FastAPI
            with st.spinner("Uploading document..."):

                upload_response = requests.post(
                    "http://127.0.0.1:8000/upload",
                    files=files,
                    timeout=60
                )

                upload_response.raise_for_status()

                upload_data = upload_response.json()

                document_id = upload_data["document_id"]


            # run extraction and verification
            with st.spinner(
                "Extracting, validating and verifying..."
            ):

                extract_response = requests.post(
                    f"http://127.0.0.1:8000/extract/{document_id}",
                    timeout=120
                )

                extract_response.raise_for_status()

                result = extract_response.json()


            trust = result["trust"]
            data = result["extracted_data"]


            # verification result
            render_html("""
            <div class="section-title">
                Verification Result
            </div>
            """)

            verification_score = trust.get(
                "verification_score",
                0
            )

            score_col, decision_col = st.columns(
                [1, 2]
            )


            # verification score
            with score_col:

                render_html(f"""
                <div class="score-card">

                    <div class="score-number">
                        {verification_score}/100
                    </div>

                    <div class="score-label">
                        Verification Score
                    </div>

                </div>
                """)


            # trust decision
            with decision_col:

                if trust["decision"] == "SAFE":

                    render_html(f"""
                    <div class="safe-box">

                        <h2 style="
                            margin:0;
                            color:#43d17a;
                        ">
                            ✓ SAFE
                        </h2>

                        <p style="
                            color:#c9d1d9;
                        ">
                            {trust["reason"]}
                        </p>

                    </div>
                    """)

                else:

                    render_html(f"""
                    <div class="review-box">

                        <h2 style="
                            margin:0;
                            color:#e7ad45;
                        ">
                            ⚠ REVIEW REQUIRED
                        </h2>

                        <p style="
                            color:#c9d1d9;
                        ">
                            {trust["reason"]}
                        </p>

                    </div>
                    """)


            # decision explanation
            with st.expander(
                "How did VERIQO decide?"
            ):

                render_html("""
                <div class="decision-guide">

                    <strong>
                        1. Document extraction
                    </strong>

                    <br>

                    The document is converted into usable
                    text or analyzed visually depending on
                    the document type.

                    <br><br>

                    <strong>
                        2. Structured extraction
                    </strong>

                    <br>

                    Gemini extracts the required invoice
                    fields according to the predefined schema.

                    <br><br>

                    <strong>
                        3. Business validation
                    </strong>

                    <br>

                    VERIQO independently checks extracted
                    values, such as whether subtotal + tax
                    matches the total.

                    <br><br>

                    <strong>
                        4. Reliability signals
                    </strong>

                    <br>

                    OCR confidence and validation results
                    provide additional trust signals.

                    <br><br>

                    <strong>
                        5. Human review
                    </strong>

                    <br>

                    When important information cannot be
                    verified, VERIQO recommends manual review.

                </div>
                """)


            # extracted information
            render_html("""
            <div class="section-title">
                Extracted Information
            </div>
            """)

            col1, col2, col3 = st.columns(3)


            with col1:

                render_html(f"""
                <div class="info-card">

                    <div class="card-label">
                        VENDOR
                    </div>

                    <div class="card-value">
                        {data.get("vendor") or "Not found"}
                    </div>

                </div>
                """)


            with col2:

                render_html(f"""
                <div class="info-card">

                    <div class="card-label">
                        INVOICE NUMBER
                    </div>

                    <div class="card-value">
                        {data.get("invoice_number") or "Not found"}
                    </div>

                </div>
                """)


            with col3:

                render_html(f"""
                <div class="info-card">

                    <div class="card-label">
                        TOTAL
                    </div>

                    <div class="card-value">
                        {data.get("total") or "Not found"}
                    </div>

                </div>
                """)


            # invoice date
            render_html(f"""
            <div style="
                margin-top:12px;
                color:#8b949e;
            ">

                Invoice Date:

                <span style="
                    color:#ffffff;
                    font-weight:600;
                ">
                    {data.get("invoice_date") or "Not found"}
                </span>

            </div>
            """)


            # field reliability
            render_html("""
            <div class="section-title">
                Field Reliability
            </div>
            """)

            reliability = trust.get(
                "field_reliability",
                {}
            )


            for field, details in reliability.items():

                reliability_level = details.get(
                    "reliability",
                    "REVIEW"
                )

                if reliability_level == "HIGH":
                    level_class = "high"

                elif reliability_level == "SECONDARY":
                    level_class = "secondary"

                elif reliability_level == "MEDIUM":
                    level_class = "medium"

                else:
                    level_class = "review"


                render_html(f"""
                <div class="reliability-card">

                    <strong style="
                        color:#ffffff;
                    ">
                        {field.replace("_", " ").title()}
                    </strong>

                    <span class="{level_class}">
                        &nbsp; {reliability_level}
                    </span>

                    <br>

                    <span style="
                        color:#8b949e;
                        font-size:14px;
                    ">
                        {details.get("reason", "")}
                    </span>

                </div>
                """)


            # validation checks
            render_html("""
            <div class="section-title">
                Validation Checks
            </div>
            """)


            for check in result.get(
                "validation",
                []
            ):

                check_name = (
                    check.get(
                        "check",
                        "Unknown check"
                    )
                    .replace("_", " ")
                    .title()
                )

                check_message = check.get(
                    "message",
                    ""
                )

                status = check.get(
                    "status",
                    "unable_to_verify"
                )


                if status == "passed":

                    render_html(f"""
                    <div class="validation-card">

                        <div class="validation-title">

                            <span class="validation-passed">
                                ✓ PASSED
                            </span>

                            &nbsp;

                            {check_name}

                        </div>

                        <div class="validation-message">
                            {check_message}
                        </div>

                    </div>
                    """)


                elif status == "failed":

                    render_html(f"""
                    <div class="validation-card">

                        <div class="validation-title">

                            <span class="validation-failed">
                                ✗ FAILED
                            </span>

                            &nbsp;

                            {check_name}

                        </div>

                        <div class="validation-message">
                            {check_message}
                        </div>

                    </div>
                    """)


                else:

                    render_html(f"""
                    <div class="validation-card">

                        <div class="validation-title">

                            <span class="validation-warning">
                                ⚠ UNABLE TO VERIFY
                            </span>

                            &nbsp;

                            {check_name}

                        </div>

                        <div class="validation-message">
                            {check_message}
                        </div>

                    </div>
                    """)


            # footer
            render_html("""
            <div class="footer">
                VERIQO • AI-powered document trust & verification
            </div>
            """)


        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to VERIQO backend. "
                "Make sure FastAPI is running on port 8000."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The document processing request timed out. "
                "Please try again."
            )

        except requests.exceptions.HTTPError as error:

            try:

                error_detail = extract_response.json().get(
                    "detail",
                    str(error)
                )

            except Exception:

                error_detail = str(error)

            st.error(
                f"Backend processing failed: {error_detail}"
            )

        except Exception as error:

            st.error(
                f"Something went wrong: {error}"
            )