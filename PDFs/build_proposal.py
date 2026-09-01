import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, ListFlowable, ListItem, HRFlowable, KeepTogether, Image
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------------------------
# 1. FONT SETUP
# ---------------------------------------------------------------------------
NAIRA_FONT = "Helvetica"
NAIRA_FONT_BOLD = "Helvetica-Bold"
NAIRA_SYMBOL = "\u20A6"
_FONT_FOUND = False

_CANDIDATE_FONTS = [
    (os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf"),
     os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf"), "DejaVuSansLocal"),
    ("/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans.ttf",
     "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans.ttf", "DejaVuSans"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "DejaVuSans"),
    ("/usr/share/fonts/dejavu/DejaVuSans.ttf",
     "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", "DejaVuSans"),
    ("/Library/Fonts/Arial Unicode.ttf",
     "/Library/Fonts/Arial Unicode.ttf", "ArialUnicode"),
    ("C:\\Windows\\Fonts\\arialuni.ttf",
     "C:\\Windows\\Fonts\\arialuni.ttf", "ArialUnicode"),
    ("C:\\Windows\\Fonts\\seguisym.ttf",
     "C:\\Windows\\Fonts\\seguisym.ttf", "SegoeUISymbol"),
]

for reg_path, bold_path, name in _CANDIDATE_FONTS:
    if os.path.exists(reg_path):
        try:
            pdfmetrics.registerFont(TTFont(name, reg_path))
            NAIRA_FONT = name
            _FONT_FOUND = True
            if os.path.exists(bold_path):
                pdfmetrics.registerFont(TTFont(name + "-Bold", bold_path))
                NAIRA_FONT_BOLD = name + "-Bold"
            else:
                NAIRA_FONT_BOLD = name
            print(f"Using font '{name}' from {reg_path} for Naira symbol.")
            break
        except Exception as e:
            print(f"Failed to load {reg_path}: {e}")
            continue

if not _FONT_FOUND:
    print("WARNING: No Unicode font found – the ₦ symbol may appear as a box.")

def naira(amount: str) -> str:
    if _FONT_FOUND:
        return f'<font face="{NAIRA_FONT}">{NAIRA_SYMBOL}{amount}</font>'
    else:
        return f"{NAIRA_SYMBOL}{amount}"

# ---------------------------------------------------------------------------
# 2. COLOR PALETTE – light blue + white theme
# ---------------------------------------------------------------------------
PRIMARY_BLUE = colors.HexColor("#4A90E2")
DARKER_BLUE = colors.HexColor("#357ABD")
LIGHT_BLUE_TINT = colors.HexColor("#D6EAF8")
WHITE = colors.white
LIGHT_GREY = colors.HexColor("#F2F2F2")
MID_GREY = colors.HexColor("#D9D9D9")
TEXT_DARK = colors.HexColor("#1A1A1A")

PROJECT_LABEL = "GOD'SOWN RIDE"
OUTPUT_FILE = "Godsown_Ride_Proposal.pdf"

# ---------------------------------------------------------------------------
# 3. STYLES
# ---------------------------------------------------------------------------
styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="CoverTitle", fontName="Helvetica-Bold", fontSize=26,
    textColor=WHITE, leading=30, spaceAfter=6))
styles.add(ParagraphStyle(
    name="CoverSubtitle", fontName="Helvetica", fontSize=13,
    textColor=WHITE, leading=16, spaceAfter=20))
styles.add(ParagraphStyle(
    name="CoverMeta", fontName="Helvetica", fontSize=10,
    textColor=WHITE, leading=15))
styles.add(ParagraphStyle(
    name="CoverBoxText", fontName="Helvetica", fontSize=10.5,
    textColor=WHITE, leading=15))
styles.add(ParagraphStyle(
    name="CoverNotice", fontName="Helvetica-Bold", fontSize=9,
    textColor=WHITE, leading=12))
styles.add(ParagraphStyle(
    name="H1", fontName="Helvetica-Bold", fontSize=15,
    textColor=DARKER_BLUE, spaceBefore=14, spaceAfter=10))
