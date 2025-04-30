from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from datetime import datetime

def generate_invoice(data):
    invoice_date_str = datetime.now().strftime('%Y-%m-%d')
    output_filename = f"invoice_{data['invoice_number']}_{invoice_date_str}.pdf"
    
    c = canvas.Canvas(output_filename, pagesize=A4)
    height = A4[1]

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20 * mm, height - 30 * mm, "INVOICE")
    c.setFont("Helvetica", 10)
    c.drawString(20 * mm, height - 35 * mm, f"Jamstar Invoice No. {data['invoice_number']}")
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
    c.drawString(30 * mm, height - 75 * mm, data['bill_to'])
    c.drawString(30 * mm, height - 80 * mm, data['department'])

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

    for item in data['line_items']:
        desc, units, cost_per_unit = item
        amount = units * cost_per_unit
        subtotal += amount

        # Truncate long descriptions
        max_desc_width = 80 * mm
        if c.stringWidth(desc) > max_desc_width:
            while c.stringWidth(desc + "...") > max_desc_width:
                desc = desc[:-1]
            desc += "..."

        c.drawString(20 * mm, y, desc)
        c.drawRightString(115 * mm, y, f"{units}")
        c.drawRightString(145 * mm, y, f"{cost_per_unit:,.2f}")
        c.drawRightString(180 * mm, y, f"{amount:,.2f}")
        y -= 10 * mm

    # Calculate Tax and Total
    total = subtotal
    pretax_amount = total / (1 + data['tax_rate'])
    tax_amount = total - pretax_amount

    y -= 10 * mm
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(155 * mm, y, "Invoice Subtotal:")
    c.drawRightString(190 * mm, y, f"{pretax_amount:,.2f} KES")
    y -= 7 * mm
    c.drawRightString(155 * mm, y, f"Tax {int(data['tax_rate'] * 100)}%:")
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
    print(f"Invoice generated successfully as {output_filename}!")
    return output_filename


def main():
    try:
        data = {
            'invoice_number': input("Enter invoice number: ").strip(),
            'bill_to': input("Enter 'Bill To' name: ").strip(),
            'department': input("Enter department: ").strip(),
            'tax_rate': float(input("Enter tax rate (e.g. 0.05 for 5%): ").strip()),
            'line_items': []
        }

        print("\nEnter line items (leave description blank to finish):")
        item_number = 1
        while True:
            print(f"\nItem #{item_number}")
            desc = input("Description: ").strip()
            if not desc:
                if not data['line_items']:
                    print("At least one item is required!")
                    continue
                break

            try:
                units = int(input("Units: ").strip())
                if units <= 0:
                    print("Units must be greater than 0.")
                    continue

                cost = float(input("Cost per unit: ").strip())
                if cost <= 0:
                    print("Cost must be greater than 0.")
                    continue

                data['line_items'].append((desc, units, cost))
                item_number += 1

            except ValueError:
                print("Please enter valid numbers for units and cost.")

        if data['line_items']:
            filename = generate_invoice(data)
            print(f"\nInvoice generated successfully: {filename}")
        else:
            print("\nNo items entered. Invoice generation cancelled.")

    except KeyboardInterrupt:
        print("\nInvoice generation cancelled.")
    except Exception as e:
        print(f"\nError generating invoice: {e}")


if __name__ == "__main__":
    main()
