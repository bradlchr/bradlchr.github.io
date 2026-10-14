#!/usr/bin/env python3
"""
scripts/enrich_descriptions_and_maintenance.py

Enriches all 185 native plants in data/plants_enriched.json and index.html:
1. Synthesizes concise, 2-3 sentence advisor_description with direct markdown links to sources
   (Missouri Botanical Garden PlantFinder, Grow Native!, MDC Field Guide).
2. Sets scientifically grounded maintenance_level ('Low', 'Medium', 'High').
3. Sets structured seasonal maintenance_guide containing ONLY actionable tasks,
   omitting seasons with no recommended maintenance actions.
4. Enhances Wildlife & Ecological Value with specific host insects (caterpillars, butterflies,
   moths, specialist bees), wildlife interactions (songbirds, small mammals), and cited sources with links.
5. Updates embeddedMasterPlants in index.html.
"""

import json
import os
import sys

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
    mobot_url = plant.get('plant_url') or 'https://www.missouribotanicalgarden.org/PlantFinder/'
    grownative_url = 'https://grownative.org'
    mdc_url = 'https://mdc.mo.gov/discover-nature/field-guide'

    # 1. Shorter summary advisor_description with links to sources
    summary = profile['summary'].strip()
    sources_text = f"Sources: [Missouri Botanical Garden PlantFinder]({mobot_url}), [Grow Native!]({grownative_url}), [MDC Field Guide]({mdc_url})."
    plant['advisor_description'] = f"{summary} {sources_text}"

    # 2. Set maintenance_level
    maint_level = profile['maint_level']
    plant['maintenance_level'] = maint_level

    # 3. Create structured maintenance_guide (strictly actionable only)
    maint_summary = (
        f"{maint_level} Maintenance. Requires minimal care once established. "
        f"Follow ecological cutback practices (50°F+ spring timing) to protect native bees and songbirds."
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

    guide = {
        'summary': maint_summary,
        'level': maint_level,
        'sources': 'Xerces Society for Invertebrate Conservation, Grow Native! (Missouri Prairie Foundation), Missouri Botanical Garden PlantFinder'
    }

    # Only include seasons with actionable maintenance
    if profile.get('spring_care'):
        guide['spring'] = profile['spring_care']
    if profile.get('summer_care'):
        guide['summer'] = profile['summer_care']
    if profile.get('fall_care'):
        guide['fall'] = profile['fall_care']
    if profile.get('winter_care'):
        guide['winter'] = profile['winter_care']
    if profile.get('division'):
        guide['division'] = profile['division']

    plant['maintenance_guide'] = guide

    # 4. Enhanced Wildlife and Ecological Value
    host_insects = profile.get('host_insects', 'Provides essential nectar and pollen for native bees and pollinators.')
    wildlife_users = profile.get('wildlife_users', 'Songbirds forage on seeds, berries, and beneficial insects hosted by this plant.')
    wildlife_sources = profile.get('wildlife_sources', '[National Wildlife Federation Native Plant Finder](https://www.nwf.org/nativeplantfinder/), [Xerces Society](https://xerces.org/), [MDC](https://mdc.mo.gov)')

    plant['wildlife_detail'] = {
        'host_insects': host_insects,
        'wildlife_users': wildlife_users,
        'sources': wildlife_sources
    }
    plant['wildlife_ecological_value'] = (
        f"**Host Plant Value:** {host_insects}\n\n"
        f"**Wildlife & Ecological Interactions:** {wildlife_users}\n\n"
        f"**Conservation & Scientific Sources:** {wildlife_sources}"
    )

    return plant

def main():
    profiles = build_full_catalog()
    print(f"Loaded {len(profiles)} botanical profiles.")

    with open('data/plants_enriched.json', 'r', encoding='utf-8') as f:
        plants = json.load(f)

    print(f"Loaded {len(plants)} plants from data/plants_enriched.json.")

    level_counts = {'Low': 0, 'Medium': 0, 'High': 0}
    season_counts = {'spring': 0, 'summer': 0, 'fall': 0, 'winter': 0, 'division': 0}

    for p in plants:
        sname = p.get('scientific_name')
        if sname not in profiles:
            raise KeyError(f"Species not found in botanical profiles: {sname}")
        enrich_plant_record(p, profiles[sname])
        level_counts[p['maintenance_level']] += 1
        for s in ['spring', 'summer', 'fall', 'winter', 'division']:
            if s in p['maintenance_guide']:
                season_counts[s] += 1

    print("\nMaintenance Level Distribution:")
    for lvl, count in level_counts.items():
        print(f"  - {lvl} Maintenance: {count} species ({count/len(plants)*100:.1f}%)")

    print("\nActionable Maintenance Season Coverage (Omitted if no actions):")
    for s, count in season_counts.items():
        print(f"  - {s.capitalize()}: {count} species ({count/len(plants)*100:.1f}%)")

    # Save to data/plants_enriched.json
    with open('data/plants_enriched.json', 'w', encoding='utf-8') as f:
        json.dump(plants, f, indent=2, ensure_ascii=False)
    print("\nSuccessfully updated data/plants_enriched.json")

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

    json_str = json.dumps(plants, separators=(',', ':'), ensure_ascii=False)
    new_html = html_content[:start_pos + len(start_tag)] + "\n" + json_str + "\n" + html_content[end_pos:]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"Successfully updated embeddedMasterPlants in index.html with {len(plants)} enriched botanical records.")

if __name__ == '__main__':
    main()
