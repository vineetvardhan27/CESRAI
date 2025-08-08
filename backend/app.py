from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import json
import re
from decimal import Decimal, InvalidOperation
import os
from werkzeug.utils import secure_filename
import tempfile
import pymongo
from dotenv import load_dotenv
from bson.objectid import ObjectId
import pandas as pd
from jinja2 import Template
from reportlab.pdfgen import canvas
from export_utils import export_utils
import textwrap

# --- Flask App Initialization ---
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# --- Load environment variables ---
load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/digestadoc')
MONGODB_DB = os.getenv('MONGODB_DB', 'digestadoc')
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default_secret')
app.secret_key = FLASK_SECRET_KEY

# --- MongoDB Client Setup with Error Handling ---
try:
    mongo_client = pymongo.MongoClient(MONGODB_URI)
    # Test the connection
    mongo_client.admin.command('ping')
    db = mongo_client[MONGODB_DB]
    pdf_collection = db['pdfs']
    summary_collection = db['summaries']
    print("✅ MongoDB connected successfully")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    mongo_client = None
    db = None
    pdf_collection = None
    summary_collection = None

# --- Save PDF and Summary to MongoDB ---
def save_pdf_and_summary(pdf_filename, summary_json, company_details=None):
    if not mongo_client:
        return None, None
    
    try:
        pdf_doc = {
            "filename": pdf_filename, 
            "summary_id": None,
            "company_details": company_details  # Include company details
        }
        pdf_id = pdf_collection.insert_one(pdf_doc).inserted_id
        summary_doc = {"pdf_id": pdf_id, "summary": summary_json}
        summary_id = summary_collection.insert_one(summary_doc).inserted_id
        pdf_collection.update_one({"_id": pdf_id}, {"$set": {"summary_id": summary_id}})
        return str(pdf_id), str(summary_id)
    except Exception as e:
        print(f"Error saving to MongoDB: {e}")
        return None, None

# --- Retrieve Summary by PDF ID ---
def get_summary_by_pdf_id(pdf_id):
    if not mongo_client:
        return None
    
    try:
        summary_doc = summary_collection.find_one({"pdf_id": ObjectId(pdf_id)})
        return summary_doc["summary"] if summary_doc else None
    except Exception as e:
        print(f"Error retrieving from MongoDB: {e}")
        return None

# --- Export utilities are now handled by export_utils.py ---

# --- Your Corrected and Integrated PDF Parsing Logic ---

def safe_get_value(text_blob, pattern, group=1, default="-"):
    """
    Safely extracts a value from a text blob using a regex pattern.
    Returns the found group or a default value if not found.
    """
    try:
        match = re.search(pattern, text_blob, re.DOTALL | re.IGNORECASE)
        if match and group <= len(match.groups()):
            # Ensure the matched group is not None before stripping
            value = match.group(group)
            return value.strip().replace('\n', ' ') if value else default
    except IndexError:
        print(f"Warning: Group {group} does not exist for pattern: {pattern}")
    return default

def convert_to_lakhs(amount_str):
    """
    Converts a string amount to a formatted string in Lakhs.
    Example: "374400000.00" -> "3744.00 Lakhs"
    """
    if not amount_str or amount_str == '-':
        return "0.00 Lakhs"
    try:
        amount = Decimal(amount_str)
        lakhs = amount / Decimal('100000')
        return f"{lakhs:.2f} Lakhs"
    except (InvalidOperation, TypeError):
        return "0.00 Lakhs"

