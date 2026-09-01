from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
from reportlab.lib.utils import simpleSplit
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

# --- CONFIGURATION ---
WIDTH, HEIGHT = letter
LEFT_MARGIN = 60
RIGHT_MARGIN = 60
MAX_WIDTH = WIDTH - LEFT_MARGIN - RIGHT_MARGIN
Y_START = HEIGHT - 60
FONT_BODY = 'Helvetica'
FONT_HEADER = 'Helvetica-Bold'
FONT_CODE = 'Courier'
FONT_SIZE_NORMAL = 10
FONT_SIZE_SMALL = 9
LINE_HEIGHT = 16

def draw_text(c, text, x, y, font=FONT_BODY, size=FONT_SIZE_NORMAL, max_width=MAX_WIDTH):
    """Splits text and draws it, returning the new Y position."""
    lines = simpleSplit(text, font, size, max_width)
    for line in lines:
        c.drawString(x, y, line)
        y -= (size * 1.4)
    return y + (size * 0.2) # Return exact bottom coordinate

def create_handover_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    y = Y_START

    # --- Header ---
    c.setFont(FONT_HEADER, 18)
    c.drawString(LEFT_MARGIN, y, "RINANZE TOKEN – PHASE 1 HANDOVER")
    y -= 30
    
    c.setFont(FONT_BODY, 10)
    c.drawString(LEFT_MARGIN, y, "Date: August 1, 2026")
    y -= 25

    # Horizontal Line
    c.setStrokeColor(black)
    c.setLineWidth(1)
    c.line(LEFT_MARGIN, y, WIDTH - RIGHT_MARGIN, y)
    y -= 30

    # --- Section 1: Token 1 ---
    c.setFont(FONT_HEADER, 12)
    c.drawString(LEFT_MARGIN, y, "1. TOKEN 1: MAIN RINANZE (MANUAL UUPS PROXY)")
    y -= 20

    # Contract Address
    c.setFont(FONT_CODE, FONT_SIZE_NORMAL)
    y = draw_text(c, "Contract Address:", LEFT_MARGIN, y, FONT_HEADER, FONT_SIZE_NORMAL)
    y = draw_text(c, "0xBdf9e9B29720389EeBf9b6D95a5077341E66114c", LEFT_MARGIN + 10, y, FONT_CODE, FONT_SIZE_NORMAL)
    
    # Minting Control
    c.setFont(FONT_BODY, FONT_SIZE_NORMAL)
    y = draw_text(c, "Minting Control:", LEFT_MARGIN, y, FONT_HEADER, FONT_SIZE_NORMAL)
    y = draw_text(c, "✅ Full control (MINTER_ROLE + DEFAULT_ADMIN_ROLE held by deployer).", LEFT_MARGIN + 10, y)

    # Price Control
    y = draw_text(c, "Price Control:", LEFT_MARGIN, y, FONT_HEADER, FONT_SIZE_NORMAL)
    y = draw_text(c, "✅ Price shows on DexScreener & Trust Wallet sub-menu. ❌ Not auto-displayed on Trust Wallet main dashboard.", LEFT_MARGIN + 10, y)

    # Way Forward
    y -= 5
    y = draw_text(c, "Way Forward (To unlock main dashboard display):", LEFT_MARGIN, y, FONT_HEADER, FONT_SIZE_NORMAL)
    y = draw_text(c, "• Must meet strict Trust Wallet GitHub asset listing requirements:", LEFT_MARGIN + 10, y)
    
    # Bullets inside Way Forward
    y = draw_text(c, "  - On-chain Transactions: Minimum of 15,000.", LEFT_MARGIN + 10, y, FONT_BODY, FONT_SIZE_SMALL)
    y = draw_text(c, "  - Unique Holders: Minimum of 10,000.", LEFT_MARGIN + 10, y, FONT_BODY, FONT_SIZE_SMALL)
    y = draw_text(c, "  - PR Fee: 500 TWT or 2.5 BNB (non-refundable processing fee) via GitHub submission.", LEFT_MARGIN + 10, y, FONT_BODY, FONT_SIZE_SMALL)

    # --- Section 2: Token 2 ---
    y -= 25
    c.setFont(FONT_HEADER, 12)
    c.drawString(LEFT_MARGIN, y, "2. TOKEN 2: FLAP RINANZE (LAUNCHPAD PROXY)")
    y -= 20

    # Contract Address
    c.setFont(FONT_CODE, FONT_SIZE_NORMAL)
    y = draw_text(c, "Contract Address:", LEFT_MARGIN, y, FONT_HEADER, FONT_SIZE_NORMAL)
    y = draw_text(c, "0xec7f676abd0fe12163bdf4a2ad93514637b17777", LEFT_MARGIN + 10, y, FONT_CODE, FONT_SIZE_NORMAL)

    # Minting Control
    c.setFont(FONT_BODY, FONT_SIZE_NORMAL)
    y = draw_text(c, "Minting Control:", LEFT_MARGIN, y, FONT_HEADER, FONT_SIZE_NORMAL)
    y = draw_text(c, "❌ Renounced (Owner is 0x000...). Supply is permanently fixed.", LEFT_MARGIN + 10, y)

    # Price Display
    y = draw_text(c, "Price Display:", LEFT_MARGIN, y, FONT_HEADER, FONT_SIZE_NORMAL)
    y = draw_text(c, "✅ Queued for auto-display on Trust Wallet main dashboard via Flap's backend integration.", LEFT_MARGIN + 10, y)

    # Way Forward
    y -= 5
    y = draw_text(c, "Way Forward (To activate/graduate):", LEFT_MARGIN, y, FONT_HEADER, FONT_SIZE_NORMAL)
    y = draw_text(c, "• The token must be traded internally on Flap until the bonding curve reaches 16 BNB.", LEFT_MARGIN + 10, y)
    y = draw_text(c, "  - Cost estimate: ~$9,400 USD (~₦13 million Naira).", LEFT_MARGIN + 10, y, FONT_BODY, FONT_SIZE_SMALL)
    y = draw_text(c, "  - Once hit, Flap auto-creates external liquidity pools and forces recognition on Trust Wallet.", LEFT_MARGIN + 10, y, FONT_BODY, FONT_SIZE_SMALL)

    # --- Section 3: Table Summary ---
    y -= 30
    c.setFont(FONT_HEADER, 12)
    c.drawString(LEFT_MARGIN, y, "3. SUMMARY FOR CLIENT")
    y -= 15

    # Table Data
    table_data = [
        ["Token", "Minting Control", "Price Display", "Cost to Unlock Final Stage"],
        ["Main Rinanze", "✅ Yes", "❌ Manual listing", "15k txs / 10k holders + 2.5 BNB"],
        ["Flap Rinanze", "❌ No", "✅ Auto-graduation", "16 BNB (~₦13M) into bonding curve"]
    ]

    # Define Table
    t = Table(table_data, colWidths=[100, 110, 120, 170])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), FONT_BODY),
        ('FONTNAME', (0, 0), (-1, 0), FONT_HEADER),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black), # Add a subtle grid
    ]))

    # Wrap and draw table
    table_width, table_height = t.wrap(0, 0)
    t.drawOn(c, LEFT_MARGIN, y - table_height)
    y -= (table_height + 20)

    # --- Footer ---
    c.setFont(FONT_BODY, 9)
    y -= 20
    c.drawString(LEFT_MARGIN, y, "Prepared by: Lead Engineer, Rinanze Development Team")

    # --- Finish ---
    c.save()
    print(f"✅ Black-and-white PDF generated successfully: {filename}")

if __name__ == '__main__':
    create_handover_pdf("Rinanze_Handover_BW.pdf")
