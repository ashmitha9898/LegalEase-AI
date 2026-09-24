from ai_core.gemini_generator import GeminiDocumentGenerator

generator = GeminiDocumentGenerator()

print("Gemini configured:", generator.is_configured)
print("Model:", generator.model_name)

document = generator.generate_document(
    document_type="Non-Disclosure Agreement",
    parties="Party A: ABC Company\nParty B: John Doe",
    terms="Confidentiality of company information for 2 years.",
    dates="Effective date: 23 September 2026",
)

print("\n--- GENERATED DOCUMENT ---\n")
print(document)