# --- Asset and Security Field Maps (from user logic) ---
asset_field_map = {
    "asset_id": r"Asset ID\s*([0-9]+)",
    "plot_id": r"Plot Number\s*([^\n\r]+?)(?:\s+Area|\n|$)",
    "survey_no": r"Survey Number\s*/\s*Municipal Number\s*([^\n\r]+?)(?:\s+Plot|\n|$)",
    "house_id": r"House\s*/\s*Flat Number\s*/\s*Unit No\s*([^\n\r]+?)(?:\s+Floor|\n|$)",
    "floor_no": r"Floor No\s*([^\n\r]+?)(?:\s+Building|\n|$)",
    "building_no": r"Building\s*/\s*Tower Name\s*/\s*Number\s*([^\n\r]+?)(?:\s+Name|\n|$)",
    "building_name": r"Name of the Project\s*/\s*Scheme\s*/\s*Society\s*/\s*Zone\s*([^\n\r]+?)(?:\s+Street|\n|$)",
    "buildup_area": r"Area\s*([0-9.]+)",
    "street_name": r"Street Name\s*/\s*Number\s*([^\n\r]+?)(?:\s+Pocket|\n|$)",
    "sector_ward_no": r"Locality\s*/\s*Sector\s*([^\n\r]+?)(?:\s+City|\n|$)",
    "locality": r"Locality\s*/\s*Sector\s*([^\n\r]+?)(?:\s+City|\n|$)",
    "landmark": r"Landmark\s*([^\n\r]+?)(?:\s+Block|\n|$)",
    "block_no": r"Block Number\s*([^\n\r]+?)(?:\s+Village|\n|$)",
    "village": r"City\s*/\s*Town\s*/\s*Village\s*([^\n\r]+?)(?:\s+District|\n|$)",
    "town": r"City\s*/\s*Town\s*/\s*Village\s*([^\n\r]+?)(?:\s+District|\n|$)",
    "taluka": r"Taluka\s*([^\n\r]+?)(?:\s+District|\n|$)",
    "district": r"District\s*([^\n\r]+?)(?:\s+State|\n|$)",
    "pin_code": r"Pin Code\s*/\s*Post Code\s*([0-9]+)",
    "state": r"State\s*/\s*UT\s*([^\n\r]+)",
}

security_field_map = {
    "security_interest_id": r"Security Interest ID\s*([0-9]+)",
    "security_interest_type": r"Type Of Security Interest\s*([^\n\r]+?)(?:\s+Type Of Finance|\s+Details Of Charge|\n|$)",
    "si_creation_date": r"SI Creation Date In Bank\s*([0-9\-]+)",
    "charge_holder_name": r"Charge Holder Name\s+Office / Ward / Branch Name\s*(.*?)\s*(?:Original View|Transaction History)",
    "charge_amount": r"Total Secured Amount\s*([0-9.]+)",
    "borrower_type": r"Borrower Type\s*([^\n\r]+?)(?:\s+Asset Category|\s+Name of the Debtor|\n|$)",
    "details_of_charge": r"Details Of Charge\s*([^\n\r]+)",
}

def parse_borrower_details(text_blob):
    borrower_section_match = re.search(r"Borrower\(s\) Details(.*?)Holder Details", text_blob, re.DOTALL | re.IGNORECASE)
    if not borrower_section_match:
        return None, None
    borrower_text = borrower_section_match.group(1)
    borrower_line_match = re.search(r"^\s*1\s+.*?Company\s+(.*?)\s+NA\s+(Yes|No)", borrower_text, re.MULTILINE | re.IGNORECASE)
    if borrower_line_match:
        borrower_name = borrower_line_match.group(1).strip().replace('\n', ' ')
        is_owner = borrower_line_match.group(2).strip()
        borrower_name_formatted = f"{borrower_name} (Maharashtra, PIN: 400013)"
        third_party_mortgagee = "N/A"
        if is_owner.lower() == 'no':
            third_party_mortgagee = "Details to be extracted"
        return borrower_name_formatted, third_party_mortgagee
    return None, None

