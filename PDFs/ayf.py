#!/usr/bin/env python3
"""
Generate a premium PDF report of 2026 St. Stephen AYF Vows.
Uses ReportLab with DejaVu Sans font (supports the Naira sign ₦).
Tested on Termux and standard Linux. Adjust font path if needed.
"""

import json
import os
import sys
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Font registration: DejaVu Sans (contains ₦) ─────────────────────
def find_dejavu_sans():
    """Return the path to DejaVuSans.ttf if found, otherwise None."""
    possible_paths = [
        # Termux typical path
        "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans.ttf",
        # Alternative Termux location
        os.path.expandvars("$PREFIX/share/fonts/TTF/DejaVuSans.ttf"),
        # Standard Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
        # macOS (via homebrew)
        "/usr/local/share/fonts/dejavu-sans/DejaVuSans.ttf",
        # Windows (if present)
        "C:/Windows/Fonts/DejaVuSans.ttf",
        # Fallback – try inside the script directory
        os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf"),
    ]
    for path in possible_paths:
        if os.path.isfile(path):
            return path
    return None

FONT_PATH = find_dejavu_sans()
if FONT_PATH:
    pdfmetrics.registerFont(TTFont('DejaVuSans', FONT_PATH))
    # Also register bold variant if available (same directory)
    bold_path = FONT_PATH.replace('DejaVuSans.ttf', 'DejaVuSans-Bold.ttf')
    if os.path.isfile(bold_path):
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', bold_path))
    else:
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', FONT_PATH))  # fallback
else:
    print("WARNING: DejaVuSans.ttf not found! Naira symbol may appear as a box.",
          file=sys.stderr)
    # Fall back to Courier (no Naira)
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'Courier'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'Courier-Bold'))

# ── Helper: currency formatting ─────────────────────────────────────
def naira(amount):
    """Format amount as ₦ with comma separator."""
    return f"₦{amount:,.0f}"

# ── Styles ──────────────────────────────────────────────────────────
def create_styles():
    styles = getSampleStyleSheet()
    # Main title style
    styles.add(ParagraphStyle(
        name='ReportTitle',
        fontName='DejaVuSans-Bold',
        fontSize=18,
        leading=22,
        alignment=1,  # center
        textColor=colors.HexColor('#1A3B5C'),  # dark navy
        spaceAfter=6*mm
    ))
    # Section heading (for Paid / Partially Paid / Not Paid)
    styles.add(ParagraphStyle(
        name='SectionHeading',
        fontName='DejaVuSans-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#2E5266'),
        spaceAfter=4*mm,
        spaceBefore=6*mm
    ))
    # Summary text
    styles.add(ParagraphStyle(
        name='SummaryText',
        fontName='DejaVuSans',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#333333'),
        spaceAfter=2*mm
    ))
    # Table header style
    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName='DejaVuSans-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white,
        alignment=1  # center
    ))
    # Table cell style
    styles.add(ParagraphStyle(
        name='TableCell',
        fontName='DejaVuSans',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#222222'),
        alignment=2  # right for numbers, left for names (we'll override)
    ))
    return styles

# ── Table builder ───────────────────────────────────────────────────
def build_vows_table(vows, styles, include_remaining=True):
    """
    Create a formatted table for a list of vow items.
    Columns: S/N, Member Name, Amount Vowed, Total Paid, (Remaining)
    """
    # Prepare header
    if include_remaining:
        headers = ['S/N', 'Member Name', 'Vowed', 'Paid', 'Remaining']
        col_widths = [30*mm, 70*mm, 30*mm, 30*mm, 30*mm]
    else:
        headers = ['S/N', 'Member Name', 'Vowed', 'Paid']
        col_widths = [30*mm, 85*mm, 35*mm, 35*mm]

    header_row = [Paragraph(h, styles['TableHeader']) for h in headers]
    data = [header_row]

    for idx, vow in enumerate(vows, start=1):
        sn = str(idx)
        name = vow['memberName']
        vowed = naira(vow['amount'])
        paid = naira(vow['totalPaid'])
        if include_remaining:
            remaining = naira(vow['remaining'])
            row = [
                Paragraph(sn, styles['TableCell']),
                Paragraph(name, styles['TableCell']),
                Paragraph(vowed, styles['TableCell']),
                Paragraph(paid, styles['TableCell']),
                Paragraph(remaining, styles['TableCell']),
            ]
        else:
            row = [
                Paragraph(sn, styles['TableCell']),
                Paragraph(name, styles['TableCell']),
                Paragraph(vowed, styles['TableCell']),
                Paragraph(paid, styles['TableCell']),
            ]
        data.append(row)

    # Build table
    table = Table(data, colWidths=col_widths, repeatRows=1)
    # Style
    style_commands = [
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E5266')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6*mm),
        ('TOPPADDING', (0, 0), (-1, 0), 6*mm),
        # Body
        ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),  # numeric columns right-aligned
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),   # S/N centered
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # Grid lines: light horizontal lines only
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.HexColor('#2E5266')),
        ('LINEBELOW', (0, 1), (-1, -1), 0.3, colors.HexColor('#D3D9DE')),
        # Row background: alternating light gray
    ]
    # Add alternating row colors
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_commands.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F4F6F8')))

    table.setStyle(TableStyle(style_commands))
    return table

# ── Main report generation ──────────────────────────────────────────
def generate_report(json_path, output_pdf):
    # Load data
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    vows = data['vows']

    # Categorize
    paid = []
    partially_paid = []
    not_paid = []
    for v in vows:
        if v['remaining'] == 0:
            paid.append(v)
        elif v['totalPaid'] > 0:
            partially_paid.append(v)
        else:
            not_paid.append(v)

    # Sort each list alphabetically by name
    for lst in (paid, partially_paid, not_paid):
        lst.sort(key=lambda x: x['memberName'])

    # Quick summary numbers
    total_vows = len(vows)
    total_amount = sum(v['amount'] for v in vows)
    total_paid_amount = sum(v['totalPaid'] for v in vows)
    total_remaining = sum(v['remaining'] for v in vows)

    styles = create_styles()

    # Build story
    story = []

    # Title
    story.append(Paragraph("2026 St. Stephen AYF Vows Report", styles['ReportTitle']))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(f"Generated: {datetime.now():%B %d, %Y %I:%M %p}",
                           styles['SummaryText']))
    story.append(Spacer(1, 5*mm))

    # Quick-glance summary table
    summary_data = [
        [Paragraph("Quick Summary", styles['TableHeader']),
         Paragraph("", styles['TableHeader'])],
        [Paragraph("Total Vows", styles['TableCell']),
         Paragraph(str(total_vows), styles['TableCell'])],
        [Paragraph("Total Amount Vowed", styles['TableCell']),
         Paragraph(naira(total_amount), styles['TableCell'])],
        [Paragraph("Total Paid", styles['TableCell']),
         Paragraph(naira(total_paid_amount), styles['TableCell'])],
        [Paragraph("Total Outstanding", styles['TableCell']),
         Paragraph(naira(total_remaining), styles['TableCell'])],
        [Paragraph("Fulfilled (Paid)", styles['TableCell']),
         Paragraph(str(len(paid)), styles['TableCell'])],
        [Paragraph("Partially Paid", styles['TableCell']),
         Paragraph(str(len(partially_paid)), styles['TableCell'])],
        [Paragraph("Not Paid", styles['TableCell']),
         Paragraph(str(len(not_paid)), styles['TableCell'])],
    ]
    summary_table = Table(summary_data, colWidths=[80*mm, 60*mm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E5266')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('SPAN', (0, 0), (-1, 0)),  # merge first row
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('LINEBELOW', (0, 0), (-1, -1), 0.3, colors.HexColor('#D3D9DE')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 8*mm))

    # Section: Paid (Fulfilled)
    if paid:
        story.append(Paragraph("Fulfilled (Paid)", styles['SectionHeading']))
        table = build_vows_table(paid, styles, include_remaining=False)
        story.append(table)
        story.append(Spacer(1, 6*mm))
    else:
        story.append(Paragraph("Fulfilled (Paid) — None", styles['SectionHeading']))

    # Section: Partially Paid
    if partially_paid:
        story.append(Paragraph("Partially Paid", styles['SectionHeading']))
        table = build_vows_table(partially_paid, styles, include_remaining=True)
        story.append(table)
        story.append(Spacer(1, 6*mm))
    else:
        story.append(Paragraph("Partially Paid — None", styles['SectionHeading']))

    # Section: Not Paid
    if not_paid:
        story.append(Paragraph("Not Paid", styles['SectionHeading']))
        table = build_vows_table(not_paid, styles, include_remaining=True)
        story.append(table)
    else:
        story.append(Paragraph("Not Paid — None", styles['SectionHeading']))

    # Build PDF
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=15*mm,
        rightMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )
    doc.build(story)
    print(f"Report generated: {output_pdf}")

# ── Entry point ─────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python vows_report.py <vows.json> <output.pdf>")
        sys.exit(1)
    generate_report(sys.argv[1], sys.argv[2])
