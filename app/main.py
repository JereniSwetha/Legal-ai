from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS (optional but recommended)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from app.routes.upload import router as upload_router
from app.routes.analyze import router as analyze_router

# Include routers
app.include_router(upload_router, prefix="/upload")
app.include_router(analyze_router, prefix="/analyze")

@app.get("/")
def root():
    return {"message": "Backend running successfully"}
