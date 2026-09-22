#!/usr/bin/env python3
"""Build a PI-facing progress report for the core outdoor sensor-box research."""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    LongTable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "pdf"
OUT_PDF = OUT_DIR / "pi_progress_since_may15.pdf"

TITLE = "Progress Report Since May 15"
SUBTITLE = "Low-Cost Outdoor Sensor-Box Research"
REPORT_DATE = "June 19, 2026"

BLUE = colors.HexColor("#1F4E79")
DARK = colors.HexColor("#17324D")
LIGHT_BLUE = colors.HexColor("#EAF2F8")
LIGHT_GRAY = colors.HexColor("#F2F4F7")
MID_GRAY = colors.HexColor("#667085")
BORDER = colors.HexColor("#CBD5E1")
GREEN = colors.HexColor("#D9EAD3")
AMBER = colors.HexColor("#FFF2CC")
WHITE = colors.white
BLACK = colors.black


class HR(Flowable):
    def __init__(self, color=BLUE, thickness=1.2, width="100%"):
        super().__init__()
        self.color = color
        self.thickness = thickness
        self.width_setting = width
        self.height = 0.10 * inch

    def wrap(self, avail_width, avail_height):
        self.width = avail_width if self.width_setting == "100%" else self.width_setting
        return self.width, self.height

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.height / 2, self.width, self.height / 2)


