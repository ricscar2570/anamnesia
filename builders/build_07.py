"""
build_07.py — Roll20 Digital Pack
Genera output/en/07_roll20_pack.zip contenente SETUP_GUIDE.html e character_sheet.html.
Viene eseguito SOLO per lang='en' (Roll20 è anglofono); per le altre lingue restituisce subito.
"""

import sys, os, yaml, zipfile, html
sys.path.insert(0, os.path.dirname(__file__))
from shared import BUILD_DIR, OUTPUT_DIR

# ── Costanti ──────────────────────────────────────────────────────────────────

ROLL20_ONLY_LANG = 'en'

# ── Loader dati ───────────────────────────────────────────────────────────────

def load(lang):
    p = os.path.join(BUILD_DIR, 'content', lang, '07.yaml')
    with open(p, encoding='utf-8') as f:
        return yaml.safe_load(f)

# ── Generatori HTML ───────────────────────────────────────────────────────────

def esc(s):
    return html.escape(str(s), quote=False)

def _table_rows_html(rows):
    out = []
    for row in rows:
        cells = ''.join(f'<td>{esc(c)}</td>' for c in row)
        out.append(f'<tr>{cells}</tr>')
    return '\n'.join(out)

def build_setup_guide(d):
    """Genera il contenuto HTML del SETUP_GUIDE."""

    # ── CSS ──────────────────────────────────────────────────────────────────
    css = """
        :root {
            --bg: #0b0907;
            --surface: #130f0a;
            --surface2: #1c1510;
            --border: #3a2d1e;
            --accent: #8b1a1a;
            --accent2: #c0392b;
            --text: #e8ddd0;
            --muted: #8a7a6a;
            --code-bg: #0e1a0e;
            --code-border: #2a4a2a;
            --code-text: #a8d8a8;
            --keeper-bg: #1a0e0e;
            --keeper-border: #6b1515;
            --font-serif: 'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif;
            --font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', Consolas, monospace;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: var(--bg);
            color: var(--text);
            font-family: var(--font-serif);
            font-size: 15px;
            line-height: 1.7;
            display: flex;
            min-height: 100vh;
        }
        /* ── Sidebar ── */
        nav {
            position: fixed;
            top: 0; left: 0;
            width: 220px;
            height: 100vh;
            background: var(--surface);
            border-right: 1px solid var(--border);
            overflow-y: auto;
            padding: 24px 0;
            z-index: 100;
        }
        nav .brand {
            font-size: 10px;
            letter-spacing: 3px;
            color: var(--accent);
            text-transform: uppercase;
            padding: 0 20px 20px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 16px;
        }
        nav .progress-bar {
            height: 3px;
            background: var(--border);
            margin: 0 20px 20px;
            border-radius: 2px;
            overflow: hidden;
        }
        nav .progress-fill {
            height: 100%;
            background: var(--accent);
            width: 0%;
            transition: width 0.3s ease;
        }
        nav a {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 20px;
            color: var(--muted);
            text-decoration: none;
            font-size: 12px;
            letter-spacing: 0.5px;
            transition: all 0.2s;
            border-left: 2px solid transparent;
        }
        nav a:hover, nav a.active {
            color: var(--text);
            background: var(--surface2);
            border-left-color: var(--accent);
        }
        nav a .check { color: #4caf50; margin-left: auto; font-size: 14px; opacity: 0; transition: opacity 0.3s; }
        nav a.done .check { opacity: 1; }
        nav a .step-num {
            width: 20px; height: 20px;
            background: var(--border);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 10px;
            flex-shrink: 0;
        }
        /* ── Main ── */
        main {
            margin-left: 220px;
            padding: 48px 56px;
            max-width: 900px;
            width: 100%;
        }
        /* ── Header ── */
        .site-header {
            text-align: center;
            padding-bottom: 40px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 48px;
        }
        .site-header .eyebrow {
            font-size: 10px;
            letter-spacing: 4px;
            color: var(--accent);
            text-transform: uppercase;
            margin-bottom: 12px;
        }
        .site-header h1 {
            font-size: 32px;
            font-weight: normal;
            letter-spacing: 2px;
            color: var(--text);
            margin-bottom: 8px;
        }
        .site-header .subtitle {
            color: var(--muted);
            font-style: italic;
            font-size: 14px;
        }
        /* ── Sections ── */
        .section {
            margin-bottom: 64px;
            padding-top: 16px;
        }
        .section-header {
            display: flex;
            align-items: baseline;
            gap: 16px;
            margin-bottom: 24px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border);
        }
        .step-badge {
            background: var(--accent);
            color: #fff;
            font-size: 10px;
            letter-spacing: 1px;
            padding: 3px 10px;
            border-radius: 12px;
            text-transform: uppercase;
            flex-shrink: 0;
        }
        h2 {
            font-size: 20px;
            font-weight: normal;
            letter-spacing: 1px;
            color: var(--text);
        }
        h3 {
            font-size: 14px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 12px;
            margin-top: 28px;
        }
        p { margin-bottom: 12px; color: var(--text); }
        .intro-note {
            background: var(--surface2);
            border-left: 3px solid var(--accent);
            padding: 16px 20px;
            margin-bottom: 32px;
            font-size: 14px;
            color: var(--muted);
            font-style: italic;
        }
        /* ── Mark complete ── */
        .mark-done-btn {
            background: none;
            border: 1px solid var(--border);
            color: var(--muted);
            padding: 6px 14px;
            font-size: 11px;
            letter-spacing: 1px;
            cursor: pointer;
            border-radius: 4px;
            margin-left: auto;
            font-family: var(--font-serif);
            transition: all 0.2s;
        }
        .mark-done-btn:hover { border-color: var(--accent); color: var(--text); }
        .mark-done-btn.done { border-color: #4caf50; color: #4caf50; }
        /* ── Item cards ── */
        .item-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 6px;
            margin-bottom: 20px;
            overflow: hidden;
        }
        .item-card .card-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 14px 18px;
            background: var(--surface2);
            border-bottom: 1px solid var(--border);
        }
        .item-card .card-title {
            font-size: 13px;
            font-weight: bold;
            letter-spacing: 0.5px;
            color: var(--text);
        }
        .item-card .card-meta {
            font-size: 11px;
            color: var(--muted);
            font-style: italic;
        }
        .item-card .card-body { padding: 16px 18px; }
        .item-card .card-desc {
            font-size: 12px;
            color: var(--muted);
            font-style: italic;
            margin-bottom: 12px;
        }
        /* ── Code blocks ── */
        .code-block {
            background: var(--code-bg);
            border: 1px solid var(--code-border);
            border-radius: 4px;
            overflow: hidden;
        }
        .code-block .code-toolbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 14px;
            background: #0a140a;
            border-bottom: 1px solid var(--code-border);
        }
        .code-block .code-label {
            font-size: 10px;
            letter-spacing: 1.5px;
            color: #5a8a5a;
            text-transform: uppercase;
            font-family: var(--font-mono);
        }
        .code-block pre {
            padding: 14px 16px;
            font-family: var(--font-mono);
            font-size: 12px;
            color: var(--code-text);
            white-space: pre-wrap;
            word-break: break-all;
            line-height: 1.6;
        }
        /* ── Tables ── */
        .table-wrap { overflow-x: auto; margin-bottom: 8px; }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        thead th {
            background: #2c1a1a;
            color: var(--text);
            padding: 8px 12px;
            text-align: left;
            font-size: 11px;
            letter-spacing: 1px;
            text-transform: uppercase;
            border-bottom: 2px solid var(--accent);
        }
        tbody tr:nth-child(odd)  { background: var(--surface2); }
        tbody tr:nth-child(even) { background: var(--surface); }
        tbody td {
            padding: 8px 12px;
            border-bottom: 1px solid var(--border);
            vertical-align: top;
        }
        tbody td:first-child {
            width: 40px;
            text-align: center;
            font-weight: bold;
            color: var(--accent2);
            border-right: 1px solid var(--border);
        }
        /* ── Handouts ── */
        .handout-body {
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 16px 20px;
            font-size: 13px;
            white-space: pre-wrap;
            line-height: 1.8;
        }
        .keeper-badge {
            background: var(--keeper-bg);
            border: 1px solid var(--keeper-border);
            color: #c07070;
            font-size: 10px;
            padding: 2px 8px;
            border-radius: 10px;
            letter-spacing: 1px;
        }
        .public-badge {
            background: #0a1a0a;
            border: 1px solid #2a4a2a;
            color: #70c070;
            font-size: 10px;
            padding: 2px 8px;
            border-radius: 10px;
            letter-spacing: 1px;
        }
        /* ── Fragment cards ── */
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 16px;
        }
        .frag-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 16px;
        }
        .frag-card .fc-id {
            font-size: 10px;
            color: var(--accent);
            letter-spacing: 1px;
            margin-bottom: 6px;
        }
        .frag-card .fc-name {
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 6px;
        }
        .frag-card .fc-quote {
            font-size: 12px;
            font-style: italic;
            color: var(--muted);
            margin-bottom: 8px;
        }
        .frag-card .fc-text { font-size: 12px; color: var(--text); margin-bottom: 8px; }
        .frag-card .fc-cost {
            font-size: 11px;
            color: var(--accent2);
            letter-spacing: 0.5px;
        }
        /* ── Copy button ── */
        .copy-btn {
            background: none;
            border: 1px solid var(--border);
            color: var(--muted);
            padding: 4px 12px;
            font-size: 11px;
            cursor: pointer;
            border-radius: 3px;
            font-family: var(--font-serif);
            transition: all 0.2s;
            white-space: nowrap;
        }
        .copy-btn:hover  { border-color: var(--accent); color: var(--text); }
        .copy-btn.copied { border-color: #4caf50; color: #4caf50; }
        /* ── Footer ── */
        .site-footer {
            text-align: center;
            padding: 40px 0;
            border-top: 1px solid var(--border);
            color: var(--muted);
            font-size: 13px;
            font-style: italic;
            margin-top: 40px;
        }
        /* ── Scrollbar ── */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg); }
        ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
    """

    # ── JS ───────────────────────────────────────────────────────────────────
    js = """
        function copyText(id, btn) {
            const el = document.getElementById(id);
            navigator.clipboard.writeText(el.innerText || el.textContent).then(() => {
                btn.textContent = 'Copied';
                btn.classList.add('copied');
                setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
            });
        }
        function markDone(stepId, btn) {
            const navLink = document.querySelector(`nav a[href="#${stepId}"]`);
            if (navLink) navLink.classList.toggle('done');
            btn.classList.toggle('done');
            btn.textContent = btn.classList.contains('done') ? '✓ Done' : 'Mark done';
            updateProgress();
        }
        function updateProgress() {
            const total = document.querySelectorAll('nav a[href^="#step"]').length;
            const done  = document.querySelectorAll('nav a[href^="#step"].done').length;
            document.querySelector('.progress-fill').style.width = (done / total * 100) + '%';
        }
        // Active nav highlight on scroll
        window.addEventListener('scroll', () => {
            const sections = document.querySelectorAll('.section[id]');
            let current = '';
            sections.forEach(s => {
                if (window.scrollY >= s.offsetTop - 80) current = s.id;
            });
            document.querySelectorAll('nav a').forEach(a => {
                a.classList.toggle('active', a.getAttribute('href') === '#' + current);
            });
        });
    """

    # ── Costruzione sezioni ───────────────────────────────────────────────────

    def copy_btn(target_id):
        return f'<button class="copy-btn" onclick="copyText(\'{target_id}\', this)">Copy</button>'

    def section_open(step_num, step_id, title, description=''):
        desc_html = f'<p class="intro-note">{esc(description)}</p>' if description else ''
        return f'''
        <section class="section" id="{step_id}">
            <div class="section-header">
                <span class="step-badge">Step {step_num}</span>
                <h2>{esc(title)}</h2>
                <button class="mark-done-btn" onclick="markDone('{step_id}', this)">Mark done</button>
            </div>
            {desc_html}'''

    sections_html = []

    # ── Step 1: Rollable Tables ───────────────────────────────────────────────
    s = section_open(1, 'step-tables', 'Rollable Tables',
                     'In Roll20: open Collection tab > Add > Rollable Table. '
                     'Create one table per block below, copy-paste the name exactly, '
                     'then add each row as a table item.')
    for tbl in d['tables']:
        tid = f'tbl-{tbl["id"]}'
        s += f'''
        <div class="item-card">
            <div class="card-head">
                <span class="card-title">{esc(tbl["name"])}</span>
                <span class="card-meta">{esc(tbl["dice"])}</span>
                {copy_btn(tid + "-name")}
            </div>
            <div class="card-body">
                <div class="card-desc">{esc(tbl["description"])}</div>
                <h3>Table Name</h3>
                <div class="code-block">
                    <div class="code-toolbar">
                        <span class="code-label">copy exactly</span>
                        {copy_btn(tid + "-name")}
                    </div>
                    <pre id="{tid}-name">{esc(tbl["name"])}</pre>
                </div>
                <h3>Rows</h3>
                <div class="table-wrap">
                    <table>
                        <thead><tr><th>#</th><th>Text</th></tr></thead>
                        <tbody>{_table_rows_html(tbl["rows"])}</tbody>
                    </table>
                </div>
            </div>
        </div>'''
    s += '</section>'
    sections_html.append(s)

    # ── Step 2: Macros ────────────────────────────────────────────────────────
    s = section_open(2, 'step-macros', 'Macros',
                     'In Roll20: open Collection tab > Add Macro. '
                     'Copy the macro name exactly, paste the code, check "In Bar" if desired.')
    for mac in d['macros']:
        mid = f'mac-{mac["name"].replace(" ", "-")}'
        s += f'''
        <div class="item-card">
            <div class="card-head">
                <span class="card-title">{esc(mac["name"])}</span>
                <span class="card-meta">{esc(mac["description"])}</span>
            </div>
            <div class="card-body">
                <h3>Macro Name</h3>
                <div class="code-block">
                    <div class="code-toolbar">
                        <span class="code-label">copy exactly</span>
                        {copy_btn(mid + "-name")}
                    </div>
                    <pre id="{mid}-name">{esc(mac["name"])}</pre>
                </div>
                <h3>Macro Code</h3>
                <div class="code-block">
                    <div class="code-toolbar">
                        <span class="code-label">macro</span>
                        {copy_btn(mid + "-code")}
                    </div>
                    <pre id="{mid}-code">{esc(mac["code"].strip())}</pre>
                </div>
            </div>
        </div>'''
    s += '</section>'
    sections_html.append(s)

    # ── Step 3: Handouts ──────────────────────────────────────────────────────
    s = section_open(3, 'step-handouts', 'Handouts',
                     'In Roll20: open Journal tab > Add > Handout. '
                     'Copy the title and body into the handout. '
                     'Keeper-only handouts: set "Can Be Edited By" to GM only and do not share with players.')
    for ho in d['handouts']:
        hid = f'ho-{ho["id"]}'
        badge = ('<span class="keeper-badge">KEEPER ONLY</span>'
                 if ho['visibility'] == 'keeper'
                 else '<span class="public-badge">PUBLIC</span>')
        s += f'''
        <div class="item-card">
            <div class="card-head">
                <span class="card-title">{esc(ho["title"])}</span>
                {badge}
                {copy_btn(hid + "-body")}
            </div>
            <div class="card-body">
                <h3>Title</h3>
                <div class="code-block">
                    <div class="code-toolbar">
                        <span class="code-label">copy exactly</span>
                        {copy_btn(hid + "-title")}
                    </div>
                    <pre id="{hid}-title">{esc(ho["title"])}</pre>
                </div>
                <h3>Body</h3>
                <div class="code-block">
                    <div class="code-toolbar">
                        <span class="code-label">handout text</span>
                        {copy_btn(hid + "-body")}
                    </div>
                    <pre id="{hid}-body">{esc(ho["body"].strip())}</pre>
                </div>
            </div>
        </div>'''
    s += '</section>'
    sections_html.append(s)

    # ── Step 4: Card Decks ────────────────────────────────────────────────────
    s = section_open(4, 'step-cards', 'Card Decks',
                     'In Roll20: open Collection tab > Add Deck. '
                     'Create one deck per act (Act I, Act II, Act III). '
                     'Add each card with the name and description below. '
                     'During play, deal (players + 1) cards face-up to the table each cycle.')
    for deck in d['card_decks']:
        s += f'''
        <h3>{esc(deck["name"])}</h3>
        <p class="card-desc">{esc(deck["description"])}</p>
        <p style="font-size:12px;color:var(--muted);font-style:italic;margin-bottom:16px;">{esc(deck["setup"])}</p>
        <div class="cards-grid">'''
        for card in deck['cards']:
            s += f'''
            <div class="frag-card">
                <div class="fc-id">{esc(card["id"])}</div>
                <div class="fc-name">{esc(card["name"])}</div>
                <div class="fc-quote">{esc(card["quote"])}</div>
                <div class="fc-text">{esc(card["text"])}</div>
                <div class="fc-cost">{esc(card["cost"])}</div>
            </div>'''
        s += '</div>'
    s += '</section>'
    sections_html.append(s)

    # ── Step 5: Character Sheet ────────────────────────────────────────────────
    s = section_open(5, 'step-sheet', 'Character Sheet',
                     'Upload anamnesia_character_sheet.html to Roll20: '
                     'Game Settings > Character Sheet Template > Custom. '
                     'Paste the entire contents of the file into the HTML Layout field.')
    s += '''
        <p>The character sheet file is included separately in this ZIP as
        <strong>character_sheet/anamnesia_character_sheet.html</strong>.</p>
        <h3>Attributes used by macros</h3>
        <div class="table-wrap">
            <table>
                <thead><tr><th>Attribute</th><th>Description</th></tr></thead>
                <tbody>
                    <tr><td>pool_base</td><td>Archetype base pool (4 or 5)</td></tr>
                    <tr><td>stress</td><td>Current Stress points (0–5)</td></tr>
                    <tr><td>echo_penalty</td><td>Calculated Echo penalty (0, 1, or 3)</td></tr>
                    <tr><td>echoes</td><td>Total Echo count</td></tr>
                </tbody>
            </table>
        </div>
        <h3>Pool macros that reference sheet attributes</h3>
        <p style="font-size:13px;color:var(--muted);">
            Macros like <code>AnamnesiA_Pool</code> use @{pool_base}, @{stress}, @{echo_penalty}.
            These will only work if the character sheet is installed. For games without the sheet,
            use <code>AnamnesiA_Roll</code> or <code>AnamnesiA_Roll_Full</code> which take manual input.
        </p>
    </section>'''
    sections_html.append(s)

    # ── Nav links ─────────────────────────────────────────────────────────────
    step_links = [
        ('#step-tables',  '1', 'Rollable Tables'),
        ('#step-macros',  '2', 'Macros'),
        ('#step-handouts','3', 'Handouts'),
        ('#step-cards',   '4', 'Card Decks'),
        ('#step-sheet',   '5', 'Character Sheet'),
    ]
    nav_links = ''
    for href, num, label in step_links:
        nav_links += f'''
            <a href="{href}">
                <span class="step-num">{num}</span>
                {esc(label)}
                <span class="check">✓</span>
            </a>'''

    # ── Assemblaggio HTML finale ──────────────────────────────────────────────
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AnamnesiA — Roll20 Setup Guide</title>
<style>{css}</style>
</head>
<body>

