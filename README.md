# CERSAI Document Automation

This project automates the extraction, processing, and structured representation of data from system-generated CERSAI Search Reports. It transforms multiple input PDF documents into a consolidated and client-friendly summary report.

## Technologies Used

This project is built with:
* **Frontend:**
    * Vite
    * TypeScript
    * React
    * shadcn-ui
    * Tailwind CSS
* **Backend:**
    * Flask
    * MongoDB
    * Pandas
    * Jinja2
    * ReportLab

## Setup and Installation

### Prerequisites

* Node.js (v16+)
* Python (v3.8+)
* MongoDB (local or Atlas)
* Git

### 1. Clone the repository

```sh
git clone <YOUR_GIT_URL>
cd <YOUR_PROJECT_NAME>



# Complete Setup Guide for Digest-a-Doc

This guide will help you set up and test the complete PDF processing and export system.

## 🏗️ **System Architecture**

```
Frontend (React) ←→ Backend (Flask) ←→ MongoDB
     ↓                    ↓              ↓
  Upload PDFs    →   Process PDFs   →  Store Data
     ↓                    ↓              ↓
  Download Files ←   Export Files   ←  Retrieve Data
```

## 📋 **Prerequisites**

- **Node.js** (v16+) for frontend
- **Python** (v3.8+) for backend
- **MongoDB** (local or Atlas)
- **Git** for version control

## 🚀 **Step-by-Step Setup**

### 1. **Clone and Navigate**
```bash
cd digest-a-doc-main
```

### 2. **Backend Setup**

#### Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Set Up Environment Variables
Create a `.env` file in the `backend/` directory:
```env
MONGODB_URI=mongodb://localhost:27017/digestadoc
MONGODB_DB=digestadoc
FLASK_SECRET_KEY=your_generated_secret_key_here
```

**Generate Secret Key:**
```python
import secrets
print(secrets.token_hex(32))
```

#### Start MongoDB
- **Local MongoDB:** Start MongoDB service
- **MongoDB Atlas:** Use your connection string

#### Start Backend Server
```bash
python app.py
```

**Expected Output:**
```
🚀 Starting Flask server...
📊 MongoDB URI: mongodb://localhost:27017/digestadoc
🗄️  Database: digestadoc
🌐 Server will run at: http://127.0.0.1:5000
✅ MongoDB connected successfully
```

### 3. **Frontend Setup**

#### Install Dependencies
```bash
cd ..  # Back to root directory
npm install
```

#### Install Additional Frontend Dependencies
```bash
npm install react-dropzone
```

#### Start Frontend Server
```bash
npm run dev
```

**Expected Output:**
```
VITE v4.x.x ready in xxx ms
➜  Local:   http://localhost:3000/
```

## 🧪 **Testing the Complete Flow**

### 1. **Test Backend Health**
Visit: `http://localhost:5000/health`

**Expected Response:**
```json
{
  "status": "healthy",
  "mongodb_connected": true,
  "endpoints": {
    "process": "/process",
    "save_summary": "/save_summary",
    "get_summary": "/get_summary/<pdf_id>",
    "export": "/export/<pdf_id>/<format>"
  }
}
```

### 2. **Run Automated Tests**
```bash
cd backend
python test_flow.py
```

**Expected Output:**
```
🧪 Starting backend flow tests...
==================================================
✅ Health check: {'status': 'healthy', 'mongodb_connected': True, ...}
✅ Process endpoint info: {'message': 'PDF Processing API is running', ...}
✅ Mock JSON created successfully
✅ Saved to MongoDB with PDF ID: 507f1f77bcf86cd799439011
✅ Retrieved from MongoDB successfully
✅ HTML export successful
✅ Excel export successful
✅ PDF export successful

🎉 All tests passed! The backend flow is working correctly.
```

### 3. **Test Frontend Integration**

1. **Open Browser:** `http://localhost:3000`
2. **Upload PDF:** Drag & drop or select PDF files
3. **Process Files:** Click "Process Files" button
4. **Download Results:** Use download buttons on result page

