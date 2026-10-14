#!/usr/bin/env python3
"""
scripts/enrich_descriptions_and_maintenance.py

Updates all 185 native plants in data/plants_enriched.json and index.html:
1. Synthesizes rich advisor_description (Appearance, Growth Habit, Sociability, Recommended Garden Settings, and credited sources).
2. Sets scientifically grounded maintenance_level ('Low', 'Medium', 'High').
3. Sets structured seasonal maintenance_guide (Spring 50°F+ cutback, Summer Chelsea chop, Fall seedhead retention, Winter crown protection, Division guidelines, and credited conservation sources).
4. Updates embeddedMasterPlants in index.html.
"""

import json
import re
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from scripts.botanical_trees_shrubs import BOTANICAL_TREES_SHRUBS
from scripts.botanical_grasses_sedges_ferns_vines import BOTANICAL_GRASSES_SEDGES_FERNS_VINES
from scripts.botanical_wildflowers_1 import BOTANICAL_WILDFLOWERS_1
from scripts.botanical_wildflowers_2 import BOTANICAL_WILDFLOWERS_2

def build_full_catalog():
    all_profiles = {}
    all_profiles.update(BOTANICAL_TREES_SHRUBS)
    all_profiles.update(BOTANICAL_GRASSES_SEDGES_FERNS_VINES)
    all_profiles.update(BOTANICAL_WILDFLOWERS_1)
    all_profiles.update(BOTANICAL_WILDFLOWERS_2)
    return all_profiles

def enrich_plant_record(plant, profile):
    sci_name = plant.get('scientific_name')
    common_name = (plant.get('common_names') or [''])[0]

    appearance = profile['appearance']
    habit = profile['habit']
    sociability = profile['sociability']
    settings = profile['settings']
    maint_level = profile['maint_level']

    # 1. Synthesize advisor_description
    full_desc = (
        f"{appearance}\n\n"
        f"Growth Habit & Form: {habit}\n\n"
        f"Sociability & Matrix Role: {sociability}\n\n"
        f"Recommended Garden Settings: {settings}\n\n"
        f"Sources: Missouri Botanical Garden PlantFinder, Grow Native! (Missouri Prairie Foundation), Sow Wild Natives, City Roots Nursery, MDC."
    )
    plant['advisor_description'] = full_desc

    # 2. Set maintenance_level
    plant['maintenance_level'] = maint_level

    # 3. Create structured maintenance_guide
    maint_summary = (
        f"{maint_level} Maintenance. Requires minimal care once established. "
        f"Follow ecological cutback practices to protect native pollinators and songbirds."
    )
    if maint_level == 'High':
        maint_summary = (
            f"High Maintenance. Requires active moisture management or boundary containment to manage vigorous growth. "
            f"Adhere to seasonal timing to maximize ecological benefits while containing spread."
        )
    elif maint_level == 'Medium':
        maint_summary = (
            f"Medium Maintenance. Benefits from targeted mid-season care (such as Chelsea chopping or occasional division) "
            f"and spring cutback timing to sustain peak vigor and compact garden form."
        )

    plant['maintenance_guide'] = {
        'summary': maint_summary,
        'level': maint_level,
        'spring': profile['spring_care'],
        'summer': profile['summer_care'],
        'fall': profile['fall_care'],
        'winter': profile['winter_care'],
        'division': profile['division'],
        'sources': 'Xerces Society for Invertebrate Conservation, Grow Native! (Missouri Prairie Foundation), Missouri Botanical Garden PlantFinder, Sow Wild Natives'
    }

    # Ensure sociability tag matches
    if 'Solitary' in sociability or 'tight' in sociability.lower() or 'well-behaved' in sociability.lower() or 'non-invasive' in sociability.lower():
        if plant.get('sociability') not in ['Moderate', 'Highly Social / Gregarious']:
            plant['sociability'] = 'Less Social / Solitary'
    elif 'High-vigor' in sociability or 'aggressive' in sociability.lower() or 'colonial' in sociability.lower() or 'vigorous' in sociability.lower():
        plant['sociability'] = 'Highly Social / Gregarious'
    else:
        plant['sociability'] = 'Medium / Moderate Spreading'

    return plant

def main():
    profiles = build_full_catalog()
    print(f"Loaded {len(profiles)} botanical profiles.")

    with open('data/plants_enriched.json', 'r', encoding='utf-8') as f:
        plants = json.load(f)

    print(f"Loaded {len(plants)} plants from data/plants_enriched.json.")

    level_counts = {'Low': 0, 'Medium': 0, 'High': 0}

    for p in plants:
        sname = p.get('scientific_name')
        if sname not in profiles:
            raise KeyError(f"Species not found in botanical profiles: {sname}")
        enrich_plant_record(p, profiles[sname])
        level_counts[p['maintenance_level']] += 1

    print("\nMaintenance Level Distribution:")
    for lvl, count in level_counts.items():
        print(f"  - {lvl} Maintenance: {count} species ({count/len(plants)*100:.1f}%)")

    # Save to data/plants_enriched.json
    with open('data/plants_enriched.json', 'w', encoding='utf-8') as f:
        json.dump(plants, f, indent=2, ensure_ascii=False)
    print("Successfully updated data/plants_enriched.json")

    # Update embeddedMasterPlants in index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    start_tag = '<script type="application/json" id="embeddedMasterPlants">'
    end_tag = '</script>'
    start_pos = html_content.find(start_tag)
    if start_pos == -1:
        raise ValueError("Could not find embeddedMasterPlants tag in index.html")

    end_pos = html_content.find(end_tag, start_pos)
    if end_pos == -1:
        raise ValueError("Could not find closing script tag for embeddedMasterPlants in index.html")

    # Format JSON as a single compact line or clean JSON for embedded script
    json_str = json.dumps(plants, separators=(',', ':'), ensure_ascii=False)
    new_html = html_content[:start_pos + len(start_tag)] + "\n" + json_str + "\n" + html_content[end_pos:]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"Successfully updated embeddedMasterPlants in index.html with {len(plants)} enriched botanical records.")

if __name__ == '__main__':
    main()
