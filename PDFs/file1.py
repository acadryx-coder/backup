from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER

def create_advanced_pdf():
    doc = SimpleDocTemplate("RINANZE_Report_Advanced.pdf", pagesize=A4)
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
    story.append(Paragraph("RINANZE (RIN) Token - Ongoing R&D Status", title_style))
    
    # Date
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=0.2*inch
    )
    story.append(Paragraph("Report as at July 8, 2026", date_style))
    story.append(Spacer(1, 0.2*inch))

    # Define section heading style
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=0.1*inch,
        spaceBefore=0.2*inch
    )

    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary", heading_style))
    story.append(Paragraph(
        "The Rinanze (RIN) token infrastructure is functionally complete across three deployed smart contracts (two on ETH testnet, one on BNB Smart Chain mainnet). The administrative dashboard is live and adaptable for future projects, and core wallet transfers are functional. The remaining deliverable is achieving the desired Trust Wallet valuation display, which has transitioned the project into active R&D. We have isolated the display issue to two liquidity hypotheses. The next phase requires a minimal capital injection ($5) into the PancakeSwap pool to validate Hypothesis 1.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.1*inch))

    # 2. Project Status
    story.append(Paragraph("2. Project Status (Completed Work)", heading_style))
    status_text = """
    <para>
    - <b>Smart Contract Deployments (3 total):</b><br/>
      &nbsp;&nbsp;* Contract 1: ETH Testnet. Lacked the TRADER_ROLE.<br/>
      &nbsp;&nbsp;* Contract 2: ETH Testnet. Fully includes the TRADER_ROLE for admin-controlled transfers.<br/>
      &nbsp;&nbsp;* Contract 3: Deployed to BNB Smart Chain Mainnet via proxy. This is the current live, gas-efficient contract.<br/>
    - <b>Admin Dashboard:</b> Fully functional and accessible (rinanze-admin.vercel.app). Built to support any token contract, making it a reusable internal asset. A lean user-facing trading website is also in the pipeline.<br/>
    - <b>Liquidity Pool Creation:</b> A RIN-to-BNB pool has been created on PancakeSwap. The liquidity reflects on Trust Wallet, but the price is not displaying.<br/>
    - <b>Current Hypotheses:</b><br/>
      &nbsp;&nbsp;* Hypothesis 1 – Insufficient Liquidity: The current pool is too small (0.09 RIN / $0.09 BNB).<br/>
      &nbsp;&nbsp;* Hypothesis 2 – Volume Requirement: Trust Wallet aggregators may require baseline trading volume before recognizing the token.
    </para>
    """
    story.append(Paragraph(status_text, styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    # 3. Scope Creep
    story.append(Paragraph("3. Scope Creep & The Commitment to Perfection", heading_style))
    story.append(Paragraph(
        "This project has expanded significantly beyond its initial scope. However, this growth was not met with a demand for a higher price. We made a conscious, strategic decision to absorb this additional work. Why? Because we are not just a vendor; we are resilient experts. We chose to deliver a solution that is polished to its core rather than a rushed, imperfect product that simply satisfies minimum requirements. We are investing our expertise and time because we prioritize long-term structural integrity over short-term profit.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.1*inch))

    # 4. Chronological Report
    story.append(Paragraph("4. Chronological Report: Project Evolution & R&D Milestones", heading_style))
    chron_text = """
    <para>
    - <b>Phase 1 – Base Contract:</b> Deployed first ETH testnet contract. Blocker: Lacked TRADER_ROLE for public transfer restriction.<br/>
    - <b>Phase 2 – Governance Correction:</b> Deployed second ETH testnet contract with full TRADER_ROLE implementation.<br/>
    - <b>Phase 3 – Display Blocker & Pivot:</b> Requested to show a high dollar value on Trust Wallet. Research revealed this requires massive collateral. Pivoted deployment to BNB Smart Chain to avoid high gas fees and deployed the current mainnet contract.<br/>
    - <b>Phase 4 – Dashboard Development:</b> Built the rinanze-admin.vercel.app dashboard. Optimized it to support any token contract for future reuse.<br/>
    - <b>Phase 5 – Vendor Investigation:</b> Researched "Flash USDT" vendors. Discovery: Inspecting their exposed JavaScript source code revealed their platform is a frontend scam—it shows a fake balance for 5 minutes, then resets to zero. No real tokens are ever sent. We saved a potential ₦50k loss.<br/>
    - <b>Phase 6 – First Liquidity Test:</b> Injected minimal test liquidity ($0.09 BNB / 0.09 RIN) into PancakeSwap. Result: The pool is live, but the scale is too small to trigger a price display.
    </para>
    """
    story.append(Paragraph(chron_text, styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    # 5. R&D Status
    story.append(Paragraph("5. R&D Status & Speculations (The Way Forward)", heading_style))
    rd_text = """
    <para>
    The project is now in active R&D. Capital is being utilized for gas deployment fees and liquidity testing. We are currently exploring two possible paths:<br/><br/>
    <b>Path A – Testing Hypothesis 1 (Liquidity Scaling)</b><br/>
    We must confirm whether the missing price is purely a liquidity math issue. To scale the pool, we will inject a minimum of $5 in BNB and pair it with a massive amount of RIN.<br/>
    <i>Important Note:</i> Injecting a massive amount of RIN into the pool will temporarily drop the current live contract's price (as we are flooding the supply). However, this test is purely for gathering data. The value of proving how the price maps to Trust Wallet outweighs the temporary loss on this test contract. Once the method is validated, we can recreate a brand-new final contract with the correct data.<br/><br/>
    <b>Path B – Testing Hypothesis 2 (Volume & Market Trust)</b><br/>
    If Path A succeeds but the price still fails to show, the issue is likely an aggregator trust requirement. We can monitor the token's performance on BscScan and market aggregators for this phase. While Path B requires no direct capital injection, it is not truly "free". It burns significant development time and operational overhead. With our strict 14-day delivery timeline currently under pressure, every day spent monitoring is a day of real cost to us.
    </para>
    """
    story.append(Paragraph(rd_text, styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    # 6. Conclusion
    story.append(Paragraph("6. Conclusion & Next Steps", heading_style))
    conclusion_text = """
    <para>
    The core infrastructure (contracts, dashboard, mainnet deployment) is complete. The only unresolved aspect is the Trust Wallet display, which requires the targeted R&D testing detailed above. In the meantime, we are actively researching alternative technical strategies and workarounds to ensure we do not leave any viable solution unexplored.<br/><br/>
    <b>If you, as the project owner, choose to proceed with the project considering all these factors, the following steps will be taken:</b><br/>
    1. Allocate a $5 capital injection to the PancakeSwap pool to execute the Path A liquidity test.<br/>
    2. Monitor the pool to see if this triggers the Trust Wallet price display.<br/>
    3. If the price appears, we move to final testing and handover.<br/>
    4. If it fails, we will immediately proceed to Path B (monitoring volume) at no additional direct cost, and continue testing until we identify the root cause.
    </para>
    """
    story.append(Paragraph(conclusion_text, styles['Normal']))

    doc.build(story)
    print("Advanced PDF generated successfully.")

if __name__ == "__main__":
    create_advanced_pdf()