styles.add(ParagraphStyle(
    name="H2", fontName="Helvetica-Bold", fontSize=11.5,
    textColor=DARKER_BLUE, spaceBefore=14, spaceAfter=6))
styles.add(ParagraphStyle(
    name="Body", fontName="Helvetica", fontSize=9.7,
    textColor=TEXT_DARK, leading=14, spaceAfter=6))
styles.add(ParagraphStyle(
    name="BulletText", fontName="Helvetica", fontSize=9.7,
    textColor=TEXT_DARK, leading=13.5))
styles.add(ParagraphStyle(
    name="TOCEntry", fontName="Helvetica", fontSize=10.5,
    textColor=TEXT_DARK, leading=20))
styles.add(ParagraphStyle(
    name="TOCTitle", fontName="Helvetica-Bold", fontSize=16,
    textColor=DARKER_BLUE, spaceAfter=10))
styles.add(ParagraphStyle(
    name="TableHeader", fontName="Helvetica-Bold", fontSize=9,
    textColor=WHITE, leading=11))
styles.add(ParagraphStyle(
    name="TableCell", fontName="Helvetica", fontSize=8.7,
    textColor=TEXT_DARK, leading=11.5))
styles.add(ParagraphStyle(
    name="Note", fontName="Helvetica-Oblique", fontSize=8.3,
    textColor=colors.HexColor("#555555"), leading=11))
styles.add(ParagraphStyle(
    name="TotalRow", fontName=NAIRA_FONT_BOLD, fontSize=9,
    textColor=DARKER_BLUE, leading=11.5))

def bullets(items, style="BulletText"):
    return ListFlowable(
        [ListItem(Paragraph(t, styles[style]), leftIndent=6, spaceAfter=3)
         for t in items],
        bulletType="bullet", start="•", leftIndent=14,
    )

def section_rule():
    return HRFlowable(width="100%", thickness=1, color=PRIMARY_BLUE, spaceAfter=12)

