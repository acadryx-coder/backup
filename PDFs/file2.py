from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER

def create_simplified_pdf():
    doc = SimpleDocTemplate("RINANZE_Report_Simplified.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=0.3*inch
    )
    story.append(Paragraph("RINANZE (RIN) Token - Current Status Update", title_style))
    
    # Date
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=0.2*inch
    )
    story.append(Paragraph("Report Date: July 8, 2026", date_style))
    story.append(Spacer(1, 0.2*inch))

    # Section heading style
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=0.1*inch,
        spaceBefore=0.2*inch
    )

    # 1. Quick Overview (FULL DETAIL RESTORED)
    story.append(Paragraph("1. Quick Overview", heading_style))
    story.append(Paragraph(
        "We have successfully completed three smart contracts so far. Two are deployed on the ETH testnet—the first one lacked admin controls, so we fixed that and deployed a second one with full controls. The third one is the final live contract deployed on the BNB Smart Chain mainnet. The admin dashboard is built and working, and we plan to build a separate, simple user-facing website. Right now, the token can be minted, transferred, and frozen. However, the big issue we are still researching is how to make the token's value show up correctly on Trust Wallet. We have two theories on why it isn't showing, and testing these theories will require a small amount of money (about $50).",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.1*inch))

    # 2. What We Have Done
    story.append(Paragraph("2. What We Have Done So Far", heading_style))
    done_text = """
    <para>
    - <b>The Smart Contracts (3 in total):</b><br/>
      &nbsp;&nbsp;* Deployed the first contract on ETH testnet. It lacked admin controls to block the public.<br/>
      &nbsp;&nbsp;* Deployed a second contract on ETH testnet, now with full admin controls.<br/>
      &nbsp;&nbsp;* Deployed the third (and current live) contract to BNB Smart Chain mainnet. This is the one that is live now.<br/>
    - <b>The Admin Website:</b> The admin dashboard is built and working (rinanze-admin.vercel.app). A separate, simple user website is also in the works.<br/>
    - <b>The Pool (PancakeSwap):</b> We created a pool for RIN and BNB. But right now, the price isn't showing on Trust Wallet.<br/>
      &nbsp;&nbsp;* Theory 1: The amount of money we placed in the pool is too small (about 0.09 RIN and $0.09). We need to put more money in.<br/>
      &nbsp;&nbsp;* Theory 2: Trust Wallet might need to see people actually trading the coin before they show the price.
    </para>
    """
    story.append(Paragraph(done_text, styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    # 3. Scope Creep & Cost Structure
    story.append(Paragraph("3. Scope Creep & Cost Structure", heading_style))
    story.append(Paragraph(
        "The work has grown far beyond what was first agreed. We have absorbed significant extra effort to keep the core project moving, because we care about giving you a solid, working product. However, the deeper R&D testing (such as the $50 pool injection) and any further expansions beyond the original agreement will be treated as separate costs and may incur additional charges.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.1*inch))

    # 4. Project Story
    story.append(Paragraph("4. The Project's Story (What We Have Been Doing)", heading_style))
    story_text = """
    <para>
    - <b>Phase 1:</b> Built and deployed the first testnet contract. Realised it needed admin controls.<br/>
    - <b>Phase 2:</b> Deployed the second testnet contract, fixed with admin controls.<br/>
    - <b>Phase 3:</b> The client wanted to see a high dollar amount on Trust Wallet. We researched and discovered it requires real money backing to appear. To save costs, we switched the deployment from ETH to BNB Smart Chain (cheaper network).<br/>
    - <b>Phase 4:</b> Built the admin dashboard.<br/>
    - <b>Phase 5:</b> We investigated a "token flashing" website to see how they create flash tokens. When we inspected the site, we discovered it simply collects payment without sending any tokens – a dead end for our research. We saved ourselves from wasting money on that route.<br/>
    - <b>Phase 6:</b> Tested a tiny pool of money ($0.09) on PancakeSwap to see how it works. We realised the pool is just too small.
    </para>
    """
    story.append(Paragraph(story_text, styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    # 5. Way Forward
    story.append(Paragraph("5. Where We Stand Now & The Way Forward", heading_style))
    forward_text = """
    <para>
    Because we are testing things that haven't been done before, this project has become Research & Development (R&D). We are looking at two possible paths to fix the Trust Wallet price:<br/><br/>
    - <b>Path A – Test with $50:</b> We think adding $50 worth of BNB into the PancakeSwap pool alongside a large amount of RIN will be enough to make Trust Wallet display a price.<br/>
      &nbsp;&nbsp;<i>Important:</i> Adding a large amount of RIN will temporarily cause the price of the current live contract to drop. But this test is just for gathering data. Once we learn how to make it work, we can create a brand-new final contract and deploy it properly. The knowledge gained is more valuable than the temporary drop.<br/><br/>
    - <b>Path B – Community Trading Volume (Gas + Time cost):</b> If Path A works and the price still doesn't show up, the issue might be that Trust Wallet requires real trading volume. To test this, we would need to gather a community of users and have them trade the token among themselves to create visible volume. This approach is <b>not free</b>—it requires gas fees for every transaction, significant time coordination, and effort to build the trading activity. It's a more expensive and slower path, but we can consider it if Path A fails.
    </para>
    """
    story.append(Paragraph(forward_text, styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    # 6. Conclusion
    story.append(Paragraph("6. Conclusion & Next Steps", heading_style))
    conclusion_text = """
    <para>
    The coin, the website, and the mainnet deployment are officially complete. The only thing left is getting the price to show on Trust Wallet. In the meantime, we are also researching other strategies to solve this problem just in case this test doesn't work.<br/><br/>
    <b>If you decide to go ahead with the project based on everything we've discussed, here is exactly what will happen next:</b><br/>
    1. We will put $50 into the PancakeSwap pool to test Path A.<br/>
    2. We will watch whether the price appears on Trust Wallet.<br/>
    3. If it works, we are ready for handover. If it fails, we will move to Path B (community trading volume) – which will require additional budget for gas fees and coordination.<br/><br/>
    Just let us know when to go ahead with the $50 test funding.
    </para>
    """
    story.append(Paragraph(conclusion_text, styles['Normal']))

    doc.build(story)
    print("Simplified PDF (Full Scope) generated successfully.")

if __name__ == "__main__":
    create_simplified_pdf()
