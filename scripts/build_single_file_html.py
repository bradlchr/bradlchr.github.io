import json
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
plants_path = os.path.join(root_dir, 'android', 'app', 'src', 'main', 'assets', 'plants.json')
if not os.path.exists(plants_path):
    plants_path = os.path.join(root_dir, 'data', 'plants_enriched.json')

plants_data = json.load(open(plants_path, 'r', encoding='utf-8'))

sweet_16 = {
    'echinacea purpurea', 'coreopsis lanceolata', 'symphyotrichum oblongifolium', 
    'bouteloua curtipendula', 'asclepias verticillata', 'aquilegia canadensis',
    'sporobolus heterolepis', 'zizia aurea', 'asclepias tuberosa', 'monarda fistulosa',
    'penstemon digitalis', 'baptisia australis', 'glandularia canadensis',
    'schizachyrium scoparium', 'packera obovata', 'geranium maculatum'
}
keystone_genera = {
    'quercus', 'prunus', 'salix', 'betula', 'acer', 'solidago', 
    'symphyotrichum', 'helianthus', 'rudbeckia', 'coreopsis', 'monarda', 'asclepias'
}

for p in plants_data:
    sci = p.get('scientific_name', '').lower().strip()
    genus = sci.split()[0] if sci else ''
    is_s16 = sci in sweet_16 or any('sweet 16' in str(t).lower() for t in p.get('special_tags', [])) or p.get('is_sweet16', False) or p.get('is_sweet_16', False)
    is_key = p.get('is_kc_keystone', False) or p.get('isKcKeystone', False) or any('keystone' in str(t).lower() for t in p.get('special_tags', [])) or genus in keystone_genera
    p['is_sweet_16'] = is_s16
    p['is_sweet16'] = is_s16
    p['is_kc_keystone'] = is_key
    p['isKcKeystone'] = is_key
    
    # Ensure plant_url is present and clean
    if not p.get('plant_url'):
        for s in p.get('sources', []):
            if s.get('source_url') and s['source_url'].startswith('http'):
                p['plant_url'] = s['source_url']
                break
    p['plant_url'] = p.get('plant_url', '')

minified_json = json.dumps(plants_data, separators=(',', ':'), ensure_ascii=False)
minified_json = minified_json.replace('</script>', '<\\/script>')