def data_table(head, rows, col_widths, header_bg=DARKER_BLUE):
    table_head = [Paragraph(h, styles["TableHeader"]) for h in head]
    table_rows = [[Paragraph(str(c), styles["TableCell"]) for c in row]
                  for row in rows]
    t = Table([table_head] + table_rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.5, MID_GREY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t

# ---------------------------------------------------------------------------
# 4. PAGE DECORATION
# ---------------------------------------------------------------------------
LOGO_PATH = os.path.expanduser("~/PDFs/images/ride.jpg")

def draw_cover_background(c: canvas.Canvas, doc):
    page_w, page_h = LETTER
    c.setFillColor(PRIMARY_BLUE)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    c.setStrokeColor(WHITE)
    c.setLineWidth(10)
    c.line(0, page_h, page_w, page_h)
    c.line(0, page_h, 0, 0)

def draw_footer(c: canvas.Canvas, doc):
    page_w, page_h = LETTER
    c.setFillColor(DARKER_BLUE)
    c.rect(0, 0, page_w, 0.35 * inch, fill=1, stroke=0)
    c.rect(0, page_h - 0.28 * inch, page_w, 0.28 * inch, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(0.5 * inch, page_h - 0.2 * inch, PROJECT_LABEL)
    c.drawRightString(page_w - 0.5 * inch, 0.13 * inch, f"Page {doc.page}")

def on_cover(c, doc):
    draw_cover_background(c, doc)

def on_page(c, doc):
    draw_footer(c, doc)

# ---------------------------------------------------------------------------
# 5. BUILD THE STORY
# ---------------------------------------------------------------------------
story = []

# --- COVER PAGE (logo placed cleanly at top, no notice) ---
cover = []
cover.append(Spacer(1, 0.8 * inch))               # some breathing room at top
if os.path.exists(LOGO_PATH):
    logo = Image(LOGO_PATH, width=1.8*inch, height=1.8*inch)
    cover.append(logo)
    cover.append(Spacer(1, 0.5*inch))
else:
    cover.append(Spacer(1, 0.8*inch))

cover.append(Paragraph("GOD'SOWN RIDE", styles["CoverTitle"]))
cover.append(Paragraph("Project Proposal &amp; Scope of Work", styles["CoverSubtitle"]))
cover.append(Spacer(1, 0.15 * inch))
cover.append(Paragraph("Prepared for: God'sown Ride (Ride-Hailing Platform)", styles["CoverMeta"]))
cover.append(Paragraph("Prepared by: God'sown Ride Team", styles["CoverMeta"]))
cover.append(Paragraph("Date: July 10, 2026", styles["CoverMeta"]))
cover.append(Paragraph("Document type: Scope, Technical Approach &amp; Pricing Proposal", styles["CoverMeta"]))
cover.append(Spacer(1, 0.8 * inch))

box_table = Table([[Paragraph(
    "A three-role ride-hailing platform — Driver, Customer, Admin — "
    "comparable to leading ride-hailing services, tailored to God'sown Ride's "
    "stated requirements."
    "<br/><br/>Single web application • Shared login, three dashboards"
    "<br/>Nearest-driver matching • Real-time trip tracking • In-app payments",
    styles["CoverBoxText"])]], colWidths=[6.3 * inch])
box_table.setStyle(TableStyle([
    ("BOX", (0, 0), (-1, -1), 1.2, WHITE),
    ("BACKGROUND", (0, 0), (-1, -1), PRIMARY_BLUE),
    ("TOPPADDING", (0, 0), (-1, -1), 14),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ("LEFTPADDING", (0, 0), (-1, -1), 14),
    ("RIGHTPADDING", (0, 0), (-1, -1), 14),
]))
cover.append(box_table)
story.extend(cover)
story.append(PageBreak())

# --- TABLE OF CONTENTS ---
toc_entries = [
    ("1. Executive Summary", "3"),
    ("2. Scope of Work — By User Role", "3"),
    ("3. Page & Screen Breakdown", "4"),
    ("4. Nearest-Driver Matching & Location Tracking", "5"),
    ("5. Technology Stack", "5"),
    ("6. Security", "7"),
    ("7. Deliverables Checklist", "7"),
    ("8. Timeline", "8"),
    ("9. Investment & Cost Breakdown", "8"),
    ("10. Assumptions & Client Requirements", "9"),
    ("11. Future Enhancements (Suggested)", "10"),
]
story.append(Paragraph("Table of Contents", styles["TOCTitle"]))
story.append(section_rule())
for label, page in toc_entries:
    row = Table([[Paragraph(label, styles["TOCEntry"]),
                  Paragraph(page, styles["TOCEntry"])]],
                colWidths=[5.6 * inch, 0.6 * inch])
    row.setStyle(TableStyle([("ALIGN", (1, 0), (1, 0), "RIGHT")]))
    story.append(row)

# --- 1. EXECUTIVE SUMMARY ---
story.append(Spacer(1, 0.2*inch))
story.append(KeepTogether([
    Paragraph("1. Executive Summary", styles["H1"]),
    section_rule(),
    Paragraph(
        "God'sown Ride is a ride-hailing web application connecting "
        "three user roles — Drivers, Customers, and an Admin — through a shared "
        "login system that routes each user to a role-specific dashboard. The "
        "platform matches customers with the nearest available driver, tracks "
        "trips in real time, and handles in-app payment collection (cash or "
        "card), with full administrative oversight of all trips and finances.",
        styles["Body"]),
    Paragraph(
        "The system is built as a single web application (desktop and "
        "mobile-browser friendly) rather than three separate apps, using one "
        "shared authentication layer and three distinct dashboards.",
        styles["Body"]),
]))

# --- 2. SCOPE OF WORK ---
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("2. Scope of Work — By User Role", styles["H1"]))
story.append(section_rule())

story.append(KeepTogether([
    Paragraph("2.1 Driver Role", styles["H2"]),
    Paragraph("<b>Registration</b>", styles["Body"]),
    bullets(["Full name, date of birth, sex",
             "Email address — verified via a one-time code sent to the email",
             "Phone number"]),
    Paragraph("<b>Driver Profile</b>", styles["Body"]),
    bullets([
        "Full name, bio, and address (verified via a submitted utility bill)",
        "Identity verification — NIN, international passport, driver's license, or voter's card",
        "Profile picture",
        "Car picture, car type, and plate number",
        "Star rating and total number of trips completed"]),
    Paragraph("<b>Driver Dashboard</b>", styles["Body"]),
    bullets([
        "Active trip view — the ride currently in progress",
        "Pending ride requests — new bookings awaiting the driver's Accept / Cancel decision",
        "Earnings, ratings, and completed-trips summary panel",
        "Built as a map-centric dashboard — see Section 5.5 for the live-map, "
        "bottom-sheet, and side-drawer interaction pattern shared by the Driver "
        "and Customer dashboards"]),
]))

story.append(KeepTogether([
    Paragraph("2.2 Customer Role", styles["H2"]),
    bullets([
        "Registration with email/phone verification via one-time code, with a recovery flow for forgotten passwords",
        "Personal profile management",
        "Trip history — driver assigned, amount paid, and payment method (cash or card)",
        "Linked ATM/debit cards for in-app payment",
        "Active trip view — at trip completion, the system calculates the fare and prompts the customer to choose cash or card payment",
        "Contact / help support channel",
        "Dashboard showing active trips and the ability to rate drivers (drivers can likewise rate customers), built around the map-centric pattern described in Section 5.5",
        "Discount section — space for promo codes / referral discounts, to be defined with the client"]),
]))

story.append(KeepTogether([
    Paragraph("2.3 Admin Role", styles["H2"]),
    bullets([
        "Password-reset support for drivers and customers who lose account access",
        "Full visibility into every trip taking place on the platform",
        "Financial oversight — money received from customer trip payments and money paid out to drivers"]),
]))

story.append(KeepTogether([
    Paragraph("2.4 Shared / Site-Wide Pages", styles["H2"]),
    bullets([
        "FAQ page (content to be supplied by the client)",
        "Terms & Conditions, Privacy Policy, and Copyright notice",
        "Help / Support page"]),
]))

# --- 3. PAGE & SCREEN BREAKDOWN ---
story.append(Spacer(1, 0.2*inch))
story.append(KeepTogether([
    Paragraph("3. Page & Screen Breakdown", styles["H1"]),
    section_rule(),
    Paragraph(
        "Below is the full list of individual pages/screens that make up the "
        "platform, grouped by who uses them. This is the working build list "
        "used for estimating and tracking progress, and it maps directly onto "
        "the features in Section 2.", styles["Body"]),
]))

pages_rows = [
    ("1", "Landing Page", "All", "Public homepage; entry point with login/signup links"),
    ("2", "Login Page", "All", "Single login for all roles; redirects to the correct dashboard"),
    ("3", "Sign-Up Page", "Driver, Customer", "Role-specific registration form with OTP verification"),
    ("4", "Forgot / Reset Password Page", "All", "OTP-based password recovery"),
    ("5", "FAQ Page", "All", "Client-supplied questions and answers"),
    ("6", "Terms & Conditions / Privacy Page", "All", "Legal and policy content"),
    ("7", "Help / Support Page", "All", "Contact form / support information"),
    ("8", "Driver Profile Setup Page", "Driver", "Bio, address, ID upload, car details, profile photo"),
    ("9", "Driver Dashboard", "Driver", "Active trip, pending ride requests (accept/cancel), earnings & ratings"),
    ("10", "Driver Trip History Page", "Driver", "List of completed trips"),
    ("11", "Customer Profile Page", "Customer", "Personal details and linked ATM card"),
    ("12", "Book a Ride / Customer Dashboard", "Customer", "Request a ride, track active trip, end-of-trip payment prompt"),
    ("13", "Customer Trip History Page", "Customer", "Past trips, driver, amount paid, payment method"),
    ("14", "Rate Driver Page", "Customer", "Post-trip rating (drivers are rated similarly by customers)"),
    ("15", "Discount / Promo Page", "Customer", "View and apply promo codes"),
    ("16", "Admin Dashboard Home", "Admin", "At-a-glance overview of all trips"),
    ("17", "Admin — All Trips Page", "Admin", "Full trip list and detail view"),
    ("18", "Admin — Finance Page", "Admin", "Money in (payments) vs. money out (driver payouts)"),
    ("19", "Admin — User Management Page", "Admin", "Password reset for drivers and customers"),
]
story.append(Spacer(1, 6))
story.append(data_table(
    ["#", "Page / Screen", "Used By", "Purpose"],
    pages_rows,
    [0.3 * inch, 1.9 * inch, 1.0 * inch, 2.9 * inch]))
story.append(Paragraph(
    "The above pages form the core build. Additional pages can be considered for future phases "
    "(see Section 11 for suggestions).",
    styles["Note"]))

# --- 4. NEAREST-DRIVER MATCHING ---
story.append(Spacer(1, 0.2*inch))
story.append(KeepTogether([
    Paragraph("4. Nearest-Driver Matching & Location Tracking", styles["H1"]),
    section_rule(),
    Paragraph(
        "A hybrid location model is used so that ride-matching stays accurate "
        "whether or not a driver is actively online:", styles["Body"]),
    bullets([
        "<b>Live tracking</b> — while a driver is online, both driver and customer "
        "GPS positions update in real time, and new ride requests are matched to "
        "the nearest currently-online driver.",
        "<b>Static / last-known location</b> — when a driver goes offline, their "
        "most recent (\"home\"/last-known) position is retained so they can still "
        "be considered for matching once they reconnect, rather than "
        "disappearing from the system entirely."]),
]))

# --- 5. TECHNOLOGY STACK ---
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("5. Technology Stack", styles["H1"]))
story.append(section_rule())
story.append(KeepTogether([
    Paragraph("5.1 Frontend", styles["H2"]),
    Paragraph(
        "The application will be built with React and TypeScript on the frontend.",
        styles["Body"]),
]))

story.append(Paragraph("5.2 Backend & Database — Client's Choice", styles["H2"]))
story.append(Paragraph(
    "Two options are presented below so the client can choose the path that "
    "best fits their scaling plans and budget.", styles["Body"]))
backend_rows = [
    ("Supabase (Recommended)",
     "Managed Postgres + built-in Auth, file storage, and Row-Level "
     "Security (RLS) out of the box. Fastest path to production. Free tier "
     "available while the platform is small; predictable $25/month Pro "
     "tier once scaling past free-tier limits. Fully migratable to a "
     "self-hosted Postgres database later with no data-model rewrite.",
     "Being a managed platform, very high-traffic usage (heavy "
     "egress/compute) costs more than a self-managed server at the same "
     "scale."),
    ("Self-Hosted PostgreSQL",
     "Full control over the server and costs at very large scale; no "
     "vendor usage caps.",
     "Auth, RLS-equivalent access rules, backups, and file storage must "
     "all be built and maintained manually — longer build time and "
     "ongoing DevOps responsibility falls on the client/team."),
]
story.append(data_table(
    ["Option", "Pros", "Cons"], backend_rows,
    [1.3 * inch, 2.9 * inch, 1.9 * inch]))
story.append(Paragraph(
    "<b>Recommendation:</b> Launch on Supabase's free tier (covers up to "
    "50,000 monthly active users), and move to the $25/month Pro tier only "
    "once the platform's usage requires it (see Section 9 for recurring "
    "costs).", styles["Body"]))

