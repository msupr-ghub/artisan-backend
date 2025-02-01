# Create FastAPI instance
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.router import api_router

load_dotenv()
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

# Basic health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# If using uvicorn directly in the file
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)