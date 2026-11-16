import os
import subprocess
import html
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_bg(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def generate_docx():
    doc = docx.Document()
    
    # Page Margins
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Base Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)

    # Department Header
    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_dept = p_dept.add_run("Department of Computer Engineering (Software Engineering)\n")
    r_dept.font.size = Pt(14)
    r_dept.font.bold = True
    r_dept.font.color.rgb = RGBColor(15, 23, 42)

    r_sub = p_dept.add_run("Web Technology Laboratory — Academic Year 2026-27\n")
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("Practical No. 03: Component-Based Client-Side Web Application using React JS")
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(37, 99, 235)

    # Metadata Table
    meta_table = doc.add_table(rows=2, cols=4)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        [("Name:", "Sarthak Bhosale"), ("PRN:", "202401100051")],
        [("Batch:", "TY SE-A2"), ("Roll No:", "A50")]
    ]
    for row_idx, row in enumerate(meta_data):
        col_offset = 0
        for label, val in row:
            cell_lbl = meta_table.cell(row_idx, col_offset)
            cell_val = meta_table.cell(row_idx, col_offset + 1)
            cell_lbl.text = label
            cell_lbl.paragraphs[0].runs[0].font.bold = True
            cell_lbl.paragraphs[0].runs[0].font.color.rgb = RGBColor(71, 85, 105)
            cell_val.text = val
            cell_val.paragraphs[0].runs[0].font.bold = True
            cell_val.paragraphs[0].runs[0].font.color.rgb = RGBColor(15, 23, 42)
            set_cell_bg(cell_lbl, "F1F5F9")
            set_cell_bg(cell_val, "FFFFFF")
            set_cell_margins(cell_lbl, 80, 80, 100, 100)
            set_cell_margins(cell_val, 80, 80, 100, 100)
            col_offset += 2

    doc.add_paragraph()

    def add_section_heading(num_str, title_str):
        h = doc.add_paragraph()
        r = h.add_run(f"{num_str}. {title_str}")
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(15, 23, 42)
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        return h

    def add_code_block(title, code_str):
        p_t = doc.add_paragraph()
        r_t = p_t.add_run(title)
        r_t.font.bold = True
        r_t.font.size = Pt(11)
        r_t.font.color.rgb = RGBColor(37, 99, 235)
        p_t.paragraph_format.space_before = Pt(8)
        p_t.paragraph_format.space_after = Pt(2)

        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_bg(cell, "0F172A")
        set_cell_margins(cell, 120, 120, 150, 150)
        p = cell.paragraphs[0]
        r = p.add_run(code_str)
        r.font.name = 'Consolas'
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(241, 245, 249)
        doc.add_paragraph()

    # 1. Aim
    add_section_heading("1", "Aim")
    doc.add_paragraph(
        "To design, develop, build, and deploy a responsive, modular, component-based client-side web application "
        "for the TaskGravity task management suite using React JS, Vite, functional components, React Hooks "
        "(useState, useEffect), unidirectional data flow, and browser LocalStorage persistence."
    )

    # 2. Problem Statement
    add_section_heading("2", "Problem Statement")
    doc.add_paragraph(
        "Building sophisticated web applications with pure imperative DOM manipulation introduces complex state synchronization "
        "and error-prone UI updates. To overcome these limitations, develop TaskGravity using React's declarative component "
        "architecture. The system must feature isolated UI components (TaskForm, TaskList, TaskCard, FilterBar, StatsBar), "
        "manage reactive state immutably with useState, handle side-effects and localStorage hydration with useEffect, "
        "support full CRUD operations with priority and category assignment, and strictly follow the TaskGravity minimalist UI/UX design tokens."
    )

    # 3. Theory & Concept Review
    add_section_heading("3", "Theory & Concept Review")
    doc.add_paragraph(
        "3.1 React Architecture and Virtual DOM\n"
        "React employs a Virtual DOM—an in-memory representation of real DOM elements. When component state changes, "
        "React computes differences using its Reconciliation Algorithm (Fiber) and batches minimal real-DOM updates, "
        "yielding high rendering performance."
    )
    doc.add_paragraph(
        "3.2 Functional Components and Hooks\n"
        "Modern React prioritizes functional components over class components. Hooks allow functional components to harness "
        "state and lifecycle capabilities:\n"
        "• useState: Declares local reactive state variables and setter functions that trigger re-rendering.\n"
        "• useEffect: Manages component side-effects (e.g., initial local storage sync, browser title updates, external API calls).\n"
        "• Unidirectional Data Flow: Data flows strictly down via props, while user interactions trigger callbacks upward to parent state."
    )
    doc.add_paragraph(
        "3.3 Component Decomposition & DRY Code\n"
        "In TaskGravity, responsibilities are cleanly divided into atomic components: App (orchestrator), TaskForm (controlled inputs), "
        "TaskList (mapped collection with empty states), TaskCard (individual item with action triggers), FilterBar (status/category filters), "
        "and StatsBar (computed analytical summaries)."
    )

    # 4. Software & Hardware Requirements
    add_section_heading("4", "Software & Hardware Requirements")
    req_table = doc.add_table(rows=5, cols=2)
    req_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    req_data = [
        ("Operating System", "Microsoft Windows 11 x64"),
        ("Node.js Runtime & Package Manager", "Node.js v20.x, npm v10.x, Vite v5.x"),
        ("Development Environment", "Antigravity IDE / Visual Studio Code"),
        ("Browser & Tools", "Google Chrome 120+, React Developer Tools"),
        ("Version Control & Hosting", "Git, GitHub, GitHub Pages (via gh-pages / docs distribution)")
    ]
    for idx, (lbl, val) in enumerate(req_data):
        c1, c2 = req_table.cell(idx, 0), req_table.cell(idx, 1)
        c1.text = lbl
        c1.paragraphs[0].runs[0].font.bold = True
        c2.text = val
        set_cell_bg(c1, "F8FAFC")
        set_cell_bg(c2, "FFFFFF")
        set_cell_margins(c1, 80, 80, 100, 100)
        set_cell_margins(c2, 80, 80, 100, 100)
    doc.add_paragraph()

    # 5. Design & Architectural Implementation
    add_section_heading("5", "Design & Architectural Implementation")
    doc.add_paragraph(
        "The application architecture follows standard production React patterns:\n"
        "1. State Management: The root App component maintains master tasks state, filter criteria, and search query.\n"
        "2. Synchronization: An initial useEffect hook reads persisted tasks from localStorage. A subsequent useEffect synchronizes state back on every mutation.\n"
        "3. Immutability: Task additions use array spread syntax [...tasks, newTask]. Updates and toggles use tasks.map(). Deletions use tasks.filter().\n"
        "4. Styling: Pure minimalist CSS tokens with crisp borders, monospaced badges, neutral dark mode support, and zero AI-style gradients."
    )

    # 6. Source Code
    add_section_heading("6", "Source Code Implementation")
    base_dir = r"D:\_TY\Web-Tech\Practicals\Practical3"
    
    def read_code(rel_path):
        fpath = os.path.join(base_dir, rel_path)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                return f.read()
        return "// File not found"

    app_jsx = read_code(r"src\App.jsx")
    task_form_jsx = read_code(r"src\components\TaskForm.jsx")
    task_card_jsx = read_code(r"src\components\TaskCard.jsx")
    task_list_jsx = read_code(r"src\components\TaskList.jsx")
    stats_bar_jsx = read_code(r"src\components\StatsBar.jsx")
    css_code = read_code(r"src\index.css")

    add_code_block("6.1 App.jsx (Root Component & Reactive State Coordinator)", app_jsx)
    add_code_block("6.2 TaskForm.jsx (Controlled Input Form Component)", task_form_jsx)
    add_code_block("6.3 TaskCard.jsx (Atomic Task Card with Priority & Actions)", task_card_jsx)
    add_code_block("6.4 TaskList.jsx & StatsBar.jsx (Collection Rendering & Metrics)", task_list_jsx + "\n\n// --- StatsBar.jsx ---\n" + stats_bar_jsx)
    add_code_block("6.5 index.css (TaskGravity Minimalist Design Tokens)", css_code)

    # 7. Verification & Test Results
    add_section_heading("7", "Verification & Test Results")
    test_table = doc.add_table(rows=6, cols=3)
    test_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    test_headers = ["Test Case", "Observed Behavior & Criteria", "Status"]
    for c_idx, h in enumerate(test_headers):
        cell = test_table.cell(0, c_idx)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_bg(cell, "F1F5F9")
        set_cell_margins(cell, 80, 80, 100, 100)
    
    tests = [
        ("Component Rendering", "App, Form, Stats, and List mount cleanly with zero console warnings or key errors.", "Passed"),
        ("State Immutability", "Adding, toggling status, and deleting tasks cleanly trigger re-renders without direct state mutation.", "Passed"),
        ("LocalStorage Persistence", "State is preserved across full page reloads and browser restarts via useEffect hook.", "Passed"),
        ("Filter & Search Reactivity", "Filter buttons (All/Active/Completed) and Priority filters instantly recalculate visible task slice.", "Passed"),
        ("Production Vite Build", "Vite build runs cleanly to docs/ directory, with optimized bundle footprint suitable for GitHub Pages.", "Passed")
    ]
    for r_idx, row in enumerate(tests, start=1):
        for c_idx, val in enumerate(row):
            cell = test_table.cell(r_idx, c_idx)
            cell.text = val
            if c_idx == 2:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_bg(cell, "DCFCE7")
            else:
                set_cell_bg(cell, "FFFFFF")
            set_cell_margins(cell, 80, 80, 100, 100)
    doc.add_paragraph()

    # 8. Conclusion
    add_section_heading("8", "Conclusion")
    doc.add_paragraph(
        "Practical 03 demonstrates the implementation of a modern component-driven web application using React JS and Vite. "
        "By leveraging functional components, React Hooks (useState, useEffect), and unidirectional data flow, the TaskGravity "
        "frontend achieves high responsiveness, modularity, and reliable state persistence without imperative DOM manipulation. "
        "The application strictly maintains the TaskGravity minimalist aesthetic and was successfully bundled and deployed to GitHub Pages."
    )

    # Mandatory Links Box
    p_box = doc.add_paragraph()
    p_box.paragraph_format.space_before = Pt(14)
    tbl_links = doc.add_table(rows=1, cols=1)
    tbl_links.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_links = tbl_links.cell(0, 0)
    set_cell_bg(c_links, "F8FAFC")
    set_cell_margins(c_links, 120, 120, 150, 150)
    p_l = c_links.paragraphs[0]
    r_lh = p_l.add_run("Project Links & Deployment Information:\n")
    r_lh.font.bold = True
    r_lh.font.size = Pt(11)
    r_lh.font.color.rgb = RGBColor(15, 23, 42)

    r_gh = p_l.add_run("GitHub Link / Code Link: ")
    r_gh.font.bold = True
    p_l.add_run("https://github.com/Sarthak-1229/taskgravity-practical-03\n")

    r_live = p_l.add_run("Live Deployment Link: ")
    r_live.font.bold = True
    p_l.add_run("https://sarthak-1229.github.io/taskgravity-practical-03/")

    docx_path = r"D:\_TY\Web-Tech\Practicals\Practical3\Practical_03_Report.docx"
    doc.save(docx_path)
    print(f"Generated DOCX: {docx_path}")