html_header = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <meta name="theme-color" content="#1b5e20" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#121815" media="(prefers-color-scheme: dark)">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <title>Deep Roots Nature Advisors - Kansas City Native Plant Database</title>
  
  <!-- Fonts & Icons -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Lora:ital,wght@0,500;0,600;1,400;1,600&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/lucide@latest"></script>
  <script src="https://accounts.google.com/gsi/client" async defer onload="window.__gsiLoaded = true; if (typeof window.initGoogleAuth === 'function') window.initGoogleAuth();"></script>

  <style>
    :root {
      --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-serif: 'Lora', Georgia, serif;
      
      /* Light Palette - Botanical Nature */
      --bg-base: #f4f7f4;
      --bg-surface: #ffffff;
      --bg-surface-elevated: #ffffff;
      --bg-frosted: rgba(255, 255, 255, 0.88);
      --border-subtle: #e1e8e2;
      --border-strong: #c2d1c4;
      
      --text-main: #142117;
      --text-secondary: #3e5643;
      --text-muted: #677f6c;
      --text-inverse: #ffffff;
      
      --primary: #235c36;
      --primary-hover: #1b472a;
      --primary-light: #e8f5ec;
      --primary-border: #b8dec0;
      
      --accent-gold: #c28829;
      --accent-gold-bg: #fff8eb;
      --accent-gold-border: #f4d399;
      
      --accent-keystone: #0e7040;
      --accent-keystone-bg: #e6f7ee;
      
      --accent-terracotta: #a85232;
      --accent-terracotta-bg: #faeee9;
      
      --danger: #b91c1c;
      --danger-bg: #fee2e2;
      
      --shadow-sm: 0 1px 3px rgba(20, 33, 23, 0.05);
      --shadow-md: 0 4px 12px rgba(20, 33, 23, 0.08);
      --shadow-lg: 0 10px 25px rgba(20, 33, 23, 0.12);
      
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 16px;
      --radius-full: 9999px;
      
      --drawer-width: 440px;
    }

    [data-theme="dark"] {
      --bg-base: #0f1611;
      --bg-surface: #17211a;
      --bg-surface-elevated: #1f2c23;
      --bg-frosted: rgba(23, 33, 26, 0.88);
      --border-subtle: #27382d;
      --border-strong: #364d3d;
      
      --text-main: #ecf3ed;
      --text-secondary: #bad3c0;
      --text-muted: #829f89;
      --text-inverse: #0f1611;
      
      --primary: #4bae6d;
      --primary-hover: #60c582;
      --primary-light: #163321;
      --primary-border: #245535;
      
      --accent-gold: #e5a73e;
      --accent-gold-bg: #32250d;
      --accent-gold-border: #5b4213;
      
      --accent-keystone: #3ec985;
      --accent-keystone-bg: #0f3822;
      
      --accent-terracotta: #e57e5e;
      --accent-terracotta-bg: #3c1e14;
      
      --danger: #f87171;
      --danger-bg: #450a0a;
      
      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
      --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.4);
      --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.5);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: var(--font-sans);
      background-color: var(--bg-base);
      color: var(--text-main);
      line-height: 1.5;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
      transition: background-color 0.25s ease, color 0.25s ease;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }
    ::-webkit-scrollbar-track {
      background: var(--bg-base);
    }
    ::-webkit-scrollbar-thumb {
      background: var(--border-strong);
      border-radius: var(--radius-full);
    }
    ::-webkit-scrollbar-thumb:hover {
      background: var(--text-muted);
    }

    /* Header */
    header {
      position: sticky;
      top: 0;
      z-index: 40;
      background: var(--bg-frosted);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border-subtle);
      height: 68px;
      display: flex;
      align-items: center;
      padding: 0 24px;
      gap: 16px;
    }

    .header-brand {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: inherit;
    }

    .brand-logo {
      width: 40px;
      height: 40px;
      border-radius: var(--radius-md);
      background: linear-gradient(135deg, var(--primary) 0%, #153b23 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-size: 20px;
      box-shadow: var(--shadow-sm);
    }

    .brand-text h1 {
      font-size: 17px;
      font-weight: 800;
      letter-spacing: -0.02em;
      line-height: 1.2;
    }

    .brand-text p {
      font-size: 11px;
      font-weight: 500;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .header-stats {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-left: 20px;
    }

    .stat-pill {
      font-size: 12px;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: var(--radius-full);
      display: flex;
      align-items: center;
      gap: 6px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      cursor: pointer;
    }

    .stat-pill strong {
      color: var(--text-main);
      font-weight: 800;
    }

    .stat-pill.db-status {
      background: var(--primary-light);
      border-color: var(--primary-border);
      color: var(--primary);
    }

    .stat-pill.sweet16 {
      background: var(--accent-gold-bg);
      border-color: var(--accent-gold-border);
      color: var(--accent-gold);
    }

    .stat-pill.keystone {
      background: var(--accent-keystone-bg);
      border-color: var(--border-strong);
      color: var(--accent-keystone);
    }

    .header-actions {
      margin-left: auto;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    /* Buttons */
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      font-family: var(--font-sans);
      font-size: 13px;
      font-weight: 600;
      padding: 8px 14px;
      border-radius: var(--radius-md);
      border: 1px solid transparent;
      cursor: pointer;
      transition: all 0.15s ease;
      text-decoration: none;
      white-space: nowrap;
    }

    .btn-primary {
      background: var(--primary);
      color: var(--text-inverse);
    }
    .btn-primary:hover {
      background: var(--primary-hover);
      box-shadow: var(--shadow-sm);
    }

    .btn-secondary {
      background: var(--bg-surface);
      color: var(--text-main);
      border-color: var(--border-strong);
    }
    .btn-secondary:hover {
      background: var(--bg-surface-elevated);
      border-color: var(--text-muted);
    }

    .btn-google {
      background: #ffffff;
      color: #3c4043;
      border: 1px solid #dadce0;
      box-shadow: 0 1px 2px rgba(60,64,67,0.1);
      font-weight: 600;
    }
    .btn-google:hover {
      background: #f8f9fa;
      border-color: #c6c9cc;
      box-shadow: 0 1px 3px rgba(60,64,67,0.2);
    }

    [data-theme="dark"] .btn-google {
      background: #202b24;
      color: #e6f0e8;
      border-color: var(--border-strong);
    }
    [data-theme="dark"] .btn-google:hover {
      background: #27382d;
    }

    .btn-icon {
      padding: 8px;
      border-radius: var(--radius-md);
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
    }
    .btn-icon:hover {
      color: var(--text-main);
      border-color: var(--border-strong);
    }

    .btn-report {
      background: linear-gradient(135deg, var(--primary) 0%, #174227 100%);
      color: #fff;
      border-color: rgba(255, 255, 255, 0.15);
      position: relative;
    }
    .btn-report:hover {
      box-shadow: 0 4px 14px rgba(35, 92, 54, 0.35);
      transform: translateY(-1px);
    }

    .badge-count {
      background: var(--accent-gold);
      color: #fff;
      font-size: 11px;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: var(--radius-full);
      box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }

    /* Layout */
    .app-layout {
      display: flex;
      flex: 1;
      width: 100%;
      max-width: 1720px;
      margin: 0 auto;
      padding: 20px 24px;
      gap: 24px;
      position: relative;
    }

    /* Left Sidebar - Filters */
    .filter-sidebar {
      width: 300px;
      flex-shrink: 0;
      display: flex;
      flex-direction: column;
      gap: 16px;
      position: sticky;
      top: 88px;
      height: calc(100vh - 108px);
      overflow-y: auto;
      padding-right: 4px;
    }

    .filter-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 16px;
      box-shadow: var(--shadow-sm);
    }

    .search-box {
      position: relative;
      width: 100%;
    }

    .search-input {
      width: 100%;
      padding: 10px 36px 10px 36px;
      font-family: var(--font-sans);
      font-size: 13px;
      background: var(--bg-base);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      color: var(--text-main);
      outline: none;
      transition: border-color 0.2s;
    }
    .search-input:focus {
      border-color: var(--primary);
      background: var(--bg-surface);
      box-shadow: 0 0 0 3px var(--primary-light);
    }

    .search-icon {
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      pointer-events: none;
    }

    .search-clear {
      position: absolute;
      right: 10px;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      display: none;
    }

    /* Quick Filter Badges */
    .quick-filters {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .quick-toggle-btn {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      padding: 9px 12px;
      border-radius: var(--radius-md);
      font-size: 13px;
      font-weight: 600;
      border: 1px solid var(--border-subtle);
      background: var(--bg-base);
      color: var(--text-main);
      cursor: pointer;
      transition: all 0.15s ease;
      text-align: left;
    }
    .quick-toggle-btn:hover {
      border-color: var(--border-strong);
      background: var(--bg-surface-elevated);
    }
    .quick-toggle-btn.active.sweet16 {
      background: var(--accent-gold-bg);
      border-color: var(--accent-gold);
      color: var(--accent-gold);
    }
    .quick-toggle-btn.active.keystone {
      background: var(--accent-keystone-bg);
      border-color: var(--accent-keystone);
      color: var(--accent-keystone);
    }

    /* Accordion filter group */
    .accordion {
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 12px;
      margin-bottom: 12px;
    }
    .accordion:last-child {
      border-bottom: none;
      padding-bottom: 0;
      margin-bottom: 0;
    }

    .accordion-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      padding: 6px 0;
      background: none;
      border: none;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-secondary);
      cursor: pointer;
    }
    .accordion-header:hover {
      color: var(--text-main);
    }

    .accordion-content {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      padding-top: 8px;
    }

    .chip-filter {
      font-size: 12px;
      font-weight: 500;
      padding: 4px 10px;
      border-radius: var(--radius-full);
      background: var(--bg-base);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 0.15s ease;
      user-select: none;
    }
    .chip-filter:hover {
      border-color: var(--border-strong);
      color: var(--text-main);
    }
    .chip-filter.active {
      background: var(--primary);
      border-color: var(--primary);
      color: #fff;
      font-weight: 600;
    }

    /* Main Content Area */
    .main-content {
      flex: 1;
      min-width: 0;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .controls-bar {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 12px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      box-shadow: var(--shadow-sm);
    }

    .results-count {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-secondary);
    }
    .results-count strong {
      color: var(--text-main);
      font-weight: 800;
    }

    .sort-control {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      color: var(--text-secondary);
    }

    .sort-select {
      font-family: var(--font-sans);
      font-size: 13px;
      font-weight: 600;
      padding: 6px 12px;
      background: var(--bg-base);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      color: var(--text-main);
      outline: none;
      cursor: pointer;
    }
    .sort-select:focus {
      border-color: var(--primary);
    }

    /* Active filter chips */
    .active-filters-bar {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 6px;
      padding: 0 4px;
    }

    .active-tag {
      font-size: 12px;
      font-weight: 600;
      background: var(--primary-light);
      border: 1px solid var(--primary-border);
      color: var(--primary);
      padding: 3px 8px 3px 10px;
      border-radius: var(--radius-full);
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .active-tag button {
      background: none;
      border: none;
      color: inherit;
      cursor: pointer;
      display: flex;
      align-items: center;
    }

    .clear-all-btn {
      font-size: 12px;
      font-weight: 700;
      color: var(--danger);
      background: none;
      border: none;
      cursor: pointer;
      padding: 2px 6px;
    }
    .clear-all-btn:hover {
      text-decoration: underline;
    }

    /* Plant Grid */
    .plants-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr));
      gap: clamp(14px, 2vw, 20px);
    }

    .color-chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .color-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      display: inline-block;
      flex-shrink: 0;
      box-shadow: 0 1px 3px rgba(0,0,0,0.25);
    }

    .plant-card {
      padding: 7px;
      border-radius: 20px;
      border: 1px solid var(--border-subtle);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
      transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
      position: relative;
      min-width: 0;
    }
    .plant-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.18);
      border-color: rgba(255, 255, 255, 0.45);
    }

    .plant-card-inner {
      background: rgba(255, 255, 255, 0.92);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-radius: 14px;
      border: 1px solid rgba(255, 255, 255, 0.6);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      height: 100%;
    }
    body[data-theme="dark"] .plant-card-inner,
    [data-theme="dark"] .plant-card-inner {
      background: rgba(20, 30, 24, 0.92);
      border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .card-media {
      position: relative;
      width: 100%;
      height: 180px;
      background: var(--bg-base);
      overflow: hidden;
      cursor: pointer;
      border-radius: 13px 13px 0 0;
    }

    .card-media img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s ease;
    }
    .plant-card:hover .card-media img {
      transform: scale(1.04);
    }

    .card-placeholder {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, var(--bg-base) 0%, var(--border-subtle) 100%);
      color: var(--text-muted);
      gap: 6px;
    }

    .card-badges {
      position: absolute;
      top: 10px;
      left: 10px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      z-index: 2;
    }

    .badge-sweet16 {
      background: rgba(245, 158, 11, 0.95);
      backdrop-filter: blur(4px);
      color: #fff;
      font-size: 11px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: var(--radius-full);
      box-shadow: 0 2px 5px rgba(0,0,0,0.2);
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .badge-keystone {
      background: rgba(16, 185, 129, 0.95);
      backdrop-filter: blur(4px);
      color: #fff;
      font-size: 11px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: var(--radius-full);
      box-shadow: 0 2px 5px rgba(0,0,0,0.2);
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .badge-layer {
      position: absolute;
      bottom: 10px;
      right: 10px;
      background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(4px);
      color: #fff;
      font-size: 11px;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: var(--radius-sm);
    }

    .card-body {
      padding: 16px;
      display: flex;
      flex-direction: column;
      flex: 1;
      gap: 8px;
    }

    .card-title-group {
      cursor: pointer;
    }

    .card-primary-name, .card-common-name {
      font-size: 16px;
      font-weight: 700;
      color: var(--text-main);
      line-height: 1.3;
    }
    .card-primary-name.is-scientific {
      font-family: var(--font-serif);
      font-style: italic;
    }
    .card-primary-name:hover, .card-common-name:hover {
      color: var(--primary);
    }

    .card-secondary-name, .card-sci-name {
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 1px;
    }
    .card-secondary-name.is-scientific, .card-sci-name.is-scientific {
      font-family: var(--font-serif);
      font-style: italic;
    }
    .card-secondary-name:not(.is-scientific) {
      font-family: var(--font-sans);
      font-style: normal;
    }

    .card-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 4px;
    }

    .meta-chip {
      font-size: 11px;
      font-weight: 600;
      background: var(--bg-base);
      color: var(--text-secondary);
      border: 1px solid var(--border-subtle);
      padding: 2px 8px;
      border-radius: var(--radius-sm);
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .card-desc {
      font-size: 12px;
      color: var(--text-secondary);
      line-height: 1.45;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      margin-top: 4px;
    }

    .card-footer {
      padding: 12px 16px;
      background: var(--bg-base);
      border-top: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }

    .btn-copy-desc {
      font-size: 12px;
      padding: 6px 10px;
      background: transparent;
      border: 1px solid var(--border-strong);
      color: var(--text-secondary);
      border-radius: var(--radius-md);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .btn-copy-desc:hover {
      background: var(--bg-surface);
      color: var(--text-main);
    }

    .btn-add-report {
      font-size: 12px;
      font-weight: 700;
      padding: 6px 12px;
      background: var(--primary);
      color: #fff;
      border: none;
      border-radius: var(--radius-md);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.15s ease;
    }
    .btn-add-report:hover {
      background: var(--primary-hover);
    }
    .btn-add-report.staged {
      background: var(--accent-keystone-bg);
      color: var(--accent-keystone);
      border: 1px solid var(--accent-keystone);
    }

    /* Staging Drawer */
    .drawer-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.45);
      backdrop-filter: blur(3px);
      z-index: 50;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s ease;
    }
    .drawer-overlay.open {
      opacity: 1;
      pointer-events: auto;
    }

    .staging-drawer {
      position: fixed;
      top: 0;
      right: 0;
      bottom: 0;
      width: 100%;
      max-width: var(--drawer-width);
      background: var(--bg-surface);
      box-shadow: var(--shadow-lg);
      z-index: 60;
      display: flex;
      flex-direction: column;
      transform: translateX(100%);
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      border-left: 1px solid var(--border-subtle);
    }
    .staging-drawer.open {
      transform: translateX(0);
    }

    .drawer-header {
      padding: 16px 20px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-frosted);
    }

    .drawer-header h2 {
      font-size: 16px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .drawer-body {
      flex: 1;
      overflow-y: auto;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .client-meta-form {
      display: flex;
      flex-direction: column;
      gap: 12px;
      background: var(--bg-base);
      padding: 14px;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-subtle);
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .form-group label {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-secondary);
    }
    .form-group input, .form-group textarea, .form-group select {
      font-family: var(--font-sans);
      font-size: 13px;
      padding: 8px 10px;
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      background: var(--bg-surface);
      color: var(--text-main);
      outline: none;
    }
    .form-group input:focus, .form-group textarea:focus {
      border-color: var(--primary);
    }

    .staged-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .staged-item {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      box-shadow: var(--shadow-sm);
    }

    .staged-item-header {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .staged-item-thumb {
      width: 44px;
      height: 44px;
      border-radius: var(--radius-sm);
      object-fit: cover;
      background: var(--bg-base);
      flex-shrink: 0;
    }

    .staged-item-info {
      flex: 1;
      min-width: 0;
    }
    .staged-item-name {
      font-size: 13px;
      font-weight: 700;
      color: var(--text-main);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .staged-item-sci {
      font-family: var(--font-serif);
      font-size: 11px;
      font-style: italic;
      color: var(--text-muted);
    }

    .staged-item-controls {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .quantity-control {
      display: inline-flex;
      align-items: center;
      border: 1px solid var(--border-strong);
      border-radius: var(--radius-sm);
      overflow: hidden;
      background: var(--bg-surface);
    }
    .qty-btn {
      background: none;
      border: none;
      padding: 4px 8px;
      cursor: pointer;
      color: var(--text-main);
      font-weight: bold;
    }
    .qty-btn:hover {
      background: var(--bg-base);
    }
    .qty-val {
      font-size: 12px;
      font-weight: 700;
      padding: 0 6px;
      min-width: 24px;
      text-align: center;
    }

    .staged-item-note {
      font-size: 12px;
      padding: 6px 8px;
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      background: var(--bg-base);
      color: var(--text-main);
      width: 100%;
    }

    .drawer-footer {
      padding: 16px 20px;
      border-top: 1px solid var(--border-subtle);
      background: var(--bg-surface);
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    /* Modals / Dialogs */
    dialog {
      margin: auto;
      border: none;
      border-radius: var(--radius-lg);
      background: var(--bg-surface);
      color: var(--text-main);
      box-shadow: var(--shadow-lg);
      max-width: 680px;
      width: calc(100% - 32px);
      max-height: calc(100vh - 64px);
      overflow-y: auto;
      padding: 0;
    }
    dialog::backdrop {
      background: rgba(0, 0, 0, 0.55);
      backdrop-filter: blur(4px);
    }

    .dialog-header {
      padding: 16px 20px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      background: var(--bg-surface);
      z-index: 10;
    }

    .dialog-body {
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .specs-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
      background: var(--bg-base);
      padding: 14px;
      border-radius: var(--radius-md);
    }
    .spec-item {
      display: flex;
      flex-direction: column;
    }
    .spec-label {
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
    }
    .spec-value {
      font-size: 13px;
      font-weight: 600;
      color: var(--text-main);
    }

    /* Toasts */
    .toast-container {
      position: fixed;
      bottom: 24px;
      right: 24px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      z-index: 100;
      pointer-events: none;
    }

    .toast {
      background: #1e293b;
      color: #fff;
      padding: 10px 16px;
      border-radius: var(--radius-md);
      font-size: 13px;
      font-weight: 500;
      box-shadow: var(--shadow-md);
      display: flex;
      align-items: center;
      gap: 8px;
      animation: slideInUp 0.25s ease;
      pointer-events: auto;
    }
    .toast.success {
      background: #065f46;
    }
    .toast.warning {
      background: #92400e;
    }

    @keyframes slideInUp {
      from { opacity: 0; transform: translateY(12px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Sidebar Overlay (Mobile Drawer) */
    .sidebar-overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(4px);
      -webkit-backdrop-filter: blur(4px);
      z-index: 998;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s ease;
    }
    .sidebar-overlay.open {
      opacity: 1;
      pointer-events: auto;
    }

    /* Mobile Sidebar Header & Footer */
    .sidebar-mobile-header,
    .sidebar-mobile-footer {
      display: none;
    }

    .mobile-search-bar {
      display: none;
    }

    .btn-filter-toggle {
      display: none;
      align-items: center;
      gap: 7px;
      background: var(--bg-surface);
      color: var(--text-main);
      border: 1px solid var(--border-strong);
      padding: 7px 12px;
      border-radius: var(--radius-md);
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s ease;
      white-space: nowrap;
    }
    .btn-filter-toggle:hover {
      background: var(--bg-surface-elevated);
      border-color: var(--primary);
    }
    .filter-count-badge {
      background: var(--primary);
      color: #fff;
      font-size: 11px;
      font-weight: 800;
      padding: 1px 6px;
      border-radius: var(--radius-full);
      line-height: 1.2;
    }
    .results-and-mobile-filter {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }
    .sidebar-scroll-area {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .btn-text-short {
      display: none !important;
    }

    /* Responsive Breakpoints */
    @media (max-width: 1024px) {
      .app-layout {
        flex-direction: column;
        padding: 14px 16px;
        gap: 14px;
      }
      .header-stats {
        display: none;
      }
      .sidebar-overlay {
        display: block;
      }
      .mobile-search-bar {
        display: block;
        margin-bottom: 2px;
      }
      .btn-filter-toggle {
        display: inline-flex;
      }

      /* Off-canvas mobile filter drawer */
      .filter-sidebar {
        position: fixed;
        top: 0;
        left: 0;
        bottom: 0;
        width: min(88vw, 360px);
        max-width: 100%;
        height: 100%;
        height: 100dvh;
        z-index: 1000;
        background: var(--bg-surface);
        box-shadow: 4px 0 28px rgba(0, 0, 0, 0.3);
        transform: translateX(-100%);
        transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1);
        overflow: hidden;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: 0;
        border-right: 1px solid var(--border-subtle);
      }
      .filter-sidebar.open {
        transform: translateX(0);
      }

      .sidebar-mobile-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 18px;
        background: var(--bg-frosted);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-bottom: 1px solid var(--border-subtle);
        flex-shrink: 0;
      }
      .sidebar-mobile-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 15px;
        font-weight: 800;
        color: var(--text-main);
      }

      .sidebar-scroll-area {
        flex: 1;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
        padding: 16px;
        gap: 14px;
      }

      .sidebar-mobile-footer {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 16px;
        padding-bottom: max(12px, env(safe-area-inset-bottom, 12px));
        background: var(--bg-surface);
        border-top: 1px solid var(--border-subtle);
        flex-shrink: 0;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
      }
    }

    @media (max-width: 768px) {
      header {
        height: 60px;
        padding: 0 14px;
        gap: 10px;
      }
      .brand-logo {
        width: 34px;
        height: 34px;
        font-size: 18px;
      }
      .brand-text h1 {
        font-size: 15px;
      }
      .brand-text p {
        font-size: 10px;
      }
      .header-actions {
        gap: 6px;
      }

      .btn-text-long {
        display: none !important;
      }
      .btn-text-short {
        display: inline !important;
      }

      /* Prevent mobile Safari auto-zoom on input focus */
      input, textarea, select {
        font-size: 16px !important;
      }

      .controls-bar {
        padding: 10px 14px;
        gap: 10px;
      }
      .controls-actions {
        width: 100%;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
      }
      .sort-control {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 3px;
        font-size: 11px;
      }
      .sort-control select {
        width: 100%;
      }

      /* Staging drawer full-width on mobile with dvh and safe-area */
      .staging-drawer {
        width: 100%;
        max-width: 100%;
        height: 100%;
        height: 100dvh;
      }
      .drawer-footer {
        padding-bottom: max(16px, env(safe-area-inset-bottom, 16px));
      }

      /* Dialogs fit viewport with safe area */
      dialog {
        width: calc(100% - 20px);
        max-width: 100%;
        max-height: 92dvh;
        margin: auto;
      }
      .specs-grid {
        grid-template-columns: 1fr 1fr;
      }
      .toast-container {
        left: 14px;
        right: 14px;
        bottom: max(14px, env(safe-area-inset-bottom, 14px));
      }
    }

    @media (max-width: 520px) {
      .app-layout {
        padding: 10px 10px;
        gap: 12px;
      }
      .brand-text p {
        display: none;
      }
      .brand-text h1 {
        font-size: 14px;
      }
      .btn-text-short {
        display: none !important;
      }
      .user-profile-name {
        display: none !important;
      }
      .btn-report {
        padding: 7px 10px;
      }
      .btn-google {
        padding: 7px 10px;
      }

      .controls-actions {
        grid-template-columns: 1fr;
      }

      .results-count {
        font-size: 13px;
      }

      .card-media {
        height: 190px;
      }

      .specs-grid {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 360px) {
      .brand-text h1 {
        font-size: 13px;
      }
      .btn {
        padding: 6px 8px;
      }
    }
  </style>
</head>
<body data-theme="light">

  <!-- Header -->
  <header>
    <div class="header-brand">
      <div class="brand-logo">🌱</div>
      <div class="brand-text">
        <h1>Deep Roots Nature Advisors</h1>
        <p>Kansas City Native Plant Database</p>
      </div>
    </div>

    <div class="header-stats">
      <div class="stat-pill db-status" id="dbStatusPill" title="Click to view shared database sync status">
        <i data-lucide="database" style="width:14px;height:14px;"></i>
        <span>Shared DB:</span>
        <strong id="statDbCount">184 Species</strong>
      </div>
      <div class="stat-pill sweet16" id="statSweet16Pill">
        ⭐ Sweet 16: <strong id="statSweet16Count">16</strong>
      </div>
      <div class="stat-pill keystone" id="statKeystonePill">
        🌿 KC Keystones: <strong id="statKeystoneCount">25</strong>
      </div>
    </div>

    <div class="header-actions">
      <!-- Theme Toggle -->
      <button id="themeToggleBtn" class="btn btn-icon" title="Toggle Dark/Light Mode">
        <i data-lucide="moon" id="themeIcon"></i>
      </button>

      <!-- Google Sign In / User Container -->
      <div id="authContainer">
        <button id="headerSignInBtn" class="btn btn-google">
          <svg style="width:16px;height:16px;" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
          <span class="btn-text-long">Sign In with Google</span>
          <span class="btn-text-short">Sign In</span>
        </button>
      </div>

      <!-- Sync / Database Info -->
      <button id="syncModalBtn" class="btn btn-icon" title="Database Sync & Master DB Status">
        <i data-lucide="cloud-cog"></i>
      </button>

      <!-- Consultation Report Drawer Toggle -->
      <button id="reportDrawerBtn" class="btn btn-report">
        <i data-lucide="clipboard-list"></i>
        <span class="btn-text-long">Report Staging</span>
        <span class="btn-text-short">Report</span>
        <span id="stagedBadge" class="badge-count" style="display:none;">0</span>
      </button>
    </div>
  </header>

  <!-- App Layout -->
  <div class="app-layout">
    
    <!-- Filter Sidebar Overlay (for mobile drawer) -->
    <div class="sidebar-overlay" id="sidebarOverlay"></div>

    <!-- Filter Sidebar -->
    <aside class="filter-sidebar" id="filterSidebar">
      
      <!-- Mobile Drawer Header -->
      <div class="sidebar-mobile-header">
        <div class="sidebar-mobile-title">
          <i data-lucide="sliders-horizontal" style="width:16px;height:16px;"></i>
          <span>Filter &amp; Sort</span>
        </div>
        <button id="closeSidebarBtn" class="btn-icon" aria-label="Close filters">
          <i data-lucide="x" style="width:18px;height:18px;"></i>
        </button>
      </div>

      <div class="sidebar-scroll-area">
        <!-- Search Card -->
        <div class="filter-card">
        <div class="search-box">
          <i data-lucide="search" class="search-icon" style="width:16px;height:16px;"></i>
          <input type="text" id="searchInput" class="search-input" placeholder="Search Kansas City natives...">
          <button id="searchClearBtn" class="search-clear">
            <i data-lucide="x" style="width:14px;height:14px;"></i>
          </button>
        </div>
      </div>

      <!-- Quick Toggles -->
      <div class="filter-card quick-filters">
        <button class="quick-toggle-btn sweet16" id="toggleSweet16Btn">
          <span>⭐ Deep Roots Sweet 16</span>
          <span class="badge-count" style="background:var(--accent-gold);">16</span>
        </button>
        <button class="quick-toggle-btn keystone" id="toggleKeystoneBtn">
          <span>🌿 KC Keystone Species</span>
          <span class="badge-count" style="background:var(--accent-keystone);">25</span>
        </button>
      </div>

      <!-- Faceted Filters -->
      <div class="filter-card">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
          <span style="font-size:13px;font-weight:800;text-transform:uppercase;letter-spacing:0.04em;color:var(--text-secondary);">Filters</span>
          <button id="resetAllFiltersBtn" class="clear-all-btn" style="margin-left:auto;">Reset All</button>
        </div>

        <!-- Card Display & Sort Settings -->
        <div class="accordion">
          <button class="accordion-header" data-target="sortDisplayFilterContent">
            <span>Card Display &amp; Sort</span>
            <i data-lucide="chevron-down" style="width:14px;height:14px;"></i>
          </button>
          <div class="accordion-content" id="sortDisplayFilterContent" style="display:flex;flex-direction:column;gap:10px;padding-top:6px;">
            <div>
              <label style="font-size:11px;font-weight:700;color:var(--text-secondary);display:block;margin-bottom:4px;">Default Name Display:</label>
              <select id="sidebarNameDisplaySelect" class="sort-select" style="width:100%;">
                <option value="common_first">Common Name First</option>
                <option value="scientific_first">Scientific Name First</option>
              </select>
            </div>
            <div>
              <label style="font-size:11px;font-weight:700;color:var(--text-secondary);display:block;margin-bottom:4px;">Sort By:</label>
              <select id="sidebarSortOrderSelect" class="sort-select" style="width:100%;">
                <option value="keystone_first">KC Keystones &amp; Sweet 16 First</option>
                <option value="common_asc">Common Name (A to Z)</option>
                <option value="common_desc">Common Name (Z to A)</option>
                <option value="sci_asc">Scientific Name (A to Z)</option>
                <option value="sci_desc">Scientific Name (Z to A)</option>
                <option value="height_asc">Mature Height (Low to High)</option>
                <option value="height_desc">Mature Height (High to Low)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Habitat / Environment -->
        <div class="accordion">
          <button class="accordion-header" data-target="habitatFilterContent">
            <span>Native Environment</span>
            <i data-lucide="chevron-down" style="width:14px;height:14px;"></i>
          </button>
          <div class="accordion-content" id="habitatFilterContent">
            <span class="chip-filter" data-group="habitat" data-val="Prairie">Prairie</span>
            <span class="chip-filter" data-group="habitat" data-val="Savannah/Woodland">Savannah / Woodland</span>
            <span class="chip-filter" data-group="habitat" data-val="Forest">Forest</span>
            <span class="chip-filter" data-group="habitat" data-val="Cliff/Glade">Cliff / Glade</span>
            <span class="chip-filter" data-group="habitat" data-val="Stream Edge/Wetland">Stream Edge / Wetland</span>
          </div>
        </div>

        <!-- Light Requirements -->
        <div class="accordion">
          <button class="accordion-header" data-target="lightFilterContent">
            <span>Light Requirements</span>
            <i data-lucide="chevron-down" style="width:14px;height:14px;"></i>
          </button>
          <div class="accordion-content" id="lightFilterContent">
            <span class="chip-filter" data-group="light" data-val="Full Sun">Full Sun</span>
            <span class="chip-filter" data-group="light" data-val="Part Sun">Part Sun</span>
            <span class="chip-filter" data-group="light" data-val="Part Shade">Part Shade</span>
            <span class="chip-filter" data-group="light" data-val="Full Shade">Full Shade</span>
          </div>
        </div>

        <!-- Soil Moisture -->
        <div class="accordion">
          <button class="accordion-header" data-target="moistureFilterContent">
            <span>Soil Moisture</span>
            <i data-lucide="chevron-down" style="width:14px;height:14px;"></i>
          </button>
          <div class="accordion-content" id="moistureFilterContent">
            <span class="chip-filter" data-group="moisture" data-val="Dry">Dry</span>
            <span class="chip-filter" data-group="moisture" data-val="Medium-Dry">Medium-Dry</span>
            <span class="chip-filter" data-group="moisture" data-val="Medium">Medium</span>
            <span class="chip-filter" data-group="moisture" data-val="Medium-Wet">Medium-Wet</span>
            <span class="chip-filter" data-group="moisture" data-val="Wet">Wet</span>
          </div>
        </div>

        <!-- Mature Height -->
        <div class="accordion">
          <button class="accordion-header" data-target="heightFilterContent">
            <span>Mature Height</span>
            <i data-lucide="chevron-down" style="width:14px;height:14px;"></i>
          </button>
          <div class="accordion-content" id="heightFilterContent">
            <span class="chip-filter" data-group="height" data-val="< 1 ft">&lt; 1 ft (Groundcover)</span>
            <span class="chip-filter" data-group="height" data-val="1 - 3 ft">1 – 3 ft (Low)</span>
            <span class="chip-filter" data-group="height" data-val="3 - 6 ft">3 – 6 ft (Medium)</span>
            <span class="chip-filter" data-group="height" data-val="6 - 15 ft">6 – 15 ft (Tall/Shrub)</span>
            <span class="chip-filter" data-group="height" data-val="15+ ft">15+ ft (Tree/Large Shrub)</span>
          </div>
        </div>

        <!-- Plant Type -->
        <div class="accordion">
          <button class="accordion-header" data-target="typeFilterContent">
            <span>Plant Type</span>
            <i data-lucide="chevron-down" style="width:14px;height:14px;"></i>
          </button>
          <div class="accordion-content" id="typeFilterContent">
            <span class="chip-filter" data-group="type" data-val="Wildflower">Wildflower / Forb</span>
            <span class="chip-filter" data-group="type" data-val="Grass">Grass</span>
            <span class="chip-filter" data-group="type" data-val="Sedge">Sedge</span>
            <span class="chip-filter" data-group="type" data-val="Tree">Tree</span>
            <span class="chip-filter" data-group="type" data-val="Shrub">Shrub</span>
            <span class="chip-filter" data-group="type" data-val="Vine">Vine</span>
            <span class="chip-filter" data-group="type" data-val="Fern">Fern</span>
          </div>
        </div>

        <!-- Ecological Layer -->
        <div class="accordion">
          <button class="accordion-header" data-target="layerFilterContent">
            <span>Garden / Forest Layer</span>
            <i data-lucide="chevron-down" style="width:14px;height:14px;"></i>
          </button>
          <div class="accordion-content" id="layerFilterContent">
            <span class="chip-filter" data-group="layer" data-val="Canopy">Canopy</span>
            <span class="chip-filter" data-group="layer" data-val="Understory">Understory</span>
            <span class="chip-filter" data-group="layer" data-val="Structural">Structural Layer</span>
            <span class="chip-filter" data-group="layer" data-val="Herbaceous">Herbaceous Layer</span>
            <span class="chip-filter" data-group="layer" data-val="Groundcover">Groundcover</span>
          </div>
        </div>

        <!-- Bloom Season -->
        <div class="accordion">
          <button class="accordion-header" data-target="bloomFilterContent">
            <span>Bloom Season</span>
            <i data-lucide="chevron-down" style="width:14px;height:14px;"></i>
          </button>
          <div class="accordion-content" id="bloomFilterContent">
            <span class="chip-filter" data-group="season" data-val="Spring">Spring</span>
            <span class="chip-filter" data-group="season" data-val="Early Summer">Early Summer</span>
            <span class="chip-filter" data-group="season" data-val="Summer">Summer</span>
            <span class="chip-filter" data-group="season" data-val="Late Summer">Late Summer</span>
            <span class="chip-filter" data-group="season" data-val="Fall">Fall</span>
          </div>
        </div>

        <!-- Bloom Color -->
        <div class="accordion">
          <button class="accordion-header" data-target="bloomColorFilterContent">
            <span>Bloom Color</span>
            <i data-lucide="chevron-down" style="width:14px;height:14px;"></i>
          </button>
          <div class="accordion-content" id="bloomColorFilterContent">
            <span class="chip-filter color-chip" data-group="bloomColor" data-val="Yellow"><span class="color-dot" style="background:#FFB300;"></span>Yellow</span>
            <span class="chip-filter color-chip" data-group="bloomColor" data-val="White"><span class="color-dot" style="background:#B0BEC5;"></span>White</span>
            <span class="chip-filter color-chip" data-group="bloomColor" data-val="Purple"><span class="color-dot" style="background:#8E24AA;"></span>Purple</span>
            <span class="chip-filter color-chip" data-group="bloomColor" data-val="Pink"><span class="color-dot" style="background:#D81B60;"></span>Pink</span>
            <span class="chip-filter color-chip" data-group="bloomColor" data-val="Blue"><span class="color-dot" style="background:#1E88E5;"></span>Blue</span>
            <span class="chip-filter color-chip" data-group="bloomColor" data-val="Orange"><span class="color-dot" style="background:#FB8C00;"></span>Orange</span>
            <span class="chip-filter color-chip" data-group="bloomColor" data-val="Red"><span class="color-dot" style="background:#E53935;"></span>Red</span>
            <span class="chip-filter color-chip" data-group="bloomColor" data-val="Lavender"><span class="color-dot" style="background:#7E57C2;"></span>Lavender</span>
            <span class="chip-filter color-chip" data-group="bloomColor" data-val="Cream"><span class="color-dot" style="background:#FFCA28;"></span>Cream</span>
            <span class="chip-filter color-chip" data-group="bloomColor" data-val="Greenish"><span class="color-dot" style="background:#43A047;"></span>Greenish</span>
            <span class="chip-filter color-chip" data-group="bloomColor" data-val="Brown/Tan"><span class="color-dot" style="background:#8D6E63;"></span>Brown/Tan</span>
          </div>
        </div>

        <!-- Plant Sociability -->
        <div class="accordion">
          <button class="accordion-header" data-target="sociabilityFilterContent">
            <span>Plant Sociability</span>
            <i data-lucide="chevron-down" style="width:14px;height:14px;"></i>
          </button>
          <div class="accordion-content" id="sociabilityFilterContent">
            <span class="chip-filter" data-group="sociability" data-val="Solitary">Less Social / Solitary</span>
            <span class="chip-filter" data-group="sociability" data-val="Moderate">Medium / Moderate Spreader</span>
            <span class="chip-filter" data-group="sociability" data-val="Gregarious">Highly Social / Gregarious</span>
          </div>
        </div>

      </div>

      <!-- Mobile Drawer Footer -->
      <div class="sidebar-mobile-footer">
        <button id="resetAllFiltersMobileBtn" class="btn btn-secondary">Reset</button>
        <button id="applyFiltersMobileBtn" class="btn btn-primary" style="flex:1;">
          View <span id="mobileFilteredCount">184</span> Plants
        </button>
      </div>

    </aside>

    <!-- Main Content Grid -->
    <main class="main-content">
      
      <!-- Mobile Search Bar (prominent on mobile / <= 1024px) -->
      <div class="mobile-search-bar">
        <div class="search-box">
          <i data-lucide="search" class="search-icon" style="width:16px;height:16px;"></i>
          <input type="text" id="mobileSearchInput" class="search-input" placeholder="Search Kansas City natives...">
          <button id="mobileSearchClearBtn" class="search-clear">
            <i data-lucide="x" style="width:14px;height:14px;"></i>
          </button>
        </div>
      </div>

      <!-- Controls Bar -->
      <div class="controls-bar">
        <div class="results-and-mobile-filter">
          <button id="openSidebarBtn" class="btn btn-filter-toggle">
            <i data-lucide="sliders-horizontal" style="width:15px;height:15px;"></i>
            <span>Filters</span>
            <span id="mobileFilterBadge" class="filter-count-badge" style="display:none;">0</span>
          </button>
          <div class="results-count" id="resultsCount">
            Showing <strong>184</strong> Kansas City Native Plants
          </div>
        </div>

        <div class="controls-actions" style="display:flex;align-items:center;flex-wrap:wrap;gap:12px;">
          <div class="sort-control">
            <label for="defaultNameDisplaySelect">Default Title:</label>
            <select id="defaultNameDisplaySelect" class="sort-select" title="Default name shown first when sorting by criteria other than name">
              <option value="common_first">Common Name First</option>
              <option value="scientific_first">Scientific Name First</option>
            </select>
          </div>

          <div class="sort-control">
            <label for="sortOrderSelect">Sort by:</label>
            <select id="sortOrderSelect" class="sort-select">
              <option value="keystone_first">KC Keystones &amp; Sweet 16 First</option>
              <option value="common_asc">Common Name (A to Z)</option>
              <option value="common_desc">Common Name (Z to A)</option>
              <option value="sci_asc">Scientific Name (A to Z)</option>
              <option value="sci_desc">Scientific Name (Z to A)</option>
              <option value="height_asc">Mature Height (Low to High)</option>
              <option value="height_desc">Mature Height (High to Low)</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Active Filters Tag Bar -->
      <div id="activeFiltersBar" class="active-filters-bar" style="display:none;"></div>

      <!-- Plants Grid -->
      <div id="plantsGrid" class="plants-grid"></div>

      <!-- Empty State -->
      <div id="emptyState" style="display:none;text-align:center;padding:60px 20px;background:var(--bg-surface);border-radius:var(--radius-lg);border:1px solid var(--border-subtle);">
        <div style="font-size:48px;margin-bottom:12px;">🍃</div>
        <h3 style="font-size:18px;font-weight:700;margin-bottom:6px;">No Kansas City native plants match your filters</h3>
        <p style="font-size:13px;color:var(--text-muted);margin-bottom:16px;">Try adjusting your light, moisture, or habitat criteria</p>
        <button id="resetFiltersEmptyBtn" class="btn btn-secondary">Reset All Filters</button>
      </div>

    </main>

  </div>

  <!-- Staging Drawer & Overlay -->
  <div class="drawer-overlay" id="drawerOverlay"></div>
  <aside class="staging-drawer" id="stagingDrawer">
    <div class="drawer-header">
      <h2>
        <i data-lucide="clipboard-check" style="color:var(--primary);"></i>
        <span>Consultation Report</span>
      </h2>
      <button id="closeDrawerBtn" class="btn-icon">
        <i data-lucide="x"></i>
      </button>
    </div>

    <div class="drawer-body">
      <!-- Client Metadata Form -->
      <div class="client-meta-form">
        <div class="form-group">
          <label for="clientNameInput">Client Name</label>
          <input type="text" id="clientNameInput" placeholder="e.g. Eleanor Vance">
        </div>
        <div class="form-group">
          <label for="projectAddressInput">Project Address / Location</label>
          <input type="text" id="projectAddressInput" placeholder="e.g. 4520 Rockhill Rd, Kansas City, MO">
        </div>
        <div class="form-group">
          <label for="consultDateInput">Consultation Date</label>
          <input type="date" id="consultDateInput">
        </div>
        <div class="form-group">
          <label for="advisorNameInput">Nature Advisor Name</label>
          <input type="text" id="advisorNameInput" placeholder="Sign in with Google to auto-fill">
        </div>
        <div class="form-group">
          <label for="advisorNotesInput">Advisor Overview & Site Strategy</label>
          <textarea id="advisorNotesInput" rows="3" placeholder="Summary of soil, sun microclimates, and ecological goals..."></textarea>
        </div>
      </div>

      <!-- Staged Plants List -->
      <div>
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
          <span style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.04em;color:var(--text-secondary);">
            Selected Plants (<span id="stagedCount">0</span>)
          </span>
          <button id="clearAllStagedBtn" class="clear-all-btn">Clear All</button>
        </div>
        <div id="stagedList" class="staged-list">
          <div style="text-align:center;padding:30px 10px;color:var(--text-muted);font-size:13px;">
            No plants added to report yet.<br>Click <strong>+ Add to Report</strong> on any plant card.
          </div>
        </div>
      </div>
    </div>

    <!-- Drawer Footer Actions -->
    <div class="drawer-footer">
      <button id="copyMarkdownReportBtn" class="btn btn-secondary" style="width:100%;">
        <i data-lucide="copy"></i>
        <span>Copy Formatted Markdown Report</span>
      </button>
      <button id="downloadHtmlReportBtn" class="btn btn-secondary" style="width:100%;">
        <i data-lucide="download"></i>
        <span>Download Formatted Document (.doc / .html)</span>
      </button>
      <button id="exportGoogleDocsBtn" class="btn btn-primary" style="width:100%;">
        <i data-lucide="file-text"></i>
        <span>Export Directly to Google Docs</span>
      </button>
    </div>
  </aside>

  <!-- Google Sign-In Modal -->
  <dialog id="googleAuthModal">
    <div class="dialog-header">
      <div style="display:flex;align-items:center;gap:10px;">
        <svg style="width:24px;height:24px;" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
        <h3 style="font-size:17px;font-weight:800;">Sign in with Google</h3>
      </div>
      <button onclick="document.getElementById('googleAuthModal').close()" class="btn-icon">
        <i data-lucide="x"></i>
      </button>
    </div>
    <div class="dialog-body" style="text-align:center;">
      <p style="font-size:13px;color:var(--text-secondary);margin-bottom:18px;line-height:1.5;">
        Sign in with your Google account to enable live Cloud Firestore database synchronization, advisor record editing, and Google Drive consultation report exports.
      </p>

      <!-- Origin warning banner (shown when loaded via content:// or file://) -->
      <div id="gsiOriginWarning" style="display:none;background:#FFF3CD;color:#856404;border:1px solid #FFEEBA;padding:12px;border-radius:var(--radius-md);margin-bottom:14px;text-align:left;font-size:12px;line-height:1.5;">
        <strong>Google Protocol Notice:</strong> This file is open via <code>content://</code> preview. Google OAuth strictly blocks sign-in from <code>content://</code> URIs (Error 400). Run <code>python3 app/server.py</code> and open <a href="http://localhost:8080" target="_blank" style="color:var(--primary);font-weight:700;text-decoration:underline;">http://localhost:8080</a> in Chrome.
      </div>

      <!-- Google Official One-Tap / Button container -->
      <div id="gsiButtonContainer" style="display:flex;justify-content:center;margin-bottom:12px;"></div>

      <button id="modalGoogleSignInBtn" class="btn btn-google" style="width:100%;max-width:320px;margin:0 auto 16px;padding:12px 18px;font-size:14px;box-shadow:var(--shadow-sm);">
        <svg style="width:18px;height:18px;" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
        <span>Continue with Google</span>
      </button>

      <div style="background:var(--bg-base);padding:14px;border-radius:var(--radius-md);text-align:left;font-size:12px;color:var(--text-muted);display:flex;flex-direction:column;gap:6px;">
        <div style="font-weight:700;color:var(--text-main);font-size:11px;text-transform:uppercase;letter-spacing:0.04em;">Integrated Nature Advisor Permissions</div>
        <div>• Cloud Firestore shared database synchronization</div>
        <div>• Google Docs consultation report creation directly in your Google Drive</div>
        <div>• Edit and submit native plant records and URLs</div>
      </div>
    </div>
  </dialog>

  <!-- Google OAuth Protocol Notice Modal (for content:// or file:// origins) -->
  <dialog id="contentUriNoticeModal">
    <div class="dialog-header">
      <div style="display:flex;align-items:center;gap:10px;">
        <i data-lucide="shield-alert" style="color:var(--accent-orange);width:24px;height:24px;"></i>
        <h3 style="font-size:16px;font-weight:800;color:var(--text-main);">Google OAuth Protocol Notice</h3>
      </div>
      <button onclick="document.getElementById('contentUriNoticeModal').close()" class="btn-icon">
        <i data-lucide="x"></i>
      </button>
    </div>
    <div class="dialog-body" style="font-size:13px;color:var(--text-secondary);line-height:1.6;">
      <div style="background:#FFF3CD;color:#856404;border:1px solid #FFEEBA;padding:12px;border-radius:var(--radius-md);margin-bottom:14px;font-size:12px;">
        <strong>Error 400: origin=content://...</strong><br>
        This file was opened directly from Android file storage (<code>content://</code>). Google's OAuth security policy strictly blocks web sign-in from <code>content://</code> and <code>file://</code> URLs.
      </div>
      <p style="margin-bottom:10px;">
        To sign in with Google and enable live Cloud Firestore syncing and Google Drive export:
      </p>
      <ol style="margin-left:20px;margin-bottom:14px;display:flex;flex-direction:column;gap:6px;">
        <li>Start the local server in your terminal: <code style="background:var(--bg-base);padding:2px 6px;border-radius:4px;font-weight:700;">python3 app/server.py</code></li>
        <li>Open Chrome on your device and navigate to <a href="http://localhost:8080" target="_blank" style="color:var(--primary);font-weight:700;text-decoration:underline;">http://localhost:8080</a>.</li>
      </ol>
      <div style="background:var(--bg-base);border:1px solid var(--border-subtle);border-radius:var(--radius-md);padding:12px;margin-bottom:14px;">
        <strong style="color:var(--text-main);">Offline Features Fully Functional:</strong><br>
        All 184 native plant species, advanced search, Sweet 16 & Keystone filters, staging, custom notes, Markdown report copying, and formatted document downloads work 100% offline right here without signing in!
      </div>
      <div style="display:flex;gap:10px;justify-content:flex-end;">
        <button onclick="document.getElementById('contentUriNoticeModal').close()" class="btn btn-secondary">
          Continue Offline
        </button>
        <a href="http://localhost:8080" target="_blank" class="btn btn-primary" style="text-decoration:none;display:inline-flex;align-items:center;gap:6px;">
          <i data-lucide="external-link"></i>
          <span>Open http://localhost:8080</span>
        </a>
      </div>
    </div>
  </dialog>

  <!-- Safari / Pop-up Blocked Dialog -->
  <dialog id="popupBlockedModal">
    <div class="dialog-header">
      <div style="display:flex;align-items:center;gap:10px;">
        <i data-lucide="alert-circle" style="color:var(--accent-orange);width:24px;height:24px;"></i>
        <h3 style="font-size:16px;font-weight:800;color:var(--text-main);">Safari Blocked the Sign-In Window</h3>
      </div>
      <button onclick="document.getElementById('popupBlockedModal').close()" class="btn-icon">
        <i data-lucide="x"></i>
      </button>
    </div>
    <div class="dialog-body" style="font-size:13px;color:var(--text-secondary);line-height:1.6;">
      <p style="margin-bottom:12px;">
        iPhone Safari has <strong>Block Pop-ups</strong> enabled by default, which blocks the Google sign-in window from opening.
      </p>
      <div style="background:var(--bg-base);padding:14px;border-radius:var(--radius-md);border:1px solid var(--border-subtle);margin-bottom:16px;display:flex;flex-direction:column;gap:8px;">
        <div style="font-weight:700;color:var(--text-main);">To allow sign-in on iPhone:</div>
        <div>1. Open iPhone <strong>Settings</strong></div>
        <div>2. Scroll down and tap <strong>Safari</strong></div>
        <div>3. Turn OFF <strong>Block Pop-ups</strong></div>
        <div>4. Return to Safari and tap <strong>Sign In with Google</strong> again</div>
      </div>
      <div style="background:var(--bg-base);border:1px solid var(--border-subtle);border-radius:var(--radius-md);padding:12px;margin-bottom:16px;">
        <strong style="color:var(--text-main);">In-App Browser Note:</strong><br>
        If you opened this link from a text message or chat app, tap the <strong>Safari compass icon</strong> (bottom right) to open in real Safari.
      </div>
      <div style="display:flex;gap:10px;justify-content:flex-end;">
        <button onclick="document.getElementById('popupBlockedModal').close()" class="btn btn-secondary">
          Close
        </button>
        <button onclick="document.getElementById('popupBlockedModal').close(); triggerGoogleSignIn();" class="btn btn-primary" style="display:inline-flex;align-items:center;gap:6px;">
          <i data-lucide="refresh-cw"></i>
          <span>Try Again</span>
        </button>
      </div>
    </div>
  </dialog>

  <!-- User Profile & Sign Out Modal -->
  <dialog id="userProfileModal">
    <div class="dialog-header">
      <h3 style="font-size:16px;font-weight:800;">Google Account</h3>
      <button onclick="document.getElementById('userProfileModal').close()" class="btn-icon">
        <i data-lucide="x"></i>
      </button>
    </div>
    <div class="dialog-body" style="text-align:center;">
      <div id="profileAvatarContainer" style="margin:0 auto 12px;width:64px;height:64px;border-radius:50%;background:var(--primary-light);color:var(--primary);display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:800;overflow:hidden;border:2px solid var(--primary-border);"></div>
      <h4 id="profileNameTxt" style="font-size:17px;font-weight:800;color:var(--text-main);"></h4>
      <p id="profileEmailTxt" style="font-size:13px;color:var(--text-secondary);margin-bottom:6px;"></p>
      <div style="display:inline-flex;align-items:center;gap:6px;background:var(--primary-light);color:var(--primary);padding:3px 12px;border-radius:var(--radius-full);font-size:11px;font-weight:700;margin-bottom:20px;">
        <i data-lucide="shield-check" style="width:13px;height:13px;"></i>
        <span>Google Verified Nature Advisor</span>
      </div>

      <div style="background:var(--bg-base);padding:12px;border-radius:var(--radius-md);border:1px solid var(--border-subtle);text-align:left;font-size:12px;color:var(--text-secondary);margin-bottom:16px;">
        <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
          <span>Firestore Integration:</span>
          <strong style="color:var(--accent-keystone);">Active & Connected</strong>
        </div>
        <div style="display:flex;justify-content:space-between;">
          <span>Google Drive Access:</span>
          <strong style="color:var(--primary);">Authorized</strong>
        </div>
      </div>

      <button id="signOutGoogleBtn" class="btn btn-secondary" style="width:100%;color:var(--danger);border-color:var(--danger-bg);">
        <i data-lucide="log-out"></i>
        <span>Sign Out</span>
      </button>
    </div>
  </dialog>

  <!-- Plant Detail Dialog -->
  <dialog id="plantDetailModal">
    <div class="dialog-header">
      <div>
        <h3 id="modalCommonName" style="font-size:18px;font-weight:800;line-height:1.2;"></h3>
        <p id="modalSciName" style="font-family:var(--font-serif);font-style:italic;font-size:13px;color:var(--text-muted);"></p>
        <div id="modalBadges" style="display:flex;gap:8px;margin-top:6px;flex-wrap:wrap;"></div>
      </div>
      <button onclick="document.getElementById('plantDetailModal').close()" class="btn-icon">
        <i data-lucide="x"></i>
      </button>
    </div>
    <div class="dialog-body">
      <!-- Image with caption -->
      <div style="border-radius:var(--radius-md);overflow:hidden;background:var(--bg-base);max-height:300px;">
        <img id="modalImg" src="" alt="" style="width:100%;height:260px;object-fit:cover;">
        <div id="modalImgAttr" style="padding:6px 12px;font-size:11px;color:var(--text-muted);background:var(--bg-surface-elevated);"></div>
      </div>

      <!-- Action bar in modal -->
      <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
        <a id="modalOfficialUrl" href="#" target="_blank" rel="noopener noreferrer" class="btn btn-secondary" style="font-size:12px;">
          <i data-lucide="external-link"></i>
          <span>Official Plant Profile</span>
        </a>
        <button id="modalAddToReportBtn" class="btn btn-primary" style="font-size:12px;margin-left:auto;">
          <i data-lucide="plus"></i>
          <span>Add to Report</span>
        </button>
        <button id="modalEditBtn" class="btn btn-secondary" style="font-size:12px;">
          <i data-lucide="edit-3"></i>
          <span>Edit Record</span>
        </button>
      </div>

      <!-- Advisor Description -->
      <div style="background:var(--bg-base);padding:14px;border-radius:var(--radius-md);border-left:4px solid var(--primary);">
        <div style="font-size:11px;font-weight:800;text-transform:uppercase;color:var(--primary);margin-bottom:4px;">Advisor Description</div>
        <p id="modalAdvisorDesc" style="font-size:13px;line-height:1.5;color:var(--text-main);"></p>
      </div>

      <!-- Specifications Grid -->
      <div class="specs-grid">
        <div class="spec-item">
          <span class="spec-label">Light</span>
          <span class="spec-value" id="modalLight">-</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">Moisture</span>
          <span class="spec-value" id="modalMoisture">-</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">Mature Height</span>
          <span class="spec-value" id="modalHeight">-</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">Soil Types</span>
          <span class="spec-value" id="modalSoil">-</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">Bloom Period</span>
          <span class="spec-value" id="modalBloomPeriod">-</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">Bloom Color</span>
          <span class="spec-value" id="modalBloomColor">-</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">Garden Layer</span>
          <span class="spec-value" id="modalLayer">-</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">Plant Sociability</span>
          <span class="spec-value" id="modalSociability">-</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">Native Habitat</span>
          <span class="spec-value" id="modalHabitat">-</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">Plant Type</span>
          <span class="spec-value" id="modalPlantType">-</span>
        </div>
      </div>

      <!-- Wildlife & Keystone Interactions -->
      <div style="background:var(--bg-base);padding:14px;border-radius:var(--radius-md);">
        <div style="font-size:11px;font-weight:800;text-transform:uppercase;color:var(--accent-keystone);margin-bottom:6px;">Wildlife & Ecological Value</div>
        <p id="modalWildlife" style="font-size:13px;line-height:1.5;color:var(--text-secondary);"></p>
      </div>

    </div>
  </dialog>

  <!-- Edit Plant Dialog -->
  <dialog id="editPlantModal">
    <div class="dialog-header">
      <h3 style="font-size:16px;font-weight:800;">Edit Plant Record</h3>
      <button onclick="document.getElementById('editPlantModal').close()" class="btn-icon">
        <i data-lucide="x"></i>
      </button>
    </div>
    <form id="editPlantForm" class="dialog-body">
      <input type="hidden" id="editPlantId">
      <div class="form-group">
        <label for="editCommonName">Common Name</label>
        <input type="text" id="editCommonName" required>
      </div>
      <div class="form-group">
        <label for="editSciName">Scientific Name</label>
        <input type="text" id="editSciName" required>
      </div>
      <div class="form-group">
        <label for="editOfficialUrl">Official Plant Profile URL</label>
        <input type="url" id="editOfficialUrl" placeholder="https://grownative.org/native_plants/...">
      </div>
      <div class="form-group">
        <label for="editAdvisorDesc">Advisor Description</label>
        <textarea id="editAdvisorDesc" rows="3" required></textarea>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
        <div class="form-group">
          <label for="editLight">Light Requirements</label>
          <input type="text" id="editLight">
        </div>
        <div class="form-group">
          <label for="editMoisture">Moisture</label>
          <input type="text" id="editMoisture">
        </div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
        <div class="form-group">
          <label for="editHeight">Mature Height</label>
          <input type="text" id="editHeight">
        </div>
        <div class="form-group">
          <label for="editSociability">Plant Sociability</label>
          <input type="text" id="editSociability">
        </div>
      </div>
      <div class="form-group">
        <label for="editImageUrl">Image URL</label>
        <input type="url" id="editImageUrl">
      </div>
      <div class="form-group">
        <label for="editImageAttr">Photographer / Attribution</label>
        <input type="text" id="editImageAttr">
      </div>
      <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:10px;">
        <button type="button" onclick="document.getElementById('editPlantModal').close()" class="btn btn-secondary">Cancel</button>
        <button type="submit" class="btn btn-primary">Save Changes to Local & Shared Database</button>
      </div>
    </form>
  </dialog>

  <!-- Database Sync & Admin Dialog -->
  <dialog id="syncModal">
    <div class="dialog-header">
      <h3 style="font-size:16px;font-weight:800;">Shared Master Database Status</h3>
      <button onclick="document.getElementById('syncModal').close()" class="btn-icon">
        <i data-lucide="x"></i>
      </button>
    </div>
    <div class="dialog-body">
      <div style="background:var(--bg-base);padding:14px;border-radius:var(--radius-md);border:1px solid var(--border-subtle);display:flex;flex-direction:column;gap:8px;">
        <div style="display:flex;justify-content:space-between;font-size:13px;">
          <span>Database Engine:</span>
          <strong id="dbEngineTxt" style="color:var(--primary);">Active Shared Master Catalog</strong>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:13px;">
          <span>Master Plants Count:</span>
          <strong id="dbCountTxt">185 Species</strong>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:13px;">
          <span>Last Synchronized:</span>
          <strong id="dbLastSyncTxt">Just now</strong>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:13px;">
          <span>Custom Local Edits:</span>
          <strong id="dbCustomCountTxt">0 Modified</strong>
        </div>
      </div>

      <!-- Cloud Target Status Badge -->
      <div style="background:var(--bg-base);padding:12px;border-radius:var(--radius-md);border:1px solid var(--border-subtle);display:flex;align-items:center;justify-content:space-between;font-size:12px;">
        <div style="display:flex;align-items:center;gap:8px;">
          <i data-lucide="cloud" style="width:16px;height:16px;color:var(--primary);"></i>
          <div>
            <div style="font-weight:700;color:var(--text-main);">Google Cloud Firestore</div>
            <div style="font-size:11px;color:var(--text-muted);font-family:monospace;">deep-roots-nature-advisors</div>
          </div>
        </div>
        <span style="font-size:11px;font-weight:700;padding:3px 10px;border-radius:999px;background:rgba(46,125,50,0.12);color:var(--primary);border:1px solid rgba(46,125,50,0.25);">Connected</span>
      </div>

      <div style="display:flex;flex-direction:column;gap:10px;">
        <button id="refreshFromDbBtn" class="btn btn-primary" style="width:100%;font-size:13px;">
          <i data-lucide="refresh-cw"></i>
          <span>Pull Fresh Data from Master Database</span>
        </button>
        <button id="seedFirestoreBtn" class="btn btn-secondary" style="width:100%;font-size:12px;color:var(--primary);">
          <i data-lucide="upload-cloud"></i>
          <span>Upload Master Plant Catalog to Firestore</span>
        </button>
        <button id="resetCustomEditsBtn" class="btn btn-secondary" style="width:100%;font-size:12px;color:var(--danger);">
          <i data-lucide="rotate-ccw"></i>
          <span>Reset Local Edits to Clean Master Catalog</span>
        </button>
        <div style="border-top:1px solid var(--border-subtle);padding-top:10px;">
          <label class="btn btn-secondary" style="width:100%;font-size:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;box-sizing:border-box;">
            <i data-lucide="file-up"></i>
            <span>Import Plants JSON (Android Backup)</span>
            <input type="file" id="importJsonFileInput" accept=".json" style="display:none;">
          </label>
        </div>
      </div>
    </div>
  </dialog>

  <!-- Google Docs Export Success Dialog -->
  <dialog id="exportSuccessModal">
    <div class="dialog-header">
      <h3 style="font-size:16px;font-weight:800;color:var(--accent-keystone);">Document Exported Successfully!</h3>
      <button onclick="document.getElementById('exportSuccessModal').close()" class="btn-icon">
        <i data-lucide="x"></i>
      </button>
    </div>
    <div class="dialog-body" style="text-align:center;">
      <div style="font-size:44px;margin-bottom:8px;">📄</div>
      <h4 id="exportDocTitle" style="font-size:16px;font-weight:700;margin-bottom:6px;"></h4>
      <p style="font-size:13px;color:var(--text-secondary);margin-bottom:20px;">
        Your consultation report has been saved directly to your Google Drive.
      </p>
      <a id="exportDocLink" href="#" target="_blank" rel="noopener noreferrer" class="btn btn-primary" style="padding:10px 20px;">
        <i data-lucide="external-link"></i>
        <span>Open in Google Docs</span>
      </a>
    </div>
  </dialog>

  <!-- Toast Notification Container -->
  <div class="toast-container" id="toastContainer"></div>

  <!-- Embedded Master Plant Data (184 Species from Shared Database) -->
  <script type="application/json" id="embeddedMasterPlants">
"""

html_footer = """
  </script>

  <!-- Main ES Module Application Logic -->
  <script type="module">
    // Application State
    const state = {
      allPlants: [],
      filteredPlants: [],
      stagedPlants: JSON.parse(localStorage.getItem('dr_staged_plants') || '[]'),
      clientMeta: JSON.parse(localStorage.getItem('dr_client_meta') || '{"name":"","address":"","date":"","advisor":"","notes":""}'),
      customPlants: JSON.parse(localStorage.getItem('dr_custom_plants') || '{}'),
      filters: {
        search: '',
        sweet16: false,
        keystone: false,
        habitat: new Set(),
        light: new Set(),
        moisture: new Set(),
        height: new Set(),
        type: new Set(),
        layer: new Set(),
        season: new Set(),
        bloomColor: new Set(),
        sociability: new Set(),
      },
      sortOrder: localStorage.getItem('dr_sort_order') || 'common_asc',
      defaultNameDisplay: localStorage.getItem('dr_default_name_display') || 'common_first',
      currentUser: JSON.parse(localStorage.getItem('dr_current_user') || 'null'),
      gdriveToken: localStorage.getItem('dr_gdrive_token') || null,
      activeModalPlant: null,
      lastSyncTime: new Date().toLocaleTimeString()
    };

    function shouldShowScientificFirst() {
      if (state.sortOrder === 'sci_asc' || state.sortOrder === 'sci_desc') {
        return true;
      }
      if (state.sortOrder === 'common_asc' || state.sortOrder === 'common_desc') {
        return false;
      }
      return state.defaultNameDisplay === 'scientific_first';
    }

    // Google Web Application Client ID (from client_secret_636374214354-idc96pfjogkq13cqochh48it37h7jele...)
        // Authoritative Deep Roots Sweet 16 & Keystone definitions
    const SWEET_16_SPECIES = new Set([
      'echinacea purpurea', 'coreopsis lanceolata', 'symphyotrichum oblongifolium', 
      'bouteloua curtipendula', 'asclepias verticillata', 'aquilegia canadensis',
      'sporobolus heterolepis', 'zizia aurea', 'asclepias tuberosa', 'monarda fistulosa',
      'penstemon digitalis', 'baptisia australis', 'glandularia canadensis',
      'schizachyrium scoparium', 'packera obovata', 'geranium maculatum'
    ]);

    function isSweet16(plant) {
      if (!plant) return false;
      if (plant.is_sweet16 === true || plant.is_sweet_16 === true) return true;
      const sci = (plant.scientific_name || '').toLowerCase().trim();
      if (SWEET_16_SPECIES.has(sci)) return true;
      const tags = plant.special_tags || [];
      return tags.some(t => String(t).toLowerCase().includes('sweet 16'));
    }

    function isKcKeystone(plant) {
      if (!plant) return false;
      if (plant.is_kc_keystone === true || plant.isKcKeystone === true) return true;
      const tags = plant.special_tags || [];
      return tags.some(t => String(t).toLowerCase().includes('keystone'));
    }

    const GOOGLE_CLIENT_ID = "636374214354-idc96pfjogkq13cqochh48it37h7jele.apps.googleusercontent.com";
    let tokenClient = null;

    // Detect non-HTTP schemes (content:// or file://)
    function isNonHttpOrigin() {
      return window.location.protocol === 'content:' ||
             window.location.protocol === 'file:' ||
             !window.location.origin ||
             window.location.origin === 'null' ||
             window.location.origin.startsWith('content:');
    }

    // Helper: Detect in-app webview on iOS (e.g. Messages, WhatsApp, Slack, Instagram)
    function isIosInAppBrowser() {
      const ua = navigator.userAgent || '';
      const isIOS = /iPad|iPhone|iPod/.test(ua) && !window.MSStream;
      if (!isIOS) return false;
      return (ua.includes('FBAN') || ua.includes('FBAV') || ua.includes('Instagram') ||
              ua.includes('Line') || ua.includes('Twitter') || ua.includes('MicroMessenger') ||
              ua.includes('Snapchat') || (!ua.includes('Safari') && ua.includes('Mobile')));
    }

    function showPopupBlockedNotice() {
      const modal = document.getElementById('popupBlockedModal');
      if (modal) {
        modal.showModal();
        if (window.lucide) lucide.createIcons();
      } else {
        alert("Safari blocked the Google Sign-In window. On iPhone, open Settings > Safari and turn off Block Pop-ups, then tap Sign In again.");
      }
    }

    // Initialize Google Identity Services
    function initGoogleAuth() {
      if (isNonHttpOrigin()) {
        const warnDiv = document.getElementById('gsiOriginWarning');
        if (warnDiv) warnDiv.style.display = 'block';
      }

      if (window.google && window.google.accounts) {
        // Initialize ID token client (for standard button in modal)
        try {
          google.accounts.id.initialize({
            client_id: GOOGLE_CLIENT_ID,
            callback: handleGoogleIdTokenResponse,
            auto_select: false
          });
          const btnDiv = document.getElementById("gsiButtonContainer");
          if (btnDiv && !isNonHttpOrigin()) {
            google.accounts.id.renderButton(btnDiv, {
              theme: "outline",
              size: "large",
              width: 280,
              text: "continue_with"
            });
          }
        } catch (e) {
          console.warn("GSI ID init notice:", e);
        }

        // Initialize OAuth 2.0 Token Client for Google Drive & Firestore
        try {
          tokenClient = google.accounts.oauth2.initTokenClient({
            client_id: GOOGLE_CLIENT_ID,
            scope: 'https://www.googleapis.com/auth/datastore https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid',
            callback: handleGoogleTokenResponse,
            error_callback: (err) => {
              console.warn("Google Token Client Error:", err);
              if (err && (err.type === 'popup_blocked' || err.type === 'popup_closed')) {
                showPopupBlockedNotice();
              } else if (err && err.message) {
                showToast("Google Sign-In: " + err.message, "warning", 6000);
              }
            }
          });
        } catch (e) {
          console.warn("GSI OAuth Token Client notice:", e);
        }
      }
    }
    window.initGoogleAuth = initGoogleAuth;

    // Trigger Google Sign-In with iOS & Pop-up Handling
    function triggerGoogleSignIn() {
      if (isNonHttpOrigin()) {
        const authModal = document.getElementById('googleAuthModal');
        if (authModal && authModal.open) authModal.close();

        const warningModal = document.getElementById('contentUriNoticeModal');
        if (warningModal) {
          warningModal.showModal();
        } else {
          alert("Google Sign-In blocked: Google OAuth requires an HTTP origin (e.g. http://localhost:8080) and forbids opening directly from Android file storage (content://). Run 'python3 app/server.py' in the terminal and open http://localhost:8080 in Chrome.");
        }
        return;
      }

      // Check if user is in an embedded webview on iOS (e.g. iMessage, SMS link, WhatsApp, Slack)
      if (isIosInAppBrowser()) {
        showPopupBlockedNotice();
        showToast("Tap the Safari compass icon (bottom right) to open in real Safari for Google Sign-In.", "warning", 9000);
        return;
      }

      // Lazy initialization if Google script loaded after initial DOM ready
      if (!tokenClient && window.google && window.google.accounts) {
        initGoogleAuth();
      }

      if (tokenClient) {
        try {
          tokenClient.requestAccessToken({ prompt: 'select_account' });
        } catch (err) {
          console.warn("requestAccessToken exception:", err);
          showPopupBlockedNotice();
        }
      } else if (window.google && window.google.accounts && window.google.accounts.id) {
        // Fallback for ID token prompt
        try {
          google.accounts.id.prompt((notification) => {
            if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
              console.warn("One Tap suppressed:", notification.getNotDisplayedReason());
              showPopupBlockedNotice();
            }
          });
        } catch (e) {
          showPopupBlockedNotice();
        }
      } else {
        // Library still downloading over cellular/slow network
        showToast("Connecting to Google Identity Services...", "info", 3000);
        let attempts = 0;
        const interval = setInterval(() => {
          attempts++;
          if (window.google && window.google.accounts) {
            clearInterval(interval);
            initGoogleAuth();
            if (tokenClient) {
              tokenClient.requestAccessToken({ prompt: 'select_account' });
            }
          } else if (attempts > 12) {
            clearInterval(interval);
            showToast("Could not load Google Sign-In library. Check your network or disable content blockers.", "danger", 6000);
          }
        }, 250);
      }
    }

    // Handle Google OAuth Access Token
    async function handleGoogleTokenResponse(tokenResponse) {
      if (tokenResponse.error) {
        console.error("Google Token Response Error:", tokenResponse);
        showToast("Google Sign-In Error: " + tokenResponse.error, "warning");
        return;
      }

      state.gdriveToken = tokenResponse.access_token;
      localStorage.setItem('dr_gdrive_token', tokenResponse.access_token);

      try {
        const res = await fetch("https://www.googleapis.com/oauth2/v3/userinfo", {
          headers: { Authorization: `Bearer ${tokenResponse.access_token}` }
        });
        if (res.ok) {
          const info = await res.json();
          const user = {
            uid: info.sub,
            name: info.name || 'Nature Advisor',
            email: info.email || '',
            photoURL: info.picture || '',
            accessToken: tokenResponse.access_token,
            role: (info.email && info.email.toLowerCase().includes('admin')) ? 'admin' : 'advisor'
          };
          setGoogleUser(user);
        }
      } catch (err) {
        console.error("UserInfo fetch error:", err);
      }
    }

    // Handle Google ID Token JWT
    function handleGoogleIdTokenResponse(response) {
      if (!response.credential) return;
      try {
        const base64Url = response.credential.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''));
        const payload = JSON.parse(jsonPayload);
        const user = {
          uid: payload.sub,
          name: payload.name || 'Nature Advisor',
          email: payload.email || '',
          photoURL: payload.picture || '',
          idToken: response.credential,
          role: (payload.email && payload.email.toLowerCase().includes('admin')) ? 'admin' : 'advisor'
        };
        setGoogleUser(user);
      } catch (e) {
        console.error("ID Token parse error:", e);
      }
    }

    // Set signed-in Google user
    async function setGoogleUser(user) {
      state.currentUser = user;
      localStorage.setItem('dr_current_user', JSON.stringify(user));
      renderAuthUser();
      showToast(`Signed in with Google as ${user.name}`);
      
      const modal = document.getElementById('googleAuthModal');
      if (modal && modal.open) modal.close();

      // Synchronize authenticated user profile to Cloud Firestore
      syncUserProfileToFirestore(user);
      tryLiveSyncFromDatabase();
    }

    // Sign out from Google
    function signOutGoogle() {
      state.currentUser = null;
      state.gdriveToken = null;
      localStorage.removeItem('dr_current_user');
      localStorage.removeItem('dr_gdrive_token');
      if (window.google && window.google.accounts && window.google.accounts.id) {
        google.accounts.id.disableAutoSelect();
      }
      renderAuthUser();
      const modal = document.getElementById('userProfileModal');
      if (modal && modal.open) modal.close();
      showToast("Signed out from Google");
    }

    // Sync authenticated user profile to Firestore
    async function syncUserProfileToFirestore(user) {
      const token = user.accessToken || state.gdriveToken;
      if (!token) return;

      try {
        const projectId = localStorage.getItem('dr_firestore_project_id') || 'deep-roots-nature-advisors';
        let dbId = localStorage.getItem('dr_firestore_database_id');
        if (!dbId || dbId === '(default)') dbId = 'deep-roots-nature-advisors';
        const firestoreUrl = `https://firestore.googleapis.com/v1/projects/${projectId}/databases/${dbId}/documents/users/${user.uid}`;
        await fetch(firestoreUrl, {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            fields: {
              uid: { stringValue: user.uid },
              name: { stringValue: user.name },
              email: { stringValue: user.email },
              photoURL: { stringValue: user.photoURL || '' },
              role: { stringValue: user.role || 'advisor' },
              last_login: { stringValue: new Date().toISOString() }
            }
          })
        });
      } catch (e) {
        console.warn("Firestore profile sync notice:", e);
      }
    }

    // Toast Helper
    window.showToast = function(msg, type = "success") {
      const container = document.getElementById('toastContainer');
      const toast = document.createElement('div');
      toast.className = `toast ${type}`;
      toast.innerHTML = `<span>${msg}</span>`;
      container.appendChild(toast);
      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(12px)';
        setTimeout(() => toast.remove(), 300);
      }, 3500);
    };

    // Safe getters for plant fields
    function getPlantUrl(p) {
      if (p.plant_url && p.plant_url.startsWith('http')) return p.plant_url;
      if (p.official_url && p.official_url.startsWith('http')) return p.official_url;
      if (p.sources && p.sources.length > 0) {
        for (const s of p.sources) {
          const u = s.source_url || s.url;
          if (u && u.startsWith('http')) return u;
        }
      }
      return `https://grownative.org/native_plants/${(p.common_names?.[0] || p.scientific_name).toLowerCase().replace(/[^a-z0-9]+/g, '-')}/`;
    }

    function getPlantHeight(p) {
      if (p.height_display) return p.height_display;
      if (p.mature_height && p.mature_height.display) return p.mature_height.display;
      if (p.mature_height_min || p.mature_height_max) {
        return `${p.mature_height_min || 1}–${p.mature_height_max || 3} ft`;
      }
      return '-';
    }

    function getPlantLayer(p) {
      return p.architectural_layer || p.ecological_layer || 'Herbaceous Layer';
    }

    function getPlantDesc(p) {
      return p.advisor_description || p.raw_desc || 'High-value native species for Kansas City landscapes.';
    }

    function getPlantSociability(p) {
      return p.sociability || p.plant_sociability || 'Medium / Moderate Spreading';
    }

    // Load and Synchronize Plants
    async function loadMasterPlants() {
      // 1. Initial load from local Firestore cache or embedded master catalog
      const cached = localStorage.getItem('dr_firestore_cache_plants');
      if (cached) {
        try {
          const parsedCache = JSON.parse(cached);
          if (Array.isArray(parsedCache) && parsedCache.length > 50) {
            state.allPlants = parsedCache;
            document.getElementById('dbEngineTxt').textContent = 'Cloud Firestore (Cached)';
          }
        } catch (e) {}
      }

      if (!state.allPlants || state.allPlants.length === 0) {
        const raw = document.getElementById('embeddedMasterPlants').textContent;
        try {
          state.allPlants = JSON.parse(raw);
        } catch (err) {
          console.error("Error loading embedded plants:", err);
        }
      }

      // Ensure all plants have consistent Sweet 16 & Keystone flags
      state.allPlants.forEach(p => {
        const s16 = isSweet16(p);
        p.is_sweet_16 = s16;
        p.is_sweet16 = s16;
        const key = isKcKeystone(p);
        p.is_kc_keystone = key;
        p.isKcKeystone = key;
      });

      // 2. Apply any custom local advisor edits
      applyCustomEditsToPlants();

      // 3. Attempt live sync from database endpoints
      await tryLiveSyncFromDatabase(false);

      applyFilters();
      updateHeaderInfo();
    }

    function applyCustomEditsToPlants() {
      const customs = state.customPlants;
      const count = Object.keys(customs).length;
      document.getElementById('dbCustomCountTxt').textContent = `${count} Modified`;

      state.allPlants.forEach((p, idx) => {
        const id = p.id || p.scientific_name;
        if (customs[id]) {
          state.allPlants[idx] = { ...p, ...customs[id] };
        }
      });
    }

    async function tryLiveSyncFromDatabase(showNotification = false) {
      // 1. Try local REST API endpoint first if running via server.py
      try {
        const res = await fetch('/api/plants?limit=300', { signal: AbortSignal.timeout(2000) });
        if (res.ok) {
          const data = await res.json();
          const remoteList = data.plants || data;
          if (Array.isArray(remoteList) && remoteList.length > 50) {
            replaceWithRemotePlants(remoteList);
            state.lastSyncTime = new Date().toLocaleTimeString();
            document.getElementById('dbEngineTxt').textContent = 'Live SQLite & Shared API';
            if (showNotification) showToast(`Synchronized ${remoteList.length} plants from local server.`);
            return;
          }
        }
      } catch (e) {}

      // 2. Try Cloud Firestore REST endpoint with pagination & multi-database fallback
      const projectId = localStorage.getItem('dr_firestore_project_id') || 'deep-roots-nature-advisors';
      let dbId = localStorage.getItem('dr_firestore_database_id');
      if (!dbId || dbId === '(default)') {
        dbId = 'deep-roots-nature-advisors';
        localStorage.setItem('dr_firestore_database_id', dbId);
      }
      const token = state.gdriveToken || (state.currentUser && state.currentUser.accessToken);
      const headers = {};
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      async function queryFirestoreDb(targetDb) {
        let docs = [];
        let pToken = '';
        let count = 0;
        let err = null;
        do {
          count++;
          let url = `https://firestore.googleapis.com/v1/projects/${projectId}/databases/${targetDb}/documents/plants?pageSize=100`;
          if (pToken) url += `&pageToken=${encodeURIComponent(pToken)}`;
          const res = await fetch(url, { headers, signal: AbortSignal.timeout(8000) });
          if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            err = { status: res.status, data: errData };
            break;
          }
          const data = await res.json();
          if (data.documents && data.documents.length > 0) {
            docs.push(...data.documents);
          }
          pToken = data.nextPageToken || '';
        } while (pToken && count < 10);
        return { docs, err };
      }

      try {
        let { docs: allDocs, err: syncError } = await queryFirestoreDb(dbId);

        // If (default) does not exist, attempt fallback to projectId
        if (syncError && syncError.data?.error?.message?.includes('database (default) does not exist') && dbId === '(default)') {
          console.info(`Database '(default)' not found. Checking database '${projectId}'...`);
          const fallback = await queryFirestoreDb(projectId);
          if (fallback.docs.length > 0 || !fallback.err) {
            allDocs = fallback.docs;
            syncError = fallback.err;
            dbId = projectId;
            localStorage.setItem('dr_firestore_database_id', projectId);
          }
        }

        if (allDocs.length > 0) {
          const parsed = allDocs.map(doc => parseFirestoreDoc(doc)).filter(Boolean);
          if (parsed.length > 0) {
            replaceWithRemotePlants(parsed);
            state.lastSyncTime = new Date().toLocaleTimeString();
            document.getElementById('dbEngineTxt').textContent = `Cloud Firestore (${dbId})`;
            updateHeaderInfo();
            try {
              localStorage.setItem('dr_firestore_cache_plants', JSON.stringify(parsed));
            } catch (e) {}
            showToast(`Synchronized ${parsed.length} plants directly from Cloud Firestore!`, 'success');
            return;
          }
        } else if (syncError) {
          const msg = syncError.data?.error?.message || `HTTP ${syncError.status}`;
          if (syncError.status === 403 && msg.includes('disabled')) {
            showToast("Cloud Firestore API is disabled in project deep-roots-nature-advisors. Please enable it in Google Cloud Console.", "warning", 9000);
          } else if (msg.includes('does not exist')) {
            showToast(`Database '${dbId}' does not exist in project '${projectId}'.`, "warning", 9000);
          } else if (syncError.status === 401 || syncError.status === 403) {
            if (showNotification) showToast("Firestore access denied. Sign in with Google to authenticate.", "warning");
          } else {
            console.warn("Firestore sync warning:", msg);
            if (showNotification) showToast("Firestore sync notice: " + msg, "warning");
          }
        }
      } catch (err) {
        console.warn("Firestore live sync exception:", err);
        if (showNotification) showToast("Could not reach Firestore: " + err.message, "warning");
      }
    }

    function replaceWithRemotePlants(remoteList) {
      if (!Array.isArray(remoteList) || remoteList.length === 0) return;
      state.allPlants = remoteList;
      applyCustomEditsToPlants();
      applyFilters();
      updateHeaderInfo();
      renderGrid();
    }

    function parseFirestoreValue(val) {
      if (!val) return null;
      if (val.stringValue !== undefined) return val.stringValue;
      if (val.integerValue !== undefined) return parseInt(val.integerValue, 10);
      if (val.doubleValue !== undefined) return parseFloat(val.doubleValue);
      if (val.booleanValue !== undefined) return val.booleanValue;
      if (val.timestampValue !== undefined) return val.timestampValue;
      if (val.arrayValue !== undefined) {
        return (val.arrayValue.values || []).map(parseFirestoreValue);
      }
      if (val.mapValue !== undefined) {
        const out = {};
        for (const [k, v] of Object.entries(val.mapValue.fields || {})) {
          out[k] = parseFirestoreValue(v);
        }
        return out;
      }
      return null;
    }

    function parseFirestoreDoc(doc) {
      if (!doc || !doc.fields) return null;
      const res = {};
      for (const [k, v] of Object.entries(doc.fields)) {
        res[k] = parseFirestoreValue(v);
      }
      if (!res.id && doc.name) {
        res.id = doc.name.split('/').pop();
      }

      // Format mature height display
      if (res.mature_height && typeof res.mature_height === 'object') {
        res.height_display = res.mature_height.display || `${res.mature_height.min_ft || ''}–${res.mature_height.max_ft || ''} ft`;
        if (res.mature_height.min_ft !== undefined) res.mature_height_min = res.mature_height.min_ft;
        if (res.mature_height.max_ft !== undefined) res.mature_height_max = res.mature_height.max_ft;
      }

      // Ensure plant_url from sources if missing
      if (!res.plant_url && Array.isArray(res.sources)) {
        for (const s of res.sources) {
          if (s && s.source_url && s.source_url.startsWith('http')) {
            res.plant_url = s.source_url;
            break;
          }
        }
      }
      res.plant_url = res.plant_url || '';

      // Normalize tags & sweet 16 / keystone flags
      const sci = (res.scientific_name || '').toLowerCase().trim();
      const tags = (res.special_tags || []).map(t => String(t).toLowerCase());
      const s16 = Boolean(
        res.is_sweet16 === true ||
        res.is_sweet_16 === true ||
        SWEET_16_SPECIES.has(sci) ||
        tags.some(t => t.includes('sweet 16'))
      );
      res.is_sweet_16 = s16;
      res.is_sweet16 = s16;

      const key = Boolean(
        res.is_kc_keystone === true ||
        res.isKcKeystone === true ||
        tags.some(t => t.includes('keystone'))
      );
      res.is_kc_keystone = key;
      res.isKcKeystone = key;

      return res;
    }

    function updateHeaderInfo() {
      document.getElementById('statDbCount').textContent = `${state.allPlants.length} Species`;
      document.getElementById('statSweet16Count').textContent = state.allPlants.filter(isSweet16).length;
      document.getElementById('statKeystoneCount').textContent = state.allPlants.filter(isKcKeystone).length;
      document.getElementById('dbCountTxt').textContent = `${state.allPlants.length} Species`;
      document.getElementById('dbLastSyncTxt').textContent = state.lastSyncTime;
      renderAuthUser();
    }

    // Render Auth in Header
    function renderAuthUser() {
      const container = document.getElementById('authContainer');
      const u = state.currentUser;
      if (u && u.name) {
        const firstName = u.name.split(' ')[0];
        container.innerHTML = `
          <button id="userProfileBtn" class="btn btn-secondary" style="padding:4px 10px;gap:8px;">
            ${u.photoURL ? `<img src="${u.photoURL}" style="width:24px;height:24px;border-radius:50%;object-fit:cover;">` : `
              <div style="width:24px;height:24px;border-radius:50%;background:var(--primary);color:#fff;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;">
                ${u.name.substring(0,2).toUpperCase()}
              </div>
            `}
            <span class="user-profile-name" style="font-size:12px;font-weight:700;">${firstName}</span>
          </button>
        `;
        document.getElementById('userProfileBtn').addEventListener('click', openUserProfileModal);

        // Set advisor name in report staging if blank
        const advInput = document.getElementById('advisorNameInput');
        if (!advInput.value) {
          advInput.value = u.name;
          state.clientMeta.advisor = u.name;
          localStorage.setItem('dr_client_meta', JSON.stringify(state.clientMeta));
        }
      } else {
        container.innerHTML = `
          <button id="headerSignInBtn" class="btn btn-google">
            <svg style="width:16px;height:16px;" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
            <span class="btn-text-long">Sign In with Google</span>
            <span class="btn-text-short">Sign In</span>
          </button>
        `;
        document.getElementById('headerSignInBtn').addEventListener('click', () => {
          triggerGoogleSignIn();
        });
      }
      if (window.lucide) lucide.createIcons();
    }

    function openUserProfileModal() {
      const u = state.currentUser;
      if (!u) return;

      const avatarBox = document.getElementById('profileAvatarContainer');
      if (u.photoURL) {
        avatarBox.innerHTML = `<img src="${u.photoURL}" style="width:100%;height:100%;object-fit:cover;">`;
      } else {
        avatarBox.textContent = (u.name || 'NA').substring(0, 2).toUpperCase();
      }

      document.getElementById('profileNameTxt').textContent = u.name;
      document.getElementById('profileEmailTxt').textContent = u.email;
      document.getElementById('userProfileModal').showModal();
      if (window.lucide) lucide.createIcons();
    }

    // Filter Logic
    function applyFilters() {
      const f = state.filters;
      const search = f.search.toLowerCase().trim();

      state.filteredPlants = state.allPlants.filter(p => {
        // Search text
        if (search) {
          const matchCommon = (p.common_names || []).some(n => n.toLowerCase().includes(search));
          const matchSci = (p.scientific_name || '').toLowerCase().includes(search);
          const matchDesc = getPlantDesc(p).toLowerCase().includes(search);
          const matchHabitat = (p.native_environment || '').toLowerCase().includes(search);
          if (!matchCommon && !matchSci && !matchDesc && !matchHabitat) return false;
        }

        // Quick Toggles
        if (f.sweet16 && !isSweet16(p)) return false;
        if (f.keystone && !isKcKeystone(p)) return false;

        // Habitat
        if (f.habitat.size > 0) {
          const pEnv = p.native_environment || '';
          if (!f.habitat.has(pEnv)) return false;
        }

        // Light
        if (f.light.size > 0) {
          const lights = (p.light_requirements || []).map(l => l.toLowerCase());
          const matches = Array.from(f.light).some(val => lights.some(l => l.includes(val.toLowerCase())));
          if (!matches) return false;
        }

        // Moisture
        if (f.moisture.size > 0) {
          const moistures = (p.moisture_requirements || []).map(m => m.toLowerCase());
          const matches = Array.from(f.moisture).some(val => moistures.some(m => m.includes(val.toLowerCase())));
          if (!matches) return false;
        }

        // Plant Type
        if (f.type.size > 0) {
          const rawType = Array.isArray(p.plant_type) ? p.plant_type.join(' ') : (p.plant_type || '');
          const matches = Array.from(f.type).some(val => rawType.toLowerCase().includes(val.toLowerCase()));
          if (!matches) return false;
        }

        // Ecological / Garden Layer
        if (f.layer.size > 0) {
          const pLayer = getPlantLayer(p).toLowerCase();
          const matches = Array.from(f.layer).some(val => pLayer.includes(val.toLowerCase()));
          if (!matches) return false;
        }

        // Bloom Season
        if (f.season.size > 0) {
          const periods = (p.bloom_period || []).map(s => s.toLowerCase());
          const matches = Array.from(f.season).some(s => periods.some(p => p.includes(s.toLowerCase())));
          if (!matches) return false;
        }

        // Mature Height
        if (f.height.size > 0) {
          const minH = p.mature_height_min !== undefined && p.mature_height_min !== null
            ? p.mature_height_min
            : (p.mature_height?.min_ft ?? 0);
          const maxH = p.mature_height_max !== undefined && p.mature_height_max !== null
            ? p.mature_height_max
            : (p.mature_height?.max_ft ?? (minH || 0));

          const matches = Array.from(f.height).some(bracket => {
            if (bracket === '< 1 ft') return minH <= 1.0;
            if (bracket === '1 - 3 ft') return (maxH >= 1.0 && minH <= 3.0);
            if (bracket === '3 - 6 ft') return (maxH >= 3.0 && minH <= 6.0);
            if (bracket === '6 - 15 ft') return (maxH >= 6.0 && minH <= 15.0);
            if (bracket === '15+ ft') return (maxH >= 15.0);
            return false;
          });
          if (!matches) return false;
        }

        // Bloom Color
        if (f.bloomColor.size > 0) {
          const pColors = (p.bloom_color || p.bloomColor || []).map(c => String(c).toLowerCase().trim());
          const matches = Array.from(f.bloomColor).some(sel => {
            const s = sel.toLowerCase().trim();
            if (s === 'greenish') return pColors.some(c => c === 'greenish' || c === 'green');
            if (s === 'brown/tan') return pColors.some(c => c === 'brown/tan' || c === 'brown');
            return pColors.includes(s);
          });
          if (!matches) return false;
        }

        // Sociability
        if (f.sociability.size > 0) {
          const soc = getPlantSociability(p).toLowerCase();
          const matches = Array.from(f.sociability).some(s => soc.includes(s.toLowerCase()));
          if (!matches) return false;
        }

        return true;
      });

      sortPlants();
      renderGrid();
      renderActiveFilterTags();
    }

    function sortPlants() {
      const order = state.sortOrder;
      const showSciFirst = shouldShowScientificFirst();
      state.filteredPlants.sort((a, b) => {
        const sciA = a.scientific_name || '';
        const sciB = b.scientific_name || '';
        const commA = (a.common_names && a.common_names[0]) || sciA;
        const commB = (b.common_names && b.common_names[0]) || sciB;
        const nameA = showSciFirst ? sciA : commA;
        const nameB = showSciFirst ? sciB : commB;
        const hA = a.mature_height_max || 0;
        const hB = b.mature_height_max || 0;

        switch (order) {
          case 'keystone_first': {
            const keyA = (isKcKeystone(a) ? 2 : 0) + (isSweet16(a) ? 1 : 0);
            const keyB = (isKcKeystone(b) ? 2 : 0) + (isSweet16(b) ? 1 : 0);
            if (keyA !== keyB) return keyB - keyA;
            return nameA.localeCompare(nameB);
          }
          case 'common_asc':
            return commA.localeCompare(commB);
          case 'common_desc':
            return commB.localeCompare(commA);
          case 'sci_asc':
            return sciA.localeCompare(sciB);
          case 'sci_desc':
            return sciB.localeCompare(sciA);
          case 'height_asc':
            return (hA - hB) || nameA.localeCompare(nameB);
          case 'height_desc':
            return (hB - hA) || nameA.localeCompare(nameB);
          default:
            return 0;
        }
      });
    }

    // Render Active Filter Tags
    function renderActiveFilterTags() {
      const bar = document.getElementById('activeFiltersBar');
      bar.innerHTML = '';
      let count = 0;

      const addTag = (text, onRemove) => {
        count++;
        const tag = document.createElement('span');
        tag.className = 'active-tag';
        tag.innerHTML = `<span>${text}</span><button>&times;</button>`;
        tag.querySelector('button').addEventListener('click', onRemove);
        bar.appendChild(tag);
      };

      if (state.filters.sweet16) {
        addTag('⭐ Sweet 16', () => {
          state.filters.sweet16 = false;
          document.getElementById('toggleSweet16Btn').classList.remove('active');
          applyFilters();
        });
      }
      if (state.filters.keystone) {
        addTag('🌿 KC Keystone', () => {
          state.filters.keystone = false;
          document.getElementById('toggleKeystoneBtn').classList.remove('active');
          applyFilters();
        });
      }

      const groups = ['habitat', 'light', 'moisture', 'height', 'type', 'layer', 'season', 'bloomColor', 'sociability'];
      groups.forEach(g => {
        state.filters[g].forEach(val => {
          addTag(val, () => {
            state.filters[g].delete(val);
            const chip = document.querySelector(`.chip-filter[data-group="${g}"][data-val="${val}"]`);
            if (chip) chip.classList.remove('active');
            applyFilters();
          });
        });
      });

      if (count > 0) {
        bar.style.display = 'flex';
        const clearBtn = document.createElement('button');
        clearBtn.className = 'clear-all-btn';
        clearBtn.textContent = 'Clear All';
        clearBtn.addEventListener('click', resetAllFilters);
        bar.appendChild(clearBtn);
      } else {
        bar.style.display = 'none';
      }

      // Sync mobile filter badge count
      const mobileBadge = document.getElementById('mobileFilterBadge');
      if (mobileBadge) {
        if (count > 0) {
          mobileBadge.textContent = count;
          mobileBadge.style.display = 'inline-block';
        } else {
          mobileBadge.style.display = 'none';
        }
      }
    }

    function resetAllFilters() {
      state.filters.search = '';
      const sInput = document.getElementById('searchInput');
      if (sInput) sInput.value = '';
      const sClear = document.getElementById('searchClearBtn');
      if (sClear) sClear.style.display = 'none';

      const msInput = document.getElementById('mobileSearchInput');
      if (msInput) msInput.value = '';
      const msClear = document.getElementById('mobileSearchClearBtn');
      if (msClear) msClear.style.display = 'none';

      state.filters.sweet16 = false;
      document.getElementById('toggleSweet16Btn').classList.remove('active');
      state.filters.keystone = false;
      document.getElementById('toggleKeystoneBtn').classList.remove('active');
      
      const groups = ['habitat', 'light', 'moisture', 'height', 'type', 'layer', 'season', 'bloomColor', 'sociability'];
      groups.forEach(g => state.filters[g].clear());
      document.querySelectorAll('.chip-filter.active').forEach(c => c.classList.remove('active'));

      applyFilters();
    }

    // Render Grid
    function renderGrid() {
      const grid = document.getElementById('plantsGrid');
      const empty = document.getElementById('emptyState');
      const countEl = document.getElementById('resultsCount');

      countEl.innerHTML = `Showing <strong>${state.filteredPlants.length}</strong> of ${state.allPlants.length} Kansas City Native Plants`;
      const mobileFilteredCount = document.getElementById('mobileFilteredCount');
      if (mobileFilteredCount) mobileFilteredCount.textContent = state.filteredPlants.length;

      if (state.filteredPlants.length === 0) {
        grid.style.display = 'none';
        empty.style.display = 'block';
        return;
      }

      grid.style.display = 'grid';
      empty.style.display = 'none';
      grid.innerHTML = '';

      state.filteredPlants.forEach(plant => {
        const card = createPlantCard(plant);
        grid.appendChild(card);
      });

      if (window.lucide) lucide.createIcons();
    }

    function getBloomColorAccent(colorName, isDark) {
      const c = (colorName || '').toLowerCase().trim();
      if (isDark) {
        switch (c) {
          case 'yellow': return '#FFD54F';
          case 'purple': return '#CE93D8';
          case 'blue': return '#64B5F6';
          case 'white': return '#ECEFF1';
          case 'cream': return '#FFF59D';
          case 'pink': return '#F48FB1';
          case 'red': return '#EF5350';
          case 'orange': return '#FFB74D';
          case 'lavender': return '#B39DDB';
          case 'greenish':
          case 'green': return '#81C784';
          case 'brown/tan':
          case 'brown': return '#BCAAA4';
          default: return '#81C784';
        }
      } else {
        switch (c) {
          case 'yellow': return '#E5A800';
          case 'purple': return '#8E44AD';
          case 'blue': return '#1E88E5';
          case 'white': return '#78909C';
          case 'cream': return '#D4AC0D';
          case 'pink': return '#E91E63';
          case 'red': return '#C0392B';
          case 'orange': return '#E67E22';
          case 'lavender': return '#9B59B6';
          case 'greenish':
          case 'green': return '#2E7D32';
          case 'brown/tan':
          case 'brown': return '#8D6E63';
          default: return '#2E7D32';
        }
      }
    }

    function getBloomCardGradient(bloomColors, isDark) {
      if (!Array.isArray(bloomColors) || bloomColors.length === 0) {
        return isDark
          ? 'linear-gradient(135deg, #133621 0%, #0A2214 100%)'
          : 'linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%)';
      }

      const colorMap = isDark ? {
        'yellow': '#735100',
        'purple': '#4A148C',
        'blue': '#0D47A1',
        'white': '#37474F',
        'cream': '#6B5818',
        'pink': '#880E4F',
        'red': '#7F0000',
        'orange': '#8A3800',
        'lavender': '#4527A0',
        'greenish': '#1B5E20',
        'green': '#1B5E20',
        'brown/tan': '#3E2723',
        'brown': '#3E2723'
      } : {
        'yellow': '#FFB300',
        'purple': '#8E24AA',
        'blue': '#1E88E5',
        'white': '#B0BEC5',
        'cream': '#FFCA28',
        'pink': '#D81B60',
        'red': '#E53935',
        'orange': '#FB8C00',
        'lavender': '#7E57C2',
        'greenish': '#43A047',
        'green': '#43A047',
        'brown/tan': '#8D6E63',
        'brown': '#8D6E63'
      };

      const fallback = isDark ? '#133621' : '#2E7D32';
      const resolved = bloomColors.map(c => colorMap[(c || '').toLowerCase().trim()] || fallback);

      if (resolved.length === 1) {
        const c = resolved[0];
        return isDark
          ? `linear-gradient(135deg, ${c} 0%, rgba(19, 54, 33, 0.95) 100%)`
          : `linear-gradient(135deg, ${c} 0%, rgba(46, 125, 50, 0.75) 100%)`;
      } else if (resolved.length === 2) {
        return `linear-gradient(135deg, ${resolved[0]} 0%, ${resolved[1]} 100%)`;
      } else {
        // 3+ colors: Luminous multi-point mesh gradient matching Android app
        return `radial-gradient(circle at 15% 15%, ${resolved[0]} 0%, transparent 65%), ` +
               `radial-gradient(circle at 85% 85%, ${resolved[1]} 0%, transparent 65%), ` +
               `linear-gradient(135deg, ${resolved[2] || resolved[0]}, ${resolved[0]})`;
      }
    }

    // Create Plant Card
    function createPlantCard(plant) {
      const card = document.createElement('div');
      card.className = 'plant-card';
      const isDark = document.body.getAttribute('data-theme') === 'dark';
      const bloomColors = plant.bloom_color || plant.bloomColor || [];
      card.style.background = getBloomCardGradient(bloomColors, isDark);

      const showSciFirst = shouldShowScientificFirst();
      const commonName = (plant.common_names && plant.common_names[0]) || plant.scientific_name;
      const primaryName = showSciFirst ? (plant.scientific_name || commonName) : commonName;
      const secondaryName = showSciFirst ? commonName : (plant.scientific_name || '');
      const isStaged = state.stagedPlants.some(p => p.id === plant.id || p.scientific_name === plant.scientific_name);
      const imgUrl = (plant.images && plant.images[0] && plant.images[0].url) || '';

      const sunStr = (plant.light_requirements || []).join(', ') || 'Sun/Shade';
      const moistStr = (plant.moisture_requirements || []).join(', ') || 'Medium';
      const heightStr = getPlantHeight(plant);
      const layerStr = getPlantLayer(plant);
      const descStr = getPlantDesc(plant);

      let bloomPillHtml = '';
      if (Array.isArray(bloomColors) && bloomColors.length > 0) {
        const dots = bloomColors.slice(0, 3).map(c => {
          const col = getBloomColorAccent(c, isDark);
          return `<span style="width:7px;height:7px;border-radius:50%;background:${col};display:inline-block;flex-shrink:0;"></span>`;
        }).join('');
        bloomPillHtml = `<span class="meta-chip" style="display:inline-flex;align-items:center;gap:4px;">${dots}<span>${bloomColors.join('/')}</span></span>`;
      }

      card.innerHTML = `
        <div class="plant-card-inner">
          <div class="card-media">
            ${imgUrl ? `<img src="${imgUrl}" alt="${commonName}" loading="lazy" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1598880940371-c756e015fea1?auto=format&fit=crop&w=600&q=80';">` : `
              <div class="card-placeholder">
                <i data-lucide="sprout" style="width:36px;height:36px;"></i>
                <span style="font-size:11px;">Botanical Record</span>
              </div>
            `}
            <div class="card-badges">
              ${isSweet16(plant) ? `<span class="badge-sweet16">⭐ Sweet 16</span>` : ''}
              ${isKcKeystone(plant) ? `<span class="badge-keystone">🌿 Keystone</span>` : ''}
            </div>
            ${layerStr ? `<span class="badge-layer">${layerStr}</span>` : ''}
          </div>
          <div class="card-body">
            <div class="card-title-group">
              <h3 class="card-common-name card-primary-name ${showSciFirst ? 'is-scientific' : ''}">${primaryName}</h3>
              <p class="card-sci-name card-secondary-name ${!showSciFirst ? 'is-scientific' : ''}">${secondaryName}</p>
            </div>
            <div class="card-chips">
              <span class="meta-chip"><i data-lucide="sun" style="width:12px;height:12px;"></i> ${sunStr}</span>
              <span class="meta-chip"><i data-lucide="droplet" style="width:12px;height:12px;"></i> ${moistStr}</span>
              <span class="meta-chip"><i data-lucide="ruler" style="width:12px;height:12px;"></i> ${heightStr}</span>
              ${bloomPillHtml}
            </div>
            <p class="card-desc">${descStr}</p>
          </div>
          <div class="card-footer">
            <button class="btn-copy-desc" title="Copy Advisor Description">
              <i data-lucide="copy" style="width:13px;height:13px;"></i>
              <span>Copy</span>
            </button>
            <button class="btn-add-report ${isStaged ? 'staged' : ''}">
              <i data-lucide="${isStaged ? 'check' : 'plus'}" style="width:14px;height:14px;"></i>
              <span>${isStaged ? 'In Report' : 'Add to Report'}</span>
            </button>
          </div>
        </div>
      `;

      // Event Listeners
      card.querySelector('.card-media').addEventListener('click', () => openPlantDetail(plant));
      card.querySelector('.card-title-group').addEventListener('click', () => openPlantDetail(plant));

      card.querySelector('.btn-copy-desc').addEventListener('click', (e) => {
        e.stopPropagation();
        navigator.clipboard.writeText(descStr).then(() => {
          showToast(`Copied description for ${commonName}!`);
        });
      });

      const addBtn = card.querySelector('.btn-add-report');
      addBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleStagedPlant(plant);
      });

      return card;
    }

    // Staging Management
    function toggleStagedPlant(plant) {
      const idx = state.stagedPlants.findIndex(p => p.id === plant.id || p.scientific_name === plant.scientific_name);
      if (idx >= 0) {
        state.stagedPlants.splice(idx, 1);
        showToast(`Removed ${plant.common_names?.[0] || plant.scientific_name} from report.`);
      } else {
        state.stagedPlants.push({
          id: plant.id || plant.scientific_name,
          common_name: plant.common_names?.[0] || plant.scientific_name,
          scientific_name: plant.scientific_name,
          image_url: plant.images?.[0]?.url || '',
          plant_url: getPlantUrl(plant),
          advisor_description: getPlantDesc(plant),
          quantity: 1,
          custom_notes: '',
          sun: (plant.light_requirements || []).join(', '),
          moisture: (plant.moisture_requirements || []).join(', '),
          height: getPlantHeight(plant),
          layer: getPlantLayer(plant),
          sociability: getPlantSociability(plant),
          environment: plant.native_environment || ''
        });
        showToast(`Added ${plant.common_names?.[0] || plant.scientific_name} to report!`);
      }
      saveStaging();
      renderStaging();
      renderGrid();
    }

    function saveStaging() {
      localStorage.setItem('dr_staged_plants', JSON.stringify(state.stagedPlants));
      updateStagedBadge();
    }

    function updateStagedBadge() {
      const badge = document.getElementById('stagedBadge');
      const count = state.stagedPlants.length;
      document.getElementById('stagedCount').textContent = count;
      if (count > 0) {
        badge.style.display = 'inline-block';
        badge.textContent = count;
      } else {
        badge.style.display = 'none';
      }
    }

    function renderStaging() {
      const container = document.getElementById('stagedList');
      updateStagedBadge();

      if (state.stagedPlants.length === 0) {
        container.innerHTML = `
          <div style="text-align:center;padding:30px 10px;color:var(--text-muted);font-size:13px;">
            No plants added to report yet.<br>Click <strong>+ Add to Report</strong> on any plant card.
          </div>
        `;
        return;
      }

      container.innerHTML = '';
      state.stagedPlants.forEach((item, index) => {
        const el = document.createElement('div');
        el.className = 'staged-item';
        el.innerHTML = `
          <div class="staged-item-header">
            ${item.image_url ? `<img src="${item.image_url}" class="staged-item-thumb" alt="${item.common_name}">` : `
              <div class="staged-item-thumb" style="display:flex;align-items:center;justify-content:center;color:var(--text-muted);">
                <i data-lucide="sprout" style="width:20px;height:20px;"></i>
              </div>
            `}
            <div class="staged-item-info">
              <div class="staged-item-name">
                <a href="${item.plant_url}" target="_blank" rel="noopener noreferrer" style="color:inherit;text-decoration:underline;">
                  ${item.common_name}
                </a>
              </div>
              <div class="staged-item-sci">${item.scientific_name}</div>
            </div>
            <div class="quantity-control">
              <button class="qty-btn qty-minus">-</button>
              <span class="qty-val">${item.quantity || 1}</span>
              <button class="qty-btn qty-plus">+</button>
            </div>
            <button class="btn-icon remove-btn" title="Remove plant" style="color:var(--danger);padding:4px;">
              <i data-lucide="trash-2" style="width:15px;height:15px;"></i>
            </button>
          </div>
          <input type="text" class="staged-item-note" placeholder="Specific location / planting notes for client..." value="${item.custom_notes || ''}">
        `;

        // Stepper
        el.querySelector('.qty-minus').addEventListener('click', () => {
          if (item.quantity > 1) {
            item.quantity--;
            saveStaging();
            renderStaging();
          }
        });
        el.querySelector('.qty-plus').addEventListener('click', () => {
          item.quantity = (item.quantity || 1) + 1;
          saveStaging();
          renderStaging();
        });

        // Custom Note
        el.querySelector('.staged-item-note').addEventListener('input', (e) => {
          item.custom_notes = e.target.value;
          saveStaging();
        });

        // Remove
        el.querySelector('.remove-btn').addEventListener('click', () => {
          state.stagedPlants.splice(index, 1);
          saveStaging();
          renderStaging();
          renderGrid();
        });

        container.appendChild(el);
      });

      if (window.lucide) lucide.createIcons();
    }

    // Plant Detail Modal
    function openPlantDetail(plant) {
      state.activeModalPlant = plant;
      const modal = document.getElementById('plantDetailModal');
      const commonName = (plant.common_names && plant.common_names[0]) || plant.scientific_name;

      document.getElementById('modalCommonName').textContent = commonName;
      document.getElementById('modalSciName').textContent = plant.scientific_name || '';
      
      const badgeContainer = document.getElementById('modalBadges');
      if (badgeContainer) {
        let bHtml = '';
        if (isSweet16(plant)) bHtml += '<span class="badge-sweet16" style="font-size:11px;padding:3px 9px;">⭐ Deep Roots Sweet 16</span>';
        if (isKcKeystone(plant)) bHtml += '<span class="badge-keystone" style="font-size:11px;padding:3px 9px;">🌿 KC Keystone Species</span>';
        badgeContainer.innerHTML = bHtml;
        badgeContainer.style.display = bHtml ? 'flex' : 'none';
      }
      
      const img = document.getElementById('modalImg');
      const imgAttr = document.getElementById('modalImgAttr');
      if (plant.images && plant.images[0] && plant.images[0].url) {
        img.src = plant.images[0].url;
        img.onerror = function() {
          this.onerror = null;
          this.src = 'https://images.unsplash.com/photo-1598880940371-c756e015fea1?auto=format&fit=crop&w=800&q=80';
        };
        img.style.display = 'block';
        imgAttr.textContent = `Photo: ${plant.images[0].attribution_name || plant.images[0].source || 'Missouri Botanical Garden / Grow Native!'} ${plant.images[0].license ? '· ' + plant.images[0].license : ''}`;
      } else {
        img.style.display = 'none';
        imgAttr.textContent = 'Botanical record';
      }

      const officialLink = document.getElementById('modalOfficialUrl');
      officialLink.href = getPlantUrl(plant);

      document.getElementById('modalAdvisorDesc').textContent = getPlantDesc(plant);
      document.getElementById('modalLight').textContent = (plant.light_requirements || []).join(', ') || '-';
      document.getElementById('modalMoisture').textContent = (plant.moisture_requirements || []).join(', ') || '-';
      document.getElementById('modalHeight').textContent = getPlantHeight(plant);
      document.getElementById('modalSoil').textContent = (plant.soil_requirements || []).join(', ') || '-';
      document.getElementById('modalBloomPeriod').textContent = (plant.bloom_period || []).join(', ') || '-';
      document.getElementById('modalBloomColor').textContent = (plant.bloom_color || plant.bloom_colors || []).join(', ') || '-';
      document.getElementById('modalLayer').textContent = getPlantLayer(plant);
      document.getElementById('modalSociability').textContent = getPlantSociability(plant);
      document.getElementById('modalHabitat').textContent = plant.native_environment || '-';
      document.getElementById('modalPlantType').textContent = Array.isArray(plant.plant_type) ? plant.plant_type.join(', ') : (plant.plant_type || '-');

      document.getElementById('modalWildlife').textContent = (plant.wildlife_ecosystem_benefits || plant.wildlife_benefits || []).join(' · ') || 'Provides nectar, pollen, and shelter for native pollinators and wildlife.';

      // Add to report button in modal
      const isStaged = state.stagedPlants.some(p => p.id === plant.id || p.scientific_name === plant.scientific_name);
      const addBtn = document.getElementById('modalAddToReportBtn');
      addBtn.innerHTML = `<i data-lucide="${isStaged ? 'check' : 'plus'}"></i><span>${isStaged ? 'In Report' : 'Add to Report'}</span>`;
      addBtn.onclick = () => {
        toggleStagedPlant(plant);
        openPlantDetail(plant);
      };

      document.getElementById('modalEditBtn').onclick = () => {
        modal.close();
        openEditModal(plant);
      };

      modal.showModal();
      if (window.lucide) lucide.createIcons();
    }

    // Edit Plant Modal
    function openEditModal(plant) {
      document.getElementById('editPlantId').value = plant.id || plant.scientific_name;
      document.getElementById('editCommonName').value = plant.common_names?.[0] || '';
      document.getElementById('editSciName').value = plant.scientific_name || '';
      document.getElementById('editOfficialUrl').value = getPlantUrl(plant);
      document.getElementById('editAdvisorDesc').value = getPlantDesc(plant);
      document.getElementById('editLight').value = (plant.light_requirements || []).join(', ');
      document.getElementById('editMoisture').value = (plant.moisture_requirements || []).join(', ');
      document.getElementById('editHeight').value = getPlantHeight(plant);
      document.getElementById('editSociability').value = getPlantSociability(plant);
      document.getElementById('editImageUrl').value = plant.images?.[0]?.url || '';
      document.getElementById('editImageAttr').value = plant.images?.[0]?.attribution_name || plant.images?.[0]?.source || '';
      
      document.getElementById('editPlantModal').showModal();
    }

    document.getElementById('editPlantForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const id = document.getElementById('editPlantId').value;
      const plant = state.allPlants.find(p => p.id === id || p.scientific_name === id);
      if (plant) {
        const edits = {
          common_names: [document.getElementById('editCommonName').value],
          scientific_name: document.getElementById('editSciName').value,
          plant_url: document.getElementById('editOfficialUrl').value,
          advisor_description: document.getElementById('editAdvisorDesc').value,
          light_requirements: document.getElementById('editLight').value.split(',').map(s => s.trim()).filter(Boolean),
          moisture_requirements: document.getElementById('editMoisture').value.split(',').map(s => s.trim()).filter(Boolean),
          height_display: document.getElementById('editHeight').value,
          sociability: document.getElementById('editSociability').value,
        };

        const imgUrl = document.getElementById('editImageUrl').value;
        if (imgUrl) {
          edits.images = [{
            url: imgUrl,
            attribution_name: document.getElementById('editImageAttr').value,
            caption: edits.scientific_name
          }];
        }

        Object.assign(plant, edits);
        state.customPlants[id] = edits;
        localStorage.setItem('dr_custom_plants', JSON.stringify(state.customPlants));

        // Save to Firestore if token available
        if (state.gdriveToken) {
          try {
            const pId = localStorage.getItem('dr_firestore_project_id') || 'deep-roots-nature-advisors';
            let dId = localStorage.getItem('dr_firestore_database_id');
            if (!dId || dId === '(default)') dId = 'deep-roots-nature-advisors';
            const firestoreUrl = `https://firestore.googleapis.com/v1/projects/${pId}/databases/${dId}/documents/plants/${encodeURIComponent(plant.id || plant.scientific_name)}`;
            fetch(firestoreUrl, {
              method: 'PATCH',
              headers: {
                'Authorization': `Bearer ${state.gdriveToken}`,
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                fields: {
                  scientific_name: { stringValue: edits.scientific_name },
                  common_names: { arrayValue: { values: edits.common_names.map(c => ({ stringValue: c })) } },
                  plant_url: { stringValue: edits.plant_url },
                  advisor_description: { stringValue: edits.advisor_description },
                  height_display: { stringValue: edits.height_display },
                  updated_at: { stringValue: new Date().toISOString() },
                  updated_by: { stringValue: state.currentUser ? state.currentUser.email : 'nature_advisor' }
                }
              })
            }).catch(() => {});
          } catch (e) {}
        }

        applyFilters();
        updateHeaderInfo();
        showToast(`Saved changes for ${plant.common_names[0]}!`);
      }
      document.getElementById('editPlantModal').close();
    });

    // Generate Markdown Report
    function generateMarkdownReport() {
      const meta = state.clientMeta;
      let md = `# Deep Roots Nature Advisors - Consultation Report\\n\\n`;
      if (meta.name) md += `**Client:** ${meta.name}\\n`;
      if (meta.address) md += `**Project Address:** ${meta.address}\\n`;
      if (meta.date) md += `**Consultation Date:** ${meta.date}\\n`;
      if (meta.advisor) md += `**Nature Advisor:** ${meta.advisor}\\n\\n`;
      if (meta.notes) {
        md += `### Site Analysis & Strategy\\n${meta.notes}\\n\\n`;
      }
      md += `## Recommended Native Plant Palette\\n\\n`;

      state.stagedPlants.forEach(p => {
        md += `### [${p.common_name}](${p.plant_url}) (*${p.scientific_name}*)\\n\\n`;
        if (p.advisor_description) {
          md += `${p.advisor_description}\\n\\n`;
        }
        md += `* **Quantity:** ${p.quantity || 1}\\n`;
        if (p.sun) md += `* **Light Requirements:** ${p.sun}\\n`;
        if (p.moisture) md += `* **Moisture Requirements:** ${p.moisture}\\n`;
        if (p.height) md += `* **Mature Height:** ${p.height}\\n`;
        if (p.layer) md += `* **Garden Layer:** ${p.layer}\\n`;
        if (p.sociability) md += `* **Plant Sociability:** ${p.sociability}\\n`;
        if (p.custom_notes) md += `* **Advisor Recommendation:** ${p.custom_notes}\\n`;
        md += `\\n---\\n\\n`;
      });

      return md;
    }

    function buildHtmlReport() {
      const meta = state.clientMeta;
      const docTitle = `Deep Roots Consultation Report - ${meta.name || 'Kansas City Native Garden'}`;

      let html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>${docTitle}</title>
  <style>
    body { font-family: Arial, sans-serif; color: #1c281e; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 0 20px; }
    h1 { color: #235c36; font-size: 24pt; border-bottom: 2pt solid #235c36; padding-bottom: 6pt; }
    h2 { color: #235c36; font-size: 16pt; margin-top: 18pt; }
    h3 { color: #1c281e; font-size: 13pt; margin-top: 14pt; }
    a { color: #235c36; text-decoration: underline; }
    .meta-table { width: 100%; border-collapse: collapse; margin-bottom: 20pt; }
    .meta-table td { padding: 6pt 10pt; border: 1pt solid #c2d1c4; }
    .meta-label { font-weight: bold; background: #e8f5ec; width: 25%; }
    .plant-block { margin-bottom: 16pt; padding: 12pt; background: #f4f7f4; border-left: 4pt solid #235c36; border-radius: 4px; }
    ul { margin-top: 6pt; }
  </style>
</head>
<body>
  <h1>Deep Roots Nature Advisors</h1>
  <p><strong>Kansas City Native Plant Consultation Report</strong></p>
  
  <table class="meta-table">
    <tr><td class="meta-label">Client Name:</td><td>${meta.name || 'Client'}</td></tr>
    <tr><td class="meta-label">Project Address:</td><td>${meta.address || '-'}</td></tr>
    <tr><td class="meta-label">Date:</td><td>${meta.date || new Date().toLocaleDateString()}</td></tr>
    <tr><td class="meta-label">Nature Advisor:</td><td>${meta.advisor || (state.currentUser ? state.currentUser.name : 'Nature Advisor')}</td></tr>
  </table>

  ${meta.notes ? `<h2>Site Analysis & Ecological Strategy</h2><p>${meta.notes.replace(/\\n/g, '<br>')}</p>` : ''}

  <h2>Recommended Native Plant Palette</h2>
`;

      state.stagedPlants.forEach(p => {
        html += `
  <div class="plant-block">
    <h3><a href="${p.plant_url}">${p.common_name}</a> <em>(${p.scientific_name})</em></h3>
    <p>${p.advisor_description || ''}</p>
    <ul>
      <li><strong>Quantity:</strong> ${p.quantity || 1}</li>
      ${p.sun ? `<li><strong>Light Requirements:</strong> ${p.sun}</li>` : ''}
      ${p.moisture ? `<li><strong>Soil Moisture:</strong> ${p.moisture}</li>` : ''}
      ${p.height ? `<li><strong>Mature Height:</strong> ${p.height}</li>` : ''}
      ${p.layer ? `<li><strong>Garden Layer:</strong> ${p.layer}</li>` : ''}
      ${p.sociability ? `<li><strong>Plant Sociability:</strong> ${p.sociability}</li>` : ''}
      ${p.custom_notes ? `<li><strong>Advisor Recommendation:</strong> ${p.custom_notes}</li>` : ''}
    </ul>
  </div>
`;
      });

      html += `
  <hr style="margin-top: 30pt; border: none; border-top: 1pt solid #c2d1c4;">
  <p style="font-size: 10pt; color: #677f6c;">
    Report prepared by Deep Roots Nature Advisors. For cultivation guides and local ethical nurseries, visit 
    <a href="https://deeproots.org">deeproots.org</a> and <a href="https://grownative.org">grownative.org</a>.
  </p>
</body>
</html>
`;
      return html;
    }

    // Google Docs Direct Export via Drive API
    async function executeGoogleDocsExport() {
      if (!state.gdriveToken) {
        triggerGoogleSignIn();
        return;
      }

      showToast("Generating Google Doc in your Google Drive...");
      const meta = state.clientMeta;
      const docTitle = `Deep Roots Consultation Report - ${meta.name || 'Kansas City Native Garden'}`;
      const htmlContent = buildHtmlReport();

      const metadata = {
        name: docTitle,
        mimeType: 'application/vnd.google-apps.document'
      };

      const boundary = '-------314159265358979323846';
      const delimiter = "\\r\\n--" + boundary + "\\r\\n";
      const closeDelim = "\\r\\n--" + boundary + "--";

      const multipartRequestBody =
        delimiter +
        'Content-Type: application/json; charset=UTF-8\\r\\n\\r\\n' +
        JSON.stringify(metadata) +
        delimiter +
        'Content-Type: text/html; charset=UTF-8\\r\\n\\r\\n' +
        htmlContent +
        closeDelim;

      try {
        const response = await fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${state.gdriveToken}`,
            'Content-Type': `multipart/related; boundary=${boundary}`
          },
          body: multipartRequestBody
        });

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.error?.message || response.statusText);
        }

        const fileData = await response.json();
        const docUrl = `https://docs.google.com/document/d/${fileData.id}/edit`;
        
        document.getElementById('exportDocTitle').textContent = docTitle;
        document.getElementById('exportDocLink').href = docUrl;
        document.getElementById('exportSuccessModal').showModal();
        showToast("Google Doc created successfully!");
      } catch (err) {
        console.error("Google Drive export notice:", err);
        showToast("Notice: " + err.message + ". Downloading document directly.", "warning");
        downloadHtmlDocument();
      }
    }

    function downloadHtmlDocument() {
      const html = buildHtmlReport();
      const meta = state.clientMeta;
      const filename = `Deep_Roots_Report_${(meta.name || 'Kansas_City_Garden').replace(/[^a-z0-9]/gi, '_')}.doc`;
      const blob = new Blob([html], { type: 'application/msword;charset=utf-8' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      showToast(`Downloaded formatted report as ${filename}`);
    }

    // Setup Event Listeners
    function setupEventListeners() {
      // Theme toggle
      const themeBtn = document.getElementById('themeToggleBtn');
      const themeIcon = document.getElementById('themeIcon');
      const savedTheme = localStorage.getItem('dr_theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      document.body.setAttribute('data-theme', savedTheme);
      updateThemeIcon(savedTheme);

      themeBtn.addEventListener('click', () => {
        const cur = document.body.getAttribute('data-theme');
        const next = cur === 'dark' ? 'light' : 'dark';
        document.body.setAttribute('data-theme', next);
        localStorage.setItem('dr_theme', next);
        updateThemeIcon(next);
        renderGrid();
      });

      function updateThemeIcon(t) {
        themeIcon.setAttribute('data-lucide', t === 'dark' ? 'sun' : 'moon');
        if (window.lucide) lucide.createIcons();
      }

      // Drawer open/close
      const drawer = document.getElementById('stagingDrawer');
      const overlay = document.getElementById('drawerOverlay');
      const openDrawer = () => {
        drawer.classList.add('open');
        overlay.classList.add('open');
      };
      const closeDrawer = () => {
        drawer.classList.remove('open');
        overlay.classList.remove('open');
      };

      document.getElementById('reportDrawerBtn').addEventListener('click', openDrawer);
      document.getElementById('closeDrawerBtn').addEventListener('click', closeDrawer);
      overlay.addEventListener('click', closeDrawer);

      // Mobile Filter Sidebar Drawer
      const filterSidebar = document.getElementById('filterSidebar');
      const sidebarOverlay = document.getElementById('sidebarOverlay');
      const openSidebarBtn = document.getElementById('openSidebarBtn');
      const closeSidebarBtn = document.getElementById('closeSidebarBtn');
      const applyFiltersMobileBtn = document.getElementById('applyFiltersMobileBtn');
      const resetAllFiltersMobileBtn = document.getElementById('resetAllFiltersMobileBtn');

      const toggleSidebarDrawer = (open) => {
        if (!filterSidebar || !sidebarOverlay) return;
        if (open) {
          filterSidebar.classList.add('open');
          sidebarOverlay.classList.add('open');
          document.body.style.overflow = 'hidden';
        } else {
          filterSidebar.classList.remove('open');
          sidebarOverlay.classList.remove('open');
          document.body.style.overflow = '';
        }
      };

      if (openSidebarBtn) openSidebarBtn.addEventListener('click', () => toggleSidebarDrawer(true));
      if (closeSidebarBtn) closeSidebarBtn.addEventListener('click', () => toggleSidebarDrawer(false));
      if (sidebarOverlay) sidebarOverlay.addEventListener('click', () => toggleSidebarDrawer(false));
      if (applyFiltersMobileBtn) applyFiltersMobileBtn.addEventListener('click', () => toggleSidebarDrawer(false));
      if (resetAllFiltersMobileBtn) resetAllFiltersMobileBtn.addEventListener('click', resetAllFilters);

      window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          toggleSidebarDrawer(false);
          closeDrawer();
        }
      });

      window.addEventListener('resize', () => {
        if (window.innerWidth > 1024) {
          if (filterSidebar && filterSidebar.classList.contains('open')) {
            toggleSidebarDrawer(false);
          }
        }
      });

      // Search inputs (Dual desktop sidebar & mobile main content sync)
      const searchInput = document.getElementById('searchInput');
      const searchClear = document.getElementById('searchClearBtn');
      const mobileSearchInput = document.getElementById('mobileSearchInput');
      const mobileSearchClear = document.getElementById('mobileSearchClearBtn');
      let searchTimeout = null;

      const handleSearchInput = (val, sourceInput) => {
        clearTimeout(searchTimeout);
        if (searchInput && sourceInput !== searchInput) searchInput.value = val;
        if (mobileSearchInput && sourceInput !== mobileSearchInput) mobileSearchInput.value = val;
        if (searchClear) searchClear.style.display = val ? 'block' : 'none';
        if (mobileSearchClear) mobileSearchClear.style.display = val ? 'block' : 'none';

        searchTimeout = setTimeout(() => {
          state.filters.search = val;
          applyFilters();
        }, 180);
      };

      if (searchInput) {
        searchInput.addEventListener('input', (e) => handleSearchInput(e.target.value, searchInput));
      }
      if (mobileSearchInput) {
        mobileSearchInput.addEventListener('input', (e) => handleSearchInput(e.target.value, mobileSearchInput));
      }

      const handleSearchClear = () => {
        if (searchInput) searchInput.value = '';
        if (mobileSearchInput) mobileSearchInput.value = '';
        if (searchClear) searchClear.style.display = 'none';
        if (mobileSearchClear) mobileSearchClear.style.display = 'none';
        state.filters.search = '';
        applyFilters();
      };

      if (searchClear) searchClear.addEventListener('click', handleSearchClear);
      if (mobileSearchClear) mobileSearchClear.addEventListener('click', handleSearchClear);

      // Quick toggles
      const sweet16Btn = document.getElementById('toggleSweet16Btn');
      sweet16Btn.addEventListener('click', () => {
        state.filters.sweet16 = !state.filters.sweet16;
        sweet16Btn.classList.toggle('active', state.filters.sweet16);
        applyFilters();
      });

      const keystoneBtn = document.getElementById('toggleKeystoneBtn');
      keystoneBtn.addEventListener('click', () => {
        state.filters.keystone = !state.filters.keystone;
        keystoneBtn.classList.toggle('active', state.filters.keystone);
        applyFilters();
      });

      // Accordion headers
      document.querySelectorAll('.accordion-header').forEach(hdr => {
        hdr.addEventListener('click', () => {
          const targetId = hdr.getAttribute('data-target');
          const content = document.getElementById(targetId);
          const icon = hdr.querySelector('i');
          if (content.style.display === 'none') {
            content.style.display = 'flex';
            if (icon) icon.setAttribute('data-lucide', 'chevron-down');
          } else {
            content.style.display = 'none';
            if (icon) icon.setAttribute('data-lucide', 'chevron-right');
          }
          if (window.lucide) lucide.createIcons();
        });
      });

      // Chip filters
      document.querySelectorAll('.chip-filter').forEach(chip => {
        chip.addEventListener('click', () => {
          const group = chip.getAttribute('data-group');
          const val = chip.getAttribute('data-val');
          const set = state.filters[group];
          if (set.has(val)) {
            set.delete(val);
            chip.classList.remove('active');
          } else {
            set.add(val);
            chip.classList.add('active');
          }
          applyFilters();
        });
      });

      // Reset buttons
      document.getElementById('resetAllFiltersBtn').addEventListener('click', resetAllFilters);
      document.getElementById('resetFiltersEmptyBtn').addEventListener('click', resetAllFilters);

      // Sort select & Sidebar sort select
      const sortSelect = document.getElementById('sortOrderSelect');
      const sidebarSortSelect = document.getElementById('sidebarSortOrderSelect');
      if (sortSelect) sortSelect.value = state.sortOrder;
      if (sidebarSortSelect) sidebarSortSelect.value = state.sortOrder;

      const handleSortChange = (newOrder) => {
        state.sortOrder = newOrder;
        localStorage.setItem('dr_sort_order', state.sortOrder);
        if (sortSelect) sortSelect.value = state.sortOrder;
        if (sidebarSortSelect) sidebarSortSelect.value = state.sortOrder;
        sortPlants();
        renderGrid();
      };

      if (sortSelect) {
        sortSelect.addEventListener('change', (e) => handleSortChange(e.target.value));
      }
      if (sidebarSortSelect) {
        sidebarSortSelect.addEventListener('change', (e) => handleSortChange(e.target.value));
      }

      // Default Name Display select & Sidebar select
      const nameDisplaySelect = document.getElementById('defaultNameDisplaySelect');
      const sidebarNameDisplaySelect = document.getElementById('sidebarNameDisplaySelect');
      if (nameDisplaySelect) nameDisplaySelect.value = state.defaultNameDisplay;
      if (sidebarNameDisplaySelect) sidebarNameDisplaySelect.value = state.defaultNameDisplay;

      const handleNameDisplayChange = (newDisplay) => {
        state.defaultNameDisplay = newDisplay;
        localStorage.setItem('dr_default_name_display', state.defaultNameDisplay);
        if (nameDisplaySelect) nameDisplaySelect.value = state.defaultNameDisplay;
        if (sidebarNameDisplaySelect) sidebarNameDisplaySelect.value = state.defaultNameDisplay;
        sortPlants();
        renderGrid();
      };

      if (nameDisplaySelect) {
        nameDisplaySelect.addEventListener('change', (e) => handleNameDisplayChange(e.target.value));
      }
      if (sidebarNameDisplaySelect) {
        sidebarNameDisplaySelect.addEventListener('change', (e) => handleNameDisplayChange(e.target.value));
      }

      // Client Meta Inputs
      const clientInputs = {
        name: document.getElementById('clientNameInput'),
        address: document.getElementById('projectAddressInput'),
        date: document.getElementById('consultDateInput'),
        advisor: document.getElementById('advisorNameInput'),
        notes: document.getElementById('advisorNotesInput')
      };

      Object.keys(clientInputs).forEach(k => {
        clientInputs[k].value = state.clientMeta[k] || '';
        clientInputs[k].addEventListener('input', (e) => {
          state.clientMeta[k] = e.target.value;
          localStorage.setItem('dr_client_meta', JSON.stringify(state.clientMeta));
        });
      });

      // Clear Staging
      document.getElementById('clearAllStagedBtn').addEventListener('click', () => {
        if (confirm("Remove all plants from staging?")) {
          state.stagedPlants = [];
          saveStaging();
          renderStaging();
          renderGrid();
        }
      });

      // Copy Markdown Button
      document.getElementById('copyMarkdownReportBtn').addEventListener('click', () => {
        if (state.stagedPlants.length === 0) {
          showToast("No plants in report to export.", "warning");
          return;
        }
        const md = generateMarkdownReport();
        navigator.clipboard.writeText(md).then(() => {
          showToast("Copied Markdown report to clipboard!");
        });
      });

      // Download Formatted Document Button
      document.getElementById('downloadHtmlReportBtn').addEventListener('click', () => {
        if (state.stagedPlants.length === 0) {
          showToast("No plants in report to export.", "warning");
          return;
        }
        downloadHtmlDocument();
      });

      // Export Google Docs Button
      document.getElementById('exportGoogleDocsBtn').addEventListener('click', () => {
        if (state.stagedPlants.length === 0) {
          showToast("No plants in report to export.", "warning");
          return;
        }
        executeGoogleDocsExport();
      });

      // Sync Modal Controls
      document.getElementById('syncModalBtn').addEventListener('click', () => {
        document.getElementById('syncModal').showModal();
      });
      document.getElementById('dbStatusPill').addEventListener('click', () => {
        document.getElementById('syncModal').showModal();
      });

      document.getElementById('refreshFromDbBtn').addEventListener('click', async () => {
        showToast("Synchronizing with shared Cloud Firestore master database...");
        await tryLiveSyncFromDatabase(true);
        applyFilters();
        updateHeaderInfo();
      });



      // Upload / Seed Master Plants to Firestore
      document.getElementById('seedFirestoreBtn')?.addEventListener('click', async () => {
        const token = state.gdriveToken || (state.currentUser && state.currentUser.accessToken);
        if (!token) {
          showToast("Please sign in with Google first to authorize writing to Cloud Firestore.", "warning");
          triggerGoogleSignIn();
          return;
        }
        if (!confirm(`Upload all ${state.allPlants.length} species directly to Cloud Firestore collection 'plants'?`)) return;

        showToast("Starting Cloud Firestore batch upload...", "info");
        const pId = localStorage.getItem('dr_firestore_project_id') || 'deep-roots-nature-advisors';
        let dId = localStorage.getItem('dr_firestore_database_id') || 'deep-roots-nature-advisors';
        if (dId === '(default)') dId = 'deep-roots-nature-advisors';
        
        let uploaded = 0;
        for (const p of state.allPlants) {
          const docId = encodeURIComponent(p.id || p.scientific_name.toLowerCase().replace(/[^a-z0-9]+/g, '-'));
          const url = `https://firestore.googleapis.com/v1/projects/${pId}/databases/${dId}/documents/plants/${docId}`;
          
          const body = {
            fields: {
              scientific_name: { stringValue: p.scientific_name || '' },
              common_names: { arrayValue: { values: (p.common_names || []).map(n => ({ stringValue: String(n) })) } },
              native_environment: { stringValue: p.native_environment || 'Forest' },
              plant_type: { arrayValue: { values: (Array.isArray(p.plant_type) ? p.plant_type : [p.plant_type || 'Wildflower']).map(t => ({ stringValue: String(t) })) } },
              mature_height: {
                mapValue: {
                  fields: {
                    min_ft: { doubleValue: Number(p.mature_height_min || 1) },
                    max_ft: { doubleValue: Number(p.mature_height_max || 3) },
                    display: { stringValue: p.height_display || '1–3 ft' }
                  }
                }
              },
              plant_url: { stringValue: getPlantUrl(p) },
              advisor_description: { stringValue: getPlantDesc(p) },
              sociability: { stringValue: getPlantSociability(p) },
              soil_requirements: { arrayValue: { values: (p.soil_requirements || []).map(s => ({ stringValue: String(s) })) } },
              moisture_requirements: { arrayValue: { values: (p.moisture_requirements || []).map(m => ({ stringValue: String(m) })) } },
              light_requirements: { arrayValue: { values: (p.light_requirements || []).map(l => ({ stringValue: String(l) })) } },
              wildlife_ecosystem_benefits: { arrayValue: { values: (p.wildlife_ecosystem_benefits || []).map(w => ({ stringValue: String(w) })) } },
              images: {
                arrayValue: {
                  values: (p.images || []).map(img => ({
                    mapValue: {
                      fields: {
                        url: { stringValue: img.url || '' },
                        caption: { stringValue: img.caption || '' },
                        attribution_name: { stringValue: img.attribution_name || 'Grow Native!' }
                      }
                    }
                  }))
                }
              }
            }
          };

          try {
            await fetch(url, {
              method: 'PATCH',
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
              },
              body: JSON.stringify(body)
            });
            uploaded++;
          } catch (e) {
            console.error("Upload error for plant:", p.scientific_name, e);
          }
        }
        showToast(`Uploaded ${uploaded} plants to Cloud Firestore!`, 'success');
        tryLiveSyncFromDatabase(true);
      });

      document.getElementById('resetCustomEditsBtn').addEventListener('click', () => {
        if (confirm("Reset all local edits back to authoritative master catalog?")) {
          state.customPlants = {};
          localStorage.removeItem('dr_custom_plants');
          loadMasterPlants();
          showToast("Reset to pristine shared master catalog.");
        }
      });

      // Import Plants JSON (e.g. from Android backup)
      document.getElementById('importJsonFileInput')?.addEventListener('change', async (e) => {
        const file = e.target.files?.[0];
        if (!file) return;
        try {
          const text = await file.text();
          const imported = JSON.parse(text);
          if (Array.isArray(imported) && imported.length > 0) {
            replaceWithRemotePlants(imported);
            state.lastSyncTime = new Date().toLocaleTimeString();
            updateHeaderInfo();
            showToast(`Imported ${imported.length} plants from file!`, 'success');
            if (confirm(`Successfully imported ${imported.length} plants! Would you like to upload them directly to Cloud Firestore now?`)) {
              document.getElementById('seedFirestoreBtn')?.click();
            }
          } else {
            showToast("Invalid plant JSON file.", "danger");
          }
        } catch (err) {
          showToast(`Failed to parse JSON: ${err.message}`, "danger");
        }
      });

      // Google Sign-In Actions
      document.getElementById('modalGoogleSignInBtn').addEventListener('click', triggerGoogleSignIn);
      document.getElementById('signOutGoogleBtn').addEventListener('click', signOutGoogle);
    }

    // App Initialization
    window.addEventListener('DOMContentLoaded', () => {
      loadMasterPlants();
      renderStaging();
      setupEventListeners();
      // Check iOS In-App Browser (e.g. link opened from iMessage or WhatsApp)
      if (isIosInAppBrowser()) {
        const banner = document.createElement('div');
        banner.style.cssText = 'background:#1a4d2e;color:#fff;padding:8px 14px;font-size:12px;text-align:center;font-weight:600;display:flex;align-items:center;justify-content:center;gap:8px;position:sticky;top:0;z-index:9999;box-shadow:0 2px 8px rgba(0,0,0,0.15);';
        banner.innerHTML = '<span>Viewing in message app? Tap the <strong>Safari compass icon</strong> (bottom right) to open in Safari for Google Sign-In.</span>';
        document.body.prepend(banner);
      }
      initGoogleAuth();
      if (window.lucide) lucide.createIcons();
    });
  </script>
</body>
</html>
"""

full_html = html_header + minified_json + html_footer

# Write to root index.html
target_root = os.path.join(root_dir, 'index.html')
with open(target_root, 'w', encoding='utf-8') as f:
    f.write(full_html)
print(f"Wrote {os.path.getsize(target_root)} bytes to {target_root}")

# Write to app/static/index.html if directory exists
target_static = os.path.join(root_dir, 'app', 'static', 'index.html')
if os.path.exists(os.path.dirname(target_static)):
    with open(target_static, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Wrote {os.path.getsize(target_static)} bytes to {target_static}")

