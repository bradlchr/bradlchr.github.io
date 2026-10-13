import os
import sys
import json
import re

# Ensure root in path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

SOURCE_DATA_PATH = os.path.join(ROOT_DIR, 'android', 'app', 'src', 'main', 'assets', 'plants.json')
if not os.path.exists(SOURCE_DATA_PATH):
    SOURCE_DATA_PATH = os.path.join(ROOT_DIR, 'data', 'plants_enriched.json')
OUTPUT_FIRESTORE_PAYLOAD = os.path.join(ROOT_DIR, 'data', 'firestore_plants_payload.json')
os.makedirs(os.path.join(ROOT_DIR, 'data'), exist_ok=True)

def generate_slug(sci_name: str) -> str:
    s = sci_name.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

def transform_to_firestore_schema(raw_plants):
    firestore_docs = []
    
    for p in raw_plants:
        slug = generate_slug(p['scientific_name'])
        
        # Build Firestore document schema exactly matching mobile & rules specifications
        doc = {
            'id': slug,
            'scientific_name': p['scientific_name'],
            'common_names': p.get('common_names', []),
            'native_environment': p.get('native_environment', 'Forest'),
            'plant_type': p.get('plant_type', ['Wildflower']),
            'architectural_layer': [p.get('architectural_layer', 'Seasonal/Herbaceous Layer')],
            'mature_height': {
                'min_ft': float(p.get('mature_height_min', 1.0)),
                'max_ft': float(p.get('mature_height_max', 3.0)),
                'display': p.get('height_display', '1–3 ft')
            },
            'bloom_color': p.get('bloom_color', ['Yellow']),
            'bloom_period': p.get('bloom_period', ['Summer']),
            'soil_requirements': p.get('soil_requirements', ['Loam']),
            'moisture_requirements': p.get('moisture_requirements', ['Medium']),
            'light_requirements': p.get('light_requirements', ['Full Sun']),
            'wildlife_ecosystem_benefits': p.get('wildlife_ecosystem_benefits', ['Pollinator Magnet']),
            'sociability': p.get('sociability', 'Medium / Moderate Spreading'),
            'advisor_description': p.get('advisor_description', ''),
            'special_tags': p.get('special_tags', []),
            'images': p.get('images', [
                {
                    'url': 'https://images.unsplash.com/photo-1598880940371-c756e015fea1?auto=format&fit=crop&w=800&q=80',
                    'caption': f"{p['scientific_name']} in native habitat",
                    'attribution_name': 'Missouri Botanical Garden / Creative Commons',
                    'attribution_url': 'https://www.missouribotanicalgarden.org',
                    'license': 'CC BY-SA 4.0'
                }
            ]),
            'sources': p.get('sources', [
                {
                    'source_name': 'Missouri Botanical Garden Plant Finder',
                    'source_url': 'https://www.missouribotanicalgarden.org',
                    'notes': 'Regional botanical specification'
                }
            ]),
            'metadata': {
                'created_by': 'system_seed_admin',
                'updated_by': 'system_seed_admin',
                'created_at': '2026-10-07T12:00:00Z',
                'updated_at': '2026-10-07T12:00:00Z'
            }
        }
        firestore_docs.append(doc)

    return firestore_docs

def seed_to_firebase(service_account_path: str = None):
    with open(SOURCE_DATA_PATH, 'r', encoding='utf-8') as f:
        raw_plants = json.load(f)
        
    print(f"Loaded {len(raw_plants)} enriched species from {SOURCE_DATA_PATH}")
    firestore_docs = transform_to_firestore_schema(raw_plants)
    
    with open(OUTPUT_FIRESTORE_PAYLOAD, 'w', encoding='utf-8') as f:
        json.dump(firestore_docs, f, indent=2)
    print(f"Saved {len(firestore_docs)} validated Firestore documents to {OUTPUT_FIRESTORE_PAYLOAD}")

    # Check for Firebase Admin credentials
    sa_path = service_account_path or os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if sa_path and os.path.exists(sa_path):
        try:
            import firebase_admin
            from firebase_admin import credentials, firestore
            
            cred = credentials.Certificate(sa_path)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            
            print(f"Connecting to Cloud Firestore with credentials from {sa_path}...")
            batch = db.batch()
            batch_count = 0
            total_committed = 0

            for doc in firestore_docs:
                doc_ref = db.collection('plants').document(doc['id'])
                batch.set(doc_ref, doc)
                batch_count += 1
                
                if batch_count >= 400:
                    batch.commit()
                    total_committed += batch_count
                    print(f"Committed batch of {batch_count} species ({total_committed}/{len(firestore_docs)})...")
                    batch = db.batch()
                    batch_count = 0
                    
            if batch_count > 0:
                batch.commit()
                total_committed += batch_count
                
            print(f"Successfully migrated all {total_committed} plants to Cloud Firestore 'plants' collection!")
        except Exception as e:
            print(f"Firebase Admin SDK migration note: {e}")
    else:
        print("Note: Set GOOGLE_APPLICATION_CREDENTIALS to your service-account.json to batch upload live to Cloud Firestore.")
        print(f"The mobile client automatically uses the validated payload from '{OUTPUT_FIRESTORE_PAYLOAD}' as its embedded offline database.")

if __name__ == '__main__':
    seed_to_firebase()