def extract_data_from_pdf(pdf_path, company_details=None):
    """
    Extracts data from CERSAI PDF files.
    
    Args:
        pdf_path: Path to the PDF file
        company_details: Optional dict containing company information from frontend form
                        Keys: companyName, cinNumber, searchReferenceId, dateOfIncorporation, 
                              udin, registeredOffice
    
    Returns:
        Tuple of (asset_data, header_info) where header_info uses company_details if provided
    """
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
    # Asset details
    asset_details = {}
    for key, pattern in asset_field_map.items():
        asset_details[key] = safe_get_value(full_text, pattern, default="-")
    # Buildup area (combine area and unit)
    area_value = asset_details.get("buildup_area", "-")
    area_unit = safe_get_value(full_text, r"Area Unit\s*(\w+\s*\w+)", default="-")
    asset_details["buildup_area"] = f"{area_value} {area_unit}".strip() if area_value != '-' and area_unit != '-' else "-"
    # Security interest details
    security_interest_details = {}
    for key, pattern in security_field_map.items():
        security_interest_details[key] = safe_get_value(full_text, pattern, default="-")
    # Charge holder name and amount
    charge_holder_name = security_interest_details.get("charge_holder_name", "-")
    charge_amount_raw = security_interest_details.get("charge_amount", "0.00")
    charge_amount = convert_to_lakhs(charge_amount_raw)
    security_interest_details["charge_holder_name_amount"] = f"{charge_holder_name} Rs. {charge_amount}"
    # Borrower details
    borrower_name, third_party_mortgagee = parse_borrower_details(full_text)
    security_interest_details["borrowers"] = borrower_name or "-"
    security_interest_details["sub_borrower"] = "-"
    security_interest_details["third_party_mortgagees"] = third_party_mortgagee or "-"
    # Is assetUnder Charge?/ Ranking of Charge logic
    details_of_charge_pattern = r"Details Of Charge\s*([^\n\r]+)"
    details_of_charge = safe_get_value(full_text, details_of_charge_pattern, default="-")
    if details_of_charge and details_of_charge != "-":
        security_interest_details["Is assetUnder Charge?/ Ranking of Charge"] = f"Yes {details_of_charge.strip()}"
    else:
        security_interest_details["Is assetUnder Charge?/ Ranking of Charge"] = "No"
    # Remove any old keys if present
    if "Asset Under Charge Ranking" in security_interest_details:
        del security_interest_details["Asset Under Charge Ranking"]
    if "is_asset_under_charge_ranking" in security_interest_details:
        del security_interest_details["is_asset_under_charge_ranking"]
    security_interest_details["charge_release_date"] = "N/A"
    
    # Header info - Use company details from frontend if provided, otherwise extract from PDF
    if company_details:
        header_info = {
            "name_of_company": company_details.get("companyName", "-"),
            "cin_number": company_details.get("cinNumber", "-"),
            "search_reference_id": company_details.get("searchReferenceId", safe_get_value(full_text, r"Transaction ID / QRF NO\s*([0-9]+)")),
            "date_of_incorporation": company_details.get("dateOfIncorporation", "-"),
            "udin": company_details.get("udin", "-"),  # Add UDIN field
            "registered_office": company_details.get("registeredOffice", "-")
        }
    else:
        # Fallback to static values and PDF extraction if no company details provided
        header_info = {
            "name_of_company": "APRN ENTERPRISES PRIVATE LIMITED",
            "cin_number": "U21000MH1994PTC084095",
            "search_reference_id": safe_get_value(full_text, r"Transaction ID / QRF NO\s*([0-9]+)"),
            "date_of_incorporation": "28.12.1994",
            "udin": "-",  # Add UDIN field with default value
            "registered_office": "SUN PARADISE BUSINESS PLAZA, 7 TH FLOOR CITY SURVEY NO 1 A/456 SENAPATI BAPAT MA, RG, Mumbai City, LOWER PAREL MUMBAI, Maharashtra, India, 400013."
        }
    return {
        "asset_details_of_security_interest": asset_details,
        "security_interest_details": security_interest_details
    }, header_info

def process_cersai_reports(pdf_paths, company_details=None):
    """
    Processes a list of CERSAI PDF files and returns a consolidated dictionary.
    """
    if not pdf_paths:
        return {"error": "No PDF files provided."}

    final_json_structure = {"company_details": {}, "assets": []}
    for i, pdf_path in enumerate(pdf_paths):
        try:
            asset_data, header_data = extract_data_from_pdf(pdf_path, company_details)
            if i == 0:
                final_json_structure["company_details"] = header_data
            final_json_structure["assets"].append(asset_data)
        except Exception as e:
            print(f"Error processing file {pdf_path}: {e}")
            final_json_structure["assets"].append({
                "error": f"Failed to process file: {os.path.basename(pdf_path)}",
                "details": str(e)
            })
    return final_json_structure

# --- Flask API Endpoints ---

@app.route('/process', methods=['GET', 'POST'])
def process_pdf_endpoint():
    if request.method == 'GET':
        return jsonify({
            "message": "PDF Processing API is running",
            "endpoint": "/process",
            "method": "POST",
            "description": "Upload PDF files for processing"
        })
    
    if 'files[]' not in request.files:
        return jsonify({"error": "No file part in the request. Please upload files with the key 'files[]'."}), 400
    
    files = request.files.getlist('files[]')
    
    if not files or files[0].filename == '':
        return jsonify({"error": "No files were selected for upload."}), 400

    # Extract company details from form data if provided
    company_details = None
    if 'companyDetails' in request.form:
        try:
            import json
            company_details = json.loads(request.form['companyDetails'])
            print(f"📋 Company details received: {company_details.get('companyName', 'N/A')}")
        except json.JSONDecodeError:
            print("⚠️  Failed to parse company details from form data")

    # Log file upload details
    print(f"📤 Processing {len(files)} file(s):")
    for i, file in enumerate(files):
        print(f"   File {i+1}: {file.filename} ({file.content_type})")

    saved_paths = []
    with tempfile.TemporaryDirectory() as temp_dir:
        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(temp_dir, filename)
                file.save(filepath)
                saved_paths.append(filepath)
                print(f"   Saved: {filename} -> {filepath}")
        
        if not saved_paths:
            return jsonify({"error": "No valid files to process."}), 400
            
        print(f"🔄 Processing {len(saved_paths)} PDF file(s)...")
        json_output = process_cersai_reports(saved_paths, company_details)
        print(f"✅ Processing complete")

    return jsonify(json_output)

