from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import simpleSplit

# --- PREMIUM CONFIGURATION ---
DARK_BG = HexColor('#05070c')         # Deep space
PANEL_BG = HexColor('#10131f')        # Dark panel background
GOLD = HexColor('#f0b90b')            # BNB Gold
VIOLET = HexColor('#7c5cfc')          # Prime purple
TEXT_MAIN = HexColor('#f2f3f7')
TEXT_DIM = HexColor('#8b93a7')
BORDER_LINE = HexColor('#2d3142')
TITLE_FONT = 'Helvetica-Bold'
BODY_FONT = 'Helvetica'
MONO_FONT = 'Courier'

# --- EDIT YOUR TITLE HERE ---
ROLE_TITLE = "Senior Full Stack / Web3 Developer" 
# Alternative: "Senior React / Supabase Developer"

def draw_background(c, width, height):
    c.setFillColor(DARK_BG)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    c.setStrokeColor(Color(1,1,1, alpha=0.06))
    c.setLineWidth(1.5)
    c.lines([
        (width-150, 0, width, 150),
        (width-300, 0, width, 300),
        (width-450, 0, width, 450),
        (0, height-150, 150, height),
        (0, height-300, 300, height),
    ])
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(width-150, 0, width-200, 50)
    c.line(0, height-150, 50, height-100)

def draw_footer(c, width, height, page_num, total_pages):
    c.setFillColor(TEXT_DIM)
    c.setFont(BODY_FONT, 8)
    c.drawRightString(width - 60, 40, f"Page {page_num}/{total_pages}")
    c.line(60, 55, width - 60, 55)

def draw_section_header(c, y, text):
    c.setFillColor(VIOLET)
    c.setFont(TITLE_FONT, 12)
    c.drawString(60, y, text)
    return y - 20

def draw_body_text(c, text, x, y, max_width, line_height=16):
    for line in simpleSplit(text, BODY_FONT, 10, max_width):
        c.drawString(x, y, line)
        y -= line_height
    return y

