from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Secure Enterprise AI", version="0.1.0")
app.include_router(router, prefix="/api/v1")

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}

@app.get("/ready", tags=["system"])
def ready():
    # TODO: check that required services and document index are ready.
    return {"status": "ready"}
