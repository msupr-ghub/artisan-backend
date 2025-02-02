# Create FastAPI instance
import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.api.auth.auth import router as auth_router
from app.router import api_router
from app.startup import process_knowledge_base

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Artisan chat bot",
    description="Artisan chat bot",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
app.include_router(auth_router, tags=["Auth"])


@app.exception_handler(Exception)
async def http_exception_handler(request, exc):
    message = str(exc)
    logger.error(f"request: {request.url}, body {request.body}, exception: {message}")
    error_response = {
        "detail": ["Server error"],  # this will make it compliant with standard FastAPI error definition
    }
    return JSONResponse(error_response, status_code=exc.status_code if hasattr(exc, 'status_code') else 500)


@app.on_event("startup")
async def startup_event():
    await process_knowledge_base()


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# If using uvicorn directly in the file
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
