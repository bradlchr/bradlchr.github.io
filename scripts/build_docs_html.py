#!/usr/bin/env python3
"""
Compiles all markdown documentation files in docs/ into an interactive, 
zero-build single-file HTML documentation browser: docs/index.html
"""

import os
import json
import re

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir = os.path.join(root_dir, 'docs')
    output_html_path = os.path.join(docs_dir, 'index.html')

    docs_order = [
        {
            "id": "index",
            "file": "INDEX.md",
            "title": "Documentation Overview",
            "subtitle": "Suite Index, Architecture Overview & Quick Links",
            "icon": "book-open",
            "badge": "Start Here"
        },
        {
            "id": "architecture",
            "file": "ARCHITECTURE.md",
            "title": "System Architecture",
            "subtitle": "Multi-Platform MVVM + UDF & Web Architecture",
            "icon": "layers",
            "badge": "Core Arch"
        },
        {
            "id": "data-models",
            "file": "DATA_MODELS_AND_FIRESTORE.md",
            "title": "Data Models & Firestore",
            "subtitle": "185 Native Species, Typed Fields & Firestore Rules",
            "icon": "database",
            "badge": "185 Species"
        },
        {
            "id": "api-services",
            "file": "API_AND_SERVICES.md",
            "title": "API & Services Reference",
            "subtitle": "Repositories, ViewModels, Scrapers & Report Engines",
            "icon": "code-2",
            "badge": "Contract"
        },
        {
            "id": "ui-design",
            "file": "UI_AND_ADAPTIVE_DESIGN.md",
            "title": "UI & Adaptive Design",
            "subtitle": "WindowSizeClass, Mesh Gradients & Frosted Glass",
            "icon": "palette",
            "badge": "Design System"
        },
        {
            "id": "web-app",
            "file": "WEB_APPLICATION_AND_DEPLOYMENT.md",
            "title": "Web App & GitHub Pages",
            "subtitle": "Single-File Web App, Mobile Safari & OAuth",
            "icon": "globe",
            "badge": "Live Site"
        },
        {
            "id": "operations",
            "file": "MAINTENANCE_AND_OPERATIONS.md",
            "title": "Operations & Runbooks",
            "subtitle": "Build Workflows, Backups & Disaster Recovery",
            "icon": "wrench",
            "badge": "Runbooks"
        }
    ]

    docs_payload = {}
    for item in docs_order:
        file_path = os.path.join(docs_dir, item["file"])
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            docs_payload[item["id"]] = {
                "id": item["id"],
                "file": item["file"],
                "title": item["title"],
                "subtitle": item["subtitle"],
                "icon": item["icon"],
                "badge": item["badge"],
                "markdown": content
            }
        else:
            print(f"Warning: File {file_path} not found.")

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Deep Roots Nature Advisor — Technical Documentation</title>
  
  <!-- Fonts & Icons -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Lora:ital,wght@0,500;0,600;1,400;1,600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/lucide@latest"></script>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

  <style>
    :root {{
      --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-serif: 'Lora', Georgia, serif;
      --font-mono: 'JetBrains Mono', monospace;

      /* Botanical Light Palette */
      --bg-base: #f6f8f5;
      --bg-surface: #ffffff;
      --bg-surface-elevated: #f0f4ee;
      --border-subtle: #e2e8df;
      --border-strong: #c8d4c4;
      --text-main: #142217;
      --text-secondary: #4a5c4d;
      --text-muted: #728475;
      
      --primary: #2e7d32;
      --primary-hover: #1b5e20;
      --primary-light: rgba(46, 125, 50, 0.1);
      --accent-sweet16: #0d9488;
      --accent-keystone: #2e7d32;
      --accent-orange: #e65100;
      
      --code-bg: #1e2621;
      --code-text: #e6f4ea;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
      --shadow-md: 0 4px 14px rgba(0,0,0,0.08);
      --shadow-lg: 0 10px 25px rgba(0,0,0,0.12);
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 16px;
    }}

    body[data-theme="dark"], [data-theme="dark"] {{
      --bg-base: #0f1611;
      --bg-surface: #152018;
      --bg-surface-elevated: #1a271e;
      --border-subtle: #243528;
      --border-strong: #334838;
      --text-main: #edf5ee;
      --text-secondary: #a8baa9;
      --text-muted: #728475;

      --primary: #4caf50;
      --primary-hover: #81c784;
      --primary-light: rgba(76, 175, 80, 0.15);
      --accent-sweet16: #2dd4bf;
      --accent-keystone: #81c784;
      --accent-orange: #ff9800;

      --code-bg: #090e0a;
      --code-text: #dcfce7;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
      --shadow-md: 0 4px 14px rgba(0,0,0,0.35);
      --shadow-lg: 0 10px 25px rgba(0,0,0,0.5);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: var(--font-sans);
      background: var(--bg-base);
      color: var(--text-main);
      line-height: 1.6;
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
      -webkit-font-smoothing: antialiased;
    }}

    /* Top Navigation Header */
    .top-header {{
      height: 60px;
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
      flex-shrink: 0;
      z-index: 50;
    }}

    .header-brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: var(--text-main);
    }}

    .header-brand-icon {{
      width: 34px;
      height: 34px;
      border-radius: var(--radius-md);
      background: var(--primary);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      font-weight: 800;
      box-shadow: 0 2px 8px rgba(46,125,50,0.25);
    }}

    .header-title-group h1 {{
      font-size: 15px;
      font-weight: 800;
      letter-spacing: -0.01em;
      line-height: 1.2;
    }}

    .header-title-group p {{
      font-size: 11px;
      color: var(--text-muted);
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .search-box {{
      position: relative;
      width: 280px;
    }}

    .search-box input {{
      width: 100%;
      height: 34px;
      padding: 0 10px 0 32px;
      border-radius: 999px;
      border: 1px solid var(--border-subtle);
      background: var(--bg-base);
      color: var(--text-main);
      font-size: 12px;
      font-family: var(--font-sans);
      outline: none;
      transition: all 0.15s ease;
    }}

    .search-box input:focus {{
      border-color: var(--primary);
      background: var(--bg-surface);
      box-shadow: 0 0 0 3px var(--primary-light);
    }}

    .search-box i {{
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      width: 14px;
      height: 14px;
      color: var(--text-muted);
    }}

    .btn-nav {{
      height: 34px;
      padding: 0 12px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      text-decoration: none;
      cursor: pointer;
      border: 1px solid var(--border-subtle);
      background: var(--bg-surface);
      color: var(--text-main);
      transition: all 0.15s ease;
    }}

    .btn-nav:hover {{
      background: var(--bg-surface-elevated);
      border-color: var(--border-strong);
    }}

    .btn-nav.primary {{
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
    }}

    .btn-nav.primary:hover {{
      background: var(--primary-hover);
    }}

    .btn-icon {{
      width: 34px;
      height: 34px;
      padding: 0;
      border-radius: 50%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border: 1px solid var(--border-subtle);
      background: var(--bg-surface);
      color: var(--text-main);
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .btn-icon:hover {{
      background: var(--bg-surface-elevated);
    }}

    /* Main Container with 3 Panels */
    .docs-container {{
      display: flex;
      flex: 1;
      height: calc(100vh - 60px);
      overflow: hidden;
    }}

    /* Left Sidebar: Document List */
    .sidebar-left {{
      width: 290px;
      background: var(--bg-surface);
      border-right: 1px solid var(--border-subtle);
      overflow-y: auto;
      padding: 16px 12px;
      flex-shrink: 0;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .sidebar-heading {{
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-muted);
      padding: 8px 12px 4px;
      margin-top: 6px;
    }}

    .doc-nav-item {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 12px;
      border-radius: var(--radius-md);
      text-decoration: none;
      color: var(--text-main);
      font-size: 13px;
      font-weight: 600;
      transition: all 0.15s ease;
      cursor: pointer;
      user-select: none;
    }}

    .doc-nav-item:hover {{
      background: var(--bg-surface-elevated);
    }}

    .doc-nav-item.active {{
      background: var(--primary-light);
      color: var(--primary);
      font-weight: 700;
    }}

    .doc-nav-left {{
      display: flex;
      align-items: center;
      gap: 10px;
      min-width: 0;
    }}

    .doc-nav-left i {{
      width: 16px;
      height: 16px;
      flex-shrink: 0;
    }}

    .doc-nav-left span {{
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .doc-nav-badge {{
      font-size: 10px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 999px;
      background: var(--bg-surface-elevated);
      color: var(--text-muted);
      border: 1px solid var(--border-subtle);
      flex-shrink: 0;
    }}

    .doc-nav-item.active .doc-nav-badge {{
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
    }}

    /* Main Article Content Area */
    .content-center {{
      flex: 1;
      overflow-y: auto;
      padding: 36px 48px 80px;
      background: var(--bg-surface);
      scroll-behavior: smooth;
    }}

    .article-wrapper {{
      max-width: 820px;
      margin: 0 auto;
    }}

    /* Right Sidebar: Table of Contents */
    .sidebar-right {{
      width: 250px;
      background: var(--bg-surface);
      border-left: 1px solid var(--border-subtle);
      overflow-y: auto;
      padding: 24px 16px;
      flex-shrink: 0;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .toc-title {{
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .toc-link {{
      font-size: 12px;
      color: var(--text-secondary);
      text-decoration: none;
      padding: 5px 8px;
      border-radius: var(--radius-sm);
      display: block;
      line-height: 1.4;
      transition: all 0.12s ease;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .toc-link:hover {{
      color: var(--primary);
      background: var(--bg-surface-elevated);
    }}

    .toc-link.indent {{
      padding-left: 18px;
      font-size: 11.5px;
    }}

    /* Markdown Render Styling */
    .markdown-body {{
      font-size: 15px;
      line-height: 1.7;
      color: var(--text-main);
    }}

    .markdown-body h1 {{
      font-family: var(--font-serif);
      font-size: 28px;
      font-weight: 700;
      line-height: 1.25;
      margin-bottom: 14px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border-subtle);
      color: var(--text-main);
    }}

    .markdown-body h2 {{
      font-size: 20px;
      font-weight: 800;
      margin-top: 36px;
      margin-bottom: 14px;
      padding-bottom: 6px;
      border-bottom: 1px solid var(--border-subtle);
      color: var(--text-main);
      scroll-margin-top: 20px;
    }}

    .markdown-body h3 {{
      font-size: 16px;
      font-weight: 700;
      margin-top: 24px;
      margin-bottom: 10px;
      color: var(--text-main);
      scroll-margin-top: 20px;
    }}

    .markdown-body p {{
      margin-bottom: 16px;
      color: var(--text-secondary);
    }}

    .markdown-body ul, .markdown-body ol {{
      margin-bottom: 18px;
      padding-left: 24px;
      color: var(--text-secondary);
    }}

    .markdown-body li {{
      margin-bottom: 6px;
    }}

    .markdown-body li > strong {{
      color: var(--text-main);
    }}

    .markdown-body blockquote {{
      border-left: 4px solid var(--primary);
      padding: 10px 16px;
      margin: 18px 0;
      background: var(--bg-surface-elevated);
      border-radius: 0 var(--radius-md) var(--radius-md) 0;
      font-size: 14px;
      color: var(--text-secondary);
    }}

    .markdown-body hr {{
      border: 0;
      height: 1px;
      background: var(--border-subtle);
      margin: 32px 0;
    }}

    .markdown-body a {{
      color: var(--primary);
      text-decoration: underline;
      text-underline-offset: 3px;
      font-weight: 600;
    }}

    .markdown-body a:hover {{
      color: var(--primary-hover);
    }}

    .markdown-body table {{
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0 24px;
      font-size: 13px;
    }}

    .markdown-body th, .markdown-body td {{
      padding: 10px 12px;
      border: 1px solid var(--border-subtle);
      text-align: left;
    }}

    .markdown-body th {{
      background: var(--bg-surface-elevated);
      font-weight: 700;
      color: var(--text-main);
    }}

    .markdown-body tr:nth-child(even) {{
      background: var(--bg-base);
    }}

    /* Code Blocks */
    .markdown-body pre {{
      background: var(--code-bg);
      color: var(--code-text);
      padding: 16px;
      border-radius: var(--radius-md);
      overflow-x: auto;
      font-family: var(--font-mono);
      font-size: 12.5px;
      line-height: 1.5;
      margin: 18px 0 24px;
      position: relative;
    }}

    .markdown-body code {{
      font-family: var(--font-mono);
      font-size: 12.5px;
      background: var(--bg-surface-elevated);
      padding: 2px 6px;
      border-radius: 4px;
      color: var(--primary);
    }}

    .markdown-body pre code {{
      background: transparent;
      padding: 0;
      color: inherit;
    }}

    .copy-btn {{
      position: absolute;
      top: 10px;
      right: 10px;
      padding: 4px 8px;
      font-size: 10px;
      font-weight: 700;
      border-radius: 4px;
      border: 1px solid rgba(255,255,255,0.2);
      background: rgba(0,0,0,0.5);
      color: #fff;
      cursor: pointer;
      opacity: 0;
      transition: opacity 0.15s ease;
    }}

    .markdown-body pre:hover .copy-btn {{
      opacity: 1;
    }}

    /* Alert Boxes (GitHub style) */
    .markdown-body blockquote:has(strong:first-child) {{
      background: var(--bg-surface-elevated);
    }}

    /* Pagination Bar at bottom of doc */
    .doc-pagination {{
      display: flex;
      justify-content: space-between;
      margin-top: 48px;
      padding-top: 24px;
      border-top: 1px solid var(--border-subtle);
    }}

    .page-btn {{
      display: flex;
      flex-direction: column;
      gap: 4px;
      text-decoration: none;
      padding: 12px 18px;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-subtle);
      background: var(--bg-surface);
      color: var(--text-main);
      max-width: 48%;
      transition: all 0.15s ease;
    }}

    .page-btn:hover {{
      background: var(--bg-surface-elevated);
      border-color: var(--border-strong);
    }}

    .page-btn-label {{
      font-size: 11px;
      color: var(--text-muted);
      text-transform: uppercase;
      font-weight: 700;
    }}

    .page-btn-title {{
      font-size: 14px;
      font-weight: 700;
      color: var(--primary);
    }}

    /* Mobile Responsive */
    @media (max-width: 900px) {{
      .sidebar-right {{
        display: none;
      }}
      .content-center {{
        padding: 24px 20px 60px;
      }}
      .search-box {{
        width: 180px;
      }}
    }}

    @media (max-width: 640px) {{
      .sidebar-left {{
        position: fixed;
        left: -300px;
        top: 60px;
        bottom: 0;
        z-index: 100;
        transition: left 0.25s ease;
        box-shadow: var(--shadow-lg);
      }}
      .sidebar-left.open {{
        left: 0;
      }}
      .search-box {{
        display: none;
      }}
    }}
  </style>
</head>
<body>

  <!-- Top Navigation Header -->
  <header class="top-header">
    <div style="display:flex;align-items:center;gap:12px;">
      <button id="mobileMenuBtn" class="btn-icon" style="display:none;" title="Toggle Sidebar">
        <i data-lucide="menu"></i>
      </button>
      <a href="#index" class="header-brand">
        <div class="header-brand-icon">🌱</div>
        <div class="header-title-group">
          <h1>Deep Roots Nature Advisor</h1>
          <p>Technical Documentation Suite</p>
        </div>
      </a>
    </div>

    <div class="header-actions">
      <div class="search-box">
        <i data-lucide="search"></i>
        <input type="text" id="docsSearchInput" placeholder="Search documentation...">
      </div>

      <a href="../index.html" target="_blank" class="btn-nav primary" title="Open Live Web App">
        <i data-lucide="globe"></i>
        <span>Live App</span>
      </a>

      <button id="themeToggleBtn" class="btn-icon" title="Toggle Dark/Light Mode">
        <i data-lucide="moon" id="themeIcon"></i>
      </button>
    </div>
  </header>

  <!-- Main Container -->
  <div class="docs-container">
    
    <!-- Left Sidebar: Chapter List -->
    <aside class="sidebar-left" id="sidebarLeft">
      <div class="sidebar-heading">Documentation Chapters</div>
      <div id="docNavList"></div>

      <div class="sidebar-heading" style="margin-top:20px;">Direct Links</div>
      <a href="../index.html" class="doc-nav-item" target="_blank">
        <div class="doc-nav-left">
          <i data-lucide="external-link"></i>
          <span>Web Application</span>
        </div>
        <span class="doc-nav-badge">App</span>
      </a>
      <a href="../firestore.rules" class="doc-nav-item" target="_blank">
        <div class="doc-nav-left">
          <i data-lucide="shield-check"></i>
          <span>Firestore Security Rules</span>
        </div>
        <span class="doc-nav-badge">Rules</span>
      </a>
      <a href="https://console.cloud.google.com/firestore/databases/deep-roots-nature-advisors/data/panel/plants?project=deep-roots-nature-advisors" target="_blank" class="doc-nav-item">
        <div class="doc-nav-left">
          <i data-lucide="database"></i>
          <span>Google Cloud Firestore</span>
        </div>
        <span class="doc-nav-badge">GCP</span>
      </a>
    </aside>

    <!-- Center Content Article -->
    <main class="content-center" id="mainContent">
      <div class="article-wrapper">
        <div id="articleBody" class="markdown-body"></div>
        <div id="docPagination" class="doc-pagination"></div>
      </div>
    </main>

    <!-- Right Sidebar: Table of Contents -->
    <aside class="sidebar-right" id="sidebarRight">
      <div class="toc-title">
        <i data-lucide="list"></i>
        <span>On This Page</span>
      </div>
      <div id="tocList"></div>
    </aside>

  </div>

  <!-- Embedded Documentation Data -->
  <script id="embeddedDocsData" type="application/json">
{json.dumps(docs_payload, indent=2)}
  </script>

  <!-- Interactive Client Engine -->
  <script>
    const DOCS_DATA = JSON.parse(document.getElementById('embeddedDocsData').textContent);
    const DOCS_KEYS = Object.keys(DOCS_DATA);
    let currentDocId = 'index';

    // Theme Management
    const themeBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const savedTheme = localStorage.getItem('dr_docs_theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    document.body.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    themeBtn.addEventListener('click', () => {{
      const cur = document.body.getAttribute('data-theme');
      const next = cur === 'dark' ? 'light' : 'dark';
      document.body.setAttribute('data-theme', next);
      localStorage.setItem('dr_docs_theme', next);
      updateThemeIcon(next);
    }});

    function updateThemeIcon(t) {{
      themeIcon.setAttribute('data-lucide', t === 'dark' ? 'sun' : 'moon');
      if (window.lucide) lucide.createIcons();
    }}

    // Render Navigation Sidebar
    function renderNavList() {{
      const container = document.getElementById('docNavList');
      container.innerHTML = '';

      DOCS_KEYS.forEach(key => {{
        const item = DOCS_DATA[key];
        const a = document.createElement('a');
        a.className = `doc-nav-item ${{key === currentDocId ? 'active' : ''}}`;
        a.href = `#${{key}}`;
        a.innerHTML = `
          <div class="doc-nav-left">
            <i data-lucide="${{item.icon}}"></i>
            <span>${{item.title}}</span>
          </div>
          <span class="doc-nav-badge">${{item.badge}}</span>
        `;
        a.addEventListener('click', (e) => {{
          e.preventDefault();
          loadDocument(key);
        }});
        container.appendChild(a);
      }});
      if (window.lucide) lucide.createIcons();
    }}

    // Fallback Simple Markdown Parser in case CDN marked is blocked
    function simpleMarkdownParser(md) {{
      let html = md
        .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
        .replace(/^### (.*$)/gim, '<h3 id="$1">$1</h3>')
        .replace(/^## (.*$)/gim, '<h2 id="$1">$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/\\*\\*(.*?)\\*\\*/gim, '<strong>$1</strong>')
        .replace(/\\*(.*?)\\*/gim, '<em>$1</em>')
        .replace(/```([a-z]*)\\n([\\s\\S]*?)\\n```/gim, '<pre><code>$2</code></pre>')
        .replace(/`([^`]+)`/gim, '<code>$1</code>')
        .replace(/^\\> (.*$)/gim, '<blockquote>$1</blockquote>')
        .replace(/\\n\\n/gim, '</p><p>');
      return '<p>' + html + '</p>';
    }}

    function renderMarkdownToHtml(md) {{
      if (window.marked && typeof marked.parse === 'function') {{
        return marked.parse(md);
      }}
      return simpleMarkdownParser(md);
    }}

    // Load Document
    function loadDocument(docId, scrollToId = null) {{
      if (!DOCS_DATA[docId]) docId = 'index';
      currentDocId = docId;
      window.location.hash = docId + (scrollToId ? `#${{scrollToId}}` : '');

      const doc = DOCS_DATA[docId];
      document.title = `${{doc.title}} — Deep Roots Documentation`;

      // Render Markdown
      const html = renderMarkdownToHtml(doc.markdown);
      const article = document.getElementById('articleBody');
      article.innerHTML = html;

      // Rewire internal markdown links (e.g. ./ARCHITECTURE.md -> #architecture)
      article.querySelectorAll('a').forEach(link => {{
        const href = link.getAttribute('href') || '';
        if (href.endsWith('.md') || href.includes('.md#')) {{
          link.addEventListener('click', (e) => {{
            e.preventDefault();
            const parts = href.replace(/^\\.\\//, '').split('#');
            const targetFile = parts[0];
            const targetAnchor = parts[1] || null;
            const targetKey = Object.keys(DOCS_DATA).find(k => DOCS_DATA[k].file.toLowerCase() === targetFile.toLowerCase());
            if (targetKey) {{
              loadDocument(targetKey, targetAnchor);
            }}
          }});
        }}
      }});

      // Add copy buttons to pre blocks
      article.querySelectorAll('pre').forEach(pre => {{
        const btn = document.createElement('button');
        btn.className = 'copy-btn';
        btn.textContent = 'Copy';
        btn.addEventListener('click', () => {{
          const code = pre.querySelector('code')?.innerText || pre.innerText;
          navigator.clipboard.writeText(code).then(() => {{
            btn.textContent = 'Copied!';
            setTimeout(() => btn.textContent = 'Copy', 2000);
          }});
        }});
        pre.appendChild(btn);
      }});

      // Build Table of Contents
      buildTableOfContents(article);

      // Render Pagination Buttons
      renderPagination();

      // Update Nav List Active State
      renderNavList();

      // Scroll to Top or Anchor
      const contentEl = document.getElementById('mainContent');
      if (scrollToId) {{
        const el = document.getElementById(scrollToId);
        if (el) {{
          el.scrollIntoView({{ behavior: 'smooth' }});
          return;
        }}
      }}
      contentEl.scrollTop = 0;

      if (window.lucide) lucide.createIcons();
    }}

    // Build Table of Contents in Right Sidebar
    function buildTableOfContents(container) {{
      const tocContainer = document.getElementById('tocList');
      tocContainer.innerHTML = '';

      const headings = container.querySelectorAll('h2, h3');
      if (headings.length === 0) {{
        tocContainer.innerHTML = '<span style="font-size:12px;color:var(--text-muted);">No subheadings</span>';
        return;
      }}

      headings.forEach((h, idx) => {{
        let id = h.id;
        if (!id) {{
          id = 'section-' + idx + '-' + h.textContent.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
          h.id = id;
        }}

        const a = document.createElement('a');
        a.className = `toc-link ${{h.tagName === 'H3' ? 'indent' : ''}}`;
        a.href = `#${{currentDocId}}#${{id}}`;
        a.textContent = h.textContent.replace(/^[0-9]+\\.\\s*/, '');
        a.addEventListener('click', (e) => {{
          e.preventDefault();
          h.scrollIntoView({{ behavior: 'smooth' }});
          window.location.hash = `${{currentDocId}}#${{id}}`;
        }});
        tocContainer.appendChild(a);
      }});
    }}

    // Render Pagination (Prev/Next doc)
    function renderPagination() {{
      const container = document.getElementById('docPagination');
      container.innerHTML = '';
      const idx = DOCS_KEYS.indexOf(currentDocId);

      if (idx > 0) {{
        const prevDoc = DOCS_DATA[DOCS_KEYS[idx - 1]];
        const btn = document.createElement('a');
        btn.className = 'page-btn';
        btn.href = `#${{prevDoc.id}}`;
        btn.innerHTML = `
          <span class="page-btn-label">← Previous Chapter</span>
          <span class="page-btn-title">${{prevDoc.title}}</span>
        `;
        btn.addEventListener('click', (e) => {{
          e.preventDefault();
          loadDocument(prevDoc.id);
        }});
        container.appendChild(btn);
      }} else {{
        container.appendChild(document.createElement('div'));
      }}

      if (idx < DOCS_KEYS.length - 1) {{
        const nextDoc = DOCS_DATA[DOCS_KEYS[idx + 1]];
        const btn = document.createElement('a');
        btn.className = 'page-btn';
        btn.href = `#${{nextDoc.id}}`;
        btn.style.marginLeft = 'auto';
        btn.style.textAlign = 'right';
        btn.innerHTML = `
          <span class="page-btn-label">Next Chapter →</span>
          <span class="page-btn-title">${{nextDoc.title}}</span>
        `;
        btn.addEventListener('click', (e) => {{
          e.preventDefault();
          loadDocument(nextDoc.id);
        }});
        container.appendChild(btn);
      }}
    }}

    // Live Search across all markdown documentation
    const searchInput = document.getElementById('docsSearchInput');
    searchInput.addEventListener('input', (e) => {{
      const query = e.target.value.toLowerCase().trim();
      if (!query) {{
        renderNavList();
        return;
      }}

      const navContainer = document.getElementById('docNavList');
      navContainer.innerHTML = '';

      DOCS_KEYS.forEach(key => {{
        const doc = DOCS_DATA[key];
        const matchTitle = doc.title.toLowerCase().includes(query);
        const matchSub = doc.subtitle.toLowerCase().includes(query);
        const matchBody = doc.markdown.toLowerCase().includes(query);

        if (matchTitle || matchSub || matchBody) {{
          const a = document.createElement('a');
          a.className = `doc-nav-item ${{key === currentDocId ? 'active' : ''}}`;
          a.href = `#${{key}}`;
          a.innerHTML = `
            <div class="doc-nav-left">
              <i data-lucide="${{doc.icon}}"></i>
              <span>${{doc.title}}</span>
            </div>
            <span class="doc-nav-badge">${{matchTitle ? 'Match' : 'Found'}}</span>
          `;
          a.addEventListener('click', (ev) => {{
            ev.preventDefault();
            loadDocument(key);
          }});
          navContainer.appendChild(a);
        }}
      }});
      if (window.lucide) lucide.createIcons();
    }});

    // Handle URL Hash on Load & PopState
    function handleHashRoute() {{
      const hash = window.location.hash.replace(/^#/, '');
      if (hash) {{
        const parts = hash.split('#');
        const docId = parts[0];
        const anchor = parts[1] || null;
        if (DOCS_DATA[docId]) {{
          loadDocument(docId, anchor);
          return;
        }}
      }}
      loadDocument('index');
    }}

    window.addEventListener('popstate', handleHashRoute);
    window.addEventListener('DOMContentLoaded', () => {{
      handleHashRoute();
      if (window.lucide) lucide.createIcons();
    }});
  </script>
</body>
</html>
"""

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"Interactive documentation compiled: {output_html_path} ({len(html_template)} bytes)")

    # Also write a root copy docs.html for convenient access
    root_docs_path = os.path.join(root_dir, 'docs.html')
    with open(root_docs_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"Root docs mirror compiled: {root_docs_path} ({len(html_template)} bytes)")

if __name__ == '__main__':
    main()
