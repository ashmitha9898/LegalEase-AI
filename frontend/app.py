import streamlit as st
import requests
from io import BytesIO
from docx import Document


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LEGALTECH COLOR THEME
# ============================================================

st.markdown("""
<style>

    /* ========================================================
       MAIN APPLICATION
       ======================================================== */

    .stApp {
        background-color: #F5F7FB;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: #F8FAFC;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #334155;
    }


    /* ========================================================
       HEADINGS
       ======================================================== */

    h1 {
        color: #172554;
        font-weight: 750;
        letter-spacing: -0.5px;
    }

    h2 {
        color: #1E3A8A;
        font-weight: 700;
    }

    h3 {
        color: #334155;
        font-weight: 650;
    }


    /* ========================================================
       NORMAL TEXT
       ======================================================== */

    p {
        color: #475569;
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #1E3A8A;
        font-weight: 750;
    }


    /* ========================================================
       INPUT BOXES
       ======================================================== */

    div[data-baseweb="input"] {
        border-radius: 10px;
    }

    div[data-baseweb="input"] > div {
        border-color: #CBD5E1;
    }

    div[data-baseweb="input"]:focus-within > div {
        border-color: #2563EB;
        box-shadow: 0 0 0 1px #2563EB;
    }


    /* ========================================================
       TEXT AREA
       ======================================================== */

    textarea {
        border-radius: 10px !important;
    }


    /* ========================================================
       SELECT BOX
       ======================================================== */

    div[data-baseweb="select"] {
        border-radius: 10px;
    }


    /* ========================================================
       PRIMARY BUTTON
       ======================================================== */

    button[kind="primary"] {
        background-color: #2563EB !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 0.6rem 1rem !important;
    }

    button[kind="primary"]:hover {
        background-color: #1D4ED8 !important;
    }


    /* ========================================================
       SECONDARY / DOWNLOAD BUTTONS
       ======================================================== */

    button[kind="secondary"] {
        border-radius: 10px !important;
        border: 1px solid #CBD5E1 !important;
        color: #1E3A8A !important;
        font-weight: 600 !important;
    }


    /* ========================================================
       TABS
       ======================================================== */

    button[data-baseweb="tab"] {
        font-weight: 650;
        color: #64748B;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #2563EB;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border-color: #E2E8F0;
    }


    /* ========================================================
       SIDEBAR RADIO
       ======================================================== */

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label {
        border-radius: 8px;
        padding: 6px;
    }


    /* ========================================================
       CAPTIONS
       ======================================================== */

    .stCaption {
        color: #64748B;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# BACKEND
# ============================================================

BACKEND_URL = "https://legalease-ai-uv25.onrender.com"


# ============================================================
# DOCUMENT INFORMATION
# ============================================================

DOCUMENT_INFO = {
    "Employment Contract": (
        "💼",
        "Employment terms, salary, responsibilities and confidentiality."
    ),

    "Non-Disclosure Agreement (NDA)": (
        "🔐",
        "Confidentiality and protection of sensitive information."
    ),

    "Rental / Lease Agreement": (
        "🏠",
        "Rental terms, property details, rent and responsibilities."
    ),

    "Service Agreement": (
        "🤝",
        "Services, payments, responsibilities and duration."
    ),

    "Internship Agreement": (
        "🎓",
        "Internship role, duration and responsibilities."
    ),

    "Freelance Agreement": (
        "💻",
        "Freelance scope, payment, deadlines and responsibilities."
    ),

    "Partnership Agreement": (
        "🏢",
        "Partnership roles, contributions and responsibilities."
    ),

    "General Legal Agreement": (
        "⚖️",
        "A general-purpose agreement based on your requirements."
    )
}


# ============================================================
# DOCX CREATION
# ============================================================

def create_docx(text):

    document = Document()

    document.add_heading(
        "LegalEase Document",
        level=1
    )

    for line in text.split("\n"):

        if line.strip():
            document.add_paragraph(line)

        else:
            document.add_paragraph("")

    output = BytesIO()

    document.save(output)

    return output.getvalue()


# ============================================================
# GENERATE DOCUMENT
# ============================================================

def generate_document(
    document_type,
    parties,
    terms,
    dates
):

    payload = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "dates": dates
    }

    try:

        response = requests.post(
            f"{BACKEND_URL}/generate",
            json=payload,
            timeout=90
        )

        if response.status_code == 200:

            data = response.json()

            return data.get(
                "document",
                ""
            )

        try:

            error = response.json().get(
                "detail",
                response.text
            )

        except Exception:

            error = response.text

        st.error(
            f"Generation failed: {error}"
        )

        return None

    except requests.exceptions.ConnectionError:

        st.error(
            "Cannot connect to the LegalEase backend."
        )

        st.info(
            "Make sure FastAPI is running on port 8000."
        )

        return None

    except requests.exceptions.Timeout:

        st.error(
            "The AI request timed out. Please try again."
        )

        return None

    except Exception as e:

        st.error(
            f"Unexpected error: {e}"
        )

        return None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("⚖️ LegalEase")

    st.caption(
        "AI-Powered Legal Document Generator"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Workspace",
            "ℹ️ About LegalEase",
            "✨ Features",
            "📖 How It Works"
        ]
    )

    st.divider()

    if page == "🏠 Workspace":

        st.subheader(
            "Document Setup"
        )

        document_type = st.selectbox(
            "Document Type",
            list(DOCUMENT_INFO.keys())
        )

        icon, description = DOCUMENT_INFO[
            document_type
        ]

        st.write(
            f"{icon} **{document_type}**"
        )

        st.caption(
            description
        )

        st.divider()

        if "document" in st.session_state:

            st.success(
                "Document generated"
            )

        else:

            st.info(
                "Ready to create"
            )

    st.divider()

    st.caption(
        "LegalEase v1.0"
    )

    st.caption(
        "AI-powered document drafting"
    )


# ============================================================
# WORKSPACE
# ============================================================

if page == "🏠 Workspace":

    st.title(
        "Legal Document Workspace"
    )

    st.write(
        "Create, review and export professional legal document drafts "
        "using AI."
    )

    st.divider()


    # ========================================================
    # STATUS CARDS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Document",
            document_type
        )

    with col2:

        st.metric(
            "AI Engine",
            "Gemini"
        )

    with col3:

        if "document" in st.session_state:

            st.metric(
                "Status",
                "Ready"
            )

        else:

            st.metric(
                "Status",
                "Draft"
            )

    with col4:

        st.metric(
            "Formats",
            "TXT + DOCX"
        )


    st.divider()


    # ========================================================
    # TABS
    # ========================================================

    details_tab, preview_tab, export_tab = st.tabs(
        [
            "📋 Document Details",
            "📝 Preview & Edit",
            "📥 Export"
        ]
    )


    # ========================================================
    # DOCUMENT DETAILS
    # ========================================================

    with details_tab:

        st.header(
            "Create your document"
        )

        st.caption(
            "Enter the information below. Gemini will use these "
            "details to prepare your legal document."
        )

        st.divider()


        # ----------------------------------------------------
        # PARTIES
        # ----------------------------------------------------

        st.subheader(
            "👥 Parties"
        )

        party1, party2 = st.columns(2)

        with party1:

            party_one = st.text_input(
                "Party 1 / Company",
                placeholder="ABC Technologies Pvt. Ltd."
            )

        with party2:

            party_two = st.text_input(
                "Party 2 / Individual",
                placeholder="Ashmitha Sri"
            )


        st.divider()


        # ----------------------------------------------------
        # AGREEMENT INFORMATION
        # ----------------------------------------------------

        st.subheader(
            "📅 Agreement Information"
        )

        date_col, duration_col = st.columns(2)

        with date_col:

            effective_date = st.text_input(
                "Effective Date",
                placeholder="1 October 2026"
            )

        with duration_col:

            duration = st.text_input(
                "Duration",
                placeholder="1 year"
            )


        st.divider()


        # ----------------------------------------------------
        # ADDITIONAL DETAILS
        # ----------------------------------------------------

        st.subheader(
            "💼 Additional Details"
        )

        role_col, hours_col = st.columns(2)

        with role_col:

            job_title = st.text_input(
                "Role / Position",
                placeholder="Data Analyst"
            )

        with hours_col:

            working_hours = st.text_input(
                "Working Hours",
                placeholder="9 AM - 6 PM, Monday to Friday"
            )


        st.divider()


        # ----------------------------------------------------
        # TERMS
        # ----------------------------------------------------

        st.subheader(
            "📑 Key Terms & Conditions"
        )

        terms = st.text_area(
            "Important Terms",

            placeholder=(
                "Example:\n\n"
                "Salary: Rs. 30,000 per month.\n"
                "Notice period: 30 days.\n"
                "The employee must maintain confidentiality.\n"
                "The company will provide necessary resources."
            ),

            height=220,

            label_visibility="collapsed"
        )


        st.divider()


        # ----------------------------------------------------
        # GENERATE
        # ----------------------------------------------------

        st.subheader(
            "🚀 Generate"
        )

        st.caption(
            "Review the information and generate your AI-powered draft."
        )

        generate_clicked = st.button(
            "⚖️ Generate Legal Document",
            type="primary",
            use_container_width=True
        )


        if generate_clicked:

            if not party_one.strip():

                st.warning(
                    "Please enter Party 1 / Company."
                )

            elif not party_two.strip():

                st.warning(
                    "Please enter Party 2 / Individual."
                )

            elif not effective_date.strip():

                st.warning(
                    "Please enter the effective date."
                )

            elif not terms.strip():

                st.warning(
                    "Please enter the key terms."
                )

            else:

                combined_parties = (
                    f"Party 1: {party_one}\n"
                    f"Party 2: {party_two}"
                )

                combined_terms = (
                    f"Role / Position: {job_title}\n"
                    f"Working Hours: {working_hours}\n"
                    f"Duration: {duration}\n\n"
                    f"Key Terms:\n{terms}"
                )

                with st.spinner(
                    "Gemini is preparing your document..."
                ):

                    result = generate_document(
                        document_type=document_type,
                        parties=combined_parties,
                        terms=combined_terms,
                        dates=effective_date
                    )

                if result:

                    st.session_state["document"] = result

                    st.success(
                        "✅ Document generated successfully!"
                    )

                    st.info(
                        "Open Preview & Edit to review the document."
                    )


    # ========================================================
    # PREVIEW
    # ========================================================

    with preview_tab:

        st.header(
            "Document Preview"
        )

        st.caption(
            "Review and edit the AI-generated document before exporting."
        )

        st.divider()

        if "document" not in st.session_state:

            st.info(
                "No document has been generated yet."
            )

            st.write(
                "Complete the Document Details section and "
                "click Generate Legal Document."
            )

        else:

            st.success(
                "✓ AI-generated document ready for review"
            )

            edited_document = st.text_area(
                "Editable Document",
                value=st.session_state["document"],
                height=700,
                label_visibility="collapsed"
            )

            st.session_state["document"] = edited_document


    # ========================================================
    # EXPORT
    # ========================================================

    with export_tab:

        st.header(
            "Export Document"
        )

        st.caption(
            "Download your finalized document."
        )

        st.divider()

        if "document" not in st.session_state:

            st.info(
                "Generate a document first."
            )

        else:

            final_document = st.session_state["document"]

            st.success(
                "✓ Document is ready for export"
            )

            st.write(
                "### Choose your format"
            )

            txt_col, docx_col = st.columns(2)


            with txt_col:

                st.subheader(
                    "📄 TXT"
                )

                st.caption(
                    "Simple text format."
                )

                st.download_button(
                    label="⬇️ Download TXT",
                    data=final_document.encode("utf-8"),
                    file_name="legalease_document.txt",
                    mime="text/plain",
                    use_container_width=True
                )


            with docx_col:

                st.subheader(
                    "📘 DOCX"
                )

                st.caption(
                    "Editable Microsoft Word format."
                )

                try:

                    docx_data = create_docx(
                        final_document
                    )

                    st.download_button(
                        label="⬇️ Download DOCX",
                        data=docx_data,
                        file_name="legalease_document.docx",
                        mime=(
                            "application/vnd.openxmlformats-"
                            "officedocument.wordprocessingml.document"
                        ),
                        use_container_width=True
                    )

                except Exception as e:

                    st.error(
                        f"DOCX creation failed: {e}"
                    )


# ============================================================
# ABOUT PAGE
# ============================================================

elif page == "ℹ️ About LegalEase":

    st.title(
        "⚖️ About LegalEase"
    )

    st.write(
        "LegalEase is an AI-powered legal document drafting "
        "application designed to simplify the creation of "
        "structured legal document drafts."
    )

    st.divider()

    st.subheader(
        "🎯 Project Objective"
    )

    st.write(
        "The goal of LegalEase is to help users create "
        "customizable legal document drafts by providing "
        "document type, parties, dates and important terms."
    )

    st.subheader(
        "🤖 Artificial Intelligence"
    )

    st.write(
        "LegalEase uses Google's Gemini generative AI model "
        "to transform the information provided by the user "
        "into a structured legal document draft."
    )

    st.subheader(
        "🧩 Technology Stack"
    )

    tech1, tech2, tech3 = st.columns(3)

    with tech1:

        st.info(
            "🖥️ Streamlit\n\nFrontend"
        )

    with tech2:

        st.info(
            "⚡ FastAPI\n\nBackend API"
        )

    with tech3:

        st.info(
            "🤖 Gemini\n\nAI Generation"
        )

    st.divider()

    st.subheader(
        "📄 Supported Documents"
    )

    for name, details in DOCUMENT_INFO.items():

        icon, description = details

        st.write(
            f"{icon} **{name}** — {description}"
        )

    st.divider()

    st.warning(
        "LegalEase generates document drafts for informational "
        "and document-preparation purposes. It does not provide "
        "legal advice. Important documents should be reviewed "
        "by a qualified legal professional before signing."
    )


# ============================================================
# FEATURES PAGE
# ============================================================

elif page == "✨ Features":

    st.title(
        "✨ LegalEase Features"
    )

    st.write(
        "Key capabilities included in the current application."
    )

    st.divider()

    feature1, feature2 = st.columns(2)

    with feature1:

        st.subheader(
            "🤖 AI Document Generation"
        )

        st.write(
            "Gemini generates structured legal document drafts "
            "from the information supplied by the user."
        )

        st.subheader(
            "📝 Editable Preview"
        )

        st.write(
            "Users can review and modify the generated document "
            "before downloading it."
        )

        st.subheader(
            "📄 Multiple Document Types"
        )

        st.write(
            "Supports employment contracts, NDAs, rental agreements, "
            "service agreements and other document categories."
        )


    with feature2:

        st.subheader(
            "📥 Document Export"
        )

        st.write(
            "Generated documents can be downloaded as TXT or DOCX."
        )

        st.subheader(
            "⚡ FastAPI Backend"
        )

        st.write(
            "A FastAPI backend handles document-generation requests "
            "between the frontend and AI layer."
        )

        st.subheader(
            "🛡️ Draft Disclaimer"
        )

        st.write(
            "The application clearly identifies generated documents "
            "as drafts that should receive professional legal review."
        )


# ============================================================
# HOW IT WORKS
# ============================================================

elif page == "📖 How It Works":

    st.title(
        "📖 How LegalEase Works"
    )

    st.write(
        "The application follows a simple four-stage workflow."
    )

    st.divider()

    st.subheader(
        "1️⃣ User Input"
    )

    st.write(
        "The user selects a document type and provides parties, "
        "dates, role information and key terms."
    )

    st.subheader(
        "2️⃣ FastAPI Backend"
    )

    st.write(
        "The Streamlit frontend sends the information to the "
        "FastAPI backend through the /generate endpoint."
    )

    st.subheader(
        "3️⃣ Gemini AI"
    )

    st.write(
        "The backend sends a structured prompt to Gemini, which "
        "creates the legal document draft."
    )

    st.subheader(
        "4️⃣ Review & Export"
    )

    st.write(
        "The generated document is displayed in an editable preview. "
        "The user can review it and download it as TXT or DOCX."
    )

    st.divider()

    st.subheader(
        "System Flow"
    )

    st.info(
        "User Input  →  Streamlit  →  FastAPI  →  Gemini AI  "
        "→  Generated Document  →  Review  →  Export"
    )

    st.divider()

    st.warning(
        "AI-generated legal documents should be reviewed by a "
        "qualified legal professional before use or signing."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "⚖️ LegalEase | AI-Powered Legal Document Generator"
)

st.caption(
    "Generated documents are drafts for informational and "
    "document-preparation purposes."
)