## 📊 **Complete Data Flow**

### **Step 1: PDF Upload & Processing**
```
Frontend → POST /process → Backend processes PDF → Returns JSON
```

### **Step 2: MongoDB Storage**
```
Backend → POST /save_summary → MongoDB stores data → Returns PDF ID
```

### **Step 3: Data Retrieval**
```
Frontend → GET /get_summary/<pdf_id> → MongoDB retrieves data → Returns JSON
```

### **Step 4: Export Generation**
```
Frontend → GET /export/<pdf_id>/<format> → Backend generates file → Downloads file
```

## 🗄️ **MongoDB Collections**

### **`pdfs` Collection**
```json
{
  "_id": "ObjectId",
  "filename": "document.pdf",
  "summary_id": "ObjectId"
}
```

### **`summaries` Collection**
```json
{
  "_id": "ObjectId",
  "pdf_id": "ObjectId",
  "summary": {
    "company_details": {...},
    "assets": [...]
  }
}
```

## 🔧 **API Endpoints Reference**

| Endpoint | Method | Description | Request | Response |
|----------|--------|-------------|---------|----------|
| `/health` | GET | Health check | - | Status info |
| `/process` | GET | API info | - | Endpoint details |
| `/process` | POST | Upload PDFs | FormData | JSON data |
| `/save_summary` | POST | Save to MongoDB | JSON | PDF ID |
| `/get_summary/<id>` | GET | Get summary | - | JSON data |
| `/export/<id>/html` | GET | Export HTML | - | HTML file |
| `/export/<id>/pdf` | GET | Export PDF | - | PDF file |
| `/export/<id>/excel` | GET | Export Excel | - | Excel file |

## 🐛 **Troubleshooting**

### **Backend Issues**

#### MongoDB Connection Failed
```bash
# Check if MongoDB is running
mongosh --eval "db.adminCommand('ping')"

# Update .env with correct URI
MONGODB_URI=mongodb://localhost:27017/digestadoc
```

#### Missing Dependencies
```bash
pip install -r requirements.txt
```

#### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

### **Frontend Issues**

#### CORS Errors
- Ensure backend has CORS enabled
- Check backend is running on `http://localhost:5000`

#### Network Errors
- Verify backend server is running
- Check browser console for detailed errors

### **Export Issues**

#### PDF Generation Fails
- Ensure `reportlab` is installed
- Check file permissions

#### Excel Generation Fails
- Ensure `openpyxl` is installed
- Check available disk space

## 📁 **File Structure**

```
digest-a-doc-main/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── export_utils.py     # Export utilities
│   ├── requirements.txt    # Python dependencies
│   ├── test_flow.py       # Automated tests
│   ├── .env               # Environment variables
│   └── README.md          # Backend documentation
├── src/
│   ├── components/
│   │   ├── FileUpload.tsx     # File upload component
│   │   ├── DownloadButtons.tsx # Download buttons
│   │   └── SummaryResult.tsx   # Result page
│   └── ...
├── package.json
└── SETUP_GUIDE.md         # This file
```

## 🎯 **Success Criteria**

✅ **Backend running on port 5000**  
✅ **Frontend running on port 3000**  
✅ **MongoDB connected successfully**  
✅ **Health check returns 200**  
✅ **PDF upload and processing works**  
✅ **Data saved to MongoDB**  
✅ **Export functionality works**  
✅ **Frontend can download files**  

## 🚀 **Next Steps**

1. **Customize PDF Processing:** Modify `extract_data_from_pdf()` in `app.py`
2. **Enhance Export Templates:** Update `export_utils.py`
3. **Add Authentication:** Implement user management
4. **Scale Database:** Use MongoDB Atlas for production
5. **Add Error Handling:** Implement comprehensive error handling
6. **Add Logging:** Implement proper logging system

---

**🎉 Congratulations! Your PDF processing and export system is now fully functional!**