def make_styles():
    base = getSampleStyleSheet()
    styles = {
        "Title": ParagraphStyle(
            "TitleCustom",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=27,
            textColor=DARK,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "Subtitle": ParagraphStyle(
            "SubtitleCustom",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=12,
            leading=16,
            textColor=MID_GRAY,
            alignment=TA_CENTER,
            spaceAfter=14,
        ),
        "H1": ParagraphStyle(
            "H1Custom",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=BLUE,
            spaceBefore=12,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "H2": ParagraphStyle(
            "H2Custom",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11.5,
            leading=15,
            textColor=DARK,
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "Body": ParagraphStyle(
            "BodyCustom",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.4,
            leading=12.4,
            textColor=BLACK,
            spaceAfter=5,
        ),
        "Small": ParagraphStyle(
            "SmallCustom",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.1,
            leading=10.4,
            textColor=BLACK,
            spaceAfter=3,
        ),
        "Tiny": ParagraphStyle(
            "TinyCustom",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.2,
            leading=9,
            textColor=BLACK,
        ),
        "Bullet": ParagraphStyle(
            "BulletCustom",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.1,
            leading=12.2,
            leftIndent=14,
            firstLineIndent=-8,
            spaceAfter=3,
            bulletIndent=0,
        ),
        "TableHead": ParagraphStyle(
            "TableHeadCustom",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7.8,
            leading=9.2,
            textColor=WHITE,
            alignment=TA_LEFT,
        ),
        "TableCell": ParagraphStyle(
            "TableCellCustom",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.4,
            leading=8.8,
            textColor=BLACK,
        ),
        "TableCellBold": ParagraphStyle(
            "TableCellBoldCustom",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7.4,
            leading=8.8,
            textColor=DARK,
        ),
        "Caption": ParagraphStyle(
            "CaptionCustom",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=7.8,
            leading=9.5,
            textColor=MID_GRAY,
            alignment=TA_CENTER,
            spaceBefore=2,
            spaceAfter=6,
        ),
    }
    return styles


STYLES = make_styles()


def p(text, style="Body"):
    return Paragraph(escape(text), STYLES[style])


def rich(text, style="Body"):
    return Paragraph(text, STYLES[style])


def bullet(text):
    return Paragraph("- " + escape(text), STYLES["Bullet"])


def bullets(items):
    return [bullet(item) for item in items]


def cell(text, style="TableCell"):
    return Paragraph(escape(text), STYLES[style])


def table(data, widths, header=True, row_colors=True):
    rows = []
    for row_index, row in enumerate(data):
        style_name = "TableHead" if header and row_index == 0 else "TableCell"
        rows.append([cell(str(value), style_name) for value in row])

    t = LongTable(rows, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.35, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        commands.extend(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ]
        )
    if row_colors:
        start = 1 if header else 0
        for idx in range(start, len(rows)):
            if (idx - start) % 2 == 1:
                commands.append(("BACKGROUND", (0, idx), (-1, idx), colors.HexColor("#F8FAFC")))
    t.setStyle(TableStyle(commands))
    return t


def metadata_table():
    data = [
        ["Prepared for", "Principal Investigator review"],
        ["Scope", "Core outdoor sensor-box research only"],
        ["Excluded", "Military/environmental sensing application branch and military_applications files"],
        ["Repository", "500ft/Enclosure-Research"],
        ["Progress window", "May 15, 2026 through June 19, 2026"],
        ["Core research commit", "263080f, June 12, 2026, initial literature review, PI deliverables, and manuscript V1"],
    ]
    rows = []
    for label, value in data:
        rows.append([cell(label, "TableCellBold"), cell(value, "TableCell")])
    t = Table(rows, colWidths=[1.55 * inch, 4.85 * inch], hAlign="CENTER")
    t.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.35, BORDER),
                ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def section(title):
    return [p(title, "H1"), HR()]


def subsection(title):
    return p(title, "H2")


def build_story():
    story = []
    story.extend(
        [
            p(TITLE, "Title"),
            p(SUBTITLE, "Subtitle"),
            p("Detailed PI progress report - " + REPORT_DATE, "Subtitle"),
            metadata_table(),
            Spacer(1, 0.16 * inch),
            rich(
                "<b>One-sentence update:</b> Since May 15, the work has moved from a broad enclosure idea into a documented, literature-backed, system-level research plan for evaluating the lab's low-cost outdoor multi-sensor box.",
                "Body",
            ),
        ]
    )

    story.extend(section("1. Executive Summary"))
    story.extend(
        bullets(
            [
                "The central research frame is now the complete deployed sensor box, not only the enclosure shell. The enclosure remains important, but it is treated as one source of measurement error, autonomy limits, and maintenance burden.",
                "A working manuscript V1.0 has been drafted around calibration, ambient-condition effects, integration effects, autonomy, and design criteria for a low-cost outdoor sensor box.",
                "The literature base now contains 19 bibliography entries, and every entry has a matching per-paper sensor and physical-box pros/cons analysis.",
                "The literature review has been converted into structured engineering artifacts: a literature matrix, sensor/material/geometry summary, materials options table, geometry options table, prioritized added-literature list, and consolidated design selections.",
                "PI-ready deliverables already exist: a full literature synthesis PDF/DOCX, a shorter cover memo PDF/DOCX, and rendered page images used for visual verification.",
                "The project now has reusable data-collection and analysis infrastructure: a baseline system description template, deployment log, calibration/metric definitions, a literature coverage checker, and a first-pass metrics script.",
                "The main gap is no longer literature organization; it is experimental data. The next needed step is to inventory the exact lab hardware and run a baseline co-location deployment against reference measurements.",
            ]
        )
    )
    story.append(
        p(
            "Important scope note: this PDF intentionally ignores the later military/environmental sensing application work. That work is useful as a future application pathway, but it is not part of this PI progress report."
        )
    )

    story.extend(section("2. Timeline and Repository Snapshot"))
    story.append(
        p(
            "The meaningful core research progress appears in the June 12 initial research commit. The later June 19 branch added a defense application extension; because you asked to ignore that branch, the report below focuses on the June 12 core research artifacts and the non-military research direction."
        )
    )
    story.append(
        table(
            [
                ["Date", "Repository event", "Progress significance"],
                [
                    "May 15 onward",
                    "Research direction developed toward outdoor sensor-box enclosure and deployed-system performance.",
                    "Starting point for the progress window requested for PI review.",
                ],
                [
                    "June 12, 2026",
                    "Initial core research commit: 67 files, 3405 insertions.",
                    "Created manuscript draft, literature review, per-paper analyses, PI deliverables, templates, and analysis scripts.",
                ],
                [
                    "June 19, 2026",
                    "Separate defense/military application branch work.",
                    "Excluded from this report per your instruction; it should not distract from the core research update.",
                ],
            ],
            [0.85 * inch, 2.2 * inch, 3.35 * inch],
        )
    )

    story.extend(section("3. Research Framing: What Changed"))
    story.append(
        p(
            "The largest intellectual change is the move from an enclosure-only comparison to a full deployed-instrument evaluation. The current manuscript argues that low-cost outdoor boxes fail or bias data through a chain of coupled mechanisms: sensor calibration, solar heating, low airflow, internal electronics heat, moisture ingress, dust, sensor aging, battery limits, firmware reliability, and data gaps."
        )
    )
    story.append(subsection("Current research question"))
    story.append(
        rich(
            "<b>Can the lab's low-cost sensor box collect accurate, reliable outdoor data for a useful period of time without constant maintenance, and what factors most affect that performance?</b>",
            "Body",
        )
    )
    story.append(subsection("Why this is stronger than an enclosure-only paper"))
    story.extend(
        bullets(
            [
                "It avoids overclaiming that one material or one shield geometry is universally best.",
                "It creates measurable outcomes that matter to the lab: raw accuracy, calibrated accuracy, data completeness, uptime, maintenance burden, and failure modes.",
                "It lets the existing lab box be the baseline rather than requiring a fully new hardware design before publishable work can start.",
                "It still preserves an enclosure contribution by testing how material, surface finish, geometry, airflow path, sealing, and thermal layout affect the measurements.",
            ]
        )
    )

    story.extend(section("4. Literature Review Progress"))
    story.append(
        p(
            "The review is now organized around the specific evidence needed for the study: sensor performance, calibration, materials, shield/enclosure geometry, deployment reliability, and long-term autonomy. The coverage checker reports 19 bibliography entries and 19 matching per-paper analyses."
        )
    )
    story.append(
        table(
            [
                ["Evidence category", "Representative sources", "What they contribute"],
                [
                    "Complete sensor-box field systems",
                    "Theisen 2020; Tatsumi 2021; Grimsley 2022; Daepp 2022; Lazarescu 2015",
                    "Show that field usefulness depends on packaging, power, connectors, storage, communications, weathering, maintenance, and sensor choice together.",
                ],
                [
                    "Radiation-shield geometry",
                    "Tarara and Hoheisel 2007; Holden 2013; Botero-Valencia 2022; Liu 2023; Deford 2025; Jin 2026",
                    "Support testing passive stacked-plate/cone shields, airflow/open-area effects, reflected-radiation control, and active aspiration as an accuracy benchmark.",
                ],
                [
                    "Low-cost air-quality calibration",
                    "Clements 2017; deSouza 2022; Giordano 2021; Vajs 2021; AirSensEUR 2023; Diez 2024; Winter 2025",
                    "Support calibration against references, time-separated validation, humidity/temperature covariates, drift tracking, and caution about transferability.",
                ],
                [
                    "Long-term reliability and autonomy",
                    "Lazarescu 2015; Daepp 2022; Garcia Izquierdo 2024; Diez 2024; Winter 2025",
                    "Show that intervention frequency, sensor-hours collected, mechanical/electrical failures, fan/logger/power issues, and relocation effects should be reported.",
                ],
            ],
            [1.45 * inch, 1.85 * inch, 3.1 * inch],
        )
    )
    story.append(subsection("Added literature priorities"))
    story.append(
        p(
            "The added literature list prioritizes papers that fill specific gaps: Tarara and Hoheisel for passive shield geometry, Deford for aspirated low-cost shields, Holden for inexpensive manufacturable shields, Garcia Izquierdo for Arctic shield intercomparison and field failures, Lazarescu for long-term WSN autonomy, Liu and Jin for surface/geometry optimization, Diez and Winter for long-term calibration and failure behavior, and Daepp for expected sensor-hours as an operational metric."
        )
    )

    story.extend(section("5. Evidence Extraction and Organization"))
    story.append(
        p(
            "A key progress point is that the project now separates explicitly reported evidence from assumptions. Several papers report sensors and validation results clearly but do not report exact enclosure materials or airflow paths. The research files preserve those gaps rather than filling them in with guesses."
        )
    )
    story.append(
        table(
            [
                ["Artifact", "Status", "PI-facing value"],
                [
                    "literature/literature_matrix.csv",
                    "Created",
                    "Compact source-by-source extraction matrix for methods, sensors, materials, geometry, metrics, and relevance.",
                ],
                [
                    "literature/sensor_material_geometry_summary.md",
                    "Created",
                    "Detailed evidence table separating sensors, materials, geometry, and experimental setup for each major source.",
                ],
                [
                    "literature/materials_options.csv",
                    "Created",
                    "Material comparison for ASA, PETG, PLA, commercial IP boxes, coatings, filters, and related enclosure choices.",
                ],
                [
                    "literature/geometries_options.csv",
                    "Created",
                    "Geometry comparison for passive shields, active aspiration, sealed boxes, two-zone boxes, external probes, and airflow-guided designs.",
                ],
                [
                    "ProConsList/*.md",
                    "19 completed analyses",
                    "Each paper has a consistent sensor-selection and physical-box pros/cons summary.",
                ],
                [
                    "ProConsList/consolidated_selections.md",
                    "Created",
                    "Turns individual paper notes into consolidated design guidance for sensors, materials, and geometry.",
                ],
            ],
            [1.9 * inch, 1.0 * inch, 3.5 * inch],
        )
    )

    story.append(PageBreak())
    story.extend(section("6. Technical Conclusions So Far"))
    technical_blocks = [
        (
            "Calibration",
            [
                "The baseline should start with raw sensor-versus-reference comparison before any correction is applied.",
                "Univariate linear correction is the first defensible calibration step.",
                "Multiple linear correction should include ambient covariates where available: temperature, relative humidity, solar radiation, wind, battery voltage, and internal enclosure temperature.",
                "Machine learning should be treated as optional, not automatic. It becomes defensible only if enough co-located data exist and simpler models are insufficient.",
                "Validation should be time-separated rather than random-row splitting, because random splits can hide drift and deployment changes.",
            ],
        ),
        (
            "Materials",
            [
                "White or off-white ASA is the strongest literature-supported printed outdoor material, especially for UV and weather resistance.",
                "PETG is the practical in-house candidate if printer constraints make ASA difficult; it is useful for open-frame FDM prototyping but should be tested rather than assumed equivalent to ASA.",
                "PLA should be treated as a prototype/control material or possibly a coated short-duration option, not as the main uncoated outdoor material.",
                "Commercial IP-rated boxes are strong for sealed electronics, but they can trap heat and restrict airflow if ambient sensors are placed inside them.",
                "Surface finish and color are first-class variables. A dark enclosure near a temperature sensor can bias readings even if the base material is mechanically acceptable.",
            ],
        ),
        (
            "Geometry",
            [
                "The best-supported architecture is a two-zone design: sealed electronics/power plus a ventilated external sensing region or radiation shield.",
                "Passive stacked-plate or truncated-cone shields are the most defensible low-power starting point for temperature/RH sensing.",
                "Active aspiration can reduce low-wind, high-solar bias but adds fan power, maintenance, noise, and failure modes.",
                "Fully sealed single-compartment boxes are simpler and protective for electronics but are weak candidates for measuring true ambient air inside the same volume.",
                "PM and gas sensors need controlled inlet/outlet flow paths and maintainable filters; weather sealing and airflow cannot be solved independently.",
            ],
        ),
        (
            "Autonomy and reliability",
            [
                "Autonomy is broader than battery life. It includes uptime, missing samples, sensor dropouts, storage filling, clock drift, communication loss, firmware hangs, connector corrosion, water ingress, and repair events.",
                "The deployment should record expected versus received sensor-hours, maintenance events, battery/power behavior, resets, and physical inspection notes.",
                "Mechanical and electrical failures may appear before chemical sensor end-of-life, especially in long deployments.",
                "A useful sensor box must be evaluated as an operational system, not just as a set of low-cost sensor modules.",
            ],
        ),
    ]
    for heading, items in technical_blocks:
        story.append(subsection(heading))
        story.extend(bullets(items))

    story.extend(section("7. Manuscript Status"))
    story.append(
        p(
            "The paper draft exists as paper/manuscript_v1.md and is structured for a real experimental study once baseline data are collected. The current status is draft for PI/lab review, with methods and interpretation logic in place and results sections scaffolded."
        )
    )
    story.append(
        table(
            [
                ["Manuscript element", "Current status", "Remaining need"],
                [
                    "Title and abstract",
                    "Drafted around calibration, ambient conditions, integration effects, accuracy, and autonomy.",
                    "Update after actual deployment results identify the dominant limiting factor.",
                ],
                [
                    "Research question and framing",
                    "Clear system-level question established.",
                    "PI confirmation of exact measurement goals and acceptable performance thresholds.",
                ],
                [
                    "Literature review",
                    "Expanded across sensors, calibration, radiation shields, materials, autonomy, and failure modes.",
                    "Add any PI-required domain-specific or lab-specific references.",
                ],
                [
                    "Methods",
                    "Four-phase plan drafted: inventory/bench check, reference co-location, baseline analysis, calibration/decision analysis.",
                    "Fill in actual hardware models, reference instruments, site details, logging interval, and deployment duration.",
                ],
                [
                    "Results",
                    "Tables scaffolded for raw accuracy, calibrated accuracy, data completeness, and failure modes.",
                    "Needs real data from 14-day minimum or 30-day preferred co-location.",
                ],
                [
                    "Discussion/design criteria",
                    "Draft criteria cover accuracy, calibration robustness, autonomy, reliability, weather resistance, thermal behavior, maintainability, and manufacturability.",
                    "Tie conclusions to measured dominant failure/error sources.",
                ],
            ],
            [1.5 * inch, 2.55 * inch, 2.35 * inch],
        )
    )

    story.extend(section("8. Deliverables Produced"))
    story.append(
        table(
            [
                ["Deliverable", "File", "Why it matters"],
                [
                    "Full PI literature synthesis",
                    "deliverables/PI_Literature_Synthesis_Outdoor_Sensor_Box.pdf and .docx",
                    "PI-ready explanation of 19 sources, including sensors, materials, geometry, setup, findings, and design implications.",
                ],
                [
                    "Short cover memo",
                    "deliverables/PI_Cover_Memo_Literature_and_Next_Steps.pdf and .docx",
                    "Concise framing of what changed, strongest conclusions, recommended experimental framing, and decisions requested.",
                ],
                [
                    "Rendered verification images",
                    "deliverables/rendered_pi_summary/ and deliverables/rendered_pi_memo/",
                    "Page renderings show the deliverables were visually checked rather than only generated.",
                ],
                [
                    "Baseline inventory template",
                    "templates/baseline_system_description.md",
                    "For recording exact sensor models, microcontroller/logger, enclosure, power, placement, venting, sealing, and data handling.",
                ],
                [
                    "Deployment log",
                    "templates/deployment_log.csv",
                    "For timestamped field notes, maintenance, missing data, weather exposure, and intervention tracking.",
                ],
                [
                    "Metric definitions",
                    "templates/calibration_metrics.md",
                    "Standardizes bias, MAE, RMSE, correlation, drift, lag, uptime, data completeness, and maintenance reporting.",
                ],
                [
                    "Analysis scripts",
                    "analysis/compute_metrics.py and analysis/check_literature_coverage.py",
                    "Provide first-pass performance calculations and enforce literature-analysis completeness.",
                ],
            ],
            [1.35 * inch, 2.15 * inch, 2.9 * inch],
        )
    )

    story.extend(section("9. Experimental Plan Readiness"))
    story.append(
        p(
            "The project is ready to move from literature-supported planning into baseline data collection. The manuscript does not need a large hardware redesign before the first experiment; the most defensible next step is to test the current lab box as-is, then use the results to justify a small set of alternatives."
        )
    )
    story.append(
        table(
            [
                ["Step", "Ready now?", "Notes"],
                [
                    "Complete hardware inventory",
                    "Partly ready",
                    "Template exists, but actual lab hardware details still need to be filled in.",
                ],
                [
                    "Bench check sensors/logger/power",
                    "Ready to start",
                    "Use inventory template and confirm each measurement channel before field deployment.",
                ],
                [
                    "Reference co-location",
                    "Needs PI/lab coordination",
                    "Requires reference instrument access and a deployment location. Minimum 14 days; 30 days preferred.",
                ],
                [
                    "Raw accuracy analysis",
                    "Ready after data collection",
                    "Metrics script supports first-pass comparison once sensor and reference CSVs are available.",
                ],
                [
                    "Calibration analysis",
                    "Ready after sufficient data",
                    "Start with linear correction, then multiple linear correction with ambient covariates.",
                ],
                [
                    "Design comparison",
                    "Literature-ready, data-dependent",
                    "Choose current box, strong passive shield, and optional active aspirated benchmark after baseline results.",
                ],
            ],
            [1.65 * inch, 1.0 * inch, 3.75 * inch],
        )
    )

    story.extend(section("10. Recommended PI Discussion Points"))
    story.extend(
        bullets(
            [
                "Confirm the exact environmental variables that matter most for the lab's research use case.",
                "Confirm the exact hardware currently available: sensor models, logger/microcontroller, enclosure material, power system, solar panel if any, cable glands, filters, and mounting hardware.",
                "Identify which reference instrument can be used for co-location and what its calibration/traceability status is.",
                "Define acceptable performance thresholds: raw and calibrated error, minimum uptime, acceptable missing-data rate, maximum maintenance frequency, and required deployment duration.",
                "Decide whether the first comparison should test passive shields only or include an active aspirated benchmark to establish a practical upper bound on accuracy.",
                "Decide whether the first paper should emphasize measurement accuracy, autonomy/reliability, or the interaction between enclosure design and calibration.",
            ]
        )
    )

    story.append(PageBreak())
    story.extend(section("Appendix A. Core Artifact Map"))
    story.append(
        table(
            [
                ["Area", "Files", "Progress represented"],
                [
                    "Manuscript",
                    "paper/manuscript_v1.md; paper/references.bib",
                    "Working research paper and bibliography for the core outdoor sensor-box study.",
                ],
                [
                    "Literature extraction",
                    "literature/literature_matrix.csv; literature/sensor_material_geometry_summary.md; literature/additional_literature_list.md",
                    "Structured evidence base for sensors, materials, geometry, setup, and follow-up literature priorities.",
                ],
                [
                    "Design option analysis",
                    "literature/materials_options.csv; literature/geometries_options.csv; ProConsList/consolidated_selections.md",
                    "Engineering comparison of likely material and enclosure/shield choices.",
                ],
                [
                    "Per-paper review",
                    "ProConsList/*.md",
                    "19 individual source analyses with sensor and physical-box pros/cons.",
                ],
                [
                    "PI deliverables",
                    "deliverables/PI_Literature_Synthesis_Outdoor_Sensor_Box.*; deliverables/PI_Cover_Memo_Literature_and_Next_Steps.*",
                    "Ready-to-share PDF/DOCX summary and memo for PI review.",
                ],
                [
                    "Experiment templates",
                    "templates/baseline_system_description.md; templates/deployment_log.csv; templates/calibration_metrics.md",
                    "Reusable documentation and metric templates for the experimental phase.",
                ],
                [
                    "Analysis support",
                    "analysis/compute_metrics.py; analysis/check_literature_coverage.py",
                    "First-pass metric computation and literature completeness verification.",
                ],
            ],
            [1.25 * inch, 2.35 * inch, 2.8 * inch],
        )
    )

    story.extend(section("Appendix B. Validation and Current Limitations"))
    story.append(subsection("Validation already done"))
    story.extend(
        bullets(
            [
                "Literature coverage check passes: 19 bibliography entries and 19 per-paper analyses.",
                "PI literature synthesis and PI memo already have rendered page-image outputs in the deliverables folder.",
                "The manuscript has explicit placeholders for raw accuracy, calibrated accuracy, autonomy/data completeness, and failure-mode results, reducing the risk of collecting data without a reporting structure.",
            ]
        )
    )
    story.append(subsection("Limitations to be transparent about"))
    story.extend(
        bullets(
            [
                "The current paper is not yet a results paper; it is a literature-backed study plan and manuscript scaffold until field data are collected.",
                "Several literature sources do not report exact enclosure material, wall geometry, airflow path, or surface finish. The review documents those gaps instead of overinterpreting them.",
                "The exact lab hardware details are still needed before the methods section can be finalized.",
                "Any claim about best material or best geometry should remain conditional until the lab box is tested under representative outdoor conditions.",
            ]
        )
    )
    story.append(subsection("Recommended next week of work"))
    story.extend(
        bullets(
            [
                "Fill out the baseline system description template from the physical lab box.",
                "Photograph the enclosure, sensor placement, vents, cable routing, seals, filters, and mounting hardware.",
                "Confirm reference instrument availability and schedule a co-location deployment.",
                "Start with an unchanged baseline deployment before changing materials or shield geometry.",
                "Use the deployment log from day one so missing samples and maintenance interventions are captured.",
            ]
        )
    )

    return story


def on_page(canvas, doc):
    canvas.saveState()
    width, height = LETTER
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MID_GRAY)
    canvas.drawString(doc.leftMargin, 0.42 * inch, "Core outdoor sensor-box research progress - excluding military application branch")
    canvas.drawRightString(width - doc.rightMargin, 0.42 * inch, f"Page {doc.page}")
    if doc.page > 1:
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(BLUE)
        canvas.drawString(doc.leftMargin, height - 0.42 * inch, TITLE)
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.4)
        canvas.line(doc.leftMargin, height - 0.50 * inch, width - doc.rightMargin, height - 0.50 * inch)
    canvas.restoreState()


def build():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=LETTER,
        rightMargin=0.62 * inch,
        leftMargin=0.62 * inch,
        topMargin=0.66 * inch,
        bottomMargin=0.70 * inch,
        title=TITLE,
        author="Enclosure Research",
        subject="PI progress report for low-cost outdoor sensor-box research",
    )
    doc.build(build_story(), onFirstPage=on_page, onLaterPages=on_page)
    print(OUT_PDF)


if __name__ == "__main__":
    build()