story.append(KeepTogether([
    Paragraph("5.3 Maps & Live Location", styles["H2"]),
    Paragraph(
        "The map functionality will be powered by Leaflet with OpenStreetMap "
        "tiles. This is a completely free, open-source mapping solution with "
        "no usage limits, avoiding any recurring map API costs. It provides "
        "all necessary features: live GPS tracking, nearest-driver matching, "
        "and distance/fare calculation.", styles["Body"]),
]))

story.append(KeepTogether([
    Paragraph("5.4 Payments", styles["H2"]),
    bullets([
        "<b>Primary:</b> Flutterwave — supports cards, bank transfer, and USSD, "
        "so customers can pay however is most convenient for them.",
        "<b>Secondary option:</b> Cryptocurrency (e.g. BTC) as an alternative "
        "payout channel, if the client wants it enabled."]),
    Paragraph(
        "Flutterwave charges no setup fee. Local Naira transactions are "
        "charged 2.0% per transaction (plus 7.5% VAT on that fee), deducted "
        "automatically from each payment — this is not a cost billed "
        "separately to the client.", styles["Body"]),
]))

story.append(KeepTogether([
    Paragraph("5.5 Dashboard UX — Map-Centric Design", styles["H2"]),
    Paragraph(
        "Both the Driver and Customer dashboards are built around a single "
        "live map as the primary canvas, rather than a conventional "
        "list-and-form layout. This keeps location context on screen at all "
        "times and follows the pattern riders already expect from ride-hailing "
        "apps:", styles["Body"]),
    bullets([
        "<b>Live map with location dots</b> — the map shows real-time colored "
        "markers for the relevant elements on screen (e.g. the customer's "
        "pickup point, nearby/matched drivers, and the active trip's live "
        "position), updating as GPS data changes.",
        "<b>Bottom sheet (slide-up panel)</b> — surfaces the main dashboard "
        "actions tied to what's on the map: for a Driver, pending ride "
        "requests and Accept/Cancel controls; for a Customer, ride booking, "
        "fare estimate, and the end-of-trip payment prompt. It can be dragged "
        "up to expand or down to collapse without ever hiding the map.",
        "<b>Side drawer (slide-in panel)</b> — handles navigation and search: "
        "profile, trip history, earnings/ratings, settings, and an "
        "address/destination search field, tucked out of the way until "
        "needed."]),
]))

