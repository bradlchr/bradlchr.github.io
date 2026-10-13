#!/usr/bin/env python3
"""
Uploads the complete Missouri Botanical Garden PlantFinder enriched catalog
to Google Cloud Firestore (/plants/{docId}).
"""
import json
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

PROJECT_ID = "deep-roots-nature-advisors"
DATABASE_ID = "deep-roots-nature-advisors"
BASE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/{DATABASE_ID}/documents/plants"

def load_plants():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    start_tag = '<script type="application/json" id="embeddedMasterPlants">'
    end_tag = '</script>'
    start_idx = content.find(start_tag)
    end_idx = content.find(end_tag, start_idx)
    raw = content[start_idx + len(start_tag):end_idx]
    return json.loads(raw)

def upload_plant(plant):
    doc_id = plant.get('id') or plant.get('scientific_name', '').lower().replace(' ', '-')
    doc_id_clean = urllib.parse.quote(doc_id, safe='')
    url = f"{BASE_URL}/{doc_id_clean}"

    fields = {
        'scientific_name': {'stringValue': plant.get('scientific_name', '')},
        'common_names': {'arrayValue': {'values': [{'stringValue': str(c)} for c in plant.get('common_names', [])]}},
        'native_environment': {'stringValue': plant.get('native_environment', 'Forest')},
        'plant_url': {'stringValue': plant.get('plant_url', '') or plant.get('plantfinder_url', '')},
        'advisor_description': {'stringValue': plant.get('advisor_description', '')},
        'sociability': {'stringValue': plant.get('sociability', 'Moderately Social')},
        'height_display': {'stringValue': plant.get('height_display', '1–3 ft')}
    }

    if plant.get('plantfinder_url'):
        fields['plantfinder_url'] = {'stringValue': plant['plantfinder_url']}

    if plant.get('architectural_layer'):
        fields['architectural_layer'] = {'stringValue': plant['architectural_layer']}

    plant_types = plant.get('plant_type', ['Wildflower'])
    if isinstance(plant_types, str):
        plant_types = [plant_types]
    fields['plant_type'] = {'arrayValue': {'values': [{'stringValue': str(t)} for t in plant_types]}}

    for arr_field in ['soil_requirements', 'moisture_requirements', 'light_requirements', 'wildlife_ecosystem_benefits', 'bloom_color', 'bloom_period']:
        vals = plant.get(arr_field, [])
        if isinstance(vals, str):
            vals = [vals]
        fields[arr_field] = {'arrayValue': {'values': [{'stringValue': str(v)} for v in vals]}}

    # Images array with MOBOT attribution
    images = plant.get('images', [])
    image_maps = []
    for img in images:
        if not img.get('url'):
            continue
        im_fields = {
            'url': {'stringValue': img.get('url', '')},
            'thumbnail': {'stringValue': img.get('thumbnail') or img.get('thumbnail_url', '')},
            'label': {'stringValue': img.get('label', 'Botanical Specimen')},
            'caption': {'stringValue': img.get('caption', '')},
            'attribution_name': {'stringValue': img.get('attribution') or img.get('attribution_name', 'Courtesy Missouri Botanical Garden PlantFinder')},
            'license': {'stringValue': 'Courtesy Missouri Botanical Garden PlantFinder'},
            'attribution_url': {'stringValue': img.get('source_url') or plant.get('plantfinder_url', '')}
        }
        image_maps.append({'mapValue': {'fields': im_fields}})

    fields['images'] = {'arrayValue': {'values': image_maps}}

    body = json.dumps({'fields': fields}).encode('utf-8')
    req = urllib.request.Request(url, data=body, method='PATCH', headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status in (200, 201):
                return True, plant.get('scientific_name')
            return False, f"{plant.get('scientific_name')}: Status {resp.status}"
    except Exception as e:
        return False, f"{plant.get('scientific_name')}: {str(e)}"

def main():
    plants = load_plants()
    print(f"Loaded {len(plants)} plants from embeddedMasterPlants")

    success_count = 0
    fail_count = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(upload_plant, p): p for p in plants}
        for future in as_completed(futures):
            ok, msg = future.result()
            if ok:
                success_count += 1
            else:
                fail_count += 1
                print(f"Failed: {msg}")

    print(f"\nUpload Complete! Successfully uploaded: {success_count}/{len(plants)} (Failed: {fail_count})")

if __name__ == '__main__':
    main()
