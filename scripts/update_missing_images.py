#!/usr/bin/env python3
"""
scripts/update_missing_images.py

Applies authentic botanical photography for the species that were previously
missing images and using default fallbacks:
1. Carex blanda (Common Wood Sedge)
2. Lespedeza repens (Creeping Lespedeza)
3. Carex vulpinoidea (Fox Sedge)
4. Symphyotrichum cordifolium (Heart-leaved Aster)
5. Carex jamesii (James' Sedge)
6. Carex brevior (Short-beak Sedge)
7. Carex shortiana (Short's Sedge)
8. Scutellaria parvula (Small Skullcap)
9. Elymus virginicus (Virginia Wild Rye)
And additional plants with broken/missing imagery:
10. Carex bushii (Bush's Sedge)
11. Buchloe dactyloides (Buffalo Grass)
12. Liatris mucronata (Bottle Brush Blazing Star)
13. Andropogon gerardii (Big Bluestem)
14. Taxodium distichum (Bald Cypress - unescaped space URL fix)
"""

import json
import os
import shutil

BASE_IMAGE_URL = "https://bradlchr.github.io/images/plants"

SPECIES_IMAGE_UPDATES = {
    "Carex blanda": {
        "images": [
            {
                "url": f"{BASE_IMAGE_URL}/carex_blanda.jpg",
                "thumbnail": f"{BASE_IMAGE_URL}/carex_blanda.jpg",
                "label": "Woodland Foliage & Flowering Spikes",
                "caption": "Carex blanda (Common Wood Sedge) graceful arching foliage and emerging flower spikes in rich woodland habitat",
                "attribution": "Courtesy Wikimedia Commons / iNaturalist (CC BY-SA 4.0)",
                "source_name": "Illinois Wildflowers / Grow Native!",
                "source_url": "https://www.illinoiswildflowers.info/grasses/plants/cm_wdsedge.htm"
            }
        ]
    },
    "Lespedeza repens": {
        "images": [
            {
                "url": f"{BASE_IMAGE_URL}/lespedeza_repens.jpg",
                "thumbnail": f"{BASE_IMAGE_URL}/lespedeza_repens.jpg",
                "label": "Trailing Stems & Blossoms",
                "caption": "Lespedeza repens (Creeping Lespedeza) trailing prostrate stems with trifoliate clover-like leaves and pink-violet pea blossoms",
                "attribution": "Courtesy Wikimedia Commons / iNaturalist (CC BY 4.0)",
                "source_name": "Lady Bird Johnson Wildflower Center / Grow Native!",
                "source_url": "https://www.wildflower.org/plants/result.php?id_plant=LERE2"
            }
        ]
    },
    "Carex vulpinoidea": {
        "images": [
            {
                "url": f"{BASE_IMAGE_URL}/carex_vulpinoidea.jpg",
                "thumbnail": f"{BASE_IMAGE_URL}/carex_vulpinoidea.jpg",
                "label": "Bristly Inflorescence & Clump Habit",
                "caption": "Carex vulpinoidea (Fox Sedge) characteristic bristly fox-tail-like seed spikes in wet meadow soil",
                "attribution": "USDA NRCS Wetland Science Institute / Wikimedia Commons (Public Domain)",
                "source_name": "Missouri Botanical Garden PlantFinder",
                "source_url": "https://www.missouribotanicalgarden.org/PlantFinder/PlantFinderDetails.aspx?taxonid=279746"
            },
            {
                "url": "https://images.mobot.org/PlantRecordsVol3/prod/large960/00126000/126549.JPG",
                "thumbnail": "https://images.mobot.org/PlantRecordsVol3/prod/small240/00126000/126549.JPG",
                "label": "Carex vulpinoidea Seed Morphology",
                "caption": "Detailed achene and perigynium structure of Fox Sedge",
                "attribution": "Courtesy Missouri Botanical Garden PlantFinder",
                "source_name": "Missouri Botanical Garden PlantFinder",
                "source_url": "https://www.missouribotanicalgarden.org/PlantFinder/PlantFinderDetails.aspx?taxonid=279746"
            }
        ]
    },
    "Symphiotrichum cordifolium": {
        "images": [
            {
                "url": f"{BASE_IMAGE_URL}/symphyotrichum_cordifolium.jpg",
                "thumbnail": f"{BASE_IMAGE_URL}/symphyotrichum_cordifolium.jpg",
                "label": "Autumn Floral Display",
                "caption": "Symphyotrichum cordifolium (Heart-leaved Aster) dense clouds of pale blue-to-lavender composite blossoms and distinct heart-shaped basal foliage",
                "attribution": "Courtesy Wikimedia Commons (CC BY-SA 4.0)",
                "source_name": "Missouri Botanical Garden PlantFinder",
                "source_url": "https://www.missouribotanicalgarden.org/PlantFinder/PlantFinderDetails.aspx?taxonid=291338"
            }
        ]
    },
    "Symphyotrichum cordifolium": {
        "images": [
            {
                "url": f"{BASE_IMAGE_URL}/symphyotrichum_cordifolium.jpg",
                "thumbnail": f"{BASE_IMAGE_URL}/symphyotrichum_cordifolium.jpg",
                "label": "Autumn Floral Display",
                "caption": "Symphyotrichum cordifolium (Heart-leaved Aster) dense clouds of pale blue-to-lavender composite blossoms and distinct heart-shaped basal foliage",
                "attribution": "Courtesy Wikimedia Commons (CC BY-SA 4.0)",
                "source_name": "Missouri Botanical Garden PlantFinder",
                "source_url": "https://www.missouribotanicalgarden.org/PlantFinder/PlantFinderDetails.aspx?taxonid=291338"
            }
        ]
    },
    "Carex jamesii": {
        "images": [
            {
                "url": f"{BASE_IMAGE_URL}/carex_jamesii.jpg",
                "thumbnail": f"{BASE_IMAGE_URL}/carex_jamesii.jpg",
                "label": "Fine-Textured Foliage & Spikelets",
                "caption": "Carex jamesii (James' Sedge) graceful narrow foliage and distinctive long-beaked woodland spikelets",
                "attribution": "Courtesy Wikimedia Commons (CC BY-SA 4.0)",
                "source_name": "Illinois Wildflowers / Grow Native!",
                "source_url": "https://www.illinoiswildflowers.info/grasses/plants/james_sedge.htm"
            }
        ]
    },
    "Carex brevior": {
        "images": [
            {
                "url": f"{BASE_IMAGE_URL}/carex_brevior.jpg",
                "thumbnail": f"{BASE_IMAGE_URL}/carex_brevior.jpg",
                "label": "Prairie Clump & Perigynia Heads",
                "caption": "Carex brevior (Short-Beak Sedge / Plains Oval Sedge) erect tufts with rounded greenish-brown seed clusters",
                "attribution": "USDA NRCS / Robert H. Mohlenbrock (Public Domain)",
                "source_name": "Illinois Wildflowers / Grow Native!",
                "source_url": "https://www.illinoiswildflowers.info/grasses/plants/ploval_sedge.html"
            }
        ]
    },
    "Carex shortiana": {
        "images": [
            {
                "url": f"{BASE_IMAGE_URL}/carex_shortiana.jpg",
                "thumbnail": f"{BASE_IMAGE_URL}/carex_shortiana.jpg",
                "label": "Cylindrical Dark Spikes",
                "caption": "Carex shortiana (Short's Sedge) robust wetland tussocks with upright dark brown to cinnamon cylindrical seed spikes",
                "attribution": "Courtesy Copenhagen Botanical Garden / Daderot (Public Domain)",
                "source_name": "Grow Native! / Lady Bird Johnson Wildflower Center",
                "source_url": "https://www.wildflower.org/plants/result.php?id_plant=CASH"
            }
        ]
    },
    "Scutellaria parvula": {
        "images": [
            {
                "url": f"{BASE_IMAGE_URL}/scutellaria_parvula.jpg",
                "thumbnail": f"{BASE_IMAGE_URL}/scutellaria_parvula.jpg",
                "label": "Blossoms & Glade Foliage",
                "caption": "Scutellaria parvula (Small Skullcap) tubular violet-blue flowers with white-dotted lower lips on rocky glade substrate",
                "attribution": "Courtesy Wikimedia Commons (CC BY-SA 4.0)",
                "source_name": "Illinois Wildflowers / Grow Native!",
                "source_url": "https://www.illinoiswildflowers.info/glades/plants/sm_skullcap.htm"
            }
        ]
    },
    "Elymus virginicus": {
        "images": [
            {
                "url": f"{BASE_IMAGE_URL}/elymus_virginicus.jpg",
                "thumbnail": f"{BASE_IMAGE_URL}/elymus_virginicus.jpg",
                "label": "Bristly Awned Seedheads",
                "caption": "Elymus virginicus (Virginia Wild Rye) dense upright bristly seed spikes with prominent wheat-like awns in riverbank border",
                "attribution": "Courtesy Wikimedia Commons / Stefan.lefnaer (CC BY-SA 4.0)",
                "source_name": "Missouri Botanical Garden PlantFinder",
                "source_url": "https://www.missouribotanicalgarden.org/PlantFinder/PlantFinderDetails.aspx?taxonid=285239"
            }
        ]
    },
    "Carex bushii": {
        "images": [
            {
                "url": f"{BASE_IMAGE_URL}/carex_bushii.jpg",
                "thumbnail": f"{BASE_IMAGE_URL}/carex_bushii.jpg",
                "label": "Savannah Clump & Fruiting Spikes",
                "caption": "Carex bushii (Bush's Sedge) slender upright stems with bristly rounded green seed spikes in upland meadow",
                "attribution": "Courtesy Wikimedia Commons (CC BY-SA 4.0)",
                "source_name": "Missouri Botanical Garden PlantFinder / Grow Native!",
                "source_url": "https://www.missouribotanicalgarden.org/PlantFinder/PlantFinderDetails.aspx?taxonid=279769"
            }
        ]
    },
    "Buchloe dactyloides": {
        "images": [
            {
                "url": f"{BASE_IMAGE_URL}/buchloe_dactyloides.jpg",
                "thumbnail": f"{BASE_IMAGE_URL}/buchloe_dactyloides.jpg",
                "label": "Fine Turf & Flag-Like Seedheads",
                "caption": "Bouteloua dactyloides / Buchloe dactyloides (Buffalo Grass) fine-textured grayish-green turf and delicate staminate flag seedheads",
                "attribution": "Patrick Alexander / Wikimedia Commons (Public Domain)",
                "source_name": "Missouri Botanical Garden PlantFinder",
                "source_url": "https://www.missouribotanicalgarden.org/PlantFinder/PlantFinderDetails.aspx?taxonid=285229"
            }
        ]
    },
    "Liatris mucronata": {
        "images": [
            {
                "url": f"{BASE_IMAGE_URL}/liatris_mucronata.jpg",
                "thumbnail": f"{BASE_IMAGE_URL}/liatris_mucronata.jpg",
                "label": "Magenta Spire Inflorescence",
                "caption": "Liatris mucronata (Bottle Brush Blazing Star / Cusp Blazing Star) upright spires of fuzzy pink-purple floral disks",
                "attribution": "Courtesy Wikimedia Commons (CC BY-SA 3.0)",
                "source_name": "Lady Bird Johnson Wildflower Center / Grow Native!",
                "source_url": "https://www.wildflower.org/plants/result.php?id_plant=LIPUM"
            }
        ]
    },
    "Andropogon gerardii": {
        "images": [
            {
                "url": f"{BASE_IMAGE_URL}/andropogon_gerardii.jpg",
                "thumbnail": f"{BASE_IMAGE_URL}/andropogon_gerardii.jpg",
                "label": "Turkey-Foot Inflorescence",
                "caption": "Andropogon gerardii (Big Bluestem) iconic three-parted turkey-foot seed heads in tallgrass prairie setting",
                "attribution": "Matt Lavin / Wikimedia Commons (CC BY-SA 2.0)",
                "source_name": "Missouri Botanical Garden PlantFinder",
                "source_url": "https://www.missouribotanicalgarden.org/PlantFinder/PlantFinderDetails.aspx?taxonid=285262"
            }
        ]
    },
    "Taxodium distichum": {
        "images": [
            {
                "url": "https://images.mobot.org/PlantRecords1/prod/large960/00089000/89960.JPG",
                "thumbnail": "https://images.mobot.org/PlantRecords1/prod/small240/00089000/89960.JPG",
                "label": "Habit & Feathery Foliage",
                "caption": "Taxodium distichum (Bald Cypress) pyramidal habit, buttressed trunk base, and soft feathery needle foliage",
                "attribution": "Courtesy Missouri Botanical Garden PlantFinder",
                "source_name": "Missouri Botanical Garden PlantFinder",
                "source_url": "https://www.missouribotanicalgarden.org/PlantFinder/PlantFinderDetails.aspx?taxonid=287316"
            },
            {
                "url": f"{BASE_IMAGE_URL}/taxodium_distichum.jpg",
                "thumbnail": f"{BASE_IMAGE_URL}/taxodium_distichum.jpg",
                "label": "Autumn Copper Color",
                "caption": "Taxodium distichum (Bald Cypress) rich russet-bronze autumn coloration before deciduous needle drop",
                "attribution": "Courtesy Missouri Botanical Garden PlantFinder",
                "source_name": "Missouri Botanical Garden PlantFinder",
                "source_url": "https://www.missouribotanicalgarden.org/PlantFinder/PlantFinderDetails.aspx?taxonid=287316"
            }
        ]
    }
}

