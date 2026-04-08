import json

def read_file(name):
    with open(name, "r") as f:
        return f.read()

notebook = {
    "cells": [],
    "metadata": {
        "colab": {
            "provenance": []
        },
        "kernelspec": {
            "display_name": "Python 3",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

def add_md(text): 
    notebook["cells"].append({"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)})

def add_code(text): 
    notebook["cells"].append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": text.splitlines(True)})

md_intro = '''# 📄 LexiScan Auto — Automated Legal Entity Extractor
## Complete Project: Week 1 → Week 4

| Week | Focus | Key Deliverables |
|------|-------|------------------|
| 1 | OCR Pipeline | Setup Tesseract, pdf2image, Text Extraction |
| 2 | NER Modelling | Spacy Custom NER, Training Pipeline, Entity Extraction |
| 3 | Rules Engine | Date standardization, Business rules validation |
| 4 | Deployment | FastAPI Service, Dockerization |'''

add_md(md_intro)

add_md("## ⚙️ Step 0 — Install Dependencies")
add_code("!apt-get update -y\n!apt-get install -y tesseract-ocr poppler-utils\n!pip install pytesseract pdf2image spacy fastapi uvicorn python-multipart python-dateutil nest_asyncio -q\n!python -m spacy download en_core_web_sm -q\nprint('Dependencies ready ✅')")

add_md("## 📦 Step 1 — Import Libraries")
add_code("import os\nimport json\nimport re\nimport spacy\nimport pytesseract\nfrom pdf2image import convert_from_path\nfrom datetime import datetime\nfrom dateutil import parser\nfrom fastapi import FastAPI, UploadFile, File, Form, HTTPException\nimport uvicorn\nimport nest_asyncio\nfrom pydantic import BaseModel\nprint('Libraries Imported ✅')")

add_md("## 📄 Step 2 — OCR Pipeline (`ocr_pipeline.py`)")
add_code(read_file("ocr_pipeline.py").replace("import pytesseract\\nfrom pdf2image import convert_from_path\\nimport os", ""))

add_md("## 🧠 Step 3 — NER Script (`train_ner.py` & `ner_model.py`)")
add_code(read_file("train_ner.py").replace("import spacy\\nimport random\\nimport os", "import random"))
add_code(read_file("ner_model.py").replace("import spacy\\nimport os", ""))

add_md("## ⚖️ Step 4 — Rules Engine (`rules_engine.py`)")
add_code(read_file("rules_engine.py").replace("import re\\nfrom datetime import datetime\\nfrom dateutil import parser", ""))

add_md("## 🚀 Step 5 — FastAPI Service (`api.py`)")
api_code = read_file("api.py")
api_code = api_code.replace("from fastapi import FastAPI, UploadFile, File, Form, HTTPException\\nimport os", "")
api_code = api_code.replace("uvicorn.run(app", "#uvicorn.run(app")
add_code(api_code)

add_md("## 🧪 Step 6 — Run Complete Pipeline\\nRun the code below to see the end-to-end extraction result.")
test_code = '''# 1. Train model locally in colab
train_ner_model()

# 2. Simulate pipeline
print("\\n--- Pipeline Initialized ---")
ocr = OCRPipeline()
ner = NERPipeline()
rules = RulesEngine()

text = "This contract is effective as of January 1, 2025. The termination date is December 31, 2026. The total cost is $50,000 for Acme Corp."
print("\\nInput Text:", text)

entities = ner.extract_entities(text)
final_output = rules.validate_entities(entities)

print("\\nExtracted and Validated JSON:")
print(json.dumps(final_output, indent=4))
'''
add_code(test_code)

with open("LexiScanAuto_Week1_to_4.ipynb", "w", encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("Notebook LexiScanAuto_Week1_to_4.ipynb generated successfully!")
