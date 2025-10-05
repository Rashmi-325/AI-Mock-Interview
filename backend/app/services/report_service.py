from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_pdf_report(session: dict) -> str:
    filename = f"/tmp/report_{session.get('_id')}"
    c = canvas.Canvas(filename)
    c.setFont("Helvetica", 14)
    c.drawString(50, 800, f"Interview Report - Session ID: {session.get('_id')}")
    c.drawString(50, 780, f"User: {session.get('user_id')}")
    # write questions & answers summary
    y = 740
    for i, q in enumerate(session.get("questions", [])):
        c.drawString(50, y, f"Q{i+1}: {q.get('text')}")
        y -= 20
    c.save()
    return filename