<nav>
    <div class="brand">A N A M N E S I A</div>
    <div class="progress-bar"><div class="progress-fill"></div></div>
    {nav_links}
</nav>

<main>
    <header class="site-header">
        <div class="eyebrow">Roll20 Digital Pack</div>
        <h1>AnamnesiA</h1>
        <div class="subtitle">Setup Guide &amp; Assets &mdash; Step-by-step Roll20 configuration</div>
    </header>

    {"".join(sections_html)}

    <footer class="site-footer">
        {esc(d["closing_quote"])}<br><br>
        &copy; 2026 Riccardo Scaringi &middot; ilgiocointavolo &middot; ioGioco
    </footer>
</main>

<script>{js}</script>
</body>
</html>"""


def build_character_sheet():
    """Genera il character sheet HTML per Roll20."""
    return """<!DOCTYPE html>
<html>
<head>
<style>
  /* AnamnesiA Character Sheet for Roll20 */
  .sheet-root {
    background: #1a1410;
    color: #e8ddd0;
    font-family: 'Palatino Linotype', Georgia, serif;
    padding: 12px;
    font-size: 13px;
    line-height: 1.5;
  }
  .sheet-title {
    text-align: center;
    font-size: 18px;
    letter-spacing: 3px;
    color: #c0392b;
    border-bottom: 1px solid #3a2d1e;
    padding-bottom: 8px;
    margin-bottom: 12px;
  }
  .sheet-row { display: flex; gap: 10px; margin-bottom: 8px; align-items: center; }
  .sheet-label {
    font-size: 10px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #8a7a6a;
    min-width: 90px;
  }
  input[type=text], select {
    background: #0b0907;
    border: 1px solid #3a2d1e;
    color: #e8ddd0;
    padding: 4px 8px;
    font-family: inherit;
    font-size: 13px;
    border-radius: 3px;
    flex: 1;
  }
  input[type=number] {
    background: #0b0907;
    border: 1px solid #3a2d1e;
    color: #e8ddd0;
    padding: 4px 8px;
    font-family: inherit;
    font-size: 13px;
    border-radius: 3px;
    width: 60px;
    text-align: center;
  }
  .sheet-section {
    background: #130f0a;
    border: 1px solid #3a2d1e;
    border-radius: 4px;
    padding: 10px 14px;
    margin-bottom: 10px;
  }
  .sheet-section-title {
    font-size: 10px;
    letter-spacing: 2px;
    color: #8b1a1a;
    text-transform: uppercase;
    margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid #3a2d1e;
  }
  .pool-display {
    font-size: 20px;
    font-weight: bold;
    color: #c0392b;
    text-align: center;
    padding: 6px;
    background: #0b0907;
    border: 1px solid #3a2d1e;
    border-radius: 4px;
    min-width: 60px;
  }
  .checkbox-row { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
  input[type=checkbox] { width: 16px; height: 16px; cursor: pointer; accent-color: #8b1a1a; }
  .hint { font-size: 11px; color: #5a4a3a; font-style: italic; margin-top: 4px; }
  .approach-row { margin-bottom: 6px; }
  .approach-cost { color: #8b1a1a; font-weight: bold; min-width: 30px; }
  .archetype-quote {
    font-style: italic;
    color: #8b1a1a;
    text-align: center;
    font-size: 12px;
    margin: 4px 0 10px;
  }
  button.sheet-roll-btn {
    background: #8b1a1a;
    border: none;
    color: #fff;
    padding: 6px 16px;
    font-family: inherit;
    font-size: 12px;
    letter-spacing: 1px;
    cursor: pointer;
    border-radius: 3px;
    width: 100%;
    margin-top: 6px;
  }
  button.sheet-roll-btn:hover { background: #a52020; }
</style>
</head>
<body>
<div class="sheet-root">

  <div class="sheet-title">A N A M N E S I A</div>

  <!-- Identity -->
  <div class="sheet-section">
    <div class="sheet-section-title">Identity</div>
    <div class="sheet-row">
      <span class="sheet-label">Name</span>
      <input type="text" name="attr_character_name" placeholder="Character name">
    </div>
    <div class="sheet-row">
      <span class="sheet-label">Archetype</span>
      <select name="attr_archetype">
        <option value="survivor">The Survivor (Pool 5)</option>
        <option value="witness">The Witness (Pool 5)</option>
        <option value="protector">The Protector (Pool 4)</option>
        <option value="catalyst">The Catalyst (Pool 4)</option>
      </select>
    </div>
    <div class="sheet-row">
      <span class="sheet-label">Anchor</span>
      <input type="text" name="attr_anchor" placeholder="A physical object that ties you to reality">
    </div>
    <div class="sheet-row">
      <span class="sheet-label">Scenario</span>
      <input type="text" name="attr_scenario" placeholder="The Incident / The Betrayal / ...">
    </div>
  </div>

  <!-- Pool & Stats -->
  <div class="sheet-section">
    <div class="sheet-section-title">Pool &amp; Status</div>
    <div class="sheet-row">
      <span class="sheet-label">Pool Base</span>
      <select name="attr_pool_base">
        <option value="5">5 (Survivor / Witness)</option>
        <option value="4">4 (Protector / Catalyst)</option>
      </select>
    </div>
    <div class="sheet-row">
      <span class="sheet-label">Stress</span>
      <input type="number" name="attr_stress" value="0" min="0" max="5">
      <span style="font-size:11px;color:#8a7a6a;margin-left:8px;">4=Partial Breakdown &bull; 5=Final</span>
    </div>
    <div class="sheet-row">
      <span class="sheet-label">Echoes</span>
      <input type="number" name="attr_echoes" value="0" min="0">
      <span style="font-size:11px;color:#8a7a6a;margin-left:8px;">0–2: 0 &bull; 3–5: –1d &bull; 6–8: –3d &bull; 9+: out</span>
    </div>
    <div class="sheet-row">
      <span class="sheet-label">Echo Penalty</span>
      <select name="attr_echo_penalty">
        <option value="0">0 (Echoes 0–2)</option>
        <option value="1">1 (Echoes 3–5)</option>
        <option value="3">3 (Echoes 6–8)</option>
        <option value="99">Out of play (Echoes 9+)</option>
      </select>
    </div>
    <div class="hint">Pool = Base – Stress – Echo Penalty (min 1)</div>
  </div>

  <!-- One-use mechanics -->
  <div class="sheet-section">
    <div class="sheet-section-title">One-Use Mechanics</div>
    <div class="sheet-row">
      <input type="checkbox" name="attr_anchor_used" value="1">
      <span>Anchor invoked (1&times;/game)</span>
    </div>
    <div class="sheet-row">
      <input type="checkbox" name="attr_last_memory_used" value="1">
      <span>Last Memory used (1&times;/game)</span>
    </div>
    <div class="sheet-row">
      <input type="checkbox" name="attr_guilt_used" value="1">
      <span>Sense of Guilt used — Catalyst only (1&times;/game)</span>
    </div>
    <div class="sheet-section-title" style="margin-top:10px;">Vulnerability (max 1/cycle)</div>
    <div class="checkbox-row">
      <input type="checkbox" name="attr_vuln_c1" value="1"><span>C1</span>
      <input type="checkbox" name="attr_vuln_c2" value="1"><span>C2</span>
      <input type="checkbox" name="attr_vuln_c3" value="1"><span>C3</span>
      <input type="checkbox" name="attr_vuln_c4" value="1"><span>C4</span>
      <input type="checkbox" name="attr_vuln_c5" value="1"><span>C5</span>
    </div>
    <div class="sheet-section-title" style="margin-top:10px;">Current Cycle</div>
    <div class="checkbox-row">
      <input type="checkbox" name="attr_cycle1" value="1"><span>1</span>
      <input type="checkbox" name="attr_cycle2" value="1"><span>2</span>
      <input type="checkbox" name="attr_cycle3" value="1"><span>3</span>
      <input type="checkbox" name="attr_cycle4" value="1"><span>4</span>
      <input type="checkbox" name="attr_cycle5" value="1"><span>5</span>
    </div>
  </div>

  <!-- Roll button -->
  <div class="sheet-section">
    <div class="sheet-section-title">Quick Roll</div>
    <button type="roll" name="roll_memory" class="sheet-roll-btn"
      value="&{template:default} {{name=MEMORY ROLL}} {{roll=[[?{Dice to invest|1|2|3|4}d6]]}} {{note=5–6 Clear · 3–4 Confused · 1–2 Traumatic +1 Echo}} {{right_hand=Player to your RIGHT interprets.}}">
      Roll Memory
    </button>
  </div>

  <!-- Notes -->
  <div class="sheet-section">
    <div class="sheet-section-title">Memories &amp; Notes</div>
    <textarea name="attr_notes" style="width:100%;min-height:80px;background:#0b0907;border:1px solid #3a2d1e;color:#e8ddd0;padding:8px;font-family:inherit;font-size:12px;border-radius:3px;resize:vertical;" placeholder="Fragments recovered, connections made, echoes..."></textarea>
  </div>

</div>
</body>
</html>"""


# ── Build principale ──────────────────────────────────────────────────────────

def build(lang):
    """Entry point chiamato da build_all.py. Solo EN viene processato."""
    if lang != ROLL20_ONLY_LANG:
        return

    d = load(lang)

    out_dir = os.path.join(OUTPUT_DIR, lang)
    os.makedirs(out_dir, exist_ok=True)
    zip_path = os.path.join(out_dir, '07_roll20_pack.zip')

    setup_html      = build_setup_guide(d)
    charsheet_html  = build_character_sheet()

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('AnamnesiA_Roll20_Pack/SETUP_GUIDE.html',                        setup_html)
        zf.writestr('AnamnesiA_Roll20_Pack/character_sheet/anamnesia_character_sheet.html', charsheet_html)

    print(f'  ✓  07_roll20_pack.zip  [{os.path.getsize(zip_path) // 1024} KB]')


# ── Esecuzione diretta ────────────────────────────────────────────────────────

if __name__ == '__main__':
    lang = sys.argv[1] if len(sys.argv) > 1 else 'en'
    build(lang)