def create_handover_pdf(filename, client_name):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    total_pages = 3

    # =========================================================
    # PAGE 1: PREMIUM COVER
    # =========================================================
    draw_background(c, width, height)
    
    c.setFillColor(VIOLET)
    c.setFont(TITLE_FONT, 48)
    c.drawString(60, height - 140, "PROJECT")
    c.drawString(60, height - 195, "HANDOVER")

    c.setFillColor(GOLD)
    c.setFont(TITLE_FONT, 22)
    c.drawString(60, height - 240, "RINANZE TOKEN")

    c.setStrokeColor(GOLD)
    c.setLineWidth(3)
    c.line(60, height - 260, 240, height - 260)

    panel_x, panel_y = 60, height - 380
    panel_w, panel_h = width - 120, 110
    c.setFillColor(PANEL_BG)
    c.rect(panel_x, panel_y, panel_w, panel_h, fill=1, stroke=0)
    c.setStrokeColor(BORDER_LINE)
    c.setLineWidth(1)
    c.rect(panel_x, panel_y, panel_w, panel_h, fill=0, stroke=1)

    c.setFillColor(TEXT_MAIN)
    c.setFont(BODY_FONT, 11)
    y = panel_y + 75
    c.drawString(panel_x + 20, y, "Token Name: Rinanze (RIN) on BNB Smart Chain")
    y -= 25
    c.drawString(panel_x + 20, y, "Date of Issue: July 16, 2026")
    y -= 25
    c.drawString(panel_x + 20, y, "Status: All core engineering delivered and ready.")

    draw_footer(c, width, height, 1, total_pages)
    c.showPage()

    # =========================================================
    # PAGE 2: ASSETS, LIQUIDITY & MAINTENANCE
    # =========================================================
    draw_background(c, width, height)
    
    c.setFillColor(GOLD)
    c.setFont(TITLE_FONT, 24)
    c.drawString(60, height - 80, "Handover Assets & Support")

    y = height - 110
    
    y = draw_section_header(c, y, "1. Current Asset Status (Delivered)")
    c.setFillColor(TEXT_MAIN)
    c.setFont(BODY_FONT, 10)
    y = draw_body_text(c, "Token Name: Rinanze | Symbol: RIN | Decimals: 18", 60, y, width-120)
    c.setFont(MONO_FONT, 9)
    c.setFillColor(TEXT_DIM)
    y = draw_body_text(c, "Live Proxy Address (Token): 0xBdf9e9B29720389EeBf9b6D95a5077341E66114c", 60, y, width-120)
    y = draw_body_text(c, "Implementation Address:      0xe53Aceb9B0689e8e145931730e552Ee83c5831df", 60, y, width-120)
    c.setFillColor(TEXT_MAIN)
    c.setFont(BODY_FONT, 10)
    y = draw_body_text(c, "Admin Dashboard: rinanze-admin.vercel.app", 60, y, width-120)
    y = draw_body_text(c, "Public Portal (Live): https://rinanze.vercel.app/", 60, y, width-120)
    y = draw_body_text(c, "Total Supply: 1,000,000 RIN minted.", 60, y, width-120)

    y -= 25
    y = draw_section_header(c, y, "2. Liquidity Pool Status")
    c.setFillColor(TEXT_MAIN)
    c.setFont(BODY_FONT, 10)
    y = draw_body_text(c, "Platform: PancakeSwap | Pair: RIN / BNB", 60, y, width-120)
    y = draw_body_text(c, "Liquidity: 400 RIN + 0.004 BNB (pool value ~ $2.60 USD)", 60, y, width-120)
    y = draw_body_text(c, "Price: Approx. 0.00001 BNB per RIN (live on PancakeSwap)", 60, y, width-120)

    y -= 25
    y = draw_section_header(c, y, "3. Post-Handover Support")
    c.setFillColor(TEXT_MAIN)
    c.setFont(BODY_FONT, 10)
    y = draw_body_text(c, "We are providing 3 days of complimentary testing, bug-fixing, and maintenance", 60, y, width-120)
    y = draw_body_text(c, "for the public portal (July 16 – July 19, 2026). This covers frontend bugs,", 60, y, width-120)
    y = draw_body_text(c, "wallet connectivity, and minor smart contract interactions.", 60, y, width-120)

    draw_footer(c, width, height, 2, total_pages)
    c.showPage()

    # =========================================================
    # PAGE 3: REASON, PROCEDURE, WAY FORWARD & PREPARED BY
    # =========================================================
    draw_background(c, width, height)
    
    c.setFillColor(GOLD)
    c.setFont(TITLE_FONT, 24)
    c.drawString(60, height - 80, "Handover Procedures & Preparation")

    y = height - 110

    y = draw_section_header(c, y, "4. Reason for Handover & Scope Creep")
    c.setFillColor(TEXT_MAIN)
    c.setFont(BODY_FONT, 10)
    text = "The project expanded into a complex R&D endeavor regarding Trust Wallet valuation. We are forfeiting the remaining balance of NGN 90,000 as a goodwill gesture. Core engineering is complete; the Trust Wallet display requires a Tokenomist."
    y = draw_body_text(c, text, 60, y, width-120, line_height=18)

    y -= 25
    y = draw_section_header(c, y, "5. Handover Completion Procedure")
    c.setFillColor(TEXT_MAIN)
    c.setFont(BODY_FONT, 10)
    y = draw_body_text(c, "Upon receiving your BNB wallet address, we will:", 60, y, width-120)
    c.setFont(MONO_FONT, 9)
    c.setFillColor(TEXT_DIM)
    y = draw_body_text(c, "• Transfer full ownership of the Proxy contract to your wallet.", 70, y, width-140)
    y = draw_body_text(c, "• Transfer the remaining 999,600 RIN to your provided address.", 70, y, width-140)
    c.setFillColor(TEXT_MAIN)
    c.setFont(BODY_FONT, 10)
    y = draw_body_text(c, "(400 RIN is locked permanently in the PancakeSwap liquidity pool).", 60, y, width-120)

    y -= 25
    y = draw_section_header(c, y, "6. The Way Forward")
    c.setFillColor(TEXT_MAIN)
    c.setFont(BODY_FONT, 10)
    text = "We recommend hiring a specialized Tokenomist to handle the final economic modeling and volume simulations required for wallet price displays."
    y = draw_body_text(c, text, 60, y, width-120, line_height=18)

    # =========================================================
    # FINAL: PREPARED BY (No role hallucination, clean & small)
    # =========================================================
    y -= 35
    c.setFillColor(TEXT_DIM)
    c.setFont(BODY_FONT, 10)
    c.drawString(60, y, "Prepared by:")
    y -= 24
    
    c.setFillColor(TEXT_MAIN)  # Normal white, not gold, not huge
    c.setFont(BODY_FONT, 12)
    c.drawString(60, y, client_name)
    y -= 20
    
    c.setFillColor(TEXT_DIM)
    c.setFont(BODY_FONT, 9)
    c.drawString(60, y, ROLE_TITLE)

    draw_footer(c, width, height, 3, total_pages)
    c.save()
    print(f"✅ Premium 3-page PDF generated successfully: {filename}")

if __name__ == '__main__':
    create_handover_pdf("Rinanze_Handover_Premium.pdf", "Uduvwurode Simeon O.")
