from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_debit_note(data):
    c = canvas.Canvas("debit_note_generated.pdf", pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 40, "UTILITY COVER INSURANCE AGENCIES")
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, height - 60, "SUMMIT HOUSE, M13")
    c.drawCentredString(width / 2, height - 75, "P.O. BOX 4737 – 00100 NAIROBI")
    c.drawCentredString(width / 2, height - 90, "TEL: 020 310040/1 CELL: 0722 766 583 / 0733-766 583")
    c.drawCentredString(width / 2, height - 105, "Email: utilitycoverinsuranceagencies@gmail.com")

    y = height - 140
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "MOTOR DEBIT / RISK NOTE")

    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"SUM INSURED:        Kshs. {data['sum_insured']:,}")
    y -= 20
    c.drawString(50, y, f"BASIC PREMIUM RATE: {data['basic_premium_rate']}%")
    y -= 20
    c.drawString(50, y, f"BASIC PREMIUM:      Kshs. {data['calculated_basic_premium']:,}")
    y -= 20
    c.drawString(50, y, f"Excess Protector:   Kshs. {data['excess_protector']:,}")
    y -= 20
    c.drawString(50, y, f"Radio Cassette:     {data['radio_cassette']} (Free)")
    y -= 20
    c.drawString(50, y, f"Windscreen Cover:   {data['windscreen_cover']} (Free)")
    y -= 20
    c.drawString(50, y, f"+TL:                Kshs. {data['tl']:,}")
    y -= 20
    c.drawString(50, y, f"+SD:                Kshs. {data['sd']:,}")

    total_premium = (
        data['calculated_basic_premium']
        + data['excess_protector']
        + data['tl']
        + data['sd']
    )

    y -= 30
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, f"Total premium:      Kshs. {total_premium:,}")

    # Additional Details
    y -= 40
    c.setFont("Helvetica", 10)
    fields = [
        ("CLASS OF INSURANCE", data['class_of_insurance']),
        ("POLICY NUMBER", data['policy_number']),
        ("NAME OF INSURED", data['name_of_insured']),
        ("OCCUPATION", data['occupation']),
        ("PIN NUMBER", data['pin_number']),
        ("VEHICLE COVERED", data['vehicle_covered']),
        ("ENGINE NO.", data['engine_no']),
        ("CHASIS", data['chasis']),
        ("SITTING CAPACITY", data['sitting_capacity']),
        ("COLOR", data['color']),
        ("PERIOD OF INSURANCE", data['period_of_insurance']),
    ]
    for label, value in fields:
        c.drawString(50, y, f"{label}: {value}")
        y -= 20

    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Terms of Payment:")
    c.setFont("Helvetica", 10)
    y -= 20
    c.drawString(70, y, f"{data['terms_of_payment']}")

    y -= 40
    c.drawString(50, y, f"Date Issued: {data['date_issued']}")

    c.save()
    print("Debit Note generated successfully!")

def main():
    sum_insured = float(input("Enter Sum Insured (Kshs.): "))
    basic_premium_rate = float(input("Enter Basic Premium Rate (%): "))
    calculated_basic_premium = (sum_insured * basic_premium_rate) / 100

    data = {
        "sum_insured": sum_insured,
        "basic_premium_rate": basic_premium_rate,
        "calculated_basic_premium": round(calculated_basic_premium),
        "excess_protector": int(input("Enter Excess Protector (Kshs.): ")),
        "radio_cassette": input("Enter Radio Cassette Value: "),
        "windscreen_cover": input("Enter Windscreen Cover Value: "),
        "tl": int(input("Enter +TL Value (Kshs.): ")),
        "sd": int(input("Enter +SD Value (Kshs.): ")),
        "class_of_insurance": input("Enter Class of Insurance: "),
        "policy_number": input("Enter Policy Number: "),
        "name_of_insured": input("Enter Name of Insured: "),
        "occupation": input("Enter Occupation: "),
        "pin_number": input("Enter PIN Number: "),
        "vehicle_covered": input("Enter Vehicle Covered: "),
        "engine_no": input("Enter Engine No.: "),
        "chasis": input("Enter Chasis No.: "),
        "sitting_capacity": input("Enter Sitting Capacity: "),
        "color": input("Enter Vehicle Color: "),
        "period_of_insurance": input("Enter Period of Insurance (e.g., 26/09/2024 - 25/09/2025): "),
        "terms_of_payment": input("Enter Terms of Payment: "),
        "date_issued": datetime.now().strftime("%d/%m/%Y"),
    }

    generate_debit_note(data)

if __name__ == "__main__":
    main()
