#!/usr/bin/env python3
"""
scripts/test_maintenance_and_catalog.py
Comprehensive test suite verifying:
- Botanical completeness of all 185 plants in data/plants_enriched.json
- Advisor description richness and source citations
- Maintenance level rankings and seasonal care guides
- UI elements and JavaScript filter architecture in index.html
- ES Module JS syntax verification
"""

import json
import subprocess
import sys

def test_data_integrity():
    print("Testing data/plants_enriched.json integrity...")
    with open('data/plants_enriched.json', 'r', encoding='utf-8') as f:
        plants = json.load(f)

    assert len(plants) == 185, f"Expected 185 plants, found {len(plants)}"

    levels = {'Low': 0, 'Medium': 0, 'High': 0}
    required_guide_keys = {'summary', 'level', 'spring', 'summer', 'fall', 'winter', 'division', 'sources'}

    for idx, p in enumerate(plants):
        sname = p.get('scientific_name')
        cname = (p.get('common_names') or [''])[0]
        assert sname, f"Plant {idx} missing scientific_name"

        # Check advisor_description
        desc = p.get('advisor_description', '')
        assert len(desc) > 100, f"Plant {sname} has too short advisor_description ({len(desc)} chars)"
        assert "Growth Habit" in desc, f"Plant {sname} missing Growth Habit in description"
        assert "Sociability" in desc, f"Plant {sname} missing Sociability in description"
        assert "Recommended Garden Settings" in desc, f"Plant {sname} missing Recommended Garden Settings"
        assert "Sources:" in desc, f"Plant {sname} missing Sources attribution in description"

        # Check maintenance_level
        m_lvl = p.get('maintenance_level')
        assert m_lvl in levels, f"Plant {sname} has invalid maintenance_level: {m_lvl}"
        levels[m_lvl] += 1

        # Check maintenance_guide
        guide = p.get('maintenance_guide')
        assert isinstance(guide, dict), f"Plant {sname} missing maintenance_guide dict"
        missing_keys = required_guide_keys - set(guide.keys())
        assert not missing_keys, f"Plant {sname} maintenance_guide missing keys: {missing_keys}"
        assert guide['level'] == m_lvl, f"Plant {sname} guide level mismatch: {guide['level']} vs {m_lvl}"
        assert len(guide['spring']) >= 25, f"Plant {sname} spring care too brief"
        assert len(guide['summer']) >= 25, f"Plant {sname} summer care too brief"
        assert len(guide['fall']) >= 25, f"Plant {sname} fall care too brief"
        assert len(guide['winter']) >= 25, f"Plant {sname} winter care too brief"
        assert len(guide['division']) >= 20, f"Plant {sname} division guide too brief"
        assert "Xerces" in guide['sources'], f"Plant {sname} missing Xerces citation"

    print(f"PASSED: All 185 plants verified. Distribution: {levels}")

def test_index_html_integration():
    print("\nTesting index.html UI & logic integration...")
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Embedded JSON verification
    start_tag = '<script type="application/json" id="embeddedMasterPlants">'
    end_tag = '</script>'
    s_idx = html.find(start_tag)
    assert s_idx != -1, "embeddedMasterPlants tag missing"
    e_idx = html.find(end_tag, s_idx)
    raw = html[s_idx + len(start_tag):e_idx].strip()
    embedded_plants = json.loads(raw)
    assert len(embedded_plants) == 185, f"embeddedMasterPlants count: {len(embedded_plants)}"
    print("  ✓ embeddedMasterPlants holds 185 enriched species")

    # 2. Sidebar filter accordion
    assert 'data-target="maintenanceFilterContent"' in html, "Sidebar maintenance accordion missing"
    assert 'data-group="maintenance" data-val="Low"' in html, "Low maintenance chip missing"
    assert 'data-group="maintenance" data-val="Medium"' in html, "Medium maintenance chip missing"
    assert 'data-group="maintenance" data-val="High"' in html, "High maintenance chip missing"
    print("  ✓ Sidebar Maintenance Level accordion & filter chips present")

    # 3. Modal elements
    assert 'id="modalMaintenanceLevel"' in html, "modalMaintenanceLevel in specs-grid missing"
    assert 'id="modalMaintenanceContainer"' in html, "modalMaintenanceContainer missing"
    assert 'id="modalMaintSpring"' in html, "modalMaintSpring element missing"
    assert 'id="modalMaintSummer"' in html, "modalMaintSummer element missing"
    assert 'id="modalMaintFall"' in html, "modalMaintFall element missing"
    assert 'id="modalMaintWinter"' in html, "modalMaintWinter element missing"
    assert 'id="modalMaintDivision"' in html, "modalMaintDivision element missing"
    print("  ✓ plantDetailModal seasonal maintenance guide elements present")

    # 4. Form inputs
    assert 'id="editMaintenanceLevel"' in html, "editMaintenanceLevel select missing"
    assert 'id="addMaintenanceLevel"' in html, "addMaintenanceLevel select missing"
    print("  ✓ Edit and Add modals contain maintenance level select dropdowns")

    # 5. JS state and filter engine
    assert 'maintenance: new Set()' in html, "state.filters.maintenance Set missing"
    assert 'function getPlantMaintenanceLevel' in html, "getPlantMaintenanceLevel helper missing"
    assert 'function getPlantMaintenanceGuide' in html, "getPlantMaintenanceGuide helper missing"
    assert 'f.maintenance && f.maintenance.size > 0' in html, "applyFilters maintenance check missing"
    assert "'maintenance']" in html, "groups array missing 'maintenance'"
    assert "maintPillHtml" in html, "Plant card maintenance chip missing"
    assert "staged.maintenance_level" in html, "Staged plant maintenance fields missing"
    print("  ✓ JavaScript filter engine and card badges fully configured")

def test_js_syntax():
    print("\nTesting JavaScript module syntax with node --check...")
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    start = content.find('<script type="module">')
    end = content.find('</script>', start)
    js_code = content[start + len('<script type="module">'):end]

    with open('/tmp/test_syntax_check.js', 'w', encoding='utf-8') as f:
        f.write(js_code)

    res = subprocess.run(['node', '--check', '/tmp/test_syntax_check.js'], capture_output=True, text=True)
    assert res.returncode == 0, f"JS Syntax Error:\n{res.stderr}"
    print(f"  ✓ {js_code.count(chr(10))} lines of JavaScript validated with zero syntax errors")

if __name__ == '__main__':
    try:
        test_data_integrity()
        test_index_html_integration()
        test_js_syntax()
        print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY!")
    except AssertionError as e:
        print(f"\nTEST FAILED: {e}")
        sys.exit(1)
