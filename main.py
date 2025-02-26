from fastapi import FastAPI
from app.routes import upload, query

app = FastAPI(
    title="CV Insight API",
    description="An API for extracting and querying structured CV information.",
    version="1.0.0"
)

app.include_router(upload.router)
app.include_router(query.router)