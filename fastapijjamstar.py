from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

# Create FastAPI instance at module level
app = FastAPI(title="Invoice Generator API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LineItem(BaseModel):
    description: str
    units: int = Field(gt=0)
    cost_per_unit: float = Field(gt=0)

class InvoiceData(BaseModel):
    invoice_number: str
    bill_to: str
    department: str
    tax_rate: float = Field(ge=0, le=1)
    line_items: List[LineItem]

def generate_invoice(data: InvoiceData):
    invoice_date_str = datetime.now().strftime('%Y-%m-%d')
    output_filename = f"invoice_{data.invoice_number}_{invoice_date_str}.pdf"
    
    # Use absolute path
    abs_path = os.path.abspath(output_filename)
    
    # Create PDF with absolute path
    c = canvas.Canvas(abs_path, pagesize=A4)
    height = A4[1]

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20 * mm, height - 30 * mm, "INVOICE")
    c.setFont("Helvetica", 10)
    c.drawString(20 * mm, height - 35 * mm, f"Jamstar Invoice No. {data.invoice_number}")
    c.drawString(20 * mm, height - 40 * mm, "James Onyango")
    c.drawString(20 * mm, height - 45 * mm, "P.O. BOX 93116 - 00100 Nairobi")
    c.drawString(20 * mm, height - 50 * mm, "Email: jjamstart@gmail.com")
    c.drawString(20 * mm, height - 55 * mm, "Pin: P051846384Z")

    # Invoice Date
    c.drawString(130 * mm, height - 35 * mm, f"Invoice Date: {invoice_date_str}")

    # Bill To
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20 * mm, height - 70 * mm, "Bill To:")
    c.setFont("Helvetica", 10)
    c.drawString(30 * mm, height - 75 * mm, data.bill_to)
    c.drawString(30 * mm, height - 80 * mm, data.department)

    # Table Headers
    table_top = height - 100 * mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20 * mm, table_top, "Description")
    c.drawString(110 * mm, table_top, "Units")
    c.drawString(130 * mm, table_top, "Cost/Unit")
    c.drawString(160 * mm, table_top, "Amount")

    # Line Items
    y = table_top - 7 * mm
    c.setFont("Helvetica", 10)
    subtotal = 0

    for item in data.line_items:
        amount = item.units * item.cost_per_unit
        subtotal += amount

        # Handle long descriptions with wrapping
        max_desc_width = 80 * mm
        desc = item.description
        if c.stringWidth(desc) > max_desc_width:
            while c.stringWidth(desc + "...") > max_desc_width:
                desc = desc[:-1]
            desc += "..."

        c.drawString(20 * mm, y, desc)
        c.drawRightString(115 * mm, y, f"{item.units}")
        c.drawRightString(145 * mm, y, f"{item.cost_per_unit:,.2f}")
        c.drawRightString(180 * mm, y, f"{amount:,.2f}")
        y -= 10 * mm

    # Calculate Tax and Total
    total = subtotal
    pretax_amount = total / (1 + data.tax_rate)
    tax_amount = total - pretax_amount

    y -= 10 * mm
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(155 * mm, y, "Invoice Subtotal:")
    c.drawRightString(190 * mm, y, f"{pretax_amount:,.2f} KES")
    y -= 7 * mm
    c.drawRightString(155 * mm, y, f"Tax {int(data.tax_rate * 100)}%:")
    c.drawRightString(190 * mm, y, f"{tax_amount:,.2f} KES")
    y -= 7 * mm
    c.drawRightString(155 * mm, y, "TOTAL:")
    c.drawRightString(190 * mm, y, f"{total:,.2f} KES")

    # Footer
    y -= 20 * mm
    c.setFont("Helvetica", 9)
    c.drawString(20 * mm, y, "MAKE ALL PAYMENTS PAYABLE TO JAMES ONYANGO")
    y -= 7 * mm
    c.drawString(20 * mm, y, "1. Mpesa number 0716 951 781")
    y -= 7 * mm
    c.drawString(20 * mm, y, "2. Diamond Trust Bank Nyali Branch, Account Number 0279483001")
    y -= 7 * mm
    c.drawString(20 * mm, y, "3. Cash")
    y -= 10 * mm
    c.drawString(20 * mm, y, "Thank you for your business!")

    c.showPage()
    c.save()
    return abs_path

@app.post("/generate-invoice")
async def create_invoice(data: InvoiceData):
    temp_file = None
    try:
        # Create output directory if it doesn't exist
        output_dir = "temp_invoices"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate unique filename
        invoice_date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f"invoice_{data.invoice_number}_{invoice_date_str}.pdf"
        filepath = os.path.join(output_dir, filename)
        abs_path = os.path.abspath(filepath)
        temp_file = abs_path
        
        # Generate the invoice using the existing generate_invoice function
        abs_path = generate_invoice(data)
        
        # Verify file exists before sending
        if not os.path.exists(abs_path):
            raise HTTPException(
                status_code=500,
                detail="Failed to generate invoice file"
            )
            
        # Return file response
        return FileResponse(
            path=abs_path,
            media_type="application/pdf",
            filename=filename,
            background=None  # Remove background callback
        )
        
    except Exception as e:
        print(f"Error generating invoice: {str(e)}")
        # Clean up file if it exists
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up file after response is sent
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass