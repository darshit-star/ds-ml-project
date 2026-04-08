from fastapi import FastAPI, File, UploadFile, HTTPException
from ocr_pipeline import OCRPipeline
from ner_model import NERPipeline
from rules_engine import RulesEngine
import os
import shutil

app = FastAPI(title="LexiScan Auto API")

# Initialize models and pipelines
ocr = OCRPipeline()
ner = NERPipeline()
rules = RulesEngine()

@app.post("/extract")
async def extract_entities(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Only PDF and Image files are supported.")
        
    temp_file_path = f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Step 1: OCR Pipeline
        if file.filename.lower().endswith('.pdf'):
            text = ocr.process_pdf(temp_file_path)
        else:
            text = ocr.process_image(temp_file_path)
        
        # Step 2: NER Model
        raw_entities = ner.extract_entities(text)
        
        # Step 3: Rules Engine
        structured_output = rules.validate_entities(raw_entities)
        
        return {
            "status": "success",
            "extracted_text_preview": text[:200] + "..." if len(text) > 200 else text,
            "entities": structured_output
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
