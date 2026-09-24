import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GEMINI DOCUMENT GENERATOR
# ============================================================

class GeminiDocumentGenerator:

    def __init__(self):

        self.api_key = os.getenv(
            "GEMINI_API_KEY",
            ""
        ).strip()

        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        ).strip()

        self.client = None

        if self.api_key:

            self.client = genai.Client(
                api_key=self.api_key
            )


    # ========================================================
    # CHECK CONFIGURATION
    # ========================================================

    @property
    def is_configured(self):

        return (
            self.client is not None
            and bool(self.api_key)
        )


    # ========================================================
    # GENERATE LEGAL DOCUMENT
    # ========================================================

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        dates
    ):

        if not self.is_configured:

            raise RuntimeError(
                "Gemini API key is not configured."
            )


        # ----------------------------------------------------
        # LEGAL DOCUMENT PROMPT
        # ----------------------------------------------------

        prompt = f"""
You are the AI document-generation engine for LegalEase.

Create a professional legal document draft based strictly
on the information provided by the user.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE:
{dates}

KEY TERMS AND CONDITIONS:
{terms}

IMPORTANT INSTRUCTIONS:

1. Create a clear and professional legal-document structure.

2. Use appropriate headings and numbered sections.

3. Include the parties and effective date clearly.

4. Include the terms and conditions provided by the user.

5. Do not invent important facts such as names, addresses,
   salaries, dates, obligations, or penalties that the user
   did not provide.

6. If information is missing, use a neutral placeholder
   such as "[Not Provided]" where appropriate.

7. Use professional and easy-to-understand language.

8. Include a signature section at the end.

9. Include a short notice stating that the document is a
   generated draft and should be reviewed by a qualified
   legal professional before signing.

10. Return ONLY the document itself.

Do not explain what you are doing.
Do not add commentary before or after the document.
"""


        # ----------------------------------------------------
        # GENERATE WITH RETRIES
        # ----------------------------------------------------

        last_error = None

        for attempt in range(3):

            try:

                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.3,
                        max_output_tokens=5000
                    )
                )

                generated_text = getattr(
                    response,
                    "text",
                    None
                )


                # ------------------------------------------------
                # VALIDATE RESPONSE
                # ------------------------------------------------

                if not generated_text:

                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )


                return generated_text.strip()


            except Exception as exc:

                last_error = exc

                # Retry temporary failures
                if attempt < 2:

                    time.sleep(5)


        # ----------------------------------------------------
        # ALL RETRIES FAILED
        # ----------------------------------------------------

        raise RuntimeError(
            f"Gemini generation failed after 3 attempts: "
            f"{last_error}"
        )