# --- 6. SECURITY ---
story.append(Spacer(1, 0.2*inch))
story.append(KeepTogether([
    Paragraph("6. Security", styles["H1"]),
    section_rule(),
    bullets([
        "Row-Level Security (or equivalent access rules) so each user role can "
        "only read/write the data it's permitted to touch",
        "Encrypted password storage and OTP-based identity verification at signup",
        "Secure handling of uploaded ID documents and utility bills",
        "Rate-limiting and abuse protection on public-facing booking/auth endpoints"]),
    Paragraph(
        "Security is treated as a first-class requirement throughout — not an "
        "afterthought — given the financial and personal data the platform "
        "will handle.", styles["Body"]),
]))

# --- 7. DELIVERABLES CHECKLIST ---
story.append(Spacer(1, 0.2*inch))
story.append(KeepTogether([
    Paragraph("7. Deliverables Checklist", styles["H1"]),
    section_rule(),
    Paragraph(
        "This is the complete list of what will be delivered for the price in "
        "Section 9. Anything not listed here is outside the initial scope "
        "and can be discussed as a future enhancement (see Section 11).",
        styles["Body"]),
]))

deliverables = [
    "Shared login / registration system with role-based redirect (Driver, Customer, Admin)",
    "Driver registration + OTP email verification",
    "Driver profile (bio, address, ID verification, car details, ratings)",
    "Driver dashboard (map-centric: active trip, pending rides w/ accept-cancel, earnings/ratings)",
    "Customer registration + OTP verification + password recovery",
    "Customer profile + trip history + linked ATM card",
    "Customer dashboard (map-centric: active trip, end-of-trip cash/card prompt, ratings)",
    "Discount / promo code section",
    "Admin dashboard (password reset, all-trips view, money in/out)",
    "Live GPS tracking + nearest-driver matching (online drivers)",
    "Static/last-known location fallback (offline drivers)",
    "Flutterwave payment integration (cards, transfer, USSD)",
    "Crypto payment option (if selected by client)",
    "FAQ, Terms & Conditions, Help/Support, Copyright pages",
    "Domain connection + production deployment",
]
deliv_rows = [(str(i + 1), text, "[ ]") for i, text in enumerate(deliverables)]
story.append(Spacer(1, 6))
story.append(data_table(
    ["#", "Deliverable", "Status"], deliv_rows,
    [0.3 * inch, 5.4 * inch, 0.6 * inch]))
