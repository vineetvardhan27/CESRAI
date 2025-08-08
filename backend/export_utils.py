import json
import pandas as pd
from jinja2 import Template
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
import tempfile
import os

class ExportUtils:
    def __init__(self):
        self.html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CERSAI Report Summary</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #2c3e50;
            margin: 0;
            font-size: 2.5em;
        }
        .section {
            margin-bottom: 30px;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
        }
        .section-header {
            background: #34495e;
            color: white;
            padding: 15px 20px;
            font-size: 1.2em;
            font-weight: bold;
        }
        .section-content {
            padding: 20px;
        }
        .data-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        .data-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }
        .data-label {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        .data-value {
            color: #555;
            word-break: break-word;
            white-space: pre-line;
        }
        .company-details {
            background: #e8f4fd;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .asset-list {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .asset-item {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            background: #fafafa;
        }
        .sub-section {
            margin-top: 15px;
        }
        .sub-section h4 {
            color: #34495e;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
            margin-bottom: 15px;
        }
        @media print {
            body { background: white; }
            .container { box-shadow: none; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CERSAI Report Summary</h1>
            <p>Generated on {{ generation_date }}</p>
        </div>
        
        {% if company_details %}
        <div class="section">
            <div class="section-header">Company Details</div>
            <div class="section-content">
                <div class="company-details">
                    <div class="data-grid">
                        <div class="data-item">
                            <div class="data-label">Company Name</div>
                            <div class="data-value">{{ company_details.name_of_company }}</div>
                        </div>
                        <div class="data-item">
                            <div class="data-label">CIN Number</div>
                            <div class="data-value">{{ company_details.cin_number }}</div>
                        </div>
                        <div class="data-item">
                            <div class="data-label">Search Reference ID</div>
                            <div class="data-value">{{ company_details.search_reference_id }}</div>
                        </div>
                        <div class="data-item">
                            <div class="data-label">Date of Incorporation</div>
                            <div class="data-value">{{ company_details.date_of_incorporation }}</div>
                        </div>
                        <div class="data-item">
                            <div class="data-label">UDIN</div>
                            <div class="data-value">{{ company_details.udin }}</div>
                        </div>
                    </div>
                    <div class="data-item" style="grid-column: 1 / -1;">
                        <div class="data-label">Registered Office</div>
                        <div class="data-value" style="white-space: pre-line;">{{ company_details.registered_office }}</div>
                    </div>
                </div>
            </div>
        </div>
        {% endif %}
        
        {% if assets %}
        <div class="section">
            <div class="section-header">Asset Details</div>
            <div class="section-content">
                <div class="asset-list">
                    {% for asset in assets %}
                    <div class="asset-item">
                        <h3>Asset {{ loop.index }}</h3>
                        
                        <div class="sub-section">
                            <h4>Asset Details</h4>
                            <div class="data-grid">
                                <div class="data-item">
                                    <div class="data-label">Asset ID</div>
                                    <div class="data-value">{{ asset.asset_details_of_security_interest.asset_id }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Plot ID</div>
                                    <div class="data-value">{{ asset.asset_details_of_security_interest.plot_id }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Survey Number</div>
                                    <div class="data-value">{{ asset.asset_details_of_security_interest.survey_no }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">House ID</div>
                                    <div class="data-value">{{ asset.asset_details_of_security_interest.house_id }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Floor Number</div>
                                    <div class="data-value">{{ asset.asset_details_of_security_interest.floor_no }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Building Number</div>
                                    <div class="data-value">{{ asset.asset_details_of_security_interest.building_no }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Building Name</div>
                                    <div class="data-value">{{ asset.asset_details_of_security_interest.building_name }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Buildup Area</div>
                                    <div class="data-value">{{ asset.asset_details_of_security_interest.buildup_area }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Street Name</div>
                                    <div class="data-value">{{ asset.asset_details_of_security_interest.street_name }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Locality</div>
                                    <div class="data-value">{{ asset.asset_details_of_security_interest.locality }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Landmark</div>
                                    <div class="data-value">{{ asset.asset_details_of_security_interest.landmark }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Block Number</div>
                                    <div class="data-value">{{ asset.asset_details_of_security_interest.block_no }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Village/Town</div>
                                    <div class="data-value">{{ asset.asset_details_of_security_interest.village }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Taluka</div>
                                    <div class="data-value">{{ asset.asset_details_of_security_interest.taluka }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">District</div>
                                    <div class="data-value">{{ asset.asset_details_of_security_interest.district }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Pin Code</div>
                                    <div class="data-value">{{ asset.asset_details_of_security_interest.pin_code }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">State</div>
                                    <div class="data-value">{{ asset.asset_details_of_security_interest.state }}</div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="sub-section">
                            <h4>Security Interest Details</h4>
                            <div class="data-grid">
                                <div class="data-item">
                                    <div class="data-label">Security Interest ID</div>
                                    <div class="data-value">{{ asset.security_interest_details.security_interest_id }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Security Interest Type</div>
                                    <div class="data-value">{{ asset.security_interest_details.security_interest_type }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">SI Creation Date</div>
                                    <div class="data-value">{{ asset.security_interest_details.si_creation_date }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Charge Holder & Amount</div>
                                    <div class="data-value">{{ asset.security_interest_details.charge_holder_name_amount }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Is assetUnder Charge?/ Ranking of Charge</div>
                                    <div class="data-value">{{ asset.security_interest_details['Is assetUnder Charge?/ Ranking of Charge'] }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Charge Release Date</div>
                                    <div class="data-value">{{ asset.security_interest_details.charge_release_date }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Borrower Type</div>
                                    <div class="data-value">{{ asset.security_interest_details.borrower_type }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Borrowers</div>
                                    <div class="data-value">{{ asset.security_interest_details.borrowers }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Sub Borrower</div>
                                    <div class="data-value">{{ asset.security_interest_details.sub_borrower }}</div>
                                </div>
                                <div class="data-item">
                                    <div class="data-label">Third Party Mortgagees</div>
                                    <div class="data-value">{{ asset.security_interest_details.third_party_mortgagees }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
        """

    def json_to_html(self, json_data):
        """Convert JSON data to formatted HTML"""
        from datetime import datetime
        
        template = Template(self.html_template)
        html_content = template.render(
            company_details=json_data.get('company_details', {}),
            assets=json_data.get('assets', []),
            generation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        return html_content

    def json_to_excel(self, json_data, output_path):
        """Convert JSON data to Excel file"""
        # Create a writer object
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Company Details Sheet
            if 'company_details' in json_data:
                company_df = pd.DataFrame([json_data['company_details']])
                company_df.to_excel(writer, sheet_name='Company Details', index=False)
            
            # Assets Sheet
            if 'assets' in json_data and json_data['assets']:
                # Flatten asset details for better Excel structure
                assets_data = []
                for i, asset in enumerate(json_data['assets']):
                    asset_row = {
                        'Asset_Index': i + 1,
                        'Asset_ID': asset.get('asset_details_of_security_interest', {}).get('asset_id', ''),
                        'Plot_ID': asset.get('asset_details_of_security_interest', {}).get('plot_id', ''),
                        'Survey_Number': asset.get('asset_details_of_security_interest', {}).get('survey_no', ''),
                        'House_ID': asset.get('asset_details_of_security_interest', {}).get('house_id', ''),
                        'Floor_Number': asset.get('asset_details_of_security_interest', {}).get('floor_no', ''),
                        'Building_Number': asset.get('asset_details_of_security_interest', {}).get('building_no', ''),
                        'Building_Name': asset.get('asset_details_of_security_interest', {}).get('building_name', ''),
                        'Buildup_Area': asset.get('asset_details_of_security_interest', {}).get('buildup_area', ''),
                        'Street_Name': asset.get('asset_details_of_security_interest', {}).get('street_name', ''),
                        'Locality': asset.get('asset_details_of_security_interest', {}).get('locality', ''),
                        'Landmark': asset.get('asset_details_of_security_interest', {}).get('landmark', ''),
                        'Block_Number': asset.get('asset_details_of_security_interest', {}).get('block_no', ''),
                        'Village_Town': asset.get('asset_details_of_security_interest', {}).get('village', ''),
                        'Taluka': asset.get('asset_details_of_security_interest', {}).get('taluka', ''),
                        'District': asset.get('asset_details_of_security_interest', {}).get('district', ''),
                        'Pin_Code': asset.get('asset_details_of_security_interest', {}).get('pin_code', ''),
                        'State': asset.get('asset_details_of_security_interest', {}).get('state', ''),
                        'Security_Interest_ID': asset.get('security_interest_details', {}).get('security_interest_id', ''),
                        'Security_Interest_Type': asset.get('security_interest_details', {}).get('security_interest_type', ''),
                        'SI_Creation_Date': asset.get('security_interest_details', {}).get('si_creation_date', ''),
                        'Charge_Holder_Amount': asset.get('security_interest_details', {}).get('charge_holder_name_amount', ''),
                        'Is assetUnder Charge?/ Ranking of Charge': asset.get('security_interest_details', {}).get('Is assetUnder Charge?/ Ranking of Charge', ''),
                        'Charge_Release_Date': asset.get('security_interest_details', {}).get('charge_release_date', ''),
                        'Borrower_Type': asset.get('security_interest_details', {}).get('borrower_type', ''),
                        'Borrowers': asset.get('security_interest_details', {}).get('borrowers', ''),
                        'Sub_Borrower': asset.get('security_interest_details', {}).get('sub_borrower', ''),
                        'Third_Party_Mortgagees': asset.get('security_interest_details', {}).get('third_party_mortgagees', '')
                    }
                    assets_data.append(asset_row)
                
                assets_df = pd.DataFrame(assets_data)
                assets_df.to_excel(writer, sheet_name='Asset Details', index=False)
    # Orignal formate 
    # def json_to_pdf(self, json_data, output_path):
    #     """Convert JSON data to PDF file"""
    #     doc = SimpleDocTemplate(output_path, pagesize=A4)
    #     styles = getSampleStyleSheet()
    #     story = []
        
    #     # Title
    #     title_style = ParagraphStyle(
    #         'CustomTitle',
    #         parent=styles['Heading1'],
    #         fontSize=24,
    #         spaceAfter=30,
    #         alignment=1  # Center alignment
    #     )
    #     story.append(Paragraph("CERSAI Report Summary", title_style))
    #     story.append(Spacer(1, 20))
        
    #     # Company Details
    #     if 'company_details' in json_data:
    #         company = json_data['company_details']
    #         story.append(Paragraph("Company Details", styles['Heading2']))
    #         story.append(Spacer(1, 12))
            
    #         company_data = [
    #             ['Company Name', company.get('name_of_company', '')],
    #             ['CIN Number', company.get('cin_number', '')],
    #             ['Search Reference ID', company.get('search_reference_id', '')],
    #             ['Date of Incorporation', company.get('date_of_incorporation', '')],
    #             ['Registered Office', Paragraph(company.get('registered_office', ''), ParagraphStyle('wrap', wordWrap='CJK', fontName='Helvetica', fontSize=10))]
    #         ]
            
    #         company_table = Table(company_data, colWidths=[2*inch, 4*inch])
    #         company_table.setStyle(TableStyle([
    #             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    #             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    #             ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    #             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    #             ('FONTSIZE', (0, 0), (-1, 0), 12),
    #             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    #             ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    #             ('GRID', (0, 0), (-1, -1), 1, colors.black)
    #         ]))
    #         story.append(company_table)
    #         story.append(Spacer(1, 20))
        
    #     # Asset Details
    #     if 'assets' in json_data and json_data['assets']:
    #         story.append(Paragraph("Asset Details", styles['Heading2']))
    #         story.append(Spacer(1, 12))
            
    #         for i, asset in enumerate(json_data['assets']):
    #             story.append(Paragraph(f"Asset {i+1}", styles['Heading3']))
    #             story.append(Spacer(1, 12))
                
    #             # Asset Details Table
    #             asset_details = asset.get('asset_details_of_security_interest', {})
    #             asset_data = [
    #                 ['Asset ID', asset_details.get('asset_id', '')],
    #                 ['Plot ID', asset_details.get('plot_id', '')],
    #                 ['Survey Number', asset_details.get('survey_no', '')],
    #                 ['House ID', asset_details.get('house_id', '')],
    #                 ['Floor Number', asset_details.get('floor_no', '')],
    #                 ['Building Number', asset_details.get('building_no', '')],
    #                 ['Building Name', asset_details.get('building_name', '')],
    #                 ['Buildup Area', asset_details.get('buildup_area', '')],
    #                 ['Street Name', asset_details.get('street_name', '')],
    #                 ['Locality', asset_details.get('locality', '')],
    #                 ['Landmark', asset_details.get('landmark', '')],
    #                 ['Block Number', asset_details.get('block_no', '')],
    #                 ['Village/Town', asset_details.get('village', '')],
    #                 ['Taluka', asset_details.get('taluka', '')],
    #                 ['District', asset_details.get('district', '')],
    #                 ['Pin Code', asset_details.get('pin_code', '')],
    #                 ['State', asset_details.get('state', '')]
    #             ]
                
    #             asset_table = Table(asset_data, colWidths=[2*inch, 4*inch])
    #             asset_table.setStyle(TableStyle([
    #                 ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    #                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    #                 ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    #                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    #                 ('FONTSIZE', (0, 0), (-1, 0), 10),
    #                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    #                 ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    #                 ('GRID', (0, 0), (-1, -1), 1, colors.black)
    #             ]))
    #             story.append(asset_table)
    #             story.append(Spacer(1, 20))
                
    #             # Security Interest Details
    #             security_details = asset.get('security_interest_details', {})
    #             security_data = [
    #                 ['Security Interest ID', Paragraph(security_details.get('security_interest_id', ''), ParagraphStyle('wrap', wordWrap='CJK', fontName='Helvetica', fontSize=10))],
    #                 ['Security Interest Type', Paragraph(security_details.get('security_interest_type', ''), ParagraphStyle('wrap', wordWrap='CJK', fontName='Helvetica', fontSize=10))],
    #                 ['SI Creation Date', Paragraph(security_details.get('si_creation_date', ''), ParagraphStyle('wrap', wordWrap='CJK', fontName='Helvetica', fontSize=10))],
    #                 ['Charge Holder & Amount', Paragraph(security_details.get('charge_holder_name_amount', ''), ParagraphStyle('wrap', wordWrap='CJK', fontName='Helvetica', fontSize=10))],
    #                 ['Is assetUnder Charge?/ Ranking of Charge', Paragraph(security_details.get('Is assetUnder Charge?/ Ranking of Charge', ''), ParagraphStyle('wrap', wordWrap='CJK', fontName='Helvetica', fontSize=10))],
    #                 ['Charge Release Date', Paragraph(security_details.get('charge_release_date', ''), ParagraphStyle('wrap', wordWrap='CJK', fontName='Helvetica', fontSize=10))],
    #                 ['Borrower Type', Paragraph(security_details.get('borrower_type', ''), ParagraphStyle('wrap', wordWrap='CJK', fontName='Helvetica', fontSize=10))],
    #                 ['Borrowers', Paragraph(security_details.get('borrowers', ''), ParagraphStyle('wrap', wordWrap='CJK', fontName='Helvetica', fontSize=10))],
    #                 ['Sub Borrower', Paragraph(security_details.get('sub_borrower', ''), ParagraphStyle('wrap', wordWrap='CJK', fontName='Helvetica', fontSize=10))],
    #                 ['Third Party Mortgagees', Paragraph(security_details.get('third_party_mortgagees', ''), ParagraphStyle('wrap', wordWrap='CJK', fontName='Helvetica', fontSize=10))]
    #             ]
                
    #             security_table = Table(security_data, colWidths=[2*inch, 4*inch])
    #             security_table.setStyle(TableStyle([
    #                 ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    #                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    #                 ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    #                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    #                 ('FONTSIZE', (0, 0), (-1, 0), 10),
    #                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    #                 ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    #                 ('GRID', (0, 0), (-1, -1), 1, colors.black)
    #             ]))
    #             story.append(security_table)
    #             story.append(Spacer(1, 30))
        
    #     doc.build(story)
    
    # improved formate 
    # def json_to_pdf(self, json_data, output_path):
    #     """Convert JSON data to PDF file"""
    #     doc = SimpleDocTemplate(output_path, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    #     styles = getSampleStyleSheet()
    #     story = []

    #     # Define a consistent style for all table values that need to wrap
    #     value_style = ParagraphStyle(
    #         'value_style',
    #         parent=styles['BodyText'],
    #         fontSize=9,
    #         leading=12,  # Line spacing
    #         wordWrap='CJK' # Handles word wrapping
    #     )

    #     # Define a reusable and clean style for all key-value tables
    #     table_style = TableStyle([
    #         # Styles for the Key Column (Column 0)
    #         ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F0F0F0')), # Light grey background
    #         ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    #         ('TEXTCOLOR', (0, 0), (0, -1), colors.black),

    #         # Styles for all cells
    #         ('GRID', (0, 0), (-1, -1), 1, colors.black),
    #         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    #         ('TOPPADDING', (0, 0), (-1, -1), 6),
    #         ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    #     ])

    #     # Title
    #     title_style = ParagraphStyle(
    #         'CustomTitle',
    #         parent=styles['h1'],
    #         fontSize=18,
    #         spaceAfter=20,
    #         alignment=1  # Center alignment
    #     )
    #     story.append(Paragraph("CERSAI Report Summary", title_style))

    #     # Helper function to create table data rows with Paragraphs
    #     def create_para_row(key, value):
    #         return [key, Paragraph(str(value), value_style)]

    #     # Company Details
    #     if 'company_details' in json_data:
    #         company = json_data['company_details']
    #         story.append(Paragraph("Company Details", styles['h2']))
    #         story.append(Spacer(1, 12))

    #         company_data = [
    #             create_para_row('Company Name', company.get('name_of_company', 'N/A')),
    #             create_para_row('CIN Number', company.get('cin_number', 'N/A')),
    #             create_para_row('Search Reference ID', company.get('search_reference_id', 'N/A')),
    #             create_para_row('Date of Incorporation', company.get('date_of_incorporation', 'N/A')),
    #             create_para_row('Registered Office', company.get('registered_office', 'N/A'))
    #         ]

    #         company_table = Table(company_data, colWidths=[1.75*inch, 5.25*inch])
    #         company_table.setStyle(table_style)
    #         story.append(company_table)
    #         story.append(Spacer(1, 20))

    #     # Asset Details
    #     if 'assets' in json_data and json_data['assets']:
    #         story.append(Paragraph("Asset Details", styles['h2']))

    #         for i, asset in enumerate(json_data['assets']):
    #             story.append(Spacer(1, 12))
    #             story.append(Paragraph(f"Asset {i+1}", styles['h3']))
    #             story.append(Spacer(1, 12))

    #             # Asset Details Table
    #             asset_details = asset.get('asset_details_of_security_interest', {})
    #             asset_data = [
    #                 create_para_row('Asset ID', asset_details.get('asset_id', 'N/A')),
    #                 create_para_row('Plot ID', asset_details.get('plot_id', 'N/A')),
    #                 create_para_row('Survey Number', asset_details.get('survey_no', 'N/A')),
    #                 create_para_row('House ID', asset_details.get('house_id', 'N/A')),
    #                 create_para_row('Floor Number', asset_details.get('floor_no', 'N/A')),
    #                 create_para_row('Building Number', asset_details.get('building_no', 'N/A')),
    #                 create_para_row('Building Name', asset_details.get('building_name', 'N/A')),
    #                 create_para_row('Buildup Area', asset_details.get('buildup_area', 'N/A')),
    #                 create_para_row('Street Name', asset_details.get('street_name', 'N/A')),
    #                 create_para_row('Locality', asset_details.get('locality', 'N/A')),
    #                 create_para_row('Landmark', asset_details.get('landmark', 'N/A')),
    #                 create_para_row('Block Number', asset_details.get('block_no', 'N/A')),
    #                 create_para_row('Village/Town', asset_details.get('village', 'N/A')),
    #                 create_para_row('Taluka', asset_details.get('taluka', 'N/A')),
    #                 create_para_row('District', asset_details.get('district', 'N/A')),
    #                 create_para_row('Pin Code', asset_details.get('pin_code', 'N/A')),
    #                 create_para_row('State', asset_details.get('state', 'N/A'))
    #             ]

    #             asset_table = Table(asset_data, colWidths=[1.75*inch, 5.25*inch])
    #             asset_table.setStyle(table_style)
    #             story.append(asset_table)
    #             story.append(Spacer(1, 20))

    #             # Security Interest Details
    #             story.append(Paragraph("Security Interest Details", styles['h4']))
    #             security_details = asset.get('security_interest_details', {})
    #             security_data = [
    #                 create_para_row('Security Interest ID', security_details.get('security_interest_id', 'N/A')),
    #                 create_para_row('Security Interest Type', security_details.get('security_interest_type', 'N/A')),
    #                 create_para_row('SI Creation Date', security_details.get('si_creation_date', 'N/A')),
    #                 create_para_row('Charge Holder & Amount', security_details.get('charge_holder_name_amount', 'N/A')),
    #                 create_para_row('Is assetUnder Charge?/ Ranking of Charge', security_details.get('Is assetUnder Charge?/ Ranking of Charge', 'N/A')),
    #                 create_para_row('Charge Release Date', security_details.get('charge_release_date', 'N/A')),
    #                 create_para_row('Borrower Type', security_details.get('borrower_type', 'N/A')),
    #                 create_para_row('Borrowers', security_details.get('borrowers', 'N/A')),
    #                 create_para_row('Sub Borrower', security_details.get('sub_borrower', 'N/A')),
    #                 create_para_row('Third Party Mortgagees', security_details.get('third_party_mortgagees', 'N/A'))
    #             ]

    #             security_table = Table(security_data, colWidths=[1.75*inch, 5.25*inch])
    #             security_table.setStyle(table_style)
    #             story.append(security_table)
    #             story.append(Spacer(1, 30))

    #     doc.build(story)
    def json_to_pdf(self, json_data, output_path):
        """
        Converts JSON to PDF, wrapping both keys and values in Paragraphs to handle
        all long strings and applying dynamic spacing correctly.
        """
        doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)
        styles = getSampleStyleSheet()
        story = []

        # Style for the keys (left column) - BOLD
        key_style = ParagraphStyle(
            'key_style',
            parent=styles['BodyText'],
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=12,
            wordWrap='CJK',
        )
        
        # Style for the values (right column) - REGULAR
        value_style = ParagraphStyle(
            'value_style',
            parent=styles['BodyText'],
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            wordWrap='CJK',
        )

        # Base table style - Note: FONTNAME is removed as it's now handled by Paragraph styles
        base_table_style = TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#EAEAEA')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ])

        # Helper to create a full row with Paragraphs for both key and value
        def create_para_row(key, value):
            key_p = Paragraph(str(key), key_style)
            value_p = Paragraph(str(value or 'N/A'), value_style)
            return [key_p, value_p]

        story.append(Paragraph("CERSAI Report Summary", styles['h1']))
        story.append(Spacer(1, 0.25*inch))
        
        # --- Company Details Table ---
        if 'company_details' in json_data:
            company = json_data['company_details']
            story.append(Paragraph("Company Details", styles['h2']))
            company_data = [
                create_para_row('Company Name', company.get('name_of_company')),
                create_para_row('CIN Number', company.get('cin_number')),
                create_para_row('Search Reference ID', company.get('search_reference_id')),
                create_para_row('Date of Incorporation', company.get('date_of_incorporation')),
                create_para_row('UDIN', company.get('udin')),
                create_para_row('Registered Office', company.get('registered_office'))
            ]
            company_table = Table(company_data, colWidths=[2.0*inch, 4.7*inch])
            company_table.setStyle(base_table_style)
            story.append(company_table)
            story.append(Spacer(1, 0.25*inch))
            
        # --- Assets Tables ---
        if 'assets' in json_data and json_data['assets']:
            story.append(Paragraph("Asset Details", styles['h2']))
            for i, asset in enumerate(json_data['assets']):
                story.append(Spacer(1, 0.2*inch))
                story.append(Paragraph(f"Asset {i+1}", styles['h3']))

                # Asset Details Sub-Table
                asset_details = asset.get('asset_details_of_security_interest', {})
                asset_data = [
                    create_para_row('Asset ID', asset_details.get('asset_id')),
                    create_para_row('Plot ID', asset_details.get('plot_id')),
                    create_para_row('Survey Number', asset_details.get('survey_no')),
                    create_para_row('House ID', asset_details.get('house_id')),
                    create_para_row('Floor Number', asset_details.get('floor_no')),
                    create_para_row('Building Number', asset_details.get('building_no')),
                    create_para_row('Building Name', asset_details.get('building_name')),
                    create_para_row('Buildup Area', asset_details.get('buildup_area')),
                    create_para_row('Street Name', asset_details.get('street_name')),
                    create_para_row('Locality', asset_details.get('locality')),
                    create_para_row('Landmark', asset_details.get('landmark')),
                    create_para_row('Block Number', asset_details.get('block_no')),
                    create_para_row('Village/Town', asset_details.get('village')),
                    create_para_row('Taluka', asset_details.get('taluka')),
                    create_para_row('District', asset_details.get('district')),
                    create_para_row('Pin Code', asset_details.get('pin_code')),
                    create_para_row('State', asset_details.get('state'))
                ]
                asset_table = Table(asset_data, colWidths=[2.0*inch, 4.7*inch])
                asset_table.setStyle(base_table_style)
                story.append(asset_table)
                story.append(Spacer(1, 0.2*inch))
                
                # Security Interest Sub-Table
                story.append(Paragraph("Security Interest Details", styles['h4']))
                security_details = asset.get('security_interest_details', {})
                security_data = [
                    create_para_row('Security Interest ID', security_details.get('security_interest_id')),
                    create_para_row('Security Interest Type', security_details.get('security_interest_type')),
                    create_para_row('SI Creation Date', security_details.get('si_creation_date')),
                    create_para_row('Charge Holder & Amount', security_details.get('charge_holder_name_amount')),
                    create_para_row('Is assetUnder Charge?/ Ranking of Charge', security_details.get('Is assetUnder Charge?/ Ranking of Charge')),
                    create_para_row('Charge Release Date', security_details.get('charge_release_date')),
                    create_para_row('Borrower Type', security_details.get('borrower_type')),
                    create_para_row('Borrowers', security_details.get('borrowers')),
                    create_para_row('Sub Borrower', security_details.get('sub_borrower')),
                    create_para_row('Third Party Mortgagees', security_details.get('third_party_mortgagees'))
                ]
                
                security_table = Table(security_data, colWidths=[2.0*inch, 4.7*inch])

                # DYNAMIC PADDING LOGIC (UPDATED)
                security_specific_style = TableStyle(base_table_style.getCommands())
                long_key = 'Is assetUnder Charge?/ Ranking of Charge'
                try:
                    # Find index by checking the .text attribute of the Paragraph key
                    row_index = [row[0].text for row in security_data].index(long_key)
                    
                    security_specific_style.add('TOPPADDING', (0, row_index), (-1, row_index), 12)
                    security_specific_style.add('BOTTOMPADDING', (0, row_index), (-1, row_index), 12)
                except ValueError:
                    pass
                
                security_table.setStyle(security_specific_style)
                story.append(security_table)
                story.append(Spacer(1, 0.4*inch))
        
        doc.build(story)

# Create a global instance
export_utils = ExportUtils()

