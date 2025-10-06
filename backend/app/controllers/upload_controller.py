from fastapi import APIRouter, UploadFile, File, HTTPException
import csv
from typing import List

router = APIRouter()

@router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    content = await file.read()
    decoded = content.decode('utf-8').splitlines()
    reader = csv.reader(decoded)
    rows: List[list] = [row for row in reader]
    return {"filename": file.filename, "rows": rows}