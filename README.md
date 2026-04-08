# LexiScanAuto

LexiScanAuto is a Data Science and Machine Learning project that extracts and validates entities from PDF and Image documents using OCR and standard NER practices. 

## Features
- End-to-end OCR processing using Tesseract.
- Named Entity Recognition (NER) pipeline using SpaCy.
- Rules Engine to validate extracted data (like date validations).
- FastAPI backend to serve the model predictions.
- Docker support included.

## Installation & Setup

To run this project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd LexiScanAuto
   ```

2. **Create a Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate  
   # On macOS/Linux:
   # source venv/bin/activate  
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: You will also need Tesseract-OCR and Poppler installed on your system for OCR and PDF handling)*

4. **Run the Application / API:**
   ```bash
   python api.py
   ```

5. **Test the API:**
   Open your browser and navigate to the Swagger UI:
   `http://localhost:8001/docs`
   Here you can completely test the `/extract` endpoint visually by uploading files.

## Usage
- Train the NER model by running `python train_ner.py`.
- Run tests using `pytest`.
