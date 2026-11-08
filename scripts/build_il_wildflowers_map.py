import urllib.request, re, json

indexes = [
    ('trees', 'https://www.illinoiswildflowers.info/trees/tree_index.htm'),
    ('prairie', 'https://www.illinoiswildflowers.info/prairie/plantx/prairie_index.htm'),
    ('woodland', 'https://www.illinoiswildflowers.info/woodland/woodland_index.htm'),
    ('wetland', 'https://www.illinoiswildflowers.info/wetland/wetland_index.htm'),
    ('savanna', 'https://www.illinoiswildflowers.info/savanna/savanna_index.htm'),
    ('grasses', 'https://www.illinoiswildflowers.info/grasses/grass_index.htm'),
]

il_map = {}
for cat, url in indexes:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        matches = re.findall(r'<a href="([^"]+)">(?:<[^>]+>)*([^<]+)(?:<[^>]+>)*</a>', html)
        for path, text in matches:
            if 'plants/' in path:
                if cat == 'prairie':
                    full_url = f'https://www.illinoiswildflowers.info/prairie/plantx/{path}'
                else:
                    full_url = f'https://www.illinoiswildflowers.info/{cat}/{path}'
                m = re.match(r'([A-Z][a-z]+(?:\s+[a-z]+)+)', text.strip())
                if m:
                    sname = m.group(1).strip()
                    if sname not in il_map:
                        il_map[sname] = full_url
    except Exception as e:
        print(f'Error fetching {cat}: {e}')

print(f'Indexed {len(il_map)} species on Illinois Wildflowers.')

with open('data/plants_enriched.json') as f:
    plants = json.load(f)

matched = 0
for p in plants:
    sname = p['scientific_name']
    if sname in il_map:
        matched += 1

print(f'Matched {matched} / {len(plants)} plants in our database!')
with open('data/il_wildflowers_mapping.json', 'w') as f:
    json.dump(il_map, f, indent=2)