def generate_pdf():
    base_dir = r"D:\_TY\Web-Tech\Practicals\Practical3"
    def read_code(rel_path):
        fpath = os.path.join(base_dir, rel_path)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                return f.read()
        return "// File not found"

    app_jsx = html.escape(read_code(r"src\App.jsx"))
    task_form_jsx = html.escape(read_code(r"src\components\TaskForm.jsx"))
    task_card_jsx = html.escape(read_code(r"src\components\TaskCard.jsx"))
    task_list_jsx = html.escape(read_code(r"src\components\TaskList.jsx"))
    stats_bar_jsx = html.escape(read_code(r"src\components\StatsBar.jsx"))
    css_code = html.escape(read_code(r"src\index.css"))

    report_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Practical 03 Report - Sarthak Bhosale</title>
<style>
  @page {{
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-center {{
      content: counter(page);
    }}
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    line-height: 1.55;
    font-size: 10pt;
    margin: 0;
    padding: 0;
  }}
  .header {{
    text-align: center;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 12px;
    margin-bottom: 18px;
  }}
  .dept-title {{
    font-size: 13pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.2px;
    text-transform: uppercase;
  }}
  .sub-title {{
    font-size: 10pt;
    font-weight: 600;
    color: #64748b;
    margin-top: 2px;
  }}
  .prac-title {{
    font-size: 14pt;
    font-weight: 800;
    color: #2563eb;
    margin-top: 8px;
  }}
  .meta-grid {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    font-size: 9.5pt;
  }}
  .meta-grid td {{
    border: 1px solid #cbd5e1;
    padding: 6px 10px;
  }}
  .meta-grid .lbl {{
    background-color: #f1f5f9;
    font-weight: 700;
    color: #475569;
    width: 15%;
  }}
  .meta-grid .val {{
    font-weight: 700;
    color: #0f172a;
    width: 35%;
  }}
  h2.sec-title {{
    font-size: 11pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
    margin-top: 20px;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  h3.subsec-title {{
    font-size: 10pt;
    font-weight: 700;
    color: #2563eb;
    margin-top: 14px;
    margin-bottom: 4px;
  }}
  p, li {{
    font-size: 9.5pt;
    color: #334155;
    text-align: justify;
    margin-top: 4px;
    margin-bottom: 6px;
  }}
  ul, ol {{
    padding-left: 20px;
    margin-top: 4px;
    margin-bottom: 8px;
  }}
  .code-block {{
    background-color: #0f172a;
    color: #f8fafc;
    font-family: "Consolas", "Fira Code", monospace;
    font-size: 8pt;
    line-height: 1.4;
    padding: 10px 14px;
    border-radius: 4px;
    white-space: pre-wrap;
    word-break: break-all;
    margin: 8px 0 14px 0;
  }}
  .data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 9pt;
  }}
  .data-table th, .data-table td {{
    border: 1px solid #cbd5e1;
    padding: 7px 10px;
    text-align: left;
  }}
  .data-table th {{
    background-color: #f8fafc;
    font-weight: 700;
    color: #0f172a;
  }}
  .badge-pass {{
    color: #15803d;
    font-weight: 700;
    background-color: #dcfce7;
    padding: 2px 6px;
    border-radius: 3px;
    display: inline-block;
  }}
  .links-box {{
    margin-top: 20px;
    padding: 12px 14px;
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #2563eb;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }}
  .links-box a {{
    color: #2563eb;
    text-decoration: none;
    font-weight: 600;
  }}
</style>
</head>
<body>

<div class="header">
  <div class="dept-title">Department of Computer Engineering (Software Engineering)</div>
  <div class="sub-title">Web Technology Laboratory — Academic Year 2026-27</div>
  <div class="prac-title">Practical No. 03: Component-Based Client-Side Web Application using React JS</div>
</div>

<table class="meta-grid">
  <tr>
    <td class="lbl">Name:</td>
    <td class="val">Sarthak Bhosale</td>
    <td class="lbl">PRN:</td>
    <td class="val">202401100051</td>
  </tr>
  <tr>
    <td class="lbl">Batch:</td>
    <td class="val">TY SE-A2</td>
    <td class="lbl">Roll No:</td>
    <td class="val">A50</td>
  </tr>
</table>

<h2 class="sec-title">1. Aim</h2>
<p>
To design, develop, build, and deploy a responsive, modular, component-based client-side web application for the TaskGravity task management suite using React JS, Vite, functional components, React Hooks (<code>useState</code>, <code>useEffect</code>), unidirectional data flow, and browser LocalStorage persistence.
</p>

<h2 class="sec-title">2. Problem Statement</h2>
<p>
Building complex single-page frontends via imperative DOM manipulation results in tight coupling, fragile state sync, and redundant re-renders. To address these industry challenges, construct the TaskGravity client application using React's declarative component architecture. The system must feature decoupled components (TaskForm, TaskList, TaskCard, FilterBar, StatsBar), manage reactive state immutably with <code>useState</code>, handle side-effects and localStorage hydration with <code>useEffect</code>, support full CRUD operations with priority and category assignment, and strictly adhere to the TaskGravity minimalist UI/UX design tokens.
</p>

<h2 class="sec-title">3. Theory & Concept Review</h2>
<p>
<strong>3.1 React Architecture and Virtual DOM:</strong> React utilizes an in-memory Virtual DOM tree representation. Upon state updates, React's diffing engine computes optimal mutations and batches DOM updates, minimizing expensive layout recalculations.
</p>
<p>
<strong>3.2 Functional Components and Hooks:</strong> React Hooks allow functional components to maintain encapsulated state without class syntax:
</p>
<ul>
  <li><code>useState</code>: Encapsulates reactive values and provides setter functions to trigger UI reconciliation.</li>
  <li><code>useEffect</code>: Coordinates side-effects such as reading/writing to <code>localStorage</code> and syncing browser title.</li>
  <li><code>Unidirectional Data Flow</code>: Props pass state downstream, while callback handlers propagate events upward.</li>
</ul>
<p>
<strong>3.3 Component Decomposition & DRY Code:</strong> Codebase is structured into atomic, reusable components: App (coordinator), TaskForm (controlled inputs), TaskList (collection rendering), TaskCard (atomic item card), FilterBar (status and priority filters), and StatsBar (computed analytics).
</p>

<h2 class="sec-title">4. Software & Hardware Requirements</h2>
<table class="data-table">
  <tr><th style="width: 30%;">Component</th><th>Specification</th></tr>
  <tr><td>Operating System</td><td>Microsoft Windows 11 x64</td></tr>
  <tr><td>Node.js & Bundler</td><td>Node.js v20.x, npm v10.x, Vite v5.x</td></tr>
  <tr><td>Development Environment</td><td>Antigravity IDE / Visual Studio Code</td></tr>
  <tr><td>Browser & Diagnostics</td><td>Google Chrome 120+, React Developer Tools</td></tr>
  <tr><td>Hosting & Version Control</td><td>Git, GitHub, GitHub Pages (Vite docs distribution)</td></tr>
</table>

<h2 class="sec-title">5. Design & Architectural Implementation</h2>
<ol>
  <li>Initialize modern React development scaffolding using Vite build toolchain.</li>
  <li>Structure components in <code>src/components/</code>: TaskForm, TaskList, TaskCard, FilterBar, StatsBar.</li>
  <li>Implement state coordination in <code>App.jsx</code> with reactive task state and active filters.</li>
  <li>Incorporate <code>localStorage</code> serialization and deserialization in <code>useEffect</code> hooks.</li>
  <li>Enforce strict immutability in array state operations (spread, map, filter).</li>
  <li>Build production distribution bundle with Vite into <code>docs/</code> folder for seamless GitHub Pages hosting.</li>
</ol>

<h2 class="sec-title">6. Source Code Implementation</h2>

<h3 class="subsec-title">6.1 App.jsx (Root Component & Reactive State Coordinator)</h3>
<pre class="code-block">{app_jsx}</pre>

<h3 class="subsec-title">6.2 TaskForm.jsx (Controlled Input Form Component)</h3>
<pre class="code-block">{task_form_jsx}</pre>

<h3 class="subsec-title">6.3 TaskCard.jsx (Atomic Task Card with Priority & Actions)</h3>
<pre class="code-block">{task_card_jsx}</pre>

<h3 class="subsec-title">6.4 TaskList.jsx & StatsBar.jsx (Collection Rendering & Metrics)</h3>
<pre class="code-block">{task_list_jsx}

// --- StatsBar.jsx ---
{stats_bar_jsx}</pre>

<h3 class="subsec-title">6.5 index.css (TaskGravity Minimalist Design Tokens)</h3>
<pre class="code-block">{css_code}</pre>

<h2 class="sec-title">7. Verification & Test Results</h2>
<table class="data-table">
  <thead>
    <tr>
      <th>Test Case</th>
      <th>Observed Behavior & Criteria</th>
      <th>Verification Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Component Rendering</strong></td>
      <td>All modular components mount cleanly with zero React console warnings or unique key errors.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
    <tr>
      <td><strong>State Immutability</strong></td>
      <td>Adding, toggling status, and deleting tasks trigger reactive updates without direct array mutations.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
    <tr>
      <td><strong>LocalStorage Persistence</strong></td>
      <td>State survives page refreshes and browser restarts via useEffect persistence pipeline.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
    <tr>
      <td><strong>Filter & Search Reactivity</strong></td>
      <td>Filter buttons and priority switches instantly recalculate visible task slice.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
    <tr>
      <td><strong>Production Vite Build</strong></td>
      <td>Vite bundle generates clean production assets in docs/ directory and deploys to GitHub Pages.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
  </tbody>
</table>

<h2 class="sec-title">8. Conclusion</h2>
<p>
Practical 03 successfully demonstrates the implementation of a modern component-driven web application using React JS and Vite. By leveraging functional components, React Hooks (<code>useState</code>, <code>useEffect</code>), and unidirectional data flow, the TaskGravity frontend achieves high responsiveness, modularity, and reliable state persistence without imperative DOM manipulation. The application strictly maintains the TaskGravity minimalist aesthetic and was successfully bundled and deployed to GitHub Pages.
</p>

<div class="links-box">
  <div style="font-weight: 700; font-size: 11pt; margin-bottom: 6px; color: #0f172a;">Project Links & Deployment Information</div>
  <div><strong>GitHub Link / Code Link:</strong> <a href="https://github.com/Sarthak-1229/taskgravity-practical-03" target="_blank">https://github.com/Sarthak-1229/taskgravity-practical-03</a></div>
  <div style="margin-top: 4px;"><strong>Live Deployment Link:</strong> <a href="https://sarthak-1229.github.io/taskgravity-practical-03/" target="_blank">https://sarthak-1229.github.io/taskgravity-practical-03/</a></div>
</div>

</body>
</html>
"""
    html_report_path = r"D:\_TY\Web-Tech\Practicals\Practical3\report_temp.html"
    pdf_report_path = r"D:\_TY\Web-Tech\Practicals\Practical3\Practical_03_Report.pdf"

    with open(html_report_path, "w", encoding="utf-8") as f:
        f.write(report_html)

    chrome_cmd = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--headless=new",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_report_path}",
        html_report_path
    ]
    subprocess.run(chrome_cmd, check=True)
    
    if os.path.exists(html_report_path):
        os.remove(html_report_path)
    
    print(f"Generated PDF: {pdf_report_path}")

if __name__ == "__main__":
    generate_docx()
    generate_pdf()
