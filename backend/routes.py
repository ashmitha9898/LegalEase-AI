from fastapi import APIRouter, HTTPException

from backend.models import DocumentRequest
from ai_core.gemini_generator import GeminiDocumentGenerator


# ============================================================
# ROUTER
# ============================================================

router = APIRouter()


# ============================================================
# GEMINI GENERATOR
# ============================================================

generator = GeminiDocumentGenerator()


# ============================================================
# HEALTH CHECK
# ============================================================

@router.get("/health")
def health():

    return {
        "status": "ok",
        "service": "LegalEase",
        "mode": "gemini" if generator.is_configured else "demo"
    }


# ============================================================
# GENERATE LEGAL DOCUMENT
# ============================================================

@router.post("/generate")
def generate_legal_document(
    request: DocumentRequest
):

    try:

        # ----------------------------------------------------
        # CHECK GEMINI
        # ----------------------------------------------------

        if not generator.is_configured:

            raise HTTPException(
                status_code=500,
                detail="Gemini API key is not configured."
            )


        # ----------------------------------------------------
        # GENERATE USING GEMINI
        # ----------------------------------------------------

        document = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates
        )


        # ----------------------------------------------------
        # CHECK RESPONSE
        # ----------------------------------------------------

        if not document:

            raise HTTPException(
                status_code=500,
                detail="Gemini returned an empty document."
            )


        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return {
            "document": document,
            "document_type": request.document_type,
            "mode": "gemini"
        }


    except HTTPException:

        raise


    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Gemini document generation failed: {exc}"
        )