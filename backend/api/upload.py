from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from backend.config.settings import settings

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

# Supported document types
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document and save it locally.

    Supported formats:
    - PDF
    - DOCX
    - TXT
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    unique_filename = f"{uuid4().hex}{extension}"

    save_path = settings.UPLOAD_DIRECTORY / unique_filename

    try:
        with open(save_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                buffer.write(chunk)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(error)}"
        )

    finally:
        await file.close()

    return JSONResponse(
        status_code=201,
        content={
            "message": "File uploaded successfully.",
            "original_filename": file.filename,
            "stored_filename": unique_filename,
            "path": str(save_path),
        },
    )