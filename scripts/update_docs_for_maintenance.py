#!/usr/bin/env python3
"""
scripts/update_docs_for_maintenance.py
Updates CODE_DOCUMENTATION.md and docs.html with the new:
- Botanical Advisor Description Synthesis & Source Attribution
- Maintenance Level Ranking Engine ('Low', 'Medium', 'High') and Sidebar Filter
- Seasonal Maintenance & Conservation Guide (Xerces Society / Grow Native! / MOBOT standards)
- Word (.docx) Consultation Report Integration with maintenance recommendations
- Helpers: getPlantMaintenanceLevel and getPlantMaintenanceGuide
"""

def update_docs():
    # 1. Update CODE_DOCUMENTATION.md
    with open('CODE_DOCUMENTATION.md', 'r', encoding='utf-8') as f:
        md = f.read()

    doc_section = """
### Module 4B: Botanical Maintenance Engine & Ecological Care (New)

#### `getPlantMaintenanceLevel(plant)`
- **Line**: ~7235 | **Async**: No
- **Parameters**: `plant` (Object)
- **Description**: Returns the scientifically grounded maintenance ranking for the species (`'Low'`, `'Medium'`, or `'High'`).

#### `getPlantMaintenanceGuide(plant)`
- **Line**: ~7240 | **Async**: No
- **Parameters**: `plant` (Object)
- **Description**: Returns a structured seasonal care dictionary (`summary`, `spring`, `summer`, `fall`, `winter`, `division`, `sources`) adhering to Xerces Society and Grow Native! conservation guidelines.

#### Seasonal Maintenance Timings & Standards:
- **Spring (50°F+ Cutback)**: Wait until daytime temperatures consistently exceed 50°F before cutting back dead foliage to allow cavity-nesting solitary bees and overwintering pupae to emerge. Leave 8 to 18 inches of standing stubble as active nesting tunnels.
- **Summer Care (Chelsea Chop & Moisture)**: Taller species (*Symphyotrichum*, *Helenium*, *Monarda*) benefit from a late-May/early-June 'Chelsea chop' (pruned back by 1/3 to 1/2) to stimulate dense branching and prevent flopping. Drought resilient once established.
- **Fall Habitat Care (Seedhead Retention)**: Stems and seedheads are retained throughout autumn without cutting down, providing crucial winter seed calories for American Goldfinches, juncos, and native songbirds.
- **Winter Protection**: Standing silhouettes catch insulating snowdrifts and buffer crowns against Midwest freeze-thaw heaving. Preserves ground leaf litter for overwintering queen bumblebees.
- **Division Guidelines**: Evaluates root architecture—taprooted species (*Baptisia*, *Asclepias*, *Eryngium*) are never divided, while fibrous/rhizomatous species are divided every 3–5 years in early spring.
- **Consultation Report Inclusion**: Both the Word (.docx) report generator and consultation staging drawer inject maintenance ranking tags and seasonal instructions directly into client plant recommendations.
"""

    if "Module 4B: Botanical Maintenance Engine" not in md:
        target = "#### `applyFilters()`"
        md = md.replace(target, doc_section + "\n" + target, 1)
        with open('CODE_DOCUMENTATION.md', 'w', encoding='utf-8') as f:
            f.write(md)
        print("Updated CODE_DOCUMENTATION.md with Botanical Maintenance Engine documentation.")
    else:
        print("CODE_DOCUMENTATION.md already contains Maintenance Engine documentation.")

    # 2. Update docs.html
    with open('docs.html', 'r', encoding='utf-8') as f:
        html = f.read()

    html_section = """
        <div class="card mb-4" id="maintenance-engine">
          <div class="card-header bg-success text-white d-flex align-items-center justify-content-between">
            <h5 class="mb-0">🌿 Botanical Maintenance Engine &amp; Ecological Care Guide</h5>
            <span class="badge bg-light text-dark">Conservation Science</span>
          </div>
          <div class="card-body">
            <p>Every native plant record features a scientifically grounded maintenance ranking (<code>Low</code>, <code>Medium</code>, or <code>High</code>) and a seasonal care guide formulated according to <strong>Xerces Society for Invertebrate Conservation</strong>, <strong>Grow Native! (Missouri Prairie Foundation)</strong>, and <strong>Missouri Botanical Garden PlantFinder</strong> guidelines.</p>
            <ul>
              <li><strong>Advisor Descriptions</strong>: Comprehensive botanical summaries synthesizing appearance, growth habit, living landscape matrix role, companion compatibility, and recommended garden settings, concluding with explicit multi-source attribution credits.</li>
              <li><strong>Spring 50°F+ Cutback Rule</strong>: Advises waiting until sustained 50°F+ temperatures so stem-nesting solitary bees can emerge, leaving 8–18 inches of standing stubble for current-season nesting cavities.</li>
              <li><strong>Summer Care &amp; Chelsea Chop</strong>: Pinpoints mid-season pruning opportunities (late May/early June) for taller asters, goldenrods, and sunflowers to prevent lodging and promote compact blooming.</li>
              <li><strong>Fall Seedhead Retention</strong>: Preserves dried seedheads throughout autumn and winter to feed American Goldfinches, juncos, and native songbirds while buffering crowns against freeze-thaw cycles.</li>
              <li><strong>Consultation Report Generation</strong>: Both the Word document (<code>.docx</code>) and the live consultation staging drawer automatically include maintenance levels and seasonal care summaries in client deliverables.</li>
              <li><strong>Sidebar Filter Accordion</strong>: Dynamic chips for Low, Medium, and High maintenance allow instant filtering across all 185 native species.</li>
            </ul>
          </div>
        </div>
"""

    if "id=\"maintenance-engine\"" not in html:
        insert_marker = "<!-- System Architecture -->"
        if insert_marker in html:
            html = html.replace(insert_marker, html_section + "\n        " + insert_marker, 1)
        else:
            # fallback insert before container close
            html = html.replace("</main>", html_section + "\n</main>", 1)
        with open('docs.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Updated docs.html with Botanical Maintenance Engine documentation.")
    else:
        print("docs.html already contains Maintenance Engine documentation.")

if __name__ == '__main__':
    update_docs()
