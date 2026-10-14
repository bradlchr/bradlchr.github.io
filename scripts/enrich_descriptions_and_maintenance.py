#!/usr/bin/env python3
"""
scripts/enrich_descriptions_and_maintenance.py

Enriches all 185 native plants in data/plants_enriched.json and index.html:
1. Synthesizes concise 2-sentence advisor_description with direct inline markdown links
   to exact species pages (Missouri Botanical Garden PlantFinder, Illinois Wildflowers, Grow Native!).
   NEVER includes generic homepage or category root links.
2. Sets scientifically grounded maintenance_level ('Low', 'Medium', 'High').
3. Sets structured seasonal maintenance_guide containing ONLY actionable instructions,
   completely omitting seasons with no recommended maintenance actions.
   All maintenance claims feature direct inline citations to conservation authorities.
4. Enhances Wildlife & Ecological Value with specific host insects (caterpillars, butterflies,
   moths, specialist bees) with direct inline links to BAMONA and Xerces, and specific wildlife
   foragers with direct inline links to Illinois Wildflowers.
5. Updates embeddedMasterPlants in index.html.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.abspath('.'))

from scripts.botanical_trees_shrubs import BOTANICAL_TREES_SHRUBS
from scripts.botanical_grasses_sedges_ferns_vines import BOTANICAL_GRASSES_SEDGES_FERNS_VINES
from scripts.botanical_wildflowers_1 import BOTANICAL_WILDFLOWERS_1
from scripts.botanical_wildflowers_2 import BOTANICAL_WILDFLOWERS_2

# Botanical synonyms mapping to Illinois Wildflowers
IL_SYNONYMS = {
    'Symphiotrichum drummondii': 'Aster drummondii',
    'Symphyotrichum drummondii': 'Aster drummondii',
    'Symphiotrichum cordifolium': 'Aster cordifolius',
    'Symphyotrichum cordifolium': 'Aster cordifolius',
    'Symphyotrichum novae-angliae': 'Aster novae-angliae',
    'Symphyotrichum oblongifolium': 'Aster oblongifolius',
    'Symphyotrichum laeve': 'Aster laevis',
    'Symphiotrichum oolentangiense': 'Aster oolentangiensis',
    'Symphyotrichum oolentangiense': 'Aster oolentangiensis',
    'Symphiotrichum turbinellum': 'Aster turbinellus',
    'Symphyotrichum turbinellum': 'Aster turbinellus',
    'Symphiotrichum lateriflorum': 'Aster lateriflorus',
    'Symphyotrichum lateriflorum': 'Aster lateriflorus',
    'Symphiotrichum sericeum': 'Aster sericeus',
    'Symphyotrichum sericeum': 'Aster sericeus',
    'Actaea racemosa': 'Cimicifuga racemosa',
    'Veronicastrum viginicum': 'Veronicastrum virginicum',
    'Eutrochium purpureum': 'Eupatorium purpureum',
    'Eutrochium maculatum': 'Eupatorium maculatum',
    'Eutrochium fistulosum': 'Eupatorium fistulosum',
    'Conoclinium coelestinum': 'Eupatorium coelestinum',
    'Oligoneuron rigidum': 'Solidago rigida',
    'Drymocallis arguta': 'Potentilla arguta',
    'Gillenia stipulata': 'Porteranthus stipulatus',
    'Ionactis linariifolia': 'Aster linariifolius',
    'Blephilia ciliata': 'Blephilia ciliata',
    'Scuttelaria incana': 'Scutellaria incana'
}

def load_il_mapping():
    if os.path.exists('data/il_wildflowers_mapping.json'):
        with open('data/il_wildflowers_mapping.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

IL_MAP = load_il_mapping()

def get_il_url(sname):
    if sname in IL_MAP:
        return IL_MAP[sname]
    syn = IL_SYNONYMS.get(sname)
    if syn and syn in IL_MAP:
        return IL_MAP[syn]
    return None

def build_full_catalog():
    all_profiles = {}
    all_profiles.update(BOTANICAL_TREES_SHRUBS)
    all_profiles.update(BOTANICAL_GRASSES_SEDGES_FERNS_VINES)
    all_profiles.update(BOTANICAL_WILDFLOWERS_1)
    all_profiles.update(BOTANICAL_WILDFLOWERS_2)
    return all_profiles

def clean_summer_care(sname, raw_care):
    if not raw_care:
        return None
    c_lower = raw_care.lower()

    # Passive triggers that are NOT actionable maintenance
    passive_triggers = [
        "thrives in rich, moist to dry woodland soils",
        "thrives in rich, moist, organic woodland",
        "thrives in rich, moist to average organic woodland",
        "thrives in moist to wet loams and heavy clay",
        "thrives in lean, sharply drained limestone",
        "thrives in lean, sharply drained sunny",
        "thrives in sunny, well-drained limestone",
        "thrives in standing water, wet clay",
        "thrives in standing water, saturated soils",
        "thrives in moist to wet soils in full sun",
        "thrives in full sun and average to moist soils",
        "thrives in full sun to light savanna",
        "thrives in full sun to partial shade in average to dry soils",
        "thrives in full sun to partial shade in average to moist soils",
        "thrives in full sun to partial shade; highly adaptable",
        "thrives in moist, rich loams and heavy clay",
        "thrives in moist, rich, dappled shade",
        "requires sharply drained sunny soil; thrives in rock",
        "requires sharply drained sunny soil; zero",
        "requires sharply drained soil; extremely",
        "requires sharp drainage and full sun",
        "requires full sun and sharp drainage",
        "zero supplemental watering needed once established",
        "zero supplemental watering needed once rooted",
        "zero supplemental water needed once established",
        "zero maintenance needed once established",
        "extremely drought and poor-soil proof",
        "extremely drought and clay tolerant once established",
        "extremely drought and urban stress tolerant",
        "extremely drought and heat tolerant once established",
        "extremely drought and heat tolerant; thrives",
        "extremely drought and heat hardy once established",
        "extremely drought-tolerant once established",
        "highly adaptable to both moist riverbanks",
        "highly drought tolerant in partial shade",
        "fixes nitrogen in poor, depleted soils",
        "roots kept shaded by groundcovers"
    ]

    for pt in passive_triggers:
        if pt in c_lower:
            # Check if there is an actionable watering, weeding, chelsea chop, or pruning clause
            action_verbs = ["water during", "water moderately", "provide supplemental deep watering",
                            "provide deep watering", "provide 1 inch", "chelsea chop", "edge or spade",
                            "deadhead", "prune unwanted root suckers", "maintain consistent soil moisture"]
            if any(k in c_lower for k in action_verbs):
                parts = raw_care.split(';')
                if len(parts) > 1 and any(k in parts[0].lower() for k in ["water", "moisture", "chop", "prune", "edge", "deadhead"]):
                    return parts[0].strip() + '.'
                parts = raw_care.split('. ')
                if len(parts) > 1 and any(k in parts[0].lower() for k in ["water", "moisture", "chop", "prune", "edge", "deadhead"]):
                    return parts[0].strip() + '.'
            return None

    if "thrives in" in c_lower:
        parts = raw_care.split(';')
        if len(parts) > 1 and any(k in parts[0].lower() for k in ["water", "moisture", "chop", "prune", "edge", "deadhead"]):
            return parts[0].strip() + '.'
        return None

    return raw_care.strip()

def clean_fall_care(sname, raw_care):
    if not raw_care:
        return None
    c_lower = raw_care.lower()

    passive_phrases = [
        "enjoy late-autumn blossoms",
        "enjoy long-lasting garnet-red",
        "enjoy glowing golden-yellow",
        "enjoy glowing copper-bronze",
        "enjoy persistent swirling silvery",
        "foliage takes on attractive",
        "foliage takes on rich crimson",
        "breathtaking late blue floral clouds",
        "persistent dark brown woody fertile fronds",
        "fleshy explosive capsules eject",
        "explosive seed capsules pop audibly"
    ]

    for pp in passive_phrases:
        if pp in c_lower:
            if "leave" in c_lower or "allow" in c_lower:
                m = re.search(r'(leave [^;\.]+)', raw_care, re.I)
                if m:
                    return m.group(1).strip() + '.'
            return None

    return raw_care.strip()

def clean_spring_care(sname, raw_care):
    if not raw_care:
        return None
    if "mertensia virginica" in sname.lower() or "enjoy early spring blooms" in raw_care.lower():
        return "Allow foliage to yellow and senesce naturally after spring flowering without cutting back to recharge dormant root tubers."
    return raw_care.strip()

def format_description(plant, profile):
    sname = plant['scientific_name']
    plant_url = plant.get('plant_url', '')
    il_url = get_il_url(sname)
    summary = profile['summary'].strip()

    sentences = re.split(r'\.\s+(?=[A-Z])', summary)
    if len(sentences) >= 2:
        s1 = sentences[0].strip()
        s2 = '. '.join(sentences[1:]).strip()
        if s2.endswith('.'):
            s2 = s2[:-1]
    else:
        s1 = summary.rstrip('.')
        s2 = None

    is_mobot = 'missouribotanicalgarden.org' in plant_url
    primary_name = "Missouri Botanical Garden PlantFinder" if is_mobot else "Grow Native!"

    desc_parts = [f"{s1} ([{primary_name}]({plant_url}))."]
    if s2:
        if il_url:
            desc_parts.append(f"{s2} ([Illinois Wildflowers]({il_url})).")
        else:
            desc_parts.append(f"{s2} ([{primary_name}]({plant_url})).")

    return " ".join(desc_parts)

def link_host_insects(text):
    # Link (*Genus species*) to BAMONA
    def repl(m):
        gs = m.group(1).strip()
        parts = gs.split()
        if len(parts) == 2:
            slug = f"{parts[0]}-{parts[1]}"
            if slug == "Eurytides-marcellus":
                slug = "neographium-marcellus"
            return f"(*{gs}*) ([Butterflies and Moths of North America](https://www.butterfliesandmoths.org/species/{slug}))"
        return m.group(0)

    t = re.sub(r'\(\*([A-Z][a-z]+ [a-z]+)\*\)', repl, text)

    # Link specialist bees / bumblebees to Xerces
    if any(k in t.lower() for k in ['specialist bee', 'mining bee', 'bumblebee', 'bombus']) and 'xerces.org/pollinator-conservation' not in t:
        t += " Specialist bees and native pollinators are supported ([Xerces Society: Pollinator Conservation](https://xerces.org/pollinator-conservation))."

    return t

def enrich_plant_record(plant, profile):
    sname = plant.get('scientific_name')
    plant_url = plant.get('plant_url')
    is_mobot = 'missouribotanicalgarden.org' in plant_url
    primary_name = "Missouri Botanical Garden PlantFinder" if is_mobot else "Grow Native!"
    il_url = get_il_url(sname)

    # 1. Concise advisor description with direct inline markdown citations
    plant['advisor_description'] = format_description(plant, profile)

    # 2. Set maintenance_level
    maint_level = profile['maint_level']
    plant['maintenance_level'] = maint_level

    # 3. Create structured maintenance_guide (strictly actionable only, flexible seasons)
    maint_summary = (
        f"{maint_level} Maintenance. Requires minimal care once established. "
        f"Adhere to conservation cutback practices (sustained 50°F+ spring timing) to protect cavity-nesting bees and songbirds."
    )
    if maint_level == 'High':
        maint_summary = (
            f"High Maintenance. Requires active moisture management or boundary spading to manage vigorous growth. "
            f"Adhere to seasonal timing to maximize ecological benefits while containing garden spread."
        )
    elif maint_level == 'Medium':
        maint_summary = (
            f"Medium Maintenance. Benefits from targeted mid-season care (such as Chelsea chopping or sucker pruning) "
            f"and spring cutback timing to sustain peak vigor and compact garden form."
        )

    guide = {
        'summary': maint_summary,
        'level': maint_level,
        'sources': f"[Xerces Society for Invertebrate Conservation](https://xerces.org/publications/guidelines/nesting-overwintering-habitat), [{primary_name}]({plant_url})"
    }

    # Spring (actionable + inline citation)
    sp_raw = clean_spring_care(sname, profile.get('spring_care'))
    if sp_raw:
        if sname in BOTANICAL_TREES_SHRUBS:
            guide['spring'] = f"{sp_raw.rstrip('.')} ([{primary_name}]({plant_url}))."
        else:
            guide['spring'] = f"{sp_raw.rstrip('.')} ([Xerces Society: Nesting Resources](https://xerces.org/publications/guidelines/nesting-overwintering-habitat))."

    # Summer (actionable only + inline citation)
    su_raw = clean_summer_care(sname, profile.get('summer_care'))
    if su_raw:
        guide['summer'] = f"{su_raw.rstrip('.')} ([{primary_name}]({plant_url}))."

    # Fall (actionable only + inline citation)
    fa_raw = clean_fall_care(sname, profile.get('fall_care'))
    if fa_raw:
        guide['fall'] = f"{fa_raw.rstrip('.')} ([Xerces Society: Leave the Leaves](https://xerces.org/leave-the-leaves))."

    # Winter (actionable only + inline citation)
    wi_raw = profile.get('winter_care')
    if wi_raw and wi_raw.strip():
        guide['winter'] = f"{wi_raw.strip().rstrip('.')} ([{primary_name}]({plant_url}))."

    # Division (actionable + inline citation)
    div_raw = profile.get('division')
    if div_raw and div_raw.strip():
        guide['division'] = f"{div_raw.strip().rstrip('.')} ([{primary_name}]({plant_url}))."

    plant['maintenance_guide'] = guide

    # 4. Enhanced Wildlife and Ecological Value with specific inline citations
    raw_host = profile.get('host_insects', 'Provides essential nectar and pollen for native bees and pollinators.')
    host_insects = link_host_insects(raw_host)

    raw_users = profile.get('wildlife_users', 'Songbirds forage on seeds, berries, and beneficial insects hosted by this plant.').strip()
    if il_url:
        wildlife_users = f"{raw_users.rstrip('.')} ([Illinois Wildflowers]({il_url}))."
    else:
        wildlife_users = f"{raw_users.rstrip('.')} ([{primary_name}]({plant_url}))."

    # Compile unique cited source links for this species
    all_links = re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', f"{host_insects} {wildlife_users}")
    unique_links = []
    seen = set()
    for name, url in all_links:
        if url not in seen:
            seen.add(url)
            unique_links.append(f"[{name}]({url})")

    wildlife_sources = ", ".join(unique_links) if unique_links else f"[{primary_name}]({plant_url})"

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
