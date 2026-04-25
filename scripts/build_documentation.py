"""Generate the final project documentation PDF.

Meets the assignment's PDF submission requirements:
  - System architecture diagram
  - Implementation details
  - Performance metrics
  - Challenges and solutions
  - Future improvements
  - Ethical considerations
"""
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, Flowable,
)
from reportlab.graphics.shapes import (
    Drawing, Rect, String, Line, Polygon,
)
from reportlab.graphics import renderPDF

# ---------------- colors ----------------
INK = colors.HexColor("#0E1B2C")
INK2 = colors.HexColor("#2A3E52")
INK3 = colors.HexColor("#5A6D80")
PAPER = colors.HexColor("#F7F2E9")
PAPER2 = colors.HexColor("#EDE6D8")
RULE = colors.HexColor("#D8CDB8")
ACCENT = colors.HexColor("#8B1538")
MAJOR = colors.HexColor("#8B1538")
MODERATE = colors.HexColor("#B86B17")
MINOR = colors.HexColor("#5A6D80")

# ---------------- styles ----------------
styles = getSampleStyleSheet()

H1 = ParagraphStyle(
    "H1", parent=styles["Heading1"],
    fontName="Times-Roman", fontSize=28, leading=32,
    textColor=INK, spaceAfter=6, spaceBefore=18, alignment=TA_LEFT,
)
H2 = ParagraphStyle(
    "H2", parent=styles["Heading2"],
    fontName="Times-Roman", fontSize=18, leading=22,
    textColor=INK, spaceAfter=10, spaceBefore=22, alignment=TA_LEFT,
)
H3 = ParagraphStyle(
    "H3", parent=styles["Heading3"],
    fontName="Times-Bold", fontSize=13, leading=18,
    textColor=INK, spaceAfter=4, spaceBefore=14, alignment=TA_LEFT,
)
KICKER = ParagraphStyle(
    "Kicker", parent=styles["Normal"],
    fontName="Courier-Bold", fontSize=8, leading=11,
    textColor=ACCENT, spaceAfter=4, spaceBefore=8, alignment=TA_LEFT,
)
BODY = ParagraphStyle(
    "Body", parent=styles["Normal"],
    fontName="Times-Roman", fontSize=11, leading=16,
    textColor=INK2, spaceAfter=10, alignment=TA_JUSTIFY, firstLineIndent=0,
)
LEDE = ParagraphStyle(
    "Lede", parent=BODY,
    fontSize=13, leading=19, textColor=INK, alignment=TA_LEFT, spaceAfter=14,
)
CAPTION = ParagraphStyle(
    "Caption", parent=styles["Normal"],
    fontName="Times-Italic", fontSize=9, leading=12,
    textColor=INK3, spaceAfter=12, alignment=TA_CENTER,
)
PULLQUOTE = ParagraphStyle(
    "Pull", parent=styles["Normal"],
    fontName="Times-Italic", fontSize=13, leading=18,
    textColor=INK, leftIndent=20, rightIndent=20,
    borderPadding=(12, 14, 12, 14),
    spaceBefore=10, spaceAfter=16, alignment=TA_LEFT,
)
CODE = ParagraphStyle(
    "Code", parent=styles["Normal"],
    fontName="Courier", fontSize=9, leading=13, textColor=INK,
    leftIndent=14, rightIndent=14,
    spaceBefore=6, spaceAfter=12,
)
MONO_SMALL = ParagraphStyle(
    "MonoSmall", parent=styles["Normal"],
    fontName="Courier", fontSize=9, leading=12, textColor=INK3,
)

# ---------------- architecture diagram ----------------

def architecture_diagram() -> Drawing:
    d = Drawing(480, 320)

    def box(x, y, w, h, title, sub="", sub2="", fill=PAPER2, stroke=INK,
            title_color=INK, sub_color=INK3):
        d.add(Rect(x, y, w, h, fillColor=fill, strokeColor=stroke, strokeWidth=0.8))
        d.add(String(x + w / 2, y + h - 14, title,
                     fontName="Times-Bold", fontSize=10, textAnchor="middle", fillColor=title_color))
        if sub:
            d.add(String(x + w / 2, y + h - 28, sub,
                         fontName="Courier", fontSize=7.2, textAnchor="middle", fillColor=sub_color))
        if sub2:
            d.add(String(x + w / 2, y + h - 40, sub2,
                         fontName="Courier", fontSize=7.2, textAnchor="middle", fillColor=sub_color))

    def arrow(x1, y1, x2, y2, dashed=False):
        kwargs = {"strokeColor": INK, "strokeWidth": 0.8}
        if dashed:
            kwargs["strokeDashArray"] = [3, 2]
        d.add(Line(x1, y1, x2, y2, **kwargs))
        ah = 4
        # approximate arrowhead by computing direction
        import math
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy) or 1
        ux, uy = dx / ln, dy / ln
        px, py = -uy, ux  # perpendicular
        p1 = (x2 - ah * ux + ah * 0.5 * px, y2 - ah * uy + ah * 0.5 * py)
        p2 = (x2 - ah * ux - ah * 0.5 * px, y2 - ah * uy - ah * 0.5 * py)
        d.add(Polygon([x2, y2, p1[0], p1[1], p2[0], p2[1]],
                      fillColor=INK, strokeColor=INK))

    # -------- left column: input + 3 deterministic stages --------
    box(30, 274, 140, 34, "User input", "2–12 medications", fill=PAPER)
    arrow(100, 274, 100, 254)

    box(30, 212, 140, 42, "① Normalizer", "RxNorm + DrugBank",
        "fuzzy match · RXCUI")
    arrow(100, 212, 100, 192)

    box(30, 150, 140, 42, "② Planner", "combinations(drugs, 2)",
        "deterministic")
    arrow(100, 150, 100, 130)

    box(30, 72, 140, 58, "③ Retriever", "exact-pair lookup",
        "no_data_pairs surfaced", sub_color=ACCENT)

    # -------- middle column: knowledge base --------
    d.add(Rect(200, 60, 140, 250, fillColor=PAPER, strokeColor=ACCENT, strokeWidth=0.8))
    d.add(String(270, 295, "KNOWLEDGE BASE",
                 fontName="Times-Bold", fontSize=8.5, textAnchor="middle", fillColor=ACCENT))
    d.add(Line(210, 286, 330, 286, strokeColor=ACCENT, strokeWidth=0.4))

    sources = [
        ("TWOSIDES", "interactions / PRR"),
        ("DrugBank", "metadata · mechanisms"),
        ("SIDER", "side effects"),
        ("RxNorm + WebMD", "norm. · reviews"),
    ]
    for i, (name, desc) in enumerate(sources):
        y = 254 - i * 48
        d.add(Rect(210, y, 120, 38, fillColor=PAPER2, strokeColor=INK2, strokeWidth=0.4))
        d.add(String(270, y + 22, name,
                     fontName="Times-Bold", fontSize=9, textAnchor="middle", fillColor=INK))
        d.add(String(270, y + 9, desc,
                     fontName="Courier", fontSize=7, textAnchor="middle", fillColor=INK3))

    # Retriever → KB (dashed)
    arrow(172, 100, 198, 100, dashed=True)

    # -------- right column: generator + output --------
    box(370, 200, 90, 58, "④ Generator", "LLM w/ strict prompt",
        "[SOURCE:ID] per claim",
        fill=PAPER2, sub_color=ACCENT)
    # KB → Generator
    arrow(340, 200, 370, 220)

    arrow(415, 200, 415, 166)

    d.add(Rect(370, 108, 90, 58, fillColor=PAPER, strokeColor=ACCENT, strokeWidth=1.2))
    d.add(String(415, 148, "Clinical report",
                 fontName="Times-Bold", fontSize=10, textAnchor="middle", fillColor=ACCENT))
    d.add(String(415, 134, "severity-sorted",
                 fontName="Courier", fontSize=7, textAnchor="middle", fillColor=INK3))
    d.add(String(415, 122, "with citations",
                 fontName="Courier", fontSize=7, textAnchor="middle", fillColor=INK3))

    return d


# ---------------- page template with running head ----------------

def on_page(canvas, doc):
    canvas.saveState()
    w, h = LETTER
    # Running head rule
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(0.75 * inch, h - 0.55 * inch, w - 0.75 * inch, h - 0.55 * inch)
    # Running head text
    canvas.setFont("Courier", 8)
    canvas.setFillColor(INK3)
    canvas.drawString(0.75 * inch, h - 0.42 * inch,
                      "PHARMGUARD AI · FINAL PROJECT DOCUMENTATION")
    canvas.drawRightString(w - 0.75 * inch, h - 0.42 * inch,
                           f"PAGE {doc.page:02d}")
    # Footer
    canvas.setFont("Courier", 7.5)
    canvas.setFillColor(INK3)
    canvas.drawCentredString(w / 2, 0.45 * inch,
                             "Shwetanshu Subhash · NUID 0012034124 · Gen-AI Discovery · Spring 2026")
    canvas.restoreState()


# ---------------- build ----------------

def build(out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(out_path), pagesize=LETTER,
        leftMargin=0.95 * inch, rightMargin=0.95 * inch,
        topMargin=0.85 * inch, bottomMargin=0.75 * inch,
        title="PharmGuard AI — Final Project Documentation",
        author="Shwetanshu Subhash",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=on_page)])

    story = []
    # ============ cover page ============
    story.append(Spacer(1, 1.4 * inch))
    story.append(Paragraph(
        '<font color="#8B1538">◆</font>  '
        '<font face="Courier-Bold" size="9" color="#8B1538">'
        'FINAL PROJECT DOCUMENTATION</font>', BODY))
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph(
        "PharmGuard <i>AI</i>",
        ParagraphStyle("cover", fontName="Times-Roman", fontSize=56,
                       leading=60, textColor=INK, alignment=TA_LEFT)))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph(
        '<i>An agentic RAG system for grounded drug-interaction detection.</i>',
        ParagraphStyle("coversub", fontName="Times-Italic", fontSize=18,
                       leading=24, textColor=INK2, alignment=TA_LEFT)))

    story.append(Spacer(1, 1.5 * inch))
    meta_tbl = Table([
        ["AUTHOR", "Shwetanshu Subhash"],
        ["NUID", "0012034124"],
        ["COURSE", "Generative AI Discovery"],
        ["SEMESTER", "Spring 2026"],
        ["DATE", "April 2026"],
    ], colWidths=[1.3 * inch, 4.0 * inch])
    meta_tbl.setStyle(TableStyle([
        ("FONT", (0, 0), (0, -1), "Courier-Bold", 8.5),
        ("FONT", (1, 0), (1, -1), "Times-Roman", 11),
        ("TEXTCOLOR", (0, 0), (0, -1), INK3),
        ("TEXTCOLOR", (1, 0), (1, -1), INK),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LINEABOVE", (0, 0), (-1, 0), 0.6, INK),
        ("LINEBELOW", (0, -1), (-1, -1), 0.6, INK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(meta_tbl)

    story.append(PageBreak())

    # ============ abstract ============
    story.append(Paragraph("ABSTRACT", KICKER))
    story.append(Paragraph("A system that knows what it doesn't know.", H1))
    story.append(Spacer(1, 0.12 * inch))

    story.append(Paragraph(
        "PharmGuard AI is an agentic retrieval-augmented generation system that flags "
        "drug-drug interactions in a patient's medication list. Given two to twelve "
        "drug names, it enumerates every unique pairwise combination, retrieves "
        "interaction evidence from TWOSIDES and supporting sources (DrugBank, SIDER, "
        "RxNorm), and generates a severity-tiered clinical report in which every claim "
        "is tied to a specific source record.",
        LEDE))
    story.append(Paragraph(
        "The system is designed around the failure mode base LLMs exhibit in clinical "
        "settings: fluent, partially-correct answers with no audit trail and no explicit "
        "uncertainty. PharmGuard's architecture separates deterministic operations "
        "(pair enumeration, database lookup) from generative operations (report "
        "synthesis) so that the LLM is invoked only where fluent language is the "
        "actual product — never to enumerate, retrieve, or classify severity. Every "
        "output carries mandatory citations and a disclaimer appended by the pipeline, "
        "not by the model.",
        BODY))

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(
        "A system that scores 92% retrieval recall but has a 15% hallucination rate "
        "is not a success. This project defines what silent failure looks like before "
        "it defines what success looks like.",
        ParagraphStyle("pull", parent=PULLQUOTE,
                       leftIndent=0, borderColor=ACCENT,
                       borderWidth=0, borderPadding=0,
                       textColor=INK)))
    # Accent bar trick: use a table to fake a left border
    # (already visually apparent through indentation; move on)

    # ============ 1 problem ============
    story.append(PageBreak())
    story.append(Paragraph("§ 1  ·  THE PROBLEM", KICKER))
    story.append(Paragraph("A base LLM will sound right. That's the danger.", H2))

    story.append(Paragraph(
        "Adverse drug events drive approximately 1.3 million emergency-department "
        "visits and 350,000 hospitalizations in the United States each year (CDC, "
        "2022). The Agency for Healthcare Research and Quality estimates that "
        "in-hospital adverse drug events alone cost $3.5 billion annually. Adults "
        "over 65 take a median of five prescription medications simultaneously; each "
        "additional drug multiplies risk combinatorially rather than additively. Five "
        "drugs produce ten unique pairwise combinations; ten drugs produce forty-five. "
        "A physician with twelve minutes per visit cannot manually cross-reference "
        "forty-five potential interactions against a database of hundreds of thousands "
        "of records.",
        BODY))

    story.append(Paragraph(
        "A base large language model can produce fluent, partially-correct answers "
        "to interaction questions, but it cannot: (1) cite a specific source record "
        "with a traceable ID, (2) guarantee that every pair in an N-drug list was "
        "checked, or (3) distinguish “no known interaction” from “no data available.” "
        "In clinical decision support, the last failure is the most dangerous: a "
        "confident silence is indistinguishable from a confident correct answer.",
        BODY))

    story.append(Paragraph(
        "PharmGuard is engineered specifically around these three gaps.",
        BODY))

    # ============ 2 architecture ============
    story.append(PageBreak())
    story.append(Paragraph("§ 2  ·  SYSTEM ARCHITECTURE", KICKER))
    story.append(Paragraph("Plan, retrieve, generate — in that order.", H2))

    story.append(Paragraph(
        "The pipeline is a four-stage plan-retrieve-generate loop. The first three "
        "stages are deterministic; the LLM is invoked only at stage four, where its "
        "value (fluent clinical prose) is the actual deliverable.",
        BODY))

    story.append(Spacer(1, 0.15 * inch))
    story.append(architecture_diagram())
    story.append(Paragraph(
        "Figure 1 · End-to-end pipeline. Deterministic stages (normalize, plan, retrieve) "
        "produce an evidence bundle consumed by an LLM under a strict citation prompt.",
        CAPTION))

    story.append(Paragraph("Stage 1 — Normalizer.", H3))
    story.append(Paragraph(
        "User input is free-form: brand names, abbreviations, misspellings, mixed case. "
        "The normalizer resolves each entry to a canonical (generic_name, RXCUI, "
        "drugbank_id) triple via exact match against the combined RxNorm and DrugBank "
        "synonym index, with a fuzzy-match fallback (rapidfuzz, threshold 85). "
        "Resolutions below threshold are returned as unresolved entries rather than "
        "being silently dropped — the planner surfaces them in the final report.",
        BODY))

    story.append(Paragraph("Stage 2 — Planner.", H3))
    story.append(Paragraph(
        "The planner deduplicates by canonical generic name (so that <font face='Courier'>"
        "Lipitor + atorvastatin</font> collapses to one drug) and enumerates all unique "
        "unordered pairs via <font face='Courier'>itertools.combinations</font>. No LLM "
        "is used at this stage. Combinatorial enumeration is a closed-form operation "
        "where any probabilistic model is strictly worse than a for-loop.",
        BODY))

    story.append(Paragraph("Stage 3 — Retriever.", H3))
    story.append(Paragraph(
        "The retriever executes the plan against three knowledge sources. For "
        "interactions, it performs an O(1) hash lookup against the processed "
        "TWOSIDES index using a sorted-pair key. For per-drug side effects, it "
        "queries the processed SIDER table. Optionally, it performs vector search "
        "over WebMD patient reviews as unstructured context — never as evidence for "
        "an interaction claim. Pairs with no retrieved records are collected into "
        "a <font face='Courier'>no_data_pairs</font> field that the generator is "
        "required to surface.",
        BODY))

    story.append(Paragraph("Stage 4 — Generator.", H3))
    story.append(Paragraph(
        "The generator synthesizes the final report from the evidence bundle. Its "
        "system prompt enforces three non-negotiable constraints: every clinical "
        "claim must include an inline <font face='Courier'>[SOURCE:RECORD_ID]</font> "
        "citation; no-data pairs must be declared explicitly; and no mechanism or "
        "severity may be introduced that is not present in the retrieved evidence. "
        "A deterministic fallback produces a fully-cited report without any LLM "
        "call — used in tests and as a safety net if the LLM fails.",
        BODY))

    # ============ 3 implementation ============
    story.append(PageBreak())
    story.append(Paragraph("§ 3  ·  IMPLEMENTATION", KICKER))
    story.append(Paragraph("Modular, provider-agnostic, test-covered.", H2))

    story.append(Paragraph(
        "The codebase is approximately 2,300 lines of Python across 27 modules. "
        "Core dependencies are minimal: pandas, numpy, and rapidfuzz for data "
        "handling; chromadb (optional) for vector search; and a unified LLM client "
        "supporting Anthropic, OpenAI, and Gemini under a single "
        "<font face='Courier'>complete(system, messages)</font> API.",
        BODY))

    story.append(Paragraph("Module layout", H3))
    mod_tbl = Table([
        ["src/config.py", "Centralized configuration with env-var overrides"],
        ["src/llm.py", "Unified client (Anthropic / OpenAI / Gemini)"],
        ["src/data/normalizer.py", "RxNorm + DrugBank resolver with fuzzy fallback"],
        ["src/data/loaders.py", "Schema-aware loaders for each public dataset"],
        ["src/data/ingestion.py", "Raw → processed pipeline"],
        ["src/data/storage.py", "Parquet-with-CSV-fallback persistence helper"],
        ["src/retrieval/*", "Structured + vector retrieval modules"],
        ["src/agents/*", "Planner, retriever, generator agents"],
        ["src/pipeline.py", "End-to-end orchestration"],
        ["src/evaluation/*", "Metrics and 48-case test suite"],
        ["app/streamlit_app.py", "Web UI"],
    ], colWidths=[2.1 * inch, 4.1 * inch])
    mod_tbl.setStyle(TableStyle([
        ("FONT", (0, 0), (0, -1), "Courier", 9),
        ("FONT", (1, 0), (1, -1), "Times-Roman", 10),
        ("TEXTCOLOR", (0, 0), (0, -1), ACCENT),
        ("TEXTCOLOR", (1, 0), (1, -1), INK),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, RULE),
        ("LINEABOVE", (0, 0), (-1, 0), 0.6, INK),
        ("LINEBELOW", (0, -1), (-1, -1), 0.6, INK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(mod_tbl)
    story.append(Spacer(1, 0.12 * inch))

    story.append(Paragraph("Retrieval design choice: structured first", H3))
    story.append(Paragraph(
        "For the question “does drug A interact with drug B?”, a hash lookup against "
        "a sorted-pair key strictly dominates vector similarity. Vector search would "
        "return records for <i>similar</i> pairs, which is not what the clinician needs. "
        "Semantic retrieval is therefore reserved for unstructured context — mechanism "
        "prose and patient reviews — and kept out of the evidence path for interaction "
        "claims.",
        BODY))

    story.append(Paragraph("Severity classification", H3))
    story.append(Paragraph(
        "TWOSIDES does not carry native severity labels. Severity tiers (Major, "
        "Moderate, Minor) are derived from the proportional reporting ratio (PRR): "
        "PRR ≥ 10 is Major, ≥ 4 is Moderate, otherwise Minor. This is a deliberate "
        "proxy; the thresholds are documented in the architecture doc and can be "
        "recalibrated against DDInter 2.0 severity labels if cross-validation access "
        "is available.",
        BODY))

    story.append(Paragraph("LLM-provider neutrality", H3))
    story.append(Paragraph(
        "The <font face='Courier'>LLMClient</font> abstracts over three providers. "
        "Auto-detection selects the provider based on which API key is present, "
        "so the rest of the pipeline is entirely vendor-neutral. The default model "
        "for each provider is picked for favorable cost-quality balance; all settings "
        "are overridable via environment variables.",
        BODY))

    # ============ 4 data ============
    story.append(PageBreak())
    story.append(Paragraph("§ 4  ·  DATA SOURCES", KICKER))
    story.append(Paragraph("Narrow by design. Authoritative by default.", H2))

    story.append(Paragraph(
        "PharmGuard's knowledge base is deliberately restricted to peer-reviewed or "
        "government-maintained sources. The system does not ingest Reddit, unvetted "
        "forum content, or general web scrapes. In clinical decision support, the "
        "cost of breadth without rigor is measured in patient harm.",
        BODY))

    ds_tbl = Table([
        ["Dataset", "Authority", "Role"],
        ["TWOSIDES", "Tatonetti Lab / STM 2012",
         "Primary drug-drug interactions; ~4.6M pair records"],
        ["DrugBank 5.x", "University of Alberta",
         "Drug metadata, synonyms, mechanisms"],
        ["SIDER", "EMBL",
         "Per-drug side-effect profiles from FDA labels"],
        ["RxNorm", "NLM / NIH",
         "Brand ↔ generic ↔ RXCUI normalization"],
        ["WebMD Reviews", "Kaggle (CC0)",
         "Patient-experience context (vector-search only)"],
        ["Medicare Part D", "data.gov",
         "Prescribing patterns (analytics, not interactions)"],
    ], colWidths=[1.4 * inch, 1.9 * inch, 2.9 * inch])
    ds_tbl.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, 0), "Courier-Bold", 8),
        ("FONT", (0, 1), (0, -1), "Times-Bold", 10),
        ("FONT", (1, 1), (-1, -1), "Times-Roman", 10),
        ("TEXTCOLOR", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 1), (-1, -1), INK2),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, INK),
        ("LINEBELOW", (0, 1), (-1, -2), 0.2, RULE),
        ("LINEBELOW", (0, -1), (-1, -1), 0.6, INK),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(ds_tbl)
    story.append(Spacer(1, 0.12 * inch))

    story.append(Paragraph("Bias acknowledgment", H3))
    story.append(Paragraph(
        "No dataset is neutral. TWOSIDES is derived primarily from English-language "
        "FDA-supervised reporting, which introduces geographic and regulatory skew "
        "toward US-marketed drugs. SIDER and DrugBank inherit similar biases. The "
        "WebMD review corpus reflects the demographics of English-speaking, digitally "
        "literate users. Every PharmGuard output includes a Coverage Note describing "
        "which databases were queried and what their known limitations are. The "
        "system never claims comprehensiveness; it claims fidelity to its sources "
        "and honesty about what those sources do not cover.",
        BODY))

    # ============ 5 evaluation ============
    story.append(PageBreak())
    story.append(Paragraph("§ 5  ·  EVALUATION", KICKER))
    story.append(Paragraph("Failure defined before success.", H2))

    story.append(Paragraph(
        "The evaluation framework specifies the target failure mode before it "
        "specifies target metrics. The adversarial scenario — the one the pipeline "
        "is built to catch — is the silent-failure case:",
        BODY))

    story.append(Paragraph(
        "A patient inputs six medications. The system returns a cleanly formatted "
        "report listing four interactions with professional-sounding mechanism "
        "descriptions. It looks authoritative. But the system has missed two "
        "critical interactions — one classified as Major severity — and has "
        "fabricated a CYP3A4 inhibition pathway where the actual mechanism is "
        "P-glycoprotein competition. The output is polished, fluent, and dangerous.",
        ParagraphStyle("pull2", parent=PULLQUOTE, leftIndent=16, textColor=INK)))

    story.append(Paragraph("Metrics and targets", H3))
    m_tbl = Table([
        ["Metric", "What it measures", "Target"],
        ["Retrieval Recall", "Fraction of ground-truth pairs surfaced", "≥ 95%"],
        ["Retrieval Precision", "Fraction of retrieved results that are true-positive", "≥ 90%"],
        ["Faithfulness", "Mechanism matches the retrieved source record", "≥ 85%"],
        ["Hallucination Rate", "Clinical claims without a source citation", "≤ 5%"],
        ["Severity Accuracy", "Reported tier matches the source tier", "≥ 90%"],
        ["Completeness Flagging", "No-data pairs explicitly declared", "100%"],
    ], colWidths=[1.7 * inch, 3.3 * inch, 1.1 * inch])
    m_tbl.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, 0), "Courier-Bold", 8),
        ("FONT", (0, 1), (0, -1), "Times-Bold", 10),
        ("FONT", (1, 1), (1, -1), "Times-Roman", 9.5),
        ("FONT", (2, 1), (2, -1), "Courier-Bold", 9),
        ("TEXTCOLOR", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 1), (0, -1), INK),
        ("TEXTCOLOR", (1, 1), (1, -1), INK2),
        ("TEXTCOLOR", (2, 1), (2, -1), ACCENT),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, INK),
        ("LINEBELOW", (0, 1), (-1, -2), 0.2, RULE),
        ("LINEBELOW", (0, -1), (-1, -1), 0.6, INK),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(m_tbl)

    story.append(Spacer(1, 0.12 * inch))
    story.append(Paragraph("Test suite", H3))
    story.append(Paragraph(
        "The evaluation suite contains 48 curated cases across eight clinical "
        "domains (geriatric polypharmacy, classic textbook interactions, mental "
        "health, cardiology, endocrine, infectious disease, pain management, "
        "respiratory). Each case lists 1–12 input drugs spanning generic names, "
        "brand names, and deliberate misspellings. Ground truth for recall and "
        "precision is derived programmatically from whatever interaction table is "
        "loaded — the evaluator is self-consistent across full TWOSIDES, curated "
        "sample, or any intermediate subset.",
        BODY))

    story.append(Paragraph("Smoke-test results on sample data", H3))
    story.append(Paragraph(
        "Against the shipped sample dataset (50 curated interactions across 81 "
        "drug-name entries), the pipeline passes all 16 unit tests and achieves "
        "perfect recall and precision on the 48-case suite. End-to-end latency for "
        "the proposal's canonical 7-drug scenario is approximately 23 milliseconds, "
        "well under the 30-second target. These numbers demonstrate pipeline "
        "correctness on a small index; absolute recall/precision against full "
        "TWOSIDES will be reported once the full index is ingested.",
        BODY))

    # ============ 6 challenges ============
    story.append(PageBreak())
    story.append(Paragraph("§ 6  ·  CHALLENGES & SOLUTIONS", KICKER))
    story.append(Paragraph("What surprised us, and what we did about it.", H2))

    challenges = [
        ("Drug name normalization is messier than it looks.",
         "Users type brand names, abbreviations, and misspellings. Naive exact match "
         "drops 15–20% of valid inputs. Solution: combine RxNorm and DrugBank synonym "
         "tables into a unified index, add a fuzzy-match layer at a calibrated "
         "threshold (85 WRatio), and — critically — surface unresolved entries in "
         "the final report rather than silently dropping them."),
        ("Vector search is tempting but wrong here.",
         "The initial design considered storing interaction records in a vector "
         "database and doing semantic retrieval. This would have been strictly worse: "
         "for exact-pair queries, semantic similarity returns records for similar "
         "pairs, not the pair of interest. Solution: structured hash lookup for "
         "interactions; reserve vector search for unstructured context only."),
        ("Severity classification without native labels.",
         "TWOSIDES provides signal statistics (PRR, reporting frequency), not "
         "severity labels. Solution: derive severity from PRR thresholds as a "
         "documented design choice, and expose the raw statistics in every record "
         "so downstream consumers can recalibrate."),
        ("Base-LLM hallucination risk in generation.",
         "Even with retrieved evidence, the model can paraphrase a mechanism "
         "inaccurately. Solution: prompt-engineered constraints (mandatory inline "
         "citations, explicit no-data declaration, no mechanism introduction beyond "
         "evidence), plus a deterministic fallback that produces a valid cited "
         "report without any LLM call."),
        ("Silent failure in evaluation.",
         "Standard retrieval benchmarks (recall, precision, F1) do not penalize a "
         "fluent-looking report that missed a Major interaction. Solution: add "
         "Faithfulness, Hallucination Rate, and Completeness Flagging as first-class "
         "metrics; define the silent-failure scenario in writing before running "
         "any eval."),
    ]
    for title, body in challenges:
        story.append(Paragraph(title, H3))
        story.append(Paragraph(body, BODY))

    # ============ 7 future ============
    story.append(Paragraph("§ 7  ·  FUTURE IMPROVEMENTS", KICKER))
    story.append(Paragraph("What's next, in order of impact.", H2))

    future = [
        ("Secondary interaction source: DDInter 2.0.",
         "DDInter provides curated severity labels and mechanism prose that TWOSIDES "
         "lacks. Adding DDInter as a secondary source would improve Severity Accuracy "
         "and reduce the need for PRR-based proxies."),
        ("Real-time FAERS queries via OpenFDA.",
         "For drug pairs outside the local index, a live OpenFDA FAERS fallback "
         "would surface adverse-event signals that predate official labeling. The "
         "retriever abstraction already supports this; it needs an OpenFDA client "
         "plus rate-limit handling."),
        ("Clinician-in-the-loop evaluation.",
         "The Faithfulness metric currently uses an LLM-judge with a 20% human audit "
         "target. A prospective evaluation with pharmacist reviewers would harden "
         "the Faithfulness number and surface mechanism-paraphrase errors the "
         "auto-judge misses."),
        ("Dose-aware interaction surfacing.",
         "Many TWOSIDES signals are dose-dependent (e.g., warfarin-NSAID bleeding "
         "is risk-stratified by NSAID dose). Incorporating dose parsing and "
         "dose-conditional retrieval would dramatically improve clinical utility."),
        ("Multilingual support.",
         "TWOSIDES' English-literature skew limits international use. A RxNorm "
         "International (RxNav) integration plus locale-aware normalization would "
         "extend coverage."),
    ]
    for title, body in future:
        story.append(Paragraph(title, H3))
        story.append(Paragraph(body, BODY))

    # ============ 8 ethics ============
    story.append(PageBreak())
    story.append(Paragraph("§ 8  ·  ETHICAL CONSIDERATIONS", KICKER))
    story.append(Paragraph("The system knows what it doesn't know.", H2))

    story.append(Paragraph(
        "Clinical decision support systems carry asymmetric risk: a wrong answer "
        "can cause direct patient harm, while a correct answer confers at best a "
        "marginal improvement over routine practice. PharmGuard's ethical design "
        "reflects this asymmetry through four commitments embedded in the "
        "architecture, not added as disclaimers.",
        BODY))

    story.append(Paragraph("No patient data is stored.", H3))
    story.append(Paragraph(
        "Medication lists are processed in memory only. The web interface is "
        "stateless; there is no persistence layer, no logging of inputs, and no "
        "user identification. The data flow is designed to make accidental PHI "
        "retention impossible rather than merely prohibited.",
        BODY))

    story.append(Paragraph("Source attribution is mandatory.", H3))
    story.append(Paragraph(
        "Every interaction claim cites the source database, record ID, and version. "
        "The answer to “Where did you get this?” is always one click away. This is "
        "not a technical convenience but a safety property: a clinician can "
        "independently verify any claim before acting on it.",
        BODY))

    story.append(Paragraph("Absence of data is a first-class output.", H3))
    story.append(Paragraph(
        "When the retriever returns zero records for a pair, the report explicitly "
        "states “No interaction data available in the queried sources for A + B.” "
        "The pipeline surfaces this via a dedicated <font face='Courier'>"
        "no_data_pairs</font> field that the generator is required to echo. This "
        "prevents the most common failure mode of clinical LLMs: a confident "
        "silence on pairs the model has no evidence for.",
        BODY))

    story.append(Paragraph("Bias is declared, not denied.", H3))
    story.append(Paragraph(
        "TWOSIDES and DrugBank skew toward US-marketed, English-labeled drugs. "
        "SIDER inherits FDA-label bias. PharmGuard outputs a Coverage Note on every "
        "report describing which databases were queried and what their known "
        "limitations are. The system never claims comprehensiveness — it claims "
        "fidelity to its sources.",
        BODY))

    story.append(Paragraph("The system is not a clinician.", H3))
    story.append(Paragraph(
        "Every output carries a disclaimer stating that PharmGuard is decision "
        "support, not medical judgment. The disclaimer is appended by the pipeline "
        "itself, not by the generator — so a prompt-injection attempt cannot remove "
        "it. The safety property is enforced by code, not by the model.",
        BODY))

    # ============ 9 conclusion ============
    story.append(PageBreak())
    story.append(Paragraph("§ 9  ·  CONCLUSION", KICKER))
    story.append(Paragraph("Disciplined scope as its own form of rigor.", H2))

    story.append(Paragraph(
        "PharmGuard promises one thing — drug-interaction detection grounded in "
        "structured evidence — and measures whether that one thing works. The "
        "Minimum Viable Logic is narrow by design: it does not attempt diagnosis, "
        "dosage optimization, or patient monitoring. In a landscape of "
        "overcommitted AI proposals, this discipline is a feature.",
        BODY))

    story.append(Paragraph(
        "The architectural thesis is that certain cognitive labor — enumerating "
        "combinations, looking up records, classifying by thresholded statistics — "
        "is done more safely and more cheaply by deterministic code than by a "
        "probabilistic model. The LLM is reserved for the work where fluent "
        "natural-language synthesis is the actual product. This separation is "
        "what makes auditability possible: every deterministic step leaves a "
        "trace, and every generative claim leaves a citation.",
        BODY))

    story.append(Paragraph(
        "The evaluation framework is self-consistent: ground truth is derived "
        "from whatever interaction table is loaded, so the same metric code "
        "produces meaningful numbers against the sample dataset, the full TWOSIDES "
        "release, or any intermediate subset. Failure modes — specifically, the "
        "silent-failure scenario — are defined in writing before success criteria. "
        "A system that scores 92% recall but 15% hallucination rate does not pass "
        "this project's bar, and the metric suite is engineered to ensure that.",
        BODY))

    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("References", H3))

    refs = [
        "[1] Tatonetti, N.P. et al. Data-Driven Prediction of Drug Effects and Interactions. "
        "<i>Science Translational Medicine</i>, 2012.",
        "[2] Wishart, D.S. et al. DrugBank 5.0: a major update to the DrugBank database for 2018. "
        "<i>Nucleic Acids Research</i>, 2018.",
        "[3] Kuhn, M. et al. The SIDER database of drugs and side effects. "
        "<i>Nucleic Acids Research</i>, 2016.",
        "[4] U.S. National Library of Medicine. RxNorm. https://www.nlm.nih.gov/research/umls/rxnorm/",
        "[5] Centers for Disease Control and Prevention. Medication Safety Program, 2022.",
        "[6] Agency for Healthcare Research and Quality. Adverse Drug Events, 2021.",
        "[7] U.S. Food & Drug Administration. FAERS Adverse Event Reporting System. "
        "https://open.fda.gov/apis/drug/event/",
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle(
            "ref", parent=BODY, fontSize=9.5, leading=13, spaceAfter=6,
            leftIndent=14, firstLineIndent=-14, alignment=TA_LEFT)))

    doc.build(story)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "docs" / "PharmGuard_AI_Documentation.pdf"
    build(out)
    print(f"Wrote: {out}")
