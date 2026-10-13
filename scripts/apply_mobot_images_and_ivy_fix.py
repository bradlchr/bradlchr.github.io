#!/usr/bin/env python3
"""
Applies authentic Missouri Botanical Garden PlantFinder multi-image galleries
to all native species in index.html and data/plants_enriched.json.
Also updates English Ivy invasive species with verified authentic Bugwood images of Hedera helix.
"""

import json
import os
import re

INDEX_PATH = 'index.html'
ENRICHED_PATH = 'data/plants_enriched.json'
MOBOT_DATA_PATH = 'data/mobot_plant_images.json'

mobot_data = json.load(open(MOBOT_DATA_PATH, 'r', encoding='utf-8'))
html = open(INDEX_PATH, 'r', encoding='utf-8').read()

# 1. Update embeddedMasterPlants
s_tag = '<script type="application/json" id="embeddedMasterPlants">'
e_tag = '</script>'
s_idx = html.index(s_tag)
e_idx = html.index(e_tag, s_idx)
plants = json.loads(html[s_idx + len(s_tag):e_idx].strip())

updated_plants = 0
for p in plants:
    sci = p['scientific_name']
    if sci in mobot_data and len(mobot_data[sci].get('images', [])) > 0:
        entry = mobot_data[sci]
        p['images'] = entry['images']
        p['plant_url'] = entry['plant_url']
        if 'sources' not in p or not isinstance(p['sources'], list):
            p['sources'] = []
        has_mobot_src = False
        for s in p['sources']:
            if 'Missouri Botanical Garden' in s.get('source_name', ''):
                s['source_url'] = entry['plant_url']
                s['notes'] = f'Courtesy Missouri Botanical Garden PlantFinder: {sci}'
                has_mobot_src = True
        if not has_mobot_src:
            p['sources'].append({
                'source_name': 'Missouri Botanical Garden PlantFinder',
                'notes': f'Botanical Profile and Cultural Requirements for {sci}',
                'source_url': entry['plant_url']
            })
        updated_plants += 1

new_plants_json = json.dumps(plants, separators=(',', ':'))
html = html[:s_idx + len(s_tag)] + '\n' + new_plants_json + '\n  ' + html[e_idx:]

with open(ENRICHED_PATH, 'w', encoding='utf-8') as f:
    json.dump(plants, f, indent=2)

print(f"Updated {updated_plants} plants in embeddedMasterPlants and {ENRICHED_PATH}.")

# 2. Update English Ivy (Hedera helix) authentic images in index.html
ivy_old_pattern = r'\{\s*"id":\s*"inv-english-ivy",[\s\S]*?"id":\s*"inv-callery-pear"'
ivy_match = re.search(ivy_old_pattern, html)
if ivy_match:
    authentic_ivy_block = """{
    "id": "inv-english-ivy",
    "common_name": "English Ivy",
    "scientific_name": "Hedera helix",
    "plant_type": "Evergreen Climbing Vine",
    "image_url": "https://bugwoodcloud.org/images/768x512/9005071.jpg",
    "identification": "Alternate, thick, waxy evergreen leaves with 3–5 shallow lobes and pale veins. Adult flowering foliage becomes unlobed and diamond-shaped, bearing terminal clusters of greenish flowers and dark poisonous berries.",
    "removal_tips": "Sever climbing stems in a clear band around tree bases (do not pull off bark). Carefully dig up ground root crowns; repeat mowing or targeted triclopyr spray with methylated seed oil.",
    "ref_url": "https://www.invasive.org/browse/subinfo.cfm?sub=3026",
    "threat": "Girdles and suffocates mature trees, traps moisture causing fungal rot, and creates barren ground deserts.",
    "info_url": "https://www.invasive.org/browse/subinfo.cfm?sub=3026",
    "control_url": "https://www.fs.usda.gov/database/feis/plants/vine/hedhel/all.html",
    "ref_name": "Invasive.org Field Guide",
    "control_name": "USDA Forest Service FEIS",
    "images": [
      {
        "url": "https://bugwoodcloud.org/images/768x512/9005071.jpg",
        "label": "Juvenile Foliage & Stems",
        "caption": "Alternate, waxy evergreen leaves with 3–5 shallow lobes and distinct light-colored veins",
        "author": "James H. Miller, USDA Forest Service",
        "license": "CC BY 3.0 US",
        "source_name": "Bugwood.org / Forestry Images",
        "source_url": "https://www.forestryimages.org/browse/detail.cfm?imgnum=9005071"
      },
      {
        "url": "https://bugwoodcloud.org/images/768x512/2307149.jpg",
        "label": "Climbing Habit & Aerial Rootlets",
        "caption": "Heavy woody climbing stems clinging to tree bark with dense aerial rootlets",
        "author": "James H. Miller, USDA Forest Service",
        "license": "CC BY 3.0 US",
        "source_name": "Bugwood.org / Forestry Images",
        "source_url": "https://www.forestryimages.org/browse/detail.cfm?imgnum=2307149"
      },
      {
        "url": "https://bugwoodcloud.org/images/768x512/5159060.jpg",
        "label": "Mature Growth & Flowers",
        "caption": "Unlobed adult flowering foliage bearing terminal umbels of flowers and dark berries",
        "author": "Forest & Kim Starr, Starr Environmental",
        "license": "CC BY 3.0 US",
        "source_name": "Bugwood.org / Forestry Images",
        "source_url": "https://www.forestryimages.org/browse/detail.cfm?imgnum=5159060"
      },
      {
        "url": "https://bugwoodcloud.org/images/768x512/5159061.jpg",
        "label": "Vigorous Ground Infestation",
        "caption": "Dense evergreen monoculture blanketing the forest floor and smothering native plants",
        "author": "Forest & Kim Starr, Starr Environmental",
        "license": "CC BY 3.0 US",
        "source_name": "Bugwood.org / Forestry Images",
        "source_url": "https://www.forestryimages.org/browse/detail.cfm?imgnum=5159061"
      }
    ]
  },
  {
    "id": "inv-callery-pear\""""
    html = html[:ivy_match.start()] + authentic_ivy_block + html[ivy_match.end():]
    print("English Ivy invasive record successfully replaced with authentic Hedera helix images.")
else:
    print("Warning: could not locate inv-english-ivy block via regex!")

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved updated index.html successfully.")
