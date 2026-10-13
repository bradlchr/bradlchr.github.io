import zipfile
import xml.etree.ElementTree as ET
import re
import json

def parse_docx(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        tree = ET.fromstring(z.read('word/document.xml'))
        texts = []
        for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            p_text = ''.join(node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text)
            if p_text.strip():
                texts.append(p_text.strip())
    
    # We will identify sections
    sections = {}
    valid_envs = {
        'Forest': 'Forest',
        'Cliff/Glade': 'Cliff/Glade',
        'Prairie': 'Prairie',
        'Savannah/Woodland': 'Savannah/Woodland',
        'Stream Edge/Wetland': 'Stream Edge/Wetland'
    }
    
    current_env = None
    sociability_section = False
    curious_sociability = {
        'solitary': set(),
        'moderate': set(),
        'gregarious': set()
    }
    cur_soc_tier = None
    
    raw_plants = []
    
    i = 0
    while i < len(texts):
        line = texts[i]
        
        # Check environment headers
        matched_env = None
        for env_key in valid_envs:
            if line.strip() == env_key or (env_key in line and ('I.' in line or 'II.' in line or 'III.' in line or 'IV.' in line or 'V.' in line)):
                if not any(stop in line for stop in ['Container', 'Native Plant Designs', 'Suggested additions']):
                    matched_env = env_key
                    break
        
        if matched_env and not ('I.' in line and 'Forest1' in line and len(line) < 15 and i < 20):
            # Header check
            if line in valid_envs:
                current_env = valid_envs[line]
                sociability_section = False
                i += 1
                continue

        if 'IX.' in line or 'Sociability of plant species' in line:
            sociability_section = True
            current_env = None
            i += 1
            continue
            
        if sociability_section:
            if 'Less Social' in line or 'Solitary' in line:
                cur_soc_tier = 'solitary'
            elif 'Medium' in line or 'Moderate' in line:
                cur_soc_tier = 'moderate'
            elif 'Highly Social' in line or 'Gregarious' in line:
                cur_soc_tier = 'gregarious'
            elif cur_soc_tier and '(' in line and ')' in line:
                # Extract sci name e.g. Rock Pink (Phemeranthus calycinus)
                m = re.search(r'\(([^)]+)\)', line)
                if m:
                    curious_sociability[cur_soc_tier].add(m.group(1).strip().lower())
            i += 1
            continue
            
        if current_env:
            if any(line.startswith(stop) for stop in ['Container Planting', 'Native Plant Designs', 'Suggested additions', 'IX.']):
                current_env = None
                i += 1
                continue
                
            # Check if this line is a plant
            # Sometimes a plant entry continues onto next line if next line doesn't have '(' and ')'
            plant_match = re.match(r'^(\*?\s*)([^(\n]+?)\s*[-–—]?\s*\(([^)]+)\)\s*[-–—]?\s*(.*)$', line)
            if plant_match:
                star, common, sci, desc = plant_match.groups()
                full_desc = desc
                # Lookahead for continuation lines
                while i + 1 < len(texts):
                    next_line = texts[i+1]
                    if any(next_line.startswith(h) for h in list(valid_envs.keys()) + ['Container', 'Native Plant Designs', 'Suggested additions', 'IX.']):
                        break
                    # If next line has (Sci Name), it's a new plant
                    if re.match(r'^(\*?\s*)([^(\n]+?)\s*[-–—]?\s*\(([^)]+)\)', next_line):
                        break
                    # Otherwise it's a continuation paragraph!
                    full_desc += ' ' + next_line
                    i += 1
                
                raw_plants.append({
                    'native_environment': current_env,
                    'is_asterisk': bool(star.strip()),
                    'common_raw': common.strip(' -–—*'),
                    'scientific_raw': sci.strip(),
                    'description_raw': full_desc.strip()
                })
        i += 1

    return raw_plants, curious_sociability

if __name__ == '__main__':
    plants, soc = parse_docx('1. MASTER PLANT LIST - NA.docx')
    print(f'Parsed {len(plants)} plants.')
    print('Sociability counts:')
    for k, v in soc.items():
        print(f'  {k}: {len(v)} species: {list(v)[:3]}...')
    
    envs = {}
    for p in plants:
        envs[p['native_environment']] = envs.get(p['native_environment'], 0) + 1
    print('Environments count:', envs)
