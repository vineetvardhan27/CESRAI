# Backend Setup Guide

This backend provides PDF processing, MongoDB storage, and export functionality for the Digest-a-Doc application.

## Prerequisites

- Python 3.8+
- MongoDB (local or Atlas)
- pip

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the backend directory with the following variables:
   ```
   MONGODB_URI=mongodb://localhost:27017/digestadoc
   MONGODB_DB=digestadoc
   FLASK_SECRET_KEY=your_generated_secret_key_here
   ```

   To generate a secret key, run:
   ```python
   import secrets
   secrets.token_hex(32)
   ```

## Running the Backend

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **The server will run on:** `http://localhost:5000`

## API Endpoints

### PDF Processing
- `POST /process` - Upload and process PDF files
  - Form data: `files[]` (multiple PDF files)

### Data Storage
- `POST /save_summary` - Save processed summary to MongoDB
  - JSON body: `{"filename": "file.pdf", "summary": {...}}`

### Data Retrieval
- `GET /get_summary/<pdf_id>` - Retrieve summary by PDF ID

### Export Functions
- `GET /export/<pdf_id>/html` - Export as HTML
- `GET /export/<pdf_id>/pdf` - Export as PDF
- `GET /export/<pdf_id>/excel` - Export as Excel

## MongoDB Collections

- `pdfs` - Stores PDF metadata and references to summaries
- `summaries` - Stores the extracted JSON summary data

## File Structure

```
backend/
├── app.py              # Main Flask application
├── export_utils.py     # Export utilities (HTML, PDF, Excel)
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
└── README.md          # This file
```

## Frontend Integration

The frontend can connect to these endpoints to:
1. Upload PDFs for processing
2. Save processed data to MongoDB
3. Download summaries in PDF/Excel formats

## Troubleshooting

- **MongoDB Connection Error:** Ensure MongoDB is running and the URI is correct
- **Import Errors:** Make sure all dependencies are installed
- **CORS Issues:** The backend is configured to work with the React frontend on localhost:3000