def main():
    enriched_path = 'data/plants_enriched.json'
    with open(enriched_path, 'r', encoding='utf-8') as f:
        plants = json.load(f)

    updated_count = 0
    for plant in plants:
        sci = plant.get('scientific_name')
        if sci in SPECIES_IMAGE_UPDATES:
            update = SPECIES_IMAGE_UPDATES[sci]
            plant['images'] = update['images']
            # Set image_url to the primary image url for compatibility
            plant['image_url'] = update['images'][0]['url']
            updated_count += 1
            print(f"Updated images for {sci} ({plant.get('common_names', [''])[0]}): {len(plant['images'])} photos")

    print(f"\nTotal species updated with authentic imagery: {updated_count}")

    # 1. Write back to data/plants_enriched.json
    with open(enriched_path, 'w', encoding='utf-8') as f:
        json.dump(plants, f, indent=2, ensure_ascii=False)
    print(f"Saved {enriched_path}")

    # 2. Update embeddedMasterPlants in index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    start_tag = '<script type="application/json" id="embeddedMasterPlants">'
    end_tag = '</script>'
    s_idx = html.find(start_tag)
    e_idx = html.find(end_tag, s_idx)
    if s_idx != -1 and e_idx != -1:
        new_json = json.dumps(plants, separators=(',', ':'), ensure_ascii=False)
        html = html[:s_idx + len(start_tag)] + "\n" + new_json + "\n  " + html[e_idx:]
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Updated embeddedMasterPlants in index.html")
    else:
        print("Warning: embeddedMasterPlants not found in index.html")

    # 3. Update android/app/src/main/assets/plants.json
    android_plants_path = 'android/app/src/main/assets/plants.json'
    if os.path.exists(android_plants_path):
        with open(android_plants_path, 'w', encoding='utf-8') as f:
            json.dump(plants, f, indent=2, ensure_ascii=False)
        print(f"Updated {android_plants_path}")

    # 4. Copy images to android assets so Android app has local copies as well
    android_images_dir = 'android/app/src/main/assets/images/plants'
    os.makedirs(android_images_dir, exist_ok=True)
    for fn in os.listdir('images/plants'):
        if fn.endswith('.jpg'):
            shutil.copy2(os.path.join('images/plants', fn), os.path.join(android_images_dir, fn))
    print(f"Synced {len(os.listdir('images/plants'))} images to {android_images_dir}")

if __name__ == '__main__':
    main()
