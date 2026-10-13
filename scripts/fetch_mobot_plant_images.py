#!/usr/bin/env python3
"""
Fetches authentic Missouri Botanical Garden PlantFinder image galleries and details
for all Kansas City native species mapped via Wikidata Taxon IDs.
Generates data/mobot_plant_images.json with structured multi-image galleries,
full URLs, thumbnails, labels, captions, and official linkbacks.
"""

import json
import os
import re
import ssl
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

MAPPING_PATH = 'data/wikidata_mobot_mapping.json'
OUTPUT_PATH = 'data/mobot_plant_images.json'

if not os.path.exists(MAPPING_PATH):
    print("Mapping file missing:", MAPPING_PATH)
    sys.exit(1)

with open(MAPPING_PATH, 'r', encoding='utf-8') as f:
    mapping = json.load(f)

print(f"Loaded {len(mapping)} species mappings.")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_plant_images(sci_name, taxon_id):
    mobot_page_url = f"https://www.missouribotanicalgarden.org/PlantFinder/PlantFinderDetails.aspx?taxonid={taxon_id}"
    fetch_url = f"https://plantfinder.mobot.org/PlantFinderDetails.aspx?taxonid={taxon_id}"
    req = urllib.request.Request(fetch_url, headers=headers)
    
    images = []
    try:
        with urllib.request.urlopen(req, timeout=12, context=ctx) as r:
            html = r.read().decode('utf-8', errors='ignore')

        # 1. Primary Image
        m_prim = re.search(r'src=\"([^\"]+)\"\s+id=\"ctl00_MainContentPlaceHolder_PrimaryImageSample\"', html)
        if m_prim:
            raw_u = m_prim.group(1)
            large_u = raw_u.replace('/small240/', '/large960/')
            images.append({
                'url': large_u,
                'thumbnail': raw_u,
                'label': 'Primary Botanical Specimen',
                'caption': f'{sci_name} botanical specimen at Missouri Botanical Garden',
                'attribution': 'Courtesy Missouri Botanical Garden PlantFinder',
                'source_name': 'Missouri Botanical Garden PlantFinder',
                'source_url': mobot_page_url
            })

        # 2. Thumbnail Gallery
        thumb_matches = re.findall(r'src=\"([^\"]+)\"\s+id=\"ctl00_MainContentPlaceHolder_ImagesList_ctl\d+_ThumbnailImageSample\"', html)
        caption_matches = re.findall(r'id=\"ctl00_MainContentPlaceHolder_ImagesList_ctl\d+_CaptionText\"[^>]*>(.*?)</a>', html)

        # Include up to 8 distinct gallery images
        seen_urls = set()
        if images:
            seen_urls.add(images[0]['url'])

        for idx, u in enumerate(thumb_matches):
            if len(images) >= 8:
                break
            large_u = u.replace('/thumbnail100/', '/large960/')
            if large_u in seen_urls:
                continue
            seen_urls.add(large_u)

            cap = caption_matches[idx].strip() if idx < len(caption_matches) else ''
            label = cap if cap else f'Botanical Detail {idx + 2}'
            images.append({
                'url': large_u,
                'thumbnail': u.replace('/thumbnail100/', '/small240/'),
                'label': label,
                'caption': cap or f'{sci_name} floral and foliage characteristics',
                'attribution': 'Courtesy Missouri Botanical Garden PlantFinder',
                'source_name': 'Missouri Botanical Garden PlantFinder',
                'source_url': mobot_page_url
            })

        return sci_name, {
            'scientific_name': sci_name,
            'mobot_taxon_id': taxon_id,
            'plant_url': mobot_page_url,
            'images': images
        }
    except Exception as e:
        return sci_name, {
            'scientific_name': sci_name,
            'mobot_taxon_id': taxon_id,
            'plant_url': mobot_page_url,
            'images': [],
            'error': str(e)
        }

results = {}
total = len(mapping)
print(f"Beginning concurrent fetch for {total} species across 8 worker threads...")

start_time = time.time()
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(fetch_plant_images, sp, tid) for sp, tid in mapping.items()]
    completed = 0
    for future in as_completed(futures):
        sp, data = future.result()
        results[sp] = data
        completed += 1
        img_count = len(data.get('images', []))
        if completed % 25 == 0 or completed == total:
            print(f"Progress: {completed}/{total} species processed ({time.time() - start_time:.1f}s)")

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

has_images = sum(1 for d in results.values() if len(d.get('images', [])) > 0)
total_images = sum(len(d.get('images', [])) for d in results.values())
print(f"\nFetch complete in {time.time() - start_time:.1f}s!")
print(f"Species with MOBOT images: {has_images}/{total}")
print(f"Total authentic botanical images retrieved: {total_images}")
