from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="Clinical Privacy Gateway",
    description=(
        "Secure clinical text de-identification gateway "
        "for protecting PHI before downstream processing."
    ),
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "clinical-privacy-gateway",
    }


app.include_router(router)