import os
import re
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

# Exact RMIT Hack-A-Venture 2026 Guideline Color Palette
HEX_RMIT_ORANGE = "F26522"      # Heading 1, Heading 2, Cover Title, Table Header Fill
HEX_TABLE_FIRST_COL = "FDE8D7"  # Soft Peach / Beige for Table Column 1 (matching Page 8-9 of Guideline)
HEX_WHITE = "FFFFFF"
HEX_BLACK = "000000"

RGB_RMIT_ORANGE = RGBColor(242, 101, 34)
RGB_BLACK = RGBColor(0, 0, 0)
RGB_DARK_TEXT = RGBColor(20, 20, 20)
RGB_GREY_FOOTER = RGBColor(102, 102, 102)
RGB_WHITE = RGBColor(255, 255, 255)


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=110, bottom=110, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def set_table_borders(table, color="000000", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def set_borderless_table(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def add_page_number_to_run(run):
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def configure_styles_and_footer(doc, footer_left_text="Round 1 Submission: RMIT Hack-A-Venture 2026"):
    for section in doc.sections:
        section.top_margin = Inches(0.95)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        footer = section.footer
        footer.is_linked_to_previous = False
        p_foot = footer.paragraphs[0]
        p_foot.text = ""
        p_foot.paragraph_format.space_before = Pt(4)
        p_foot.paragraph_format.space_after = Pt(0)
        
        # Create a 2-column borderless table in footer to align left label and right page number exactly like the Guideline PDF
        ftbl = footer.add_table(rows=1, cols=2, width=Inches(6.5))
        set_borderless_table(ftbl)
        cell_left = ftbl.rows[0].cells[0]
        cell_right = ftbl.rows[0].cells[1]
        
        pl = cell_left.paragraphs[0]
        pl.alignment = WD_ALIGN_PARAGRAPH.LEFT
        rl = pl.add_run(footer_left_text)
        rl.font.name = 'Arial'
        rl.font.size = Pt(9.5)
        rl.font.color.rgb = RGB_GREY_FOOTER
        
        pr = cell_right.paragraphs[0]
        pr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        rr = pr.add_run()
        rr.font.name = 'Arial'
        rr.font.size = Pt(9.5)
        rr.font.color.rgb = RGB_GREY_FOOTER
        add_page_number_to_run(rr)


def add_rich_text(paragraph, text, font_size=11, is_first_col=False, font_color=RGB_DARK_TEXT):
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        else:
            run = paragraph.add_run(part)
            if is_first_col:
                run.bold = True
        run.font.name = 'Arial'
        run.font.size = Pt(font_size)
        run.font.color.rgb = font_color


def add_formatted_table(doc, headers, rows):
    """
    Matches the exact RMIT Guideline PDF Table Style (Pages 8 & 9):
    - Header row: Orange background (#F26522), White bold centered text
    - First column: Soft peach background (#FDE8D7), Black bold text
    - Other columns: White background (#FFFFFF), Black regular/rich text
    - Borders: Thin solid black grid borders
    """
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="000000", sz="4", val="single")
    
    hdr_cells = table.rows[0].cells
    for i, header_text in enumerate(headers):
        hdr_cells[i].text = ""
        hdr_cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(header_text)
        run.bold = True
        run.font.name = 'Arial'
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGB_WHITE
        set_cell_background(hdr_cells[i], HEX_RMIT_ORANGE)
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=130, right=130)
        
    for row_data in rows:
        row_cells = table.add_row().cells
        for c_idx, cell_value in enumerate(row_data):
            row_cells[c_idx].text = ""
            row_cells[c_idx].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            is_col_0 = (c_idx == 0)
            add_rich_text(p, cell_value, font_size=10, is_first_col=is_col_0)
            set_cell_background(row_cells[c_idx], HEX_TABLE_FIRST_COL if is_col_0 else HEX_WHITE)
            set_cell_margins(row_cells[c_idx], top=100, bottom=100, left=130, right=130)
            
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(4)


def add_guideline_heading_1(doc, text):
    """
    Matches Guideline '1. Introduction', '2. Proposal Structure', '3. Submission Guidelines':
    Bold, 18pt, Orange (#F26522), no bottom border.
    """
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.name = 'Arial'
    run.font.size = Pt(18)
    run.font.color.rgb = RGB_RMIT_ORANGE
    return p


def add_guideline_heading_2(doc, text):
    """
    Matches Guideline '2.1. Executive Summary' ... '2.8. Appendix (Optional)':
    Bold, 14pt, Orange (#F26522), slightly indented (0.25 in).
    """
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.name = 'Arial'
    run.font.size = Pt(14)
    run.font.color.rgb = RGB_RMIT_ORANGE
    return p


def add_guideline_subheading(doc, text, underline=False):
    """
    Matches Guideline subheadings inside sections (e.g., 'Target Market and Customer Segmentation',
    'Market Sizing and Demand', 'Revenue Model', 'Competitive Landscape', 'SDG Alignment:',
    'Implementation Roadmap', 'Scalability and Infrastructure'):
    Bold, 11pt, Black (#000000), optionally underlined.
    """
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.underline = underline
    run.font.name = 'Arial'
    run.font.size = Pt(11)
    run.font.color.rgb = RGB_BLACK
    return p


def add_body_p(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.2
    add_rich_text(p, text, font_size=11)
    return p


def add_bullet_p(doc, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.2
    add_rich_text(p, text, font_size=11)
    return p


def add_code_box(doc, code_text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="F26522", sz="6", val="single")
    cell = table.rows[0].cells[0]
    set_cell_background(cell, "FFFDFB")
    set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.08
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGB_DARK_TEXT
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(4)


def add_cover_page(doc, title_line1, title_line2, project_title, project_subtitle, meta_rows):
    """
    Matches Page 1 of the RMIT Hack-A-Venture 2026 Round 1 Guidelines PDF:
    - Large centered orange title ('ROUND 1 IDEA PROPOSAL' / 'RMIT HACK-A-VENTURE 2026')
    - Project title block
    - Bottom-left borderless metadata table ('Version:', 'Prepared for:', 'Prepared by:', 'Last update:')
    """
    for _ in range(3):
        doc.add_paragraph()
        
    p_t1 = doc.add_paragraph()
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t1.paragraph_format.space_before = Pt(12)
    p_t1.paragraph_format.space_after = Pt(2)
    r_t1 = p_t1.add_run(title_line1)
    r_t1.bold = True
    r_t1.font.name = 'Arial'
    r_t1.font.size = Pt(26)
    r_t1.font.color.rgb = RGB_RMIT_ORANGE
    
    p_t2 = doc.add_paragraph()
    p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t2.paragraph_format.space_before = Pt(0)
    p_t2.paragraph_format.space_after = Pt(24)
    r_t2 = p_t2.add_run(title_line2)
    r_t2.bold = True
    r_t2.font.name = 'Arial'
    r_t2.font.size = Pt(22)
    r_t2.font.color.rgb = RGB_RMIT_ORANGE
    
    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_proj.paragraph_format.space_before = Pt(12)
    p_proj.paragraph_format.space_after = Pt(6)
    r_proj = p_proj.add_run(project_title)
    r_proj.bold = True
    r_proj.font.name = 'Arial'
    r_proj.font.size = Pt(18)
    r_proj.font.color.rgb = RGB_BLACK
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(36)
    r_sub = p_sub.add_run(project_subtitle)
    r_sub.bold = True
    r_sub.font.name = 'Arial'
    r_sub.font.size = Pt(12.5)
    r_sub.font.color.rgb = RGB_DARK_TEXT
    
    for _ in range(3):
        doc.add_paragraph()
        
    # Borderless metadata block matching Page 1 of the Guideline PDF
    meta_tbl = doc.add_table(rows=len(meta_rows), cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    set_borderless_table(meta_tbl)
    for idx, (label, val) in enumerate(meta_rows):
        c0 = meta_tbl.rows[idx].cells[0]
        c1 = meta_tbl.rows[idx].cells[1]
        c0.width = Inches(1.8)
        c1.width = Inches(4.7)
        set_cell_margins(c0, top=40, bottom=40, left=40, right=60)
        set_cell_margins(c1, top=40, bottom=40, left=40, right=40)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(1)
        p0.paragraph_format.space_after = Pt(1)
        r0 = p0.add_run(label)
        r0.bold = True
        r0.font.name = 'Arial'
        r0.font.size = Pt(11)
        r0.font.color.rgb = RGB_BLACK
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(1)
        p1.paragraph_format.space_after = Pt(1)
        r1 = p1.add_run(val)
        r1.font.name = 'Arial'
        r1.font.size = Pt(11)
        r1.font.color.rgb = RGB_BLACK
        
    doc.add_page_break()


def build_english_proposal(filepath):
    doc = Document()
    configure_styles_and_footer(doc, "Round 1 Submission: RMIT Hack-A-Venture 2026")
    
    # ================= COVER PAGE (EXCLUDED FROM WORD LIMIT) =================
    cover_meta = [
        ("Version:", "1.0 (Official Round 1 Idea Proposal)"),
        ("Prepared for:", "Organizing Committee & Judging Panel, RMIT Hack-A-Venture 2026"),
        ("Prepared by:", "Team TCQL"),
        ("Theme:", "Open Innovation for a Resilient and Sustainable Financial System in Vietnam"),
        ("Primary Pillar:", "Pillar 5: Trust Architecture & Financial Integrity"),
        ("Intersecting Pillar:", "Pillar 2: Financial Infrastructure & Ecosystem Interoperability"),
        ("Last update:", "15th November 2026")
    ]
    add_cover_page(
        doc,
        title_line1="ROUND 1 IDEA PROPOSAL",
        title_line2="RMIT HACK-A-VENTURE 2026",
        project_title="MULEHUNTER AI",
        project_subtitle="Real-Time Interbank Graph Intelligence Engine Upgrading Vietnam’s SIMO & Payment Trust Architecture",
        meta_rows=cover_meta
    )
    
    # ================= 1. INTRODUCTION =================
    add_guideline_heading_1(doc, "1. Introduction")
    add_body_p(doc, "Submitted by **Team TCQL** for **RMIT Hack-A-Venture 2026** under the theme *\"Open Innovation for a Resilient and Sustainable Financial System in Vietnam\"*, this proposal introduces **MuleHunter AI**—a real-time interbank Graph Neural Network (GNN) intelligence engine designed to upgrade the State Bank of Vietnam’s (SBV) **SIMO** fraud-monitoring platform into an automated topological circuit breaker (**'SIMO 2.0'**). Positioned at the intersection of **Pillar 5: Trust Architecture & Financial Integrity** (Primary) and **Pillar 2: Financial Infrastructure & Ecosystem Interoperability** (Secondary), this document presents our comprehensive Round 1 Idea Proposal across six core areas: Executive Summary, Problem Statement & Market Pain, Solution Architecture & FinTech Integration, Market Size & Competitive Analysis, Strategic Contribution & Expected Impact, and Implementation Roadmap & Scalability.")

    # ================= 2. PROPOSAL STRUCTURE =================
    add_guideline_heading_1(doc, "2. Proposal Structure")
    
    # 2.1 Executive Summary
    add_guideline_heading_2(doc, "2.1. Executive Summary")
    add_body_p(doc, "By mid-2026, Vietnam’s digital financial transformation reached a historic milestone: nearly **89% of citizens aged 15 and above own a payment account**, over **95% of banking transactions occur via digital channels**, and cashless payments surged **34.28% YoY to exceed 15 billion transactions in the first half of 2026** (reaching 28 times GDP). However, instant interbank payment rails (NAPAS247, VietQR) have simultaneously exposed the ecosystem to industrial-scale cyber fraud. While the State Bank of Vietnam (SBV) introduced the **SIMO (Information System for Supporting Management, Monitoring and Prevention of Payment Fraud Risks)**—which issued **4.9 million alerts** and prevented **VND 5.5 trillion** in losses across **1.6 million suspended transactions** by July 2026—official statistics reveal a critical vulnerability: **over 3.3 million alerts (67.3%) failed to stop transfers**, and static blacklists remain blind to unreported 'fresh mule' accounts and automated sub-10-million-VND 'smurfing' rings.")
    add_body_p(doc, "Aligning primarily with **Pillar 5 (Trust Architecture & Financial Integrity)** and intersecting with **Pillar 2 (Financial Infrastructure & Ecosystem Interoperability)**, Team **TCQL** proposes **MuleHunter AI**—a real-time interbank Graph Neural Network (GNN) intelligence engine that upgrades SIMO from a *reactive static blacklist* into a *proactive topological circuit breaker ('SIMO 2.0')*. Combining **In-Memory Streaming Graphs (Memgraph)** with decoupled **GraphSAGE/APAN** inference, MuleHunter AI detects multi-hop laundering topologies (**Fan-out, Fan-in, Circular Routing**) across banks in **under 500 milliseconds**. Leveraging **Open APIs (Circular 64/2024/TT-NHNN)**, **VNeID/Project 06 identity verification**, and **Federated Graph Learning** (preserving privacy under **Decree 13/2023/ND-CP**), MuleHunter AI dynamically triggers step-up facial biometrics or freezes illicit dispersion in real time—reinforcing institutional trust and protecting trillions of VND across Vietnam’s digital economy.")

    # 2.2 Problem Statement & Market Pain
    add_guideline_heading_2(doc, "2.2. Problem Statement & Market Pain")
    add_guideline_subheading(doc, "Specific Financial Problem & Urgency in Vietnam")
    add_body_p(doc, "As Vietnam targets a cashless payment value of **30 times GDP by 2030** (Vietnam+, 2026), instant settlement rails have become the primary conduit for transnational cyber-fraud syndicates to launder stolen funds through networks of **Money Mule accounts** (rented, purchased, or shell-company bank accounts). Once a victim authorizes a transfer, syndicates disperse funds across 3–4 banking hops within **30 to 120 seconds**, converting proceeds into cryptocurrency (USDT P2P) before banks or law enforcement can intervene.")
    
    add_guideline_subheading(doc, "Root Causes, Affected Groups & Limitations of Existing Solutions")
    add_bullet_p(doc, "**The 67.3% 'Advisory Conversion Gap' in SBV’s Current SIMO System:** By July 2026, SIMO generated **4.9 million fraud alerts**, yet only **1.6 million prompted customers to cancel transactions** (Nguoi Quan Sat, 2026; VietNamNet, 2026b). Because SIMO operates solely as an *advisory warning pop-up*, **3.3 million warned transactions still proceeded**—largely because victims under psychological manipulation (e.g., deepfake police impersonation scams) are coerced into ignoring warnings.")
    add_bullet_p(doc, "**Reactive 'Cold-Start' Blindness to Fresh Mules:** SIMO relies on post-mortem reporting: an account enters the blacklist only *after* prior victims suffer losses and file complaints. Criminal rings bypass SIMO by continuously rotating newly opened student/worker accounts ('fresh mules') that have zero negative history in SIMO.")
    add_bullet_p(doc, "**Sub-10-Million VND 'High-Velocity Smurfing' (Evading Decision 2345):** To bypass SBV’s **Decision 2345/QD-NHNN** (mandating facial biometrics for transfers >10 million VND per transaction or >20 million VND daily), syndicates deploy automated scripts to split a 150-million-VND theft into **16 parallel transfers of 9.3 million VND** across multiple banks, flying under biometric thresholds.")
    add_bullet_p(doc, "**Fragmented Single-Bank Visibility (Pillar 2 Gap):** Legacy bank AML systems (Oracle Mantas, SAS) inspect isolated transactions within a single bank’s silo. Bank A cannot see that funds sent to Bank B were immediately fractured across 10 accounts at Bank C and D.")

    prob_rows = [
        ["Detection Paradigm", "Single-bank tabular rules", "Centralized static blacklist lookup", "Blind to multi-bank network topologies"],
        ["Fresh Mule Catch", "Fails (No prior bad record)", "Fails (Not yet reported by victims)", "Zero-day mules launder money undetected"],
        ["Enforcement Action", "Post-event batch review", "Advisory pop-up (**67.3% ignored**)", "Manipulated victims still complete transfers"],
        ["False Positive Rate", "90% – 95% (Rule fatigue)", "High False Negatives on new accounts", "Severe compliance bottleneck & user friction"]
    ]
    add_formatted_table(doc, ["Dimension", "Legacy Bank AML", "Current SBV SIMO (1.0)", "Critical Unsolved Market Pain"], prob_rows)

    # 2.3 Solution Architecture & FinTech Integration
    add_guideline_heading_2(doc, "2.3. Solution Architecture & FinTech Integration")
    add_guideline_subheading(doc, "Proposed Solution & Core Features")
    add_body_p(doc, "Inspired by global benchmarks highlighted in Pillar 5 and Pillar 2—specifically **Visa AI-Powered Fraud Detection**, **Singapore’s Singpass/COSMIC**, and **PayNow**—**MuleHunter AI** operates as an interoperable, real-time graph intelligence layer plugged directly into **NAPAS247 and SIMO**:")
    add_bullet_p(doc, "**1. Zero-Day Topological Mule Detection:** Instead of checking whether an account is on a static blacklist, MuleHunter AI evaluates live structural behavior: *Fan-Out (Smurfing <10M VND)*, *Fan-In (Funneling to shell corporations)*, *Circular Wash Loops (A -> B -> C -> A)*, and *Pass-Through Velocity* (funds held <60s, end-of-day balance ~0).")
    add_bullet_p(doc, "**2. Dynamic Step-Up Biometrics (Closing the Smurfing Loophole):** When a sub-10-million-VND transfer exhibits a suspicious subgraph (**Mule Risk Score 0.60 – 0.85**), MuleHunter AI overrides static thresholds and forces an immediate **Decision 2345 facial liveness + VNeID verification challenge**, breaking psychological scam coercion and bot automation.")
    add_bullet_p(doc, "**3. Automated 15-Minute Circuit Breaker (Closing SIMO’s 67.3% Gap):** When **Mule Risk Score > 0.85** (confirming active multi-hop dispersion or fraud ring proximity), the system shifts from *advisory warning* to *active interception*—issuing a `BLOCK_AND_HOLD` command to freeze downstream dispersion for 15 minutes while alerting bank compliance teams.")
    add_bullet_p(doc, "**4. Privacy-Preserving Federated Graph Learning:** Commercial banks collaboratively train the shared GNN model on local fraud patterns by exchanging encrypted mathematical gradients (`FedAvg`) rather than raw customer records.")

    add_guideline_subheading(doc, "End-to-End Operational Workflow & System Topology")
    workflow_diagram = (
        "[Customer Initiates Transfer] ──> [NAPAS247 / VietQR Switch] ──> (Kafka Stream: Salted Hash IDs, Amount, Time)\n"
        "                                                                                │\n"
        "┌───────────────────────────────────────────────────────────────────────────────┴──────────────────────────┐\n"
        "│ MULEHUNTER AI — INTERBANK TRUST & GRAPH ENGINE (End-to-End SLA < 500ms)                                  │\n"
        "│  • TIER 1 FAST PATH (<50ms): Memgraph C++ In-Memory (3-Hop Cycle, Degree Spike & Pass-Through Filter)    │\n"
        "│  • TIER 2 DEEP GNN PATH (<300ms): 2-Hop Ego-Graph Extraction + Decoupled APAN/GraphSAGE on ONNX Runtime  │\n"
        "└───────────────────────────────────────────────────────────────────────────────┬──────────────────────────┘\n"
        "                                                                                ▼\n"
        "   ┌──────────────────────────────────────────┬─────────────────────────────────┴──────────────────────────┐\n"
        "   ▼ (Score < 0.60: ~90% Traffic)             ▼ (Score 0.60 - 0.85)                                        ▼ (Score > 0.85)\n"
        "[ALLOW INSTANT SETTLEMENT]           [DYNAMIC STEP-UP BIOMETRICS]                               [AUTOMATED CIRCUIT BREAKER]\n"
        "(Cleared in < 30ms)                  (Force QĐ 2345 Liveness + VNeID API)                       (15-Min Hold + Sync SIMO & A05)"
    )
    add_code_box(doc, workflow_diagram)

    add_guideline_subheading(doc, "Technology Stack & Open Innovation Enablement")
    add_body_p(doc, "To achieve sub-second graph inference across >30 billion annual transactions, MuleHunter AI adapts the **APAN (Asynchronous Propagation Attention Network)** architecture developed by **Ant Group / Alipay** (*ACM SIGMOD 2021*) and **TigerGraph’s 100ms payment SLA**:")
    add_bullet_p(doc, "**Streaming & In-Memory Graph (Tier 1):** **Apache Kafka** + **Memgraph (C++)** execute sub-50ms Cypher queries to clear 90% of normal transfers and flag sudden degree spikes.")
    add_bullet_p(doc, "**Inductive Graph AI (Tier 2):** **PyTorch Geometric (PyG)** running **GraphSAGE** and **CARE-GNN** compiled on **ONNX Runtime** (<250ms inference on localized 2-hop ego-graphs).")
    add_bullet_p(doc, "**Open Innovation Ecosystem:** Enabled by **Circular 64/2024/TT-NHNN (Open APIs)** for standardized bank-fintech telemetry, **Flower (`flwr`)** for decentralized Federated Learning, and **Project 06 (C06/VNeID) APIs** (Vietnam’s equivalent to *Singpass*) to cross-verify account holder legitimacy.")

    add_guideline_subheading(doc, "Technical, Regulatory & Data Barriers vs. Mitigations")
    add_bullet_p(doc, "**Barrier 1: Data Privacy (Decree 13/2023/ND-CP) & Banking Secrecy.** *Mitigation:* Account numbers and CCCD IDs undergo **Salted SHA-256 Hashing** at the switch level. Banks share zero raw PII; model intelligence is synchronized exclusively via **Federated Learning weight updates**.")
    add_bullet_p(doc, "**Barrier 2: Real-Time Throughput Bottlenecks.** *Mitigation:* Asynchronous background embedding propagation decouples heavy graph traversal from synchronous payment authorization, keeping P99 latency <400ms.")

    # 2.4 Market Size & Competitive Analysis
    add_guideline_heading_2(doc, "2.4. Market Size & Competitive Analysis")
    add_guideline_subheading(doc, "Target Market and Customer Segmentation")
    add_bullet_p(doc, "**Primary B2B / B2G Customers:** (1) **State Bank of Vietnam (SBV) & NAPAS** deploying MuleHunter AI as the analytical 'SIMO 2.0' core; (2) **46 Commercial Banks & 50+ Payment Intermediaries (e-Wallets)** (Vietcombank, BIDV, VietinBank, MB, Techcombank, MoMo, VNPay, ZaloPay) processing >95% of transactions digitally.")
    add_bullet_p(doc, "**Key Beneficiaries:** **89% of Vietnamese citizens aged 15+** owning payment accounts and **900,000+ MSMEs** protected from cyber-fraud losses.")

    add_guideline_subheading(doc, "Market Sizing and Demand")
    add_bullet_p(doc, "**Evidence-Based Demand:** In 1H 2026 alone, Vietnam recorded **15+ billion cashless transactions** (+34.28% YoY), while SIMO flagged **4.9 million risky transfers** by July 2026 (SBV, 2026; VnEconomy, 2026). APAC RegTech/AML spending is expanding at **18.4% CAGR**.")
    add_bullet_p(doc, "**Market Tiers:** **TAM (ASEAN RegTech/AML):** **$1.4 Billion USD/year** | **SAM (Vietnam Banking & Switch AML/Fraud):** **$120 Million USD/year** | **SOM (3-Year Target - SIMO Core + 15 Banks):** **$8.5 Million USD/year**.")

    add_guideline_subheading(doc, "Revenue Model")
    add_bullet_p(doc, "**Hybrid Revenue Model (>75% Gross Margin):** (1) **Annual Enterprise Licensing ($60,000 – $150,000/year per bank)** for Federated Edge Nodes & Investigation Dashboards; (2) **Micro-API Screening Fee ($0.0002 / 5 VND per high-risk graph query)**; (3) **Automated STR & Forensic RegTech Add-On**.")

    add_guideline_subheading(doc, "Competitive Landscape")
    comp_rows = [
        ["Ecosystem Scope", "Siloed within 1 bank", "Single-enterprise focus", "National database", "**National Interbank Live Graph**"],
        ["Fresh Mule Catch", "Rule-based (Delayed)", "Network entity resolution", "Reactive blacklist only", "**Proactive Zero-Day Topology**"],
        ["Enforcement", "Post-event batch review", "1–5s latency", "Advisory (**67.3% ignored**)", "**<350ms Step-Up & Circuit Breaker**"],
        ["Vietnam Legal Fit", "Costly customization", "$1M+ cost, PII barriers", "Native SBV system", "**Decree 13, QĐ 2345 & TT 64 Native**"]
    ]
    add_formatted_table(doc, ["Dimension", "Legacy Bank AML (SAS, Oracle)", "Global Graph AI (Quantexa)", "Current SBV SIMO (1.0)", "MuleHunter AI ('SIMO 2.0')"], comp_rows)
    add_body_p(doc, "**USP & Defensible Moat:** MuleHunter AI is the **only sub-500ms, privacy-preserving interbank Graph AI engine tailored to upgrade Vietnam’s SIMO and Decision 2345 architecture**. Its **Federated Learning network effect** creates a compounding collective intelligence moat that isolated vendors cannot replicate.")

    # 2.5 Strategic Contribution & Expected Impact
    add_guideline_heading_2(doc, "2.5. Strategic Contribution & Expected Impact")
    kpi_rows = [
        ["SIMO Alert Prevention Conversion", "**32.7%** (1.6M / 4.9M alerts)", "**> 85%** (via Step-Up & Hold)", "Ratio of flagged transfers successfully stopped"],
        ["End-to-End Screening Latency", "Hours (Batch) / Static Lookup", "**< 350 ms (P99 < 500 ms)**", "Real-time Kafka/Locust telemetry"],
        ["Zero-Day Fresh Mule Recall", "< 15% (Unreported in SIMO)", "**> 88% (AUC-ROC > 0.93)**", "Validation on IBM AML & pilot bank streams"],
        ["False Positive Alert Rate", "90% – 95% (Legacy rules)", "**< 15% (70%+ reduction)**", "Compliance officer Precision@K audit"]
    ]
    add_formatted_table(doc, ["Measurable Indicator (KPI)", "Current Baseline (July 2026)", "MuleHunter AI Target", "Evaluation Method"], kpi_rows)
    
    add_bullet_p(doc, "**Financial Sustainability & Adversarial Resilience:** Preventing an additional VND 5–10 trillion in annual fraud losses delivers immediate ROI to banks, sustaining operations via commercial licensing without external subsidies. To counter criminals camouflaging mules with small legitimate purchases, our **CARE-GNN** reinforcement learning module dynamically prunes noisy benign edges, avoiding wrongful freezes for honest citizens.")
    
    add_guideline_subheading(doc, "SDG Alignment:", underline=True)
    add_bullet_p(doc, "**SDG 16 (Peace, Justice and Strong Institutions — Target 16.4 & 16.a):** Directly disrupts organized cybercrime and illicit financial flows across Vietnam, equipping regulators (SBV) and law enforcement (A05) with court-admissible topological evidence.")
    add_bullet_p(doc, "**SDG 9 (Industry, Innovation and Infrastructure — Target 9.1):** Modernizes Vietnam’s core financial infrastructure (SIMO & NAPAS) through interoperable Open APIs and distributed Graph AI.")
    add_bullet_p(doc, "**SDG 8 (Decent Work and Economic Growth — Target 8.10):** Safeguards the life savings and working capital of 89% of banked citizens and MSMEs, ensuring inclusive participation in Vietnam’s digital economy.")

    # 2.6 Implementation Roadmap & Scalability
    add_guideline_heading_2(doc, "2.6. Implementation Roadmap & Scalability")
    add_guideline_subheading(doc, "Implementation Roadmap")
    roadmap_rows = [
        ["Stage 1: MVP & Benchmark", "Q1 2027", "Train GraphSAGE/CARE-GNN on **IBM AML** & **Elliptic++** (AUC > 0.92); deploy **Memgraph + FastAPI/ONNX** (<350ms SLA).", "Open-source stack (`PyG`, `Memgraph`, `Flower`); Cloud GPU testbed."],
        ["Stage 2: SBV Sandbox Entry", "Q2 2027", "Enter SBV Regulatory Sandbox (**Decree 94/2025/ND-CP**); validate Salted SHA-256 & Federated Learning with **2 pilot banks**.", "SBV Sandbox approval; Circular 09/2020/TT-NHNN security audit."],
        ["Stage 3: SIMO 2.0 Live Pilot", "Q3 2027", "Integrate bidirectional API hooks with **SBV SIMO** & **Decision 2345 Step-Up Biometrics**; launch **Cytoscape.js + XAI Dashboard**.", "NAPAS / SIMO sandbox gateway; Project 06 (C06/VNeID) APIs."],
        ["Stage 4: Ecosystem Scale", "Q4 2027", "Scale to **15+ commercial banks** and top e-wallets (MoMo, VNPay, ZaloPay) at **50,000+ TPS**; automate real-time STR filings.", "Commercial SLA agreements; Tier-3 On-Premise Data Center."]
    ]
    add_formatted_table(doc, ["Implementation Stage", "Timeline", "Key Milestones & Validation Deliverables", "Dependencies & Partners"], roadmap_rows)

    add_guideline_subheading(doc, "Scalability and Infrastructure")
    add_bullet_p(doc, "**Sub-Linear Cost Scaling (O(k^d) Complexity):** Because inference extracts localized **2-hop ego-graphs** rather than traversing the entire national graph, compute costs scale with local neighborhood degree k rather than total accounts N. Handling Vietnam’s 34.28% annual transaction growth requires only horizontal addition of stateless ONNX worker containers.")
    add_bullet_p(doc, "**Plug-and-Play Interoperability & Regional Exportability:** Built on **Circular 64 Open APIs** and **Kafka**, onboarding any bank, e-wallet, or BNPL provider requires zero architectural overhaul, making the platform immediately transferable to ASEAN instant switches (**PayNow Singapore**, **PromptPay Thailand**, **InstaPay Philippines**).")

    # ================= REFERENCES & APPENDIX (EXCLUDED FROM WORD LIMIT) =================
    doc.add_page_break()
    add_guideline_heading_2(doc, "2.7. References")
    refs = [
        "1. Bank for International Settlements (BIS). (2023). Project Aurora: The power of data, technology and collaborative analysis in Anti-Money Laundering (AML). BIS Innovation Hub. https://www.bis.org/publ/othp64.htm",
        "2. Dou, Y., Liu, Z., Sun, L., Deng, Y., Peng, H., & Yu, P. S. (2020). Enhancing Graph Neural Network-based Fraud Detectors against Camouflaged Fraudsters (CARE-GNN). Proceedings of ACM CIKM '20. https://arxiv.org/abs/2008.08692",
        "3. Government of Vietnam. (2023). Decree No. 13/2023/ND-CP on Protection of Personal Data. Hanoi, Vietnam.",
        "4. Government of Vietnam. (2025). Decree No. 94/2025/ND-CP on Controlled Testing Mechanism (Regulatory Sandbox) for FinTech Solutions in the Banking Sector. Hanoi, Vietnam.",
        "5. Monetary Authority of Singapore (MAS). (2024). MAS Launches COSMIC Platform to Strengthen Financial System's Defence Against Money Laundering. https://www.mas.gov.sg",
        "6. Nguoi Quan Sat. (2026, August). Phó vụ trưởng Vụ Thanh toán NHNN: 1,6 triệu lượt khách hàng đã kịp dừng giao dịch, bảo vệ 5.500 tỷ đồng [Deputy Director of the SBV Payment Department: 1.6 million customers promptly stopped transactions, protecting 5,500 billion VND]. https://nguoiquansat.vn/pho-vu-truong-vu-thanh-toan-nhnn-1-6-trieu-luot-khach-hang-da-kip-dung-giao-dich-bao-ve-5-500-ty-dong-truoc-nguy-co-lua-dao-309978.html",
        "7. Saigon Giai Phong. (2026). Cashless payment value reaches 28 times GDP in first half of 2026. https://en.sggp.org.vn/cashless-payment-value-reaches-28-times-gdp-in-first-half-of-2026-post128778.html",
        "8. State Bank of Vietnam (SBV). (2023). Decision No. 2345/QD-NHNN on implementing safety and security solutions for online payments and bank card payments.",
        "9. State Bank of Vietnam (SBV). (2024). Circular No. 64/2024/TT-NHNN regulating the implementation of Open Application Programming Interfaces (Open API) in the banking sector.",
        "10. VietNamNet. (2026a). Vietnam anti-fraud banking system blocks $177 million in suspicious transfers. https://vietnamnet.vn/en/vietnam-anti-fraud-banking-system-blocks-177-million-in-suspicious-transfers-2519899.html",
        "11. VietNamNet. (2026b, August 13). Vietnam bank alerts stop 1.6 million suspected scam transactions. https://vietnamnet.vn/en/vietnam-bank-alerts-stop-1-6-million-suspected-scam-transactions-2545014.html",
        "12. Visa Inc. (2025). Visa AI-Powered Fraud Detection & Protect Solutions. https://corporate.visa.com/en/solutions/visa-protect/insights/ai-fraud-detection.html",
        "13. VnEconomy. (2026, August 12). Vietnam’s cashless payment transactions rise 34.3% in first half. https://en.vneconomy.vn/vietnams-cashless-payment-transactions-rise-343-in-first-half.htm",
        "14. Wang, X., et al. (2021). APAN: Asynchronous Propagation Attention Network for Real-time Temporal Graph Embedding (Ant Group / Alipay). Proceedings of ACM SIGMOD '21. https://arxiv.org/abs/2012.06124",
        "15. Weber, M., et al. (2019). Anti-Money Laundering in Bitcoin: Experimenting with Graph Convolutional Networks for Financial Forensics. KDD '19 Workshop on Anomaly Detection in Finance, MIT-IBM Watson AI Lab. https://arxiv.org/abs/1908.02591"
    ]
    for ref in refs:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        run = p.add_run(ref)
        run.font.name = 'Arial'
        run.font.size = Pt(10)
        run.font.color.rgb = RGB_DARK_TEXT

    add_guideline_heading_2(doc, "2.8. Appendix (Optional)")
    add_guideline_subheading(doc, "Appendix A: Topological Money Laundering Signatures Detected by MuleHunter AI")
    topo_box = (
        "1. FAN-OUT (Smurfing < 10M VND)      2. FAN-IN (Funnel to Shell Corp)     3. CIRCULAR ROUTING (Wash Loop)\n"
        "       ┌─> [Mule 1] (9.5M)                [Mule 1] ─┐                        [Acc A] ──> [Acc B]\n"
        "[Victim]─┼─> [Mule 2] (9.8M)              [Mule 2] ─┼─> [Shell Company]         ▲           │\n"
        "       └─> [Mule 3] (9.2M)                [Mule 3] ─┘   (Crypto P2P Exit)    [Acc D] <── [Acc C]"
    )
    add_code_box(doc, topo_box)

    add_guideline_subheading(doc, "Appendix B: Verified Open-Source Tech Stack & Benchmark Datasets")
    add_bullet_p(doc, "**Benchmark Datasets:** IBM Transactions for Anti-Money Laundering (https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml) | Elliptic++ Dataset (https://github.com/git-disl/EllipticPlusPlus)")
    add_bullet_p(doc, "**Core Frameworks:** PyTorch Geometric (https://github.com/pyg-team/pytorch_geometric) | PyGOD Outlier Detection (https://github.com/pygod-team/pygod) | Memgraph Streaming Graph DB (https://github.com/memgraph/memgraph) | Flower Federated Learning (https://github.com/adap/flower)")

    try:
        doc.save(filepath)
        print(f"Saved English DOCX: {filepath}")
    except PermissionError:
        alt_path = filepath.replace(".docx", "_Updated.docx")
        doc.save(alt_path)
        print(f"File {filepath} is open in Word; saved to: {alt_path}")


def build_vietnamese_proposal(filepath):
    doc = Document()
    configure_styles_and_footer(doc, "Round 1 Submission: RMIT Hack-A-Venture 2026")
    
    # ================= COVER PAGE =================
    cover_meta_vi = [
        ("Phiên bản (Version):", "1.0 (Hồ sơ Đề xuất Ý tưởng Vòng 1)"),
        ("Kính gửi (Prepared for):", "Ban Tổ chức & Hội đồng Giám khảo RMIT Hack-A-Venture 2026"),
        ("Thực hiện bởi (Prepared by):", "Team TCQL"),
        ("Chủ đề (Theme):", "Open Innovation for a Resilient and Sustainable Financial System in Vietnam"),
        ("Trụ cột chính (Primary Pillar):", "Pillar 5: Trust Architecture & Financial Integrity (Kiến trúc Niềm tin & Toàn vẹn Tài chính)"),
        ("Trụ cột giao thoa (Secondary):", "Pillar 2: Financial Infrastructure & Ecosystem Interoperability (Hạ tầng & Liên thông Hệ sinh thái)"),
        ("Cập nhật (Last update):", "15/11/2026")
    ]
    add_cover_page(
        doc,
        title_line1="ROUND 1 IDEA PROPOSAL",
        title_line2="RMIT HACK-A-VENTURE 2026",
        project_title="MULEHUNTER AI",
        project_subtitle="Lõi Trí tuệ Đồ thị Thời gian thực Nâng cấp Hệ thống SIMO & Kiến trúc Niềm tin Thanh toán Quốc gia",
        meta_rows=cover_meta_vi
    )
    
    # ================= 1. INTRODUCTION =================
    add_guideline_heading_1(doc, "1. Introduction (Giới thiệu Chủ đề Dự thi)")
    add_body_p(doc, "Được thực hiện bởi **Team TCQL** trong khuôn khổ cuộc thi **RMIT Hack-A-Venture 2026** với chủ đề *\"Open Innovation for a Resilient and Sustainable Financial System in Vietnam\"* (Đổi mới Mở vì một Hệ thống Tài chính Tự cường và Bền vững tại Việt Nam), bản đề xuất này giới thiệu **MuleHunter AI** — lõi Trí tuệ Nhân tạo Đồ thị (Graph Neural Network - GNN) liên ngân hàng thời gian thực, được thiết kế nhằm nâng cấp hệ thống phòng chống gian lận **SIMO** của Ngân hàng Nhà nước Việt Nam (NHNN) thành một hệ thống ngắt mạch cấu trúc tự động (**'SIMO 2.0'**). Giải pháp giải quyết trực diện bài toán của **Pillar 5: Trust Architecture & Financial Integrity** (Trụ cột chính) kết hợp giao thoa với **Pillar 2: Financial Infrastructure & Ecosystem Interoperability** (Trụ cột phụ), được trình bày xuyên suốt qua 6 phần cốt lõi theo đúng quy chuẩn của Ban Tổ chức dưới đây.")

    # ================= 2. PROPOSAL STRUCTURE =================
    add_guideline_heading_1(doc, "2. Proposal Structure (Cấu trúc Đề xuất Dự án)")
    
    add_guideline_heading_2(doc, "2.1. Executive Summary (Tóm tắt Dự án)")
    add_body_p(doc, "Tính đến giữa năm 2026, quá trình chuyển đổi số ngành tài chính Việt Nam đã đạt những cột mốc lịch sử: gần **89% công dân từ 15 tuổi trở lên sở hữu tài khoản thanh toán**, hơn **95% giao dịch ngân hàng được xử lý qua kênh số**, và thanh toán không tiền mặt đạt **hơn 15 tỷ giao dịch chỉ trong 6 tháng đầu năm 2026** (tăng **34,28%** so với cùng kỳ năm 2025, đạt giá trị gấp **28 lần GDP**). Tuy nhiên, tốc độ thanh toán tức thời (NAPAS247, VietQR) cũng làm gia tăng rủi ro lừa đảo trực tuyến quy mô công nghiệp. Dù Ngân hàng Nhà nước (NHNN) đã đưa vào vận hành hệ thống **SIMO (Hệ thống thông tin hỗ trợ quản lý, giám sát và phòng ngừa rủi ro gian lận trong hoạt động thanh toán)** — phát đi **4,9 triệu lượt cảnh báo**, giúp **1,6 triệu khách hàng** tạm dừng giao dịch và bảo vệ **5.500 tỷ VNĐ** tính đến tháng 7/2026 — chính con số thống kê này lại phơi bày một lỗ hổng nghiêm trọng: **hơn 3,3 triệu lượt cảnh báo (67,3%) đã không thể ngăn khách hàng chuyển tiền**, đồng thời cơ chế danh sách đen tĩnh hoàn toàn 'mù' trước các 'tài khoản rác mới mở' (Fresh Mules) và thủ đoạn chia nhỏ dòng tiền dưới 10 triệu VNĐ (Smurfing).")
    add_body_p(doc, "Bám sát **Pillar 5 (Trust Architecture & Financial Integrity)** và giao thoa cùng **Pillar 2 (Financial Infrastructure & Ecosystem Interoperability)**, đội **TCQL** đề xuất **MuleHunter AI** — lớp Trí tuệ Nhân tạo Đồ thị (GNN) liên ngân hàng thời gian thực, nâng cấp SIMO từ *tra cứu danh sách đen thụ động* thành *hệ thống ngắt mạch cấu trúc chủ động ('SIMO 2.0')*. Kết hợp **Đồ thị Động trên RAM (Memgraph)** và mô hình **GraphSAGE/APAN** tách rời, MuleHunter AI phát hiện các hình thái rửa tiền đa bước (**Fan-out, Fan-in, Circular Routing**) xuyên ngân hàng trong **dưới 500 mili-giây**. Tận dụng **Open API (Thông tư 64/2024/TT-NHNN)**, định danh **VNeID/Đề án 06** và **Học liên kết (Federated Learning)** tuân thủ **Nghị định 13/2023/NĐ-CP**, giải pháp tự động ép quét sinh trắc học bổ sung hoặc phong tỏa tạm thời dòng tiền bẩn ngay lập tức — bảo vệ hàng chục nghìn tỷ đồng và củng cố niềm tin vào hệ thống tài chính số Việt Nam.")

    add_guideline_heading_2(doc, "2.2. Problem Statement & Market Pain (Đặt vấn đề & Nỗi đau Thị trường)")
    add_guideline_subheading(doc, "Vấn đề Cụ thể & Tính Cấp thiết trong Hệ thống Tài chính Việt Nam")
    add_body_p(doc, "Khi Việt Nam hướng tới mục tiêu giá trị thanh toán không tiền mặt đạt **30 lần GDP vào năm 2030** (Vietnam+, 2026), hạ tầng thanh toán tức thời liên ngân hàng đang bị các tổ chức tội phạm xuyên biên giới lợi dụng để tẩu tán tiền lừa đảo qua mạng lưới **Tài khoản Rác (Money Mule accounts)** (tài khoản thuê, mua hoặc công ty vỏ bọc). Ngay khi nạn nhân bấm chuyển tiền, các bot tự động chỉ mất **30 đến 120 giây** để phân tán tiền qua 3–4 tầng ngân hàng khác nhau trước khi rút ra tiền mã hóa (USDT P2P).")

    add_guideline_subheading(doc, "4 Nguyên nhân Gốc rễ & Hạn chế của Giải pháp Hiện tại (Dẫn chứng từ Đề bài)")
    add_bullet_p(doc, "**1. Khoảng trống chuyển đổi 67,3% của Hệ thống SIMO hiện tại:** Theo số liệu của Vụ Thanh toán NHNN (Nguoi Quan Sat, 2026; VietNamNet, 2026b), tính đến cuối tháng 7/2026, SIMO đã phát ra **4,9 triệu cảnh báo**, nhưng chỉ có **1,6 triệu giao dịch được dừng lại**. Tức là **3,3 triệu giao dịch (67,3%) vẫn tiếp tục chuyển tiền dù đã có cảnh báo đỏ** — bởi SIMO hiện chỉ là *popup khuyến cáo*, trong khi nạn nhân bị thao túng tâm lý (Deepfake giả danh công an, viện kiểm sát đe dọa) vẫn bị ép bấm 'Tiếp tục'.")
    add_bullet_p(doc, "**2. Độ trễ Hậu kiểm & Điểm mù 'Tài khoản rác mới mở' (Cold-Start Blindness):** Một tài khoản chỉ bị đưa vào danh sách SIMO *sau khi* đã có nạn nhân bị lừa và trình báo. Tội phạm dễ dàng vô hiệu hóa SIMO bằng cách liên tục thu mua các tài khoản sinh viên/công nhân mới mở ('Fresh Mules') chưa từng có tiền án trên hệ thống.")
    add_bullet_p(doc, "**3. Thủ đoạn 'Smurfing < 10 triệu VNĐ' lách Quyết định 2345/QĐ-NHNN:** Để né quy định bắt buộc quét khuôn mặt khi chuyển >10 triệu VNĐ/lần hoặc >20 triệu VNĐ/ngày, tội phạm dùng script tự động chia nhỏ 150 triệu VNĐ thành **16 lệnh chuyển 9,3 triệu VNĐ đồng thời** sang 16 tài khoản rác ở các ngân hàng khác nhau.")
    add_bullet_p(doc, "**4. Sự phân mảnh dữ liệu giữa các Ngân hàng (Nỗi đau của Pillar 2):** Các hệ thống AML truyền thống (SAS, Oracle Mantas) chỉ nhìn thấy giao dịch nằm trong nội bộ 1 ngân hàng. Ngân hàng A hoàn toàn không biết khoản tiền vừa chuyển sang Ngân hàng B đã bị xé lẻ đi 10 ngân hàng khác trong 15 giây tiếp theo.")

    prob_rows_vi = [
        ["Cơ chế cốt lõi", "Quy tắc đơn lẻ nội bộ 1 ngân hàng", "Tra cứu danh sách đen (Blacklist) tĩnh", "Mù trước cấu trúc mạng lưới đa ngân hàng"],
        ["Bắt tài khoản rác mới", "Thất bại (Chưa có lịch sử xấu)", "Thất bại (Chưa bị nạn nhân tố cáo)", "Tài khoản rác Zero-day tẩu tán tiền trót lọt"],
        ["Hành động can thiệp", "Kiểm tra hậu kiểm cuối ngày (Batch)", "Chỉ hiện popup (**67,3% vẫn chuyển**)", "Nạn nhân bị thao túng tâm lý vẫn mất tiền"],
        ["Tỷ lệ Báo động giả", "Cực cao (90% – 95%)", "Bỏ lọt tội phạm mới (False Negative cao)", "Quá tải nhân sự thẩm định tuân thủ"]
    ]
    add_formatted_table(doc, ["Tiêu chí đối chiếu", "Hệ thống AML Ngân hàng Cũ", "Hệ thống SIMO Hiện tại (1.0)", "Khoảng trống Thị trường chưa được giải quyết"], prob_rows_vi)

    add_guideline_heading_2(doc, "2.3. Solution Architecture & FinTech Integration (Kiến trúc Giải pháp & Tích hợp FinTech)")
    add_guideline_subheading(doc, "Giải pháp Đề xuất & 4 Tính năng Đột phá")
    add_body_p(doc, "Lấy cảm hứng từ các hình mẫu quốc tế được Ban tổ chức nêu trong Pillar 5 và Pillar 2 — cụ thể là **Visa AI-Powered Fraud Detection**, **Singpass/COSMIC (Singapore)** và **PayNow/Pix** — **MuleHunter AI** đóng vai trò là lớp trí tuệ đồ thị liên thông tích hợp thẳng vào **NAPAS247 và SIMO**:")
    add_bullet_p(doc, "**1. Phát hiện Hình thái Tài khoản Rác Zero-Day (Topological Detection):** Không cần đợi tài khoản có tên trong danh sách đen, hệ thống bắt trực tiếp hành vi cấu trúc đồ thị: *Fan-Out (Chia nhỏ tiền <10 triệu)*, *Fan-In (Gom tiền về công ty ma)*, *Circular Routing (Vòng tròn A -> B -> C -> A)*, và *Pass-Through Velocity* (tiền dừng lại <60 giây, số dư cuối ngày ~0).")
    add_bullet_p(doc, "**2. Kích hoạt Sinh trắc học Động (Dynamic Step-Up Biometrics — Bịt lỗ hổng Smurfing):** Khi một giao dịch 9,5 triệu VNĐ có điểm rủi ro đồ thị trung bình-cao (**Mule Risk Score 0,60 – 0,85**), MuleHunter AI lập tức ghi đè ngưỡng tĩnh và **ép ứng dụng ngân hàng kích hoạt quét khuôn mặt Liveness (Quyết định 2345) + đối soát VNeID**, cắt đứt kịch bản thao túng tâm lý hoặc bot tự động.")
    add_bullet_p(doc, "**3. Cầu dao Ngắt mạch Tự động 15 Phút (Automated Circuit Breaker — Bịt lỗ hổng 67,3% của SIMO):** Khi **Mule Risk Score > 0,85**, hệ thống chuyển từ *khuyên bảo* sang *chặn chủ động*: phát lệnh `BLOCK_AND_HOLD` đóng băng tạm thời việc tẩu tán tiền sang bước tiếp theo trong 15 phút và cảnh báo khẩn cấp cho ngân hàng.")
    add_bullet_p(doc, "**4. Học liên kết Đồ thị Bảo mật (Federated Graph Learning):** Các ngân hàng cùng huấn luyện mô hình GNN trên dữ liệu nội bộ và chỉ gửi tham số toán học (`FedAvg Gradients`) về trung tâm, bảo mật tuyệt đối dữ liệu khách hàng.")

    add_guideline_subheading(doc, "Luồng Vận hành & Sơ đồ Kiến trúc Tổng thể (End-to-End System Topology)")
    workflow_diagram_vi = (
        "[Khách hàng bấm Chuyển tiền] ──> [Cổng NAPAS247 / VietQR] ──> (Kafka Stream: Salted Hash ID, Số tiền, Time)\n"
        "                                                                                │\n"
        "┌───────────────────────────────────────────────────────────────────────────────┴──────────────────────────┐\n"
        "│ LÕI TRÍ TUỆ ĐỒ THỊ MULEHUNTER AI — 'SIMO 2.0' (Tổng độ trễ cam kết SLA < 500ms)                          │\n"
        "│  • TẦNG 1 FAST PATH (<50ms): Memgraph C++ In-Memory (Lọc chu trình 3-Hop, Đột biến bậc nút & Rút lõi)    │\n"
        "│  • TẦNG 2 DEEP GNN PATH (<300ms): Trích xuất đồ thị con 2-Hop + Mô hình APAN/GraphSAGE trên ONNX Runtime │\n"
        "└───────────────────────────────────────────────────────────────────────────────┬──────────────────────────┘\n"
        "                                                                                ▼\n"
        "   ┌──────────────────────────────────────────┬─────────────────────────────────┴──────────────────────────┐\n"
        "   ▼ (Score < 0,60: ~90% Giao dịch)           ▼ (Score 0,60 - 0,85)                                        ▼ (Score > 0,85)\n"
        "[CHO PHÉP THANH TOÁN TỨC THÌ]        [ÉP QUÉT SINH TRẮC HỌC ĐỘNG]                              [NGẮT MẠCH TỰ ĐỘNG (15 PHÚT)]\n"
        "(Xử lý siêu tốc < 30ms)              (Kích hoạt QĐ 2345 + Đối soát VNeID)                      (Tạm giữ tiền + Báo SIMO & A05)"
    )
    add_code_box(doc, workflow_diagram_vi)

    add_guideline_subheading(doc, "Công nghệ Cốt lõi, Open Innovation & Giải pháp Vượt Rào cản")
    add_bullet_p(doc, "**Kiến trúc 2 tầng chuẩn quốc tế:** Kế thừa thuật toán **APAN (Ant Group / Alipay - ACM SIGMOD 2021)** và chuẩn SLA 100ms của **TigerGraph / Visa**, kết hợp **Apache Kafka**, **Memgraph C++**, **PyTorch Geometric (GraphSAGE & CARE-GNN)** và **ONNX Runtime**.")
    add_bullet_p(doc, "**Đổi mới Mở (Open Innovation):** Vận hành trên chuẩn **Open API (Thông tư 64/2024/TT-NHNN)**, thư viện **Flower (`flwr`)** cho Federated Learning, và **API Đề án 06 (C06/VNeID)** (tương đương *Singpass*) để xác thực nhân thân chủ tài khoản.")
    add_bullet_p(doc, "**Giải quyết Rào cản Pháp lý (Nghị định 13/2023/NĐ-CP) & Độ trễ:** Mã hóa một chiều số tài khoản bằng **Salted SHA-256 Hashing**; không chia sẻ dữ liệu gốc giữa các ngân hàng. Tách rời tính toán đồ thị chạy nền bất đồng bộ giúp giữ độ trễ P99 < 400ms.")

    add_guideline_heading_2(doc, "2.4. Market Size & Competitive Analysis (Quy mô Thị trường & Phân tích Cạnh tranh)")
    add_guideline_subheading(doc, "Target Market and Customer Segmentation (Khách hàng Mục tiêu)")
    add_bullet_p(doc, "**Khách hàng Mục tiêu (B2B / B2G):** (1) **Ngân hàng Nhà nước & NAPAS** (tích hợp nâng cấp SIMO 2.0); (2) **46 Ngân hàng Thương mại & 50+ Ví điện tử** (Vietcombank, BIDV, VietinBank, MB, Techcombank, MoMo, VNPay, ZaloPay).")
    
    add_guideline_subheading(doc, "Market Sizing and Demand (Quy mô & Nhu cầu Thị trường)")
    add_bullet_p(doc, "**Quy mô Thị trường (TAM - SAM - SOM):** **TAM (ASEAN RegTech/AML):** **1,4 tỷ USD/năm** (CAGR 18,4%) | **SAM (An ninh & AML Ngành Tài chính VN):** **120 triệu USD/năm** | **SOM (3 năm đầu - SIMO + 15 Ngân hàng):** **8,5 triệu USD/năm (~210 tỷ VNĐ/năm)**.")
    
    add_guideline_subheading(doc, "Revenue Model (Mô hình Doanh thu)")
    add_bullet_p(doc, "**Mô hình Doanh thu (Biên lợi nhuận gộp >75%):** (1) **Phí bản quyền năm ($60.000 – $150.000/năm/ngân hàng)**; (2) **Phí vi mô theo lượt quét API (5 VNĐ / $0,0002 mỗi giao dịch rủi ro cao)**; (3) **Gói tự động hóa báo cáo STR & trích xuất đồ thị pháp chứng**.")

    add_guideline_subheading(doc, "Competitive Landscape (Bức tranh Cạnh tranh)")
    comp_rows_vi = [
        ["Phạm vi Giám sát", "Đóng kín trong 1 ngân hàng", "Đơn lẻ từng tổ chức", "Cơ sở dữ liệu quốc gia", "**Đồ thị Động Liên ngân hàng Quốc gia**"],
        ["Bắt tài khoản rác mới", "Luật tĩnh (Chậm trễ)", "Phân tích thực thể mạng lưới", "Chỉ tra cứu Blacklist cũ", "**Chủ động bắt hình thái Zero-Day**"],
        ["Cơ chế Can thiệp", "Hậu kiểm cuối ngày (Batch)", "Độ trễ 1–5 giây", "Khuyến cáo (**67,3% phớt lờ**)", "**<350ms Ép quét mặt & Ngắt mạch**"],
        ["Tuân thủ Luật VN", "Tùy chỉnh đắt đỏ", "Chi phí >1M USD, vướng PII", "Hệ thống nội địa của NHNN", "**Chuẩn Nghị định 13, QĐ 2345 & TT 64**"]
    ]
    add_formatted_table(doc, ["Tiêu chí", "Phần mềm AML Cũ (SAS, Oracle)", "Kỳ lân Quốc tế (Quantexa)", "Hệ thống SIMO Hiện tại (1.0)", "MuleHunter AI ('SIMO 2.0')"], comp_rows_vi)

    add_guideline_heading_2(doc, "2.5. Strategic Contribution & Expected Impact (Đóng góp Chiến lược & Tác động Dự kiến)")
    kpi_rows_vi = [
        ["Tỷ lệ Chặn Thành công Giao dịch Lừa đảo", "**32,7%** (1,6M / 4,9M cảnh báo SIMO)", "**> 85%** (Nhờ Step-Up & Ngắt mạch)", "Tỷ lệ giao dịch rủi ro cao được ngăn chặn kịp thời"],
        ["Độ trễ Phê duyệt Toàn trình", "Nhiều giờ (Batch) / Tra cứu tĩnh", "**< 350 ms (P99 < 500 ms)**", "Đo kiểm telemetry thực tế qua Kafka / Locust"],
        ["Tỷ lệ Phát hiện Tài khoản Rác Mới (Recall)", "< 15% (Chưa có trong SIMO)", "**> 88% (AUC-ROC > 0,93)**", "Kiểm thử trên bộ dữ liệu IBM AML & luồng Pilot"],
        ["Tỷ lệ Cảnh báo Giả (False Positive)", "90% – 95% (Hệ thống Rule-based)", "**< 15% (Giảm hơn 70%)**", "Đánh giá Precision@K từ chuyên viên tuân thủ"]
    ]
    add_formatted_table(doc, ["Chỉ số Đo lường (KPI)", "Thực trạng Hiện nay (Tháng 7/2026)", "Mục tiêu của MuleHunter AI", "Phương pháp Đánh giá"], kpi_rows_vi)

    add_guideline_subheading(doc, "SDG Alignment (Đóng góp vào các Mục tiêu Phát triển Bền vững LHQ):", underline=True)
    add_bullet_p(doc, "**SDG 16 (Hòa bình, Công lý và Thể chế vững mạnh — Mục tiêu 16.4 & 16.a):** Trực tiếp ngăn chặn dòng tiền bất hợp pháp, tội phạm lừa đảo công nghệ cao và rửa tiền xuyên biên giới; cung cấp hồ sơ đồ thị pháp chứng minh bạch cho Ngân hàng Nhà nước và Bộ Công an (A05).")
    add_bullet_p(doc, "**SDG 9 (Công nghiệp, Đổi mới sáng tạo và Hạ tầng — Mục tiêu 9.1):** Nâng cấp hạ tầng tài chính số cốt lõi của quốc gia (SIMO & NAPAS) bằng công nghệ AI đồ thị phân tán và chuẩn giao tiếp Open API.")
    add_bullet_p(doc, "**SDG 8 (Việc làm bền vững và Tăng trưởng kinh tế — Mục tiêu 8.10):** Bảo vệ tài sản và vốn lưu động của 89% người dân trưởng thành cùng các hộ kinh doanh/MSME, củng cố niềm tin bền vững vào nền kinh tế không tiền mặt.")

    add_guideline_heading_2(doc, "2.6. Implementation Roadmap & Scalability (Lộ trình Triển khai & Khả năng Mở rộng)")
    add_guideline_subheading(doc, "Implementation Roadmap (Lộ trình Triển khai)")
    roadmap_rows_vi = [
        ["Giai đoạn 1: MVP & Benchmark", "Quý 1/2027", "Huấn luyện GraphSAGE/CARE-GNN trên **IBM AML** & **Elliptic++** (AUC > 0,92); dựng cụm **Memgraph + FastAPI/ONNX** (<350ms SLA).", "Mã nguồn mở (`PyG`, `Memgraph`, `Flower`); Máy chủ GPU thử nghiệm."],
        ["Giai đoạn 2: Sandbox & Federated", "Quý 2/2027", "Tham gia Sandbox NHNN (**Nghị định 94/2025/NĐ-CP**); chạy thử nghiệm mã băm Salted SHA-256 & Federated Learning với **2 ngân hàng Pilot**.", "Phê duyệt Sandbox của NHNN; Kiểm toán an ninh Thông tư 09/2020/TT-NHNN."],
        ["Giai đoạn 3: Pilot SIMO 2.0", "Quý 3/2027", "Tích hợp API hai chiều với **SIMO** và kích hoạt **Sinh trắc học động Quyết định 2345**; triển khai **Cytoscape.js + XAI Dashboard**.", "Cổng API thử nghiệm NAPAS / SIMO; API Đề án 06 (C06/VNeID)."],
        ["Giai đoạn 4: Mở rộng Toàn quốc", "Quý 4/2027", "Mở rộng lên **15+ ngân hàng thương mại** và ví điện tử lớn (MoMo, VNPay, ZaloPay) ở mức chịu tải **50.000+ TPS**; tự động hóa báo cáo STR.", "Hợp đồng SLA thương mại; Hạ tầng Data Center chuẩn Tier-3 nội địa."]
    ]
    add_formatted_table(doc, ["Giai đoạn Triển khai", "Thời gian", "Cột mốc Kỹ thuật & Kiểm chứng Thực tế", "Điều kiện & Đối tác Phụ thuộc"], roadmap_rows_vi)

    add_guideline_subheading(doc, "Scalability and Infrastructure (Khả năng Mở rộng & Hạ tầng)")
    add_bullet_p(doc, "**Chi phí vận hành tăng trưởng dưới tuyến tính (O(k^d) Complexity):** Nhờ lấy mẫu đồ thị con cục bộ 2 bước (**2-hop Ego-Graph Sampling**), chi phí tính toán chỉ phụ thuộc vào số kết nối lân cận k chứ không phình to theo tổng số tài khoản quốc gia N.")
    add_bullet_p(doc, "**Xuất khẩu sang khu vực ASEAN:** Kiến trúc hoàn toàn tương thích để mở rộng sang các hệ thống thanh toán tức thời trong khu vực như **PayNow/COSMIC (Singapore)**, **PromptPay (Thái Lan)** và **InstaPay (Philippines)**.")

    doc.add_page_break()
    add_guideline_heading_2(doc, "2.7. References (Tài liệu Tham khảo)")
    for ref in [
        "1. Bank for International Settlements (BIS). (2023). Project Aurora: Collaborative analysis in Anti-Money Laundering (AML). https://www.bis.org/publ/othp64.htm",
        "2. Dou, Y., et al. (2020). Enhancing Graph Neural Network-based Fraud Detectors against Camouflaged Fraudsters (CARE-GNN). ACM CIKM '20. https://arxiv.org/abs/2008.08692",
        "3. Chính phủ Việt Nam. (2023). Nghị định 13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân.",
        "4. Chính phủ Việt Nam. (2025). Nghị định 94/2025/NĐ-CP về Cơ chế thử nghiệm có kiểm soát (Regulatory Sandbox) trong lĩnh vực ngân hàng.",
        "5. Nguoi Quan Sat. (2026, August). Phó vụ trưởng Vụ Thanh toán NHNN: 1,6 triệu lượt khách hàng đã kịp dừng giao dịch, bảo vệ 5.500 tỷ đồng.",
        "6. Saigon Giai Phong. (2026). Cashless payment value reaches 28 times GDP in first half of 2026.",
        "7. Ngân hàng Nhà nước Việt Nam (SBV). (2023). Quyết định 2345/QĐ-NHNN về giải pháp an toàn, bảo mật trong thanh toán trực tuyến.",
        "8. Ngân hàng Nhà nước Việt Nam (SBV). (2024). Thông tư 64/2024/TT-NHNN quy định về triển khai Giao diện lập trình ứng dụng mở (Open API).",
        "9. VietNamNet. (2026a & 2026b). Vietnam bank alerts stop 1.6 million suspected scam transactions / blocks $177M in suspicious transfers.",
        "10. Visa Inc. (2025). Visa AI-Powered Fraud Detection & Protect Solutions.",
        "11. VnEconomy. (2026, August 12). Vietnam’s cashless payment transactions rise 34.3% in first half.",
        "12. Wang, X., et al. (2021). APAN: Asynchronous Propagation Attention Network for Real-time Temporal Graph Embedding (Ant Group). ACM SIGMOD '21.",
        "13. Weber, M., et al. (2019). Anti-Money Laundering in Bitcoin: Experimenting with GCNs for Financial Forensics. MIT-IBM Watson AI Lab."
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        run = p.add_run(ref)
        run.font.name = 'Arial'
        run.font.size = Pt(10)
        run.font.color.rgb = RGB_DARK_TEXT

    add_guideline_heading_2(doc, "2.8. Appendix (Optional - Phụ lục Bổ trợ)")
    add_guideline_subheading(doc, "Phụ lục A: 3 Hình thái Đồ thị Rửa tiền Điển hình mà MuleHunter AI Bắt giữ")
    topo_box_vi = (
        "1. FAN-OUT (Chia nhỏ < 10M VNĐ)      2. FAN-IN (Gom về Công ty Ma)        3. CIRCULAR ROUTING (Xoay vòng)\n"
        "       ┌─> [Mule 1] (9,5M)                [Mule 1] ─┐                        [TK A] ──> [TK B]\n"
        "[Nạn nhân]─┼─> [Mule 2] (9,8M)            [Mule 2] ─┼─> [Công ty Vỏ bọc]       ▲          │\n"
        "       └─> [Mule 3] (9,2M)                [Mule 3] ─┘   (Đẩy ra Crypto P2P)  [TK D] <── [TK C]"
    )
    add_code_box(doc, topo_box_vi)

    add_guideline_subheading(doc, "Phụ lục B: Bộ dữ liệu Kiểm chứng & Thư viện Mã nguồn mở")
    add_bullet_p(doc, "**Bộ dữ liệu chuẩn (Benchmark Datasets):** IBM Transactions for Anti-Money Laundering (https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml) | Elliptic++ Dataset (https://github.com/git-disl/EllipticPlusPlus)")
    add_bullet_p(doc, "**Thư viện cốt lõi (Core Frameworks):** PyTorch Geometric (https://github.com/pyg-team/pytorch_geometric) | PyGOD Outlier Detection (https://github.com/pygod-team/pygod) | Memgraph Streaming Graph DB (https://github.com/memgraph/memgraph) | Flower Federated Learning (https://github.com/adap/flower)")

    try:
        doc.save(filepath)
        print(f"Saved Vietnamese DOCX: {filepath}")
    except PermissionError:
        alt_path = filepath.replace(".docx", "_Updated.docx")
        doc.save(alt_path)
        print(f"File {filepath} is open in Word; saved to: {alt_path}")


if __name__ == "__main__":
    build_english_proposal(r"d:\Fintech\TCQL_Round_1_Submission.docx")
    build_vietnamese_proposal(r"d:\Fintech\TCQL_Round_1_Submission_VI.docx")