# --- New API Endpoints ---
@app.route('/save_summary', methods=['POST'])
def save_summary_endpoint():
    if not mongo_client:
        return jsonify({'error': 'MongoDB not connected'}), 500
    
    data = request.json
    pdf_filename = data.get('filename')
    summary_json = data.get('summary')
    company_details = data.get('companyDetails')  # Get company details from request
    
    if not pdf_filename or not summary_json:
        return jsonify({'error': 'Missing filename or summary'}), 400
    
    # Log the incoming data for debugging
    print(f"📁 Saving to MongoDB:")
    print(f"   Filename(s): {pdf_filename}")
    print(f"   Summary keys: {list(summary_json.keys()) if isinstance(summary_json, dict) else 'Not a dict'}")
    if company_details:
        print(f"   Company: {company_details.get('companyName', 'N/A')}")
    
    pdf_id, summary_id = save_pdf_and_summary(pdf_filename, summary_json, company_details)
    if pdf_id and summary_id:
        print(f"✅ Saved successfully - PDF ID: {pdf_id}, Summary ID: {summary_id}")
        return jsonify({'pdf_id': pdf_id, 'summary_id': summary_id})
    else:
        print(f"❌ Failed to save to MongoDB")
        return jsonify({'error': 'Failed to save to MongoDB'}), 500

@app.route('/get_summary/<pdf_id>', methods=['GET'])
def get_summary_endpoint(pdf_id):
    if not mongo_client:
        return jsonify({'error': 'MongoDB not connected'}), 500
    
    summary = get_summary_by_pdf_id(pdf_id)
    if not summary:
        return jsonify({'error': 'Summary not found'}), 404
    return jsonify({'summary': summary})

# --- Updated Export Endpoints ---
@app.route('/export/<pdf_id>/<format>', methods=['GET'])
def export_summary_endpoint(pdf_id, format):
    if not mongo_client:
        return jsonify({'error': 'MongoDB not connected'}), 500
    
    summary = get_summary_by_pdf_id(pdf_id)
    if not summary:
        return jsonify({'error': 'Summary not found'}), 404
    
    try:
        if format == 'html':
            html = export_utils.json_to_html(summary)
            return html, 200, {'Content-Type': 'text/html'}
        elif format == 'excel':
            output_path = tempfile.mktemp(suffix='.xlsx')
            export_utils.json_to_excel(summary, output_path)
            with open(output_path, 'rb') as f:
                data = f.read()
            os.remove(output_path)
            return data, 200, {
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                'Content-Disposition': f'attachment; filename=summary_{pdf_id}.xlsx'
            }
        elif format == 'pdf':
            output_path = tempfile.mktemp(suffix='.pdf')
            export_utils.json_to_pdf(summary, output_path)
            with open(output_path, 'rb') as f:
                data = f.read()
            os.remove(output_path)
            return data, 200, {
                'Content-Type': 'application/pdf', 
                'Content-Disposition': f'attachment; filename=summary_{pdf_id}.pdf'
            }
        else:
            return jsonify({'error': 'Invalid format'}), 400
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

# --- Health Check Endpoint ---
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "mongodb_connected": mongo_client is not None,
        "endpoints": {
            "process": "/process",
            "save_summary": "/save_summary", 
            "get_summary": "/get_summary/<pdf_id>",
            "export": "/export/<pdf_id>/<format>"
        }
    })

# --- Main Execution Block ---
if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    print(f"📊 MongoDB URI: Is on")
    print("🌐 Server will run at: http://127.0.0.1:5000")
    print("📋 Available endpoints:")
    print("   - GET  /health - Health check")
    print("   - GET  /process - API info")
    print("   - POST /process - Upload PDFs")
    print("   - POST /save_summary - Save to MongoDB")
    print("   - GET  /get_summary/<id> - Get summary")
    print("   - GET  /export/<id>/<format> - Export files")
    app.run(debug=True, host='0.0.0.0', port=5000)