story.append(Paragraph(
    "Review rounds included: 2. Once all items are delivered and checked off, "
    "the project is considered complete for this phase.",
    styles["Body"]))

# --- 8. TIMELINE ---
story.append(Spacer(1, 0.2*inch))
story.append(KeepTogether([
    Paragraph("8. Timeline", styles["H1"]),
    section_rule(),
    Paragraph(
        "5–6 weeks from receipt of the initial deposit to full delivery of "
        "every item in Section 7, followed by the 2 included review cycles.",
        styles["Body"]),
]))

# --- 9. INVESTMENT & COST BREAKDOWN ---
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("9. Investment & Cost Breakdown", styles["H1"]))
story.append(section_rule())
story.append(Paragraph("9.1 Development Fee", styles["H2"]))
dev_fee_rows = [
    ("Core development (all deliverables in Section 7, 3 user roles, admin dashboard)",
     naira("400,000")),
]
story.append(data_table(
    ["Item", "Amount (NGN)"], dev_fee_rows, [4.9 * inch, 1.4 * inch]))
story.append(Paragraph(
    "Payment structure: an initial deposit to begin work, with the "
    "balance due on delivery — exact split to be agreed before work "
    "starts.", styles["Body"]))

story.append(Paragraph("9.2 Domain & Hosting Options", styles["H2"]))
story.append(Paragraph(
    "We evaluated multiple hosting providers to find the most cost‑effective "
    "solution for God'sown Ride. The table below compares the two strongest options.",
    styles["Body"]))

domain_price_rows = [
    (".com", "$11.25 / year", naira("15,750") + " / year"),
    (".com.ng", "—", naira("3,500") + " / year"),
    (".ng", "—", naira("15,000") + " / year"),
    (".xyz", "$1.99 / year", naira("2,800") + " / year"),
]
story.append(Spacer(1, 4))
story.append(Paragraph("<b>Domain Name Prices (for reference)</b>", styles["H2"]))
story.append(data_table(
    ["Extension", "USD (approx.)", "NGN (approx.)"],
    domain_price_rows,
    [1.3 * inch, 1.3 * inch, 1.3 * inch]))
story.append(Spacer(1, 8))

host_compare_rows = [
    ("Upperlink Shared Hosting",
     naira("30,000") + "/year (includes free .xyz domain)",
     "• Local Nigerian provider<br/>• Free domain (.xyz) included<br/>• cPanel, email accounts<br/>• Suitable for launch phase",
     "<b>Recommended</b> — Cheapest annual cost, everything included."),
    ("Vercel Pro",
     "$20/month ≈ " + naira("28,000") + "/month (" + naira("336,000") + "/year) + domain fee",
     "• Global edge network<br/>• Requires paid Pro plan for commercial use<br/>• Domain must be purchased separately<br/>• Scales easily but expensive at start",
     "Not cost‑effective for Year 1. Best if rapid global scaling is needed later."),
]
story.append(Paragraph("<b>Hosting Plan Comparison</b>", styles["H2"]))
story.append(data_table(
    ["Provider", "Yearly Cost (NGN)", "Includes", "Recommendation"],
    host_compare_rows,
    [1.2 * inch, 1.8 * inch, 2.2 * inch, 1.2 * inch]))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "<b>Our recommended path:</b> Start with <b>Upperlink Shared Hosting</b> "
    f"({naira('30,000')}/year) which includes a free .xyz domain. This keeps the "
    "first‑year operational cost extremely low while providing everything needed "
    "for launch. If the client later requires a custom domain (e.g. .com.ng), "
    "it can be purchased separately for a small additional fee (see domain prices above). "
    "Vercel remains a solid long‑term upgrade option once the platform outgrows "
    "shared hosting.",
    styles["Body"]))

