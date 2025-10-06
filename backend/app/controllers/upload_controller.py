from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import csv_service

router = APIRouter()

@router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    content = await file.read()
    rows = csv_service.process_csv(content)
    return {"filename": file.filename, "rows": rows}