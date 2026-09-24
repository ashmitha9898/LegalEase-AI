from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router


app = FastAPI(
    title="LegalEase - AI Legal Document Generator",
    description=(
        "LegalEase is a legal document drafting "
        "application with document preview and export."
    ),
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Welcome to LegalEase",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
    )