story.append(Paragraph("9.3 Grand Total (Year 1, Launch-Scale Estimate)", styles["H2"]))
grand_total_rows = [
    ("Development fee (one-time)", naira("400,000")),
    ("Hosting (Upperlink – includes free .xyz domain)", naira("30,000")),
    ("Backend + Maps (free tiers)", naira("0")),
    ("Estimated Year 1 total", naira('430,000')),
]
gt_table_data = [[Paragraph(h, styles["TableHeader"]) for h in ["Item", "Amount"]]]
for i, (item, amt) in enumerate(grand_total_rows):
    style = "TotalRow" if i == len(grand_total_rows) - 1 else "TableCell"
    gt_table_data.append([Paragraph(item, styles[style]), Paragraph(amt, styles[style])])
gt_table = Table(gt_table_data, colWidths=[4.9 * inch, 1.4 * inch])
gt_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), DARKER_BLUE),
    ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
    ("GRID", (0, 0), (-1, -1), 0.5, MID_GREY),
    ("BACKGROUND", (0, -1), (-1, -1), LIGHT_BLUE_TINT),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
]))
story.append(gt_table)
story.append(Paragraph(
    "This total reflects launch-stage costs only. As the platform scales, "
    "costs for hosting and database will increase and will be borne by the client.",
    styles["Note"]))

# --- 10. ASSUMPTIONS & CLIENT REQUIREMENTS ---
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("10. Assumptions & Client Requirements", styles["H1"]))
story.append(section_rule())

story.append(Paragraph("<b>Assumptions</b>", styles["H2"]))
story.append(bullets([
    "The client will supply all business rules (fare calculation, discounts, "
    "payout schedules, etc.) for the developer to implement.",
    "Identity documents (NIN, passport, driver's license, utility bill) are "
    "captured and stored by the platform. Verification against government "
    "databases is not included unless a dedicated API is agreed upon separately.",
    "The client is responsible for ongoing hosting and payment-processing "
    "costs as listed in Section 9.2, which are billed directly by the respective providers.",
]))
story.append(Spacer(1, 6))

story.append(Paragraph("<b>Client-Supplied Business Logic</b>", styles["H2"]))
story.append(Paragraph(
    "The following specific rules and logic must be provided by the client. "
    "The developer will implement the exact formulas supplied.",
    styles["Body"]))
story.append(bullets([
    "Fare calculation rules (base fare, distance rate, time rate, surge multipliers)",
    "Discount / promo code logic and validation rules",
    "Driver payout schedule and commission split",
    "Any other business-specific logic the platform must enforce",
]))

# --- 11. FUTURE ENHANCEMENTS (SUGGESTED) ---
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("11. Future Enhancements (Suggested)", styles["H1"]))
story.append(section_rule())
story.append(Paragraph(
    "The following features are not part of the current scope, but we recommend "
    "considering them as the platform grows. They are presented as suggestions "
    "for future development phases:",
    styles["Body"]))
story.append(bullets([
    "In-app messaging between driver and customer",
    "Voice messaging / voice calls for quick communication",
    "Native mobile applications (iOS and Android)",
    "Advanced analytics and reporting dashboard",
    "Multi-language support",
    "Automated identity verification via government APIs",
    "Integration with additional payment gateways",
]))
story.append(Paragraph(
    "These enhancements can be discussed and scoped when the client is ready.",
    styles["Body"]))

# ---------------------------------------------------------------------------
# 6. BUILD THE PDF
# ---------------------------------------------------------------------------
doc = SimpleDocTemplate(
    OUTPUT_FILE, pagesize=LETTER,
    topMargin=0.55 * inch, bottomMargin=0.55 * inch,
    leftMargin=0.6 * inch, rightMargin=0.6 * inch,
)

def on_first_page(c, doc):
    on_cover(c, doc)

def on_later_pages(c, doc):
    on_page(c, doc)

doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
print(f"Done. Wrote {OUTPUT_FILE}")
