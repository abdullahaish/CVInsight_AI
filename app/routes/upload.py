from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from app.services.extractor import extract_text
from app.services.llm_analysis import analyze_cv
from app.config import cvs_collection
from app.utils.logger import logger

router = APIRouter()


@router.post("/upload/")
async def upload_cv(file: UploadFile = File(...)):
    """Uploads and processes a CV."""
    logger.info(f"Received CV upload request: {file.filename}")

    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in ["pdf", "docx"]:
        logger.warning(f"Unsupported file type attempted: {file_ext}")
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_path = f"temp.{file_ext}"

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
        logger.debug(f"Saved uploaded file to {file_path}")

        text = extract_text(file_path, file_ext)
        if not text.strip():
            logger.error(f"Text extraction failed for {file_path}")
            raise HTTPException(status_code=400, detail="Failed to extract text from CV.")

        extracted_data = analyze_cv(text)
        inserted_cv = cvs_collection.insert_one(extracted_data)
        extracted_data["_id"] = str(inserted_cv.inserted_id)

        logger.info(f"CV successfully processed and stored with ID: {extracted_data['_id']}")

        return {"message": "CV uploaded and processed successfully", "data": extracted_data}

    except Exception as e:
        logger.exception(f"Error processing CV: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.debug(f"Temporary file {file_path} removed after processing")
