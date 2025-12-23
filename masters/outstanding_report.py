from django.db.models import Sum
from datetime import datetime
from io import BytesIO

from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from shipments.models import BankDocument, Settlement


def get_outstanding_queryset(company_id=None, doc_type=None, as_at_date=None):
    qs = BankDocument.objects.all()

    if company_id:
        qs = qs.filter(company_id=company_id)

    if doc_type and doc_type != "ALL":
        qs = qs.filter(doc_type=doc_type)

    if as_at_date:
        qs = qs.filter(issue_date__lte=as_at_date)

    return qs


def calculate_balance(document, as_at_date):
    settled = (
        document.settlements
        .filter(settlement_date__lte=as_at_date)
        .aggregate(total=Sum("amount"))["total"] or 0
    )
    return float(document.amount or 0) - float(settled)


def generate_outstanding_excel(qs, as_at_date):
    wb = Workbook()
    ws = wb.active
    ws.title = "Outstanding Report"

    ws.append([
        "Company",
        "Doc Type",
        "Reference",
        "Issue Date",
        "Amount",
        "Outstanding Balance"
    ])

    for doc in qs:
        balance = calculate_balance(doc, as_at_date)
        if balance <= 0:
            continue

        ws.append([
            doc.company.name if doc.company else "",
            doc.doc_type,
            doc.reference_number,
            doc.issue_date.strftime("%Y-%m-%d"),
            float(doc.amount or 0),
            balance
        ])

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer


def generate_outstanding_pdf(qs, as_at_date):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 40
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, f"Outstanding Report as at {as_at_date}")
    y -= 30

    pdf.setFont("Helvetica", 10)

    for doc in qs:
        balance = calculate_balance(doc, as_at_date)
        if balance <= 0:
            continue

        text = (
            f"{doc.company.name if doc.company else ''} | "
            f"{doc.doc_type} | "
            f"{doc.reference_number} | "
            f"Balance: {balance:,.2f}"
        )

        pdf.drawString(40, y, text)
        y -= 18

        if y < 50:
            pdf.showPage()
            y = height - 40

    pdf.save()
    buffer.seek(0)
    return buffer
