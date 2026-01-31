from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse
from src.rag.store import ingest_file

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
    responses={404: {"description": "Not found"}}
)

@router.post("", summary="Upload a document", description="Upload and ingest a document into the RAG system")
def add_document(file: UploadFile):
    ingest_file(file)
    return JSONResponse(content="File uploaded sucessfull",status_code=201)
    