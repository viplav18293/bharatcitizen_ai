from fastapi import APIRouter, HTTPException, UploadFile, File, Form

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form(...),
    source_url: str = Form(None)
):
    try:
        from services.ingestion_service import ingestion_service

        result = await ingestion_service.ingest_file(file, category, source_url)
        return {"message": "File ingested successfully", "details": result}
    except ImportError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Document ingestion dependencies are not installed: {e}",
        )
    except Exception as e:
        return {"error": str(e)}
