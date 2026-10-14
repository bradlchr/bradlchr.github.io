#!/usr/bin/env python3
"""
scripts/test_maintenance_and_catalog.py
Comprehensive test suite verifying:
- Botanical completeness of all 185 plants in data/plants_enriched.json
- Concise advisor descriptions with direct inline markdown links to exact species pages
- Zero generic homepage or category root links across all plants
- Actionable-only maintenance tasks and omission of inactive seasons
- Absence of passive culture/habitat text in maintenance (e.g. 'Thrives in rich, moist...')
- Exact seasonal tile titles in index.html (Spring, Summer, Fall, Winter)
- Enhanced Wildlife & Ecological Value with specific host insects and direct inline citations
- ES Module JS syntax verification
"""

import json
import os
import re
import subprocess
import sys

def test_data_integrity():
    print("Testing data/plants_enriched.json integrity...")
    with open('data/plants_enriched.json', 'r', encoding='utf-8') as f:
        plants = json.load(f)

    assert len(plants) == 185, f"Expected 185 plants, found {len(plants)}"

    levels = {'Low': 0, 'Medium': 0, 'High': 0}
    season_counts = {'spring': 0, 'summer': 0, 'fall': 0, 'winter': 0, 'division': 0}

    # Banned passive / aesthetic non-actionable maintenance phrases
    banned_passive_phrases = [
        "thrives in rich, moist to dry woodland soils in partial to full shade",
        "thrives in rich, moist, organic woodland",
        "thrives in moist to wet loams and heavy clay",
        "thrives in lean, sharply drained limestone",
        "thrives in lean, sharply drained sunny",
        "thrives in sunny, well-drained limestone",
        "thrives in standing water, wet clay",
        "thrives in standing water, saturated soils",
        "thrives in moist to wet soils in full sun",
        "thrives in full sun and average to moist soils",
        "thrives in full sun to light savanna",
        "thrives in full sun to partial shade",
        "thrives in moist, rich loams and heavy clay",
        "thrives in moist, rich, dappled shade",
        "zero supplemental watering needed once established",
        "zero supplemental water needed once established",
        "zero maintenance needed once established",
        "extremely drought and poor-soil proof",
        "extremely drought and heat tolerant",
        "extremely drought and heat hardy",
        "marbled foliage intensifies",
        "architectural winter silhouette",
        "dormant buds are velvet-coated",
        "fish-scale patterned gray bark",
        "alligator-skin textured",
        "foliage takes on attractive",
        "foliage takes on rich crimson",
        "enjoy late-autumn blossoms",
        "enjoy glowing golden-yellow",
        "enjoy glowing copper-bronze",
        "enjoy persistent swirling silvery"
    ]

    # Banned generic URLs (must always link to exact species/resource pages)
    banned_generic_urls = [
        "https://grownative.org)",
        "https://grownative.org/)",
        "https://mdc.mo.gov/discover-nature/field-guide)",
        "https://mdc.mo.gov/discover-nature/field-guide/)",
        "https://www.missouribotanicalgarden.org/PlantFinder/)",
        "https://www.missouribotanicalgarden.org/PlantFinder)",
        "https://xerces.org/)",
        "https://xerces.org)",
        "https://www.nwf.org/nativeplantfinder/)",
        "https://www.nwf.org/nativeplantfinder)",
        "https://www.butterfliesandmoths.org/)",
        "https://www.butterfliesandmoths.org)"
    ]

    for idx, p in enumerate(plants):
        sname = p.get('scientific_name')
        assert sname, f"Plant {idx} missing scientific_name"

        # 1. Check advisor_description (concise summary + direct inline links)
        desc = p.get('advisor_description', '')
        assert 100 <= len(desc) <= 650, f"Plant {sname} advisor_description length out of bounds: {len(desc)} chars"
        assert "](" in desc, f"Plant {sname} missing inline markdown links in description"
        assert not desc.endswith("Sources:"), f"Plant {sname} has dangling Sources text"

        # Ensure no generic links in description
        for bad_url in banned_generic_urls:
            assert bad_url not in desc, f"Plant {sname} has generic URL in description: {bad_url}"

        # 2. Check maintenance_level
        m_lvl = p.get('maintenance_level')
        assert m_lvl in levels, f"Plant {sname} has invalid maintenance_level: {m_lvl}"
        levels[m_lvl] += 1

        # 3. Check maintenance_guide (strictly actionable only, flexible seasons)
        guide = p.get('maintenance_guide')
        assert isinstance(guide, dict), f"Plant {sname} missing maintenance_guide dict"
        assert guide['level'] == m_lvl, f"Plant {sname} guide level mismatch: {guide['level']} vs {m_lvl}"
        assert 'summary' in guide, f"Plant {sname} guide missing summary"
        assert 'spring' in guide and len(guide['spring']) >= 20, f"Plant {sname} spring care missing or too brief"
        assert 'division' in guide and len(guide['division']) >= 15, f"Plant {sname} division guide missing or too brief"

        guide_str = json.dumps(guide).lower()
        for banned in banned_passive_phrases:
            assert banned not in guide_str, f"Plant {sname} contains passive non-actionable phrase: '{banned}'"

        for bad_url in banned_generic_urls:
            assert bad_url not in json.dumps(guide), f"Plant {sname} contains generic URL in maintenance: {bad_url}"

        for s in ['spring', 'summer', 'fall', 'winter', 'division']:
            if s in guide and guide[s]:
                season_counts[s] += 1

        # 4. Check Enhanced Wildlife & Ecological Value
        w_detail = p.get('wildlife_detail')
        assert isinstance(w_detail, dict), f"Plant {sname} missing wildlife_detail dict"
        assert 'host_insects' in w_detail and len(w_detail['host_insects']) >= 20, f"Plant {sname} missing specific host_insects"
        assert 'wildlife_users' in w_detail and len(w_detail['wildlife_users']) >= 20, f"Plant {sname} missing specific wildlife_users"
        assert 'sources' in w_detail and "](" in w_detail['sources'], f"Plant {sname} missing wildlife source links"

        # Ensure no generic links in wildlife
        for bad_url in banned_generic_urls:
            assert bad_url not in json.dumps(w_detail), f"Plant {sname} contains generic URL in wildlife: {bad_url}"

        w_eco = p.get('wildlife_ecological_value', '')
        assert "Host Plant Value:" in w_eco, f"Plant {sname} missing Host Plant Value in wildlife_ecological_value"
        assert "Wildlife & Ecological Interactions:" in w_eco, f"Plant {sname} missing Wildlife Interactions"

        # 5. Check Botanical Photography & Images (No default fallbacks or dummy placeholders)
        images = p.get('images')
        assert isinstance(images, list) and len(images) > 0, f"Plant {sname} has no images configured"
        primary_img = images[0]
        assert isinstance(primary_img, dict), f"Plant {sname} primary image is not a dict"
        img_url = primary_img.get('url', '')
        assert img_url and img_url.startswith('http'), f"Plant {sname} primary image URL is empty or not HTTP: {img_url}"

        for img in images:
            u = img.get('url', '')
            assert "NoThumbnailLarge.jpg" not in u, f"Plant {sname} contains MOBOT placeholder image: {u}"
            assert "NoThumbnail2.jpg" not in u, f"Plant {sname} contains MOBOT placeholder image: {u}"
            assert "thumb/7/77" not in u, f"Plant {sname} contains dummy Wikimedia placeholder URL: {u}"
            if "bradlchr.github.io/images/plants/" in u:
                fname = u.split("bradlchr.github.io/images/plants/")[1]
                local_f = os.path.join("images/plants", fname)
                assert os.path.exists(local_f), f"Plant {sname} referenced local image missing on disk: {local_f}"
                assert os.path.getsize(local_f) > 5000, f"Plant {sname} local image too small: {local_f}"

    print(f"PASSED: All 185 plants verified.")
    print(f"  - Maintenance Distribution: {levels}")
    print(f"  - Actionable Seasons: {season_counts}")

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

    # 2. Strict seasonal tile titles (Spring, Summer, Fall, Winter)
    assert 'Spring (50°F+ Cutback)' not in html, "Obsolete subtitle Spring (50°F+ Cutback) still in index.html"
    assert 'Summer Care' not in html, "Obsolete subtitle Summer Care still in index.html"
    assert 'Fall Timing' not in html, "Obsolete subtitle Fall Timing still in index.html"
    assert 'Winter Protection' not in html, "Obsolete subtitle Winter Protection still in index.html"

    assert '<i data-lucide="flower" style="width:12px;height:12px;"></i> Spring' in html, "Strict Spring title missing"
    assert '<i data-lucide="sun" style="width:12px;height:12px;"></i> Summer' in html, "Strict Summer title missing"
    assert '<i data-lucide="leaf" style="width:12px;height:12px;"></i> Fall' in html, "Strict Fall title missing"
    assert '<i data-lucide="snowflake" style="width:12px;height:12px;"></i> Winter' in html, "Strict Winter title missing"
    print("  ✓ Strict seasonal titles confirmed: Spring, Summer, Fall, Winter")

    # 3. Rich markdown rendering & clickable links in maintenance cards
    assert '${renderRichMarkdownText(maintGuide.spring)}' in html, "renderRichMarkdownText for spring missing"
    assert '${renderRichMarkdownText(maintGuide.summer)}' in html, "renderRichMarkdownText for summer missing"
    assert '${renderRichMarkdownText(maintGuide.fall)}' in html, "renderRichMarkdownText for fall missing"
    assert '${renderRichMarkdownText(maintGuide.winter)}' in html, "renderRichMarkdownText for winter missing"
    print("  ✓ Maintenance cards render inline links with renderRichMarkdownText")

    # 4. Dynamic maintenance grid for flexible seasons
    assert 'id="modalMaintenanceGrid"' in html, "modalMaintenanceGrid container missing"
    assert "maintGuide.spring && maintGuide.spring.trim()" in html, "Dynamic spring check missing"
    assert "maintGuide.summer && maintGuide.summer.trim()" in html, "Dynamic summer check missing"
    assert "maintGuide.fall && maintGuide.fall.trim()" in html, "Dynamic fall check missing"
    assert "maintGuide.winter && maintGuide.winter.trim()" in html, "Dynamic winter check missing"
    print("  ✓ Dynamic maintenance grid omits seasons without actionable tasks")

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
