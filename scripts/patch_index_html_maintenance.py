#!/usr/bin/env python3
"""
scripts/patch_index_html_maintenance.py
Patches index.html to add:
1. Maintenance Level filter accordion in the sidebar.
2. Maintenance Level in plantDetailModal specs-grid and dedicated seasonal guide section.
3. Maintenance Level in editPlantModal and addPlantModal.
4. state.filters.maintenance Set and applyFilters logic.
5. getPlantMaintenanceLevel and getPlantMaintenanceGuide helpers.
6. Maintenance chip on plant cards.
7. Maintenance fields in staged plants and Word docx report generation.
"""

import re

def patch_index_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add Maintenance Level Accordion in sidebar right after Sociability
    sociability_accordion_end = """            <span class="chip-filter" data-group="sociability" data-val="Gregarious">Highly Social / Gregarious</span>
          </div>
        </div>"""

    maintenance_accordion = """            <span class="chip-filter" data-group="sociability" data-val="Gregarious">Highly Social / Gregarious</span>
          </div>
        </div>

        <!-- Maintenance Level -->
        <div class="accordion">
          <button class="accordion-header" data-target="maintenanceFilterContent" aria-expanded="true" aria-controls="maintenanceFilterContent">
            <span>Maintenance Level</span>
            <i data-lucide="chevron-down" style="width:14px;height:14px;"></i>
          </button>
          <div class="accordion-content" id="maintenanceFilterContent">
            <span class="chip-filter" data-group="maintenance" data-val="Low">Low Maintenance</span>
            <span class="chip-filter" data-group="maintenance" data-val="Medium">Medium Maintenance</span>
            <span class="chip-filter" data-group="maintenance" data-val="High">High Maintenance</span>
          </div>
        </div>"""

    if "data-target=\"maintenanceFilterContent\"" not in html:
        assert sociability_accordion_end in html, "Could not find sociability accordion end in index.html"
        html = html.replace(sociability_accordion_end, maintenance_accordion, 1)
        print("Added Maintenance Level accordion to sidebar.")
    else:
        print("Maintenance Level accordion already present.")

    # 2. Add Maintenance Level to specs-grid in plantDetailModal
    specs_target = """        <div class="spec-item">
          <span class="spec-label">Plant Type</span>
          <span class="spec-value" id="modalPlantType">-</span>
        </div>
      </div>"""

    specs_replacement = """        <div class="spec-item">
          <span class="spec-label">Plant Type</span>
          <span class="spec-value" id="modalPlantType">-</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">Maintenance Level</span>
          <span class="spec-value" id="modalMaintenanceLevel">-</span>
        </div>
      </div>"""

    if "id=\"modalMaintenanceLevel\"" not in html:
        assert specs_target in html, "Could not find specs-grid target in index.html"
        html = html.replace(specs_target, specs_replacement, 1)
        print("Added Maintenance Level to modal specs-grid.")
    else:
        print("modalMaintenanceLevel already present.")

    # 3. Add Seasonal Maintenance & Conservation Care section to plantDetailModal
    maint_container_target = """      <!-- Wildlife & Keystone Interactions -->
      <div style="background:var(--bg-base);padding:14px;border-radius:var(--radius-md);">
        <div style="font-size:11px;font-weight:800;text-transform:uppercase;color:var(--accent-keystone);margin-bottom:6px;">Wildlife & Ecological Value</div>
        <p id="modalWildlife" style="font-size:13px;line-height:1.5;color:var(--text-secondary);"></p>
      </div>"""

    maint_container_html = """      <!-- Wildlife & Keystone Interactions -->
      <div style="background:var(--bg-base);padding:14px;border-radius:var(--radius-md);">
        <div style="font-size:11px;font-weight:800;text-transform:uppercase;color:var(--accent-keystone);margin-bottom:6px;">Wildlife & Ecological Value</div>
        <p id="modalWildlife" style="font-size:13px;line-height:1.5;color:var(--text-secondary);"></p>
      </div>

      <!-- Seasonal Maintenance & Conservation Care -->
      <div id="modalMaintenanceContainer" style="background:var(--bg-base);padding:14px;border-radius:var(--radius-md);border-left:4px solid var(--accent-keystone);margin-top:12px;">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;flex-wrap:wrap;gap:6px;">
          <div style="font-size:11px;font-weight:800;text-transform:uppercase;color:var(--primary);display:flex;align-items:center;gap:6px;">
            <i data-lucide="wrench" style="width:14px;height:14px;"></i>
            <span>Maintenance &amp; Ecological Care Guide</span>
          </div>
          <span id="modalMaintenanceBadge" class="meta-chip" style="font-weight:700;font-size:11px;">Low Maintenance</span>
        </div>
        <p id="modalMaintenanceSummary" style="font-size:13px;line-height:1.5;color:var(--text-main);margin-bottom:10px;"></p>
        
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(220px, 1fr));gap:10px;margin-top:10px;">
          <div style="background:var(--bg-surface);padding:10px;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
            <strong style="font-size:12px;color:var(--primary);display:flex;align-items:center;gap:4px;margin-bottom:4px;">
              <i data-lucide="flower" style="width:12px;height:12px;"></i> Spring (50°F+ Cutback)
            </strong>
            <p id="modalMaintSpring" style="font-size:12px;line-height:1.4;color:var(--text-secondary);margin:0;"></p>
          </div>
          <div style="background:var(--bg-surface);padding:10px;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
            <strong style="font-size:12px;color:#d97706;display:flex;align-items:center;gap:4px;margin-bottom:4px;">
              <i data-lucide="sun" style="width:12px;height:12px;"></i> Summer Care
            </strong>
            <p id="modalMaintSummer" style="font-size:12px;line-height:1.4;color:var(--text-secondary);margin:0;"></p>
          </div>
          <div style="background:var(--bg-surface);padding:10px;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
            <strong style="font-size:12px;color:#b45309;display:flex;align-items:center;gap:4px;margin-bottom:4px;">
              <i data-lucide="leaf" style="width:12px;height:12px;"></i> Fall (Seedhead Retention)
            </strong>
            <p id="modalMaintFall" style="font-size:12px;line-height:1.4;color:var(--text-secondary);margin:0;"></p>
          </div>
          <div style="background:var(--bg-surface);padding:10px;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
            <strong style="font-size:12px;color:#2563eb;display:flex;align-items:center;gap:4px;margin-bottom:4px;">
              <i data-lucide="snowflake" style="width:12px;height:12px;"></i> Winter Protection
            </strong>
            <p id="modalMaintWinter" style="font-size:12px;line-height:1.4;color:var(--text-secondary);margin:0;"></p>
          </div>
        </div>

        <div style="background:var(--bg-surface);padding:10px;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);margin-top:10px;">
          <strong style="font-size:12px;color:var(--text-main);display:flex;align-items:center;gap:4px;margin-bottom:4px;">
            <i data-lucide="git-branch" style="width:12px;height:12px;"></i> Root Division &amp; Propagation
          </strong>
          <p id="modalMaintDivision" style="font-size:12px;line-height:1.4;color:var(--text-secondary);margin:0;"></p>
        </div>

        <div style="margin-top:10px;font-size:11px;color:var(--text-muted);display:flex;align-items:center;gap:4px;">
          <i data-lucide="shield-check" style="width:13px;height:13px;color:var(--primary);"></i>
          <span>Conservation Standards: <strong id="modalMaintSources">Xerces Society, Grow Native!, Missouri Botanical Garden</strong></span>
        </div>
      </div>"""

    if "id=\"modalMaintenanceContainer\"" not in html:
        assert maint_container_target in html, "Could not find Wildlife container in index.html"
        html = html.replace(maint_container_target, maint_container_html, 1)
        print("Added modalMaintenanceContainer to plantDetailModal.")
    else:
        print("modalMaintenanceContainer already present.")

    # 4. Add Maintenance Level in editPlantModal
    edit_target = """        <div class="form-group">
          <label for="editSociability">Plant Sociability</label>
          <input type="text" id="editSociability">
        </div>
      </div>"""

    edit_replacement = """        <div class="form-group">
          <label for="editSociability">Plant Sociability</label>
          <input type="text" id="editSociability">
        </div>
      </div>
      <div class="form-group">
        <label for="editMaintenanceLevel">Maintenance Level</label>
        <select id="editMaintenanceLevel" style="width:100%;padding:8px;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);background:var(--bg-surface);color:var(--text-main);">
          <option value="Low">Low Maintenance</option>
          <option value="Medium">Medium Maintenance</option>
          <option value="High">High Maintenance</option>
        </select>
      </div>"""

    if "id=\"editMaintenanceLevel\"" not in html:
        assert edit_target in html, "Could not find editSociability target in index.html"
        html = html.replace(edit_target, edit_replacement, 1)
        print("Added editMaintenanceLevel to editPlantModal.")
    else:
        print("editMaintenanceLevel already present.")

    # 5. Add Maintenance Level in addPlantModal
    add_target = """      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
        <div class="form-group">
          <label for="addSociability">Plant Sociability</label>
          <select id="addSociability" class="sort-select" style="width:100%;">
            <option value="Moderately Social">Moderately Social</option>
            <option value="Highly Social / Gregarious">Highly Social / Gregarious</option>
            <option value="Less Social / Solitary">Less Social / Solitary</option>
          </select>
        </div>
        <div class="form-group">
          <label for="addWildlife">Wildlife Benefits</label>
          <input type="text" id="addWildlife" placeholder="e.g. Pollinator Magnet, Songbird Seeds">
        </div>
      </div>"""

    add_replacement = """      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;">
        <div class="form-group">
          <label for="addSociability">Plant Sociability</label>
          <select id="addSociability" class="sort-select" style="width:100%;">
            <option value="Moderately Social">Moderately Social</option>
            <option value="Highly Social / Gregarious">Highly Social / Gregarious</option>
            <option value="Less Social / Solitary">Less Social / Solitary</option>
          </select>
        </div>
        <div class="form-group">
          <label for="addMaintenanceLevel">Maintenance Level</label>
          <select id="addMaintenanceLevel" class="sort-select" style="width:100%;">
            <option value="Low">Low Maintenance</option>
            <option value="Medium">Medium Maintenance</option>
            <option value="High">High Maintenance</option>
          </select>
        </div>
        <div class="form-group">
          <label for="addWildlife">Wildlife Benefits</label>
          <input type="text" id="addWildlife" placeholder="e.g. Pollinator Magnet, Songbird Seeds">
        </div>
      </div>"""

    if "id=\"addMaintenanceLevel\"" not in html:
        assert add_target in html, "Could not find addSociability target in index.html"
        html = html.replace(add_target, add_replacement, 1)
        print("Added addMaintenanceLevel to addPlantModal.")
    else:
        print("addMaintenanceLevel already present.")

    # 6. Update state.filters in JS
    filters_target = """        bloomColor: new Set(),
        sociability: new Set(),
      },"""

    filters_replacement = """        bloomColor: new Set(),
        sociability: new Set(),
        maintenance: new Set(),
      },"""

    if "maintenance: new Set()," not in html:
        assert filters_target in html, "Could not find filters object target in index.html"
        html = html.replace(filters_target, filters_replacement, 1)
        print("Added maintenance: new Set() to state.filters.")
    else:
        print("maintenance: new Set() already in state.filters.")

    # 7. Add getPlantMaintenanceLevel and getPlantMaintenanceGuide helpers
    helper_target = """    function getPlantSociability(p) {
      return p.sociability || p.plant_sociability || 'Medium / Moderate Spreading';
    }"""

    helper_replacement = """    function getPlantSociability(p) {
      return p.sociability || p.plant_sociability || 'Medium / Moderate Spreading';
    }

    function getPlantMaintenanceLevel(p) {
      return p.maintenance_level || p.maintenanceLevel || 'Low';
    }

    function getPlantMaintenanceGuide(p) {
      if (p.maintenance_guide && typeof p.maintenance_guide === 'object') return p.maintenance_guide;
      return {
        summary: "Low-maintenance native requiring minimal care once established. Benefits from leaving standing stems over winter for cavity-nesting bees and songbirds.",
        level: p.maintenance_level || 'Low',
        spring: "Wait until daytime temperatures consistently exceed 50°F before cutting back dead foliage. Leave 8 to 18 inches of standing stems to provide nesting cavities for native solitary bees.",
        summer: "Minimal irrigation needed once established. Inspect periodically for invasive weed encroachment; no routine supplemental fertilizer required.",
        fall: "Leave seedheads and architectural dried foliage standing throughout autumn to supply vital winter seeds for native songbirds and protect the crown.",
        winter: "Preserve snow cover and natural leaf litter mulch around root zones to protect dormant crowns and overwintering beneficial insects.",
        division: "Rarely requires division; if desired, divide mature clumps in early spring just as new growth emerges.",
        sources: "Xerces Society for Invertebrate Conservation, Grow Native! (Missouri Prairie Foundation), Missouri Botanical Garden"
      };
    }"""

    if "function getPlantMaintenanceLevel" not in html:
        assert helper_target in html, "Could not find getPlantSociability target in index.html"
        html = html.replace(helper_target, helper_replacement, 1)
        print("Added getPlantMaintenanceLevel and getPlantMaintenanceGuide helpers.")
    else:
        print("getPlantMaintenanceLevel already present.")

    # 8. Add Maintenance filter to applyFilters()
    apply_filters_target = """        // Sociability
        if (f.sociability.size > 0) {
          const soc = getPlantSociability(p).toLowerCase();
          const matches = Array.from(f.sociability).some(s => soc.includes(s.toLowerCase()));
          if (!matches) return false;
        }

        return true;"""

    apply_filters_replacement = """        // Sociability
        if (f.sociability.size > 0) {
          const soc = getPlantSociability(p).toLowerCase();
          const matches = Array.from(f.sociability).some(s => soc.includes(s.toLowerCase()));
          if (!matches) return false;
        }

        // Maintenance Level
        if (f.maintenance && f.maintenance.size > 0) {
          const maint = getPlantMaintenanceLevel(p).toLowerCase();
          const matches = Array.from(f.maintenance).some(m => maint.includes(m.toLowerCase()));
          if (!matches) return false;
        }

        return true;"""

    if "if (f.maintenance && f.maintenance.size > 0)" not in html:
        assert apply_filters_target in html, "Could not find applyFilters sociability target in index.html"
        html = html.replace(apply_filters_target, apply_filters_replacement, 1)
        print("Added maintenance filter to applyFilters().")
    else:
        print("maintenance filter already present in applyFilters().")

    # 9. Add 'maintenance' to groups in renderActiveFilterTags() and resetAllFilters()
    groups_str = "const groups = ['habitat', 'light', 'moisture', 'height', 'type', 'layer', 'season', 'bloomColor', 'sociability'];"
    groups_replacement = "const groups = ['habitat', 'light', 'moisture', 'height', 'type', 'layer', 'season', 'bloomColor', 'sociability', 'maintenance'];"

    if groups_str in html:
        html = html.replace(groups_str, groups_replacement)
        print("Updated groups array in renderActiveFilterTags() and resetAllFilters().")
    else:
        print("groups array already updated.")

    # 10. Update createPlantCard with maintenance pill
    card_chips_target = """            <div class="card-chips">
              <span class="meta-chip"><i data-lucide="sun" style="width:12px;height:12px;"></i> ${sunStr}</span>
              <span class="meta-chip"><i data-lucide="droplet" style="width:12px;height:12px;"></i> ${moistStr}</span>
              <span class="meta-chip"><i data-lucide="ruler" style="width:12px;height:12px;"></i> ${heightStr}</span>
              ${bloomPillHtml}
            </div>"""

    card_chips_replacement = """            <div class="card-chips">
              <span class="meta-chip"><i data-lucide="sun" style="width:12px;height:12px;"></i> ${sunStr}</span>
              <span class="meta-chip"><i data-lucide="droplet" style="width:12px;height:12px;"></i> ${moistStr}</span>
              <span class="meta-chip"><i data-lucide="ruler" style="width:12px;height:12px;"></i> ${heightStr}</span>
              ${maintPillHtml}
              ${bloomPillHtml}
            </div>"""

    card_prep_target = """      const heightStr = getPlantHeight(plant);
      const layerStr = getPlantLayer(plant);
      const descStr = getPlantDesc(plant);"""

    card_prep_replacement = """      const heightStr = getPlantHeight(plant);
      const layerStr = getPlantLayer(plant);
      const descStr = getPlantDesc(plant);
      const maintLevel = getPlantMaintenanceLevel(plant);
      const maintColor = maintLevel === 'Low' ? '#10b981' : (maintLevel === 'Medium' ? '#f59e0b' : '#ef4444');
      const maintPillHtml = `<span class="meta-chip" style="border-left:2.5px solid ${maintColor};"><i data-lucide="wrench" style="width:11px;height:11px;color:${maintColor};"></i> <span>${maintLevel} Maint</span></span>`;"""

    if "const maintPillHtml" not in html:
        assert card_prep_target in html, "Could not find card_prep_target in index.html"
        assert card_chips_target in html, "Could not find card_chips_target in index.html"
        html = html.replace(card_prep_target, card_prep_replacement, 1)
        html = html.replace(card_chips_target, card_chips_replacement, 1)
        print("Added maintenance pill to createPlantCard().")
    else:
        print("createPlantCard already has maintenance pill.")

    # 11. Populate maintenance fields in openPlantDetail()
    modal_pop_target = """      document.getElementById('modalSociability').textContent = getPlantSociability(plant);
      document.getElementById('modalHabitat').textContent = plant.native_environment || '-';
      document.getElementById('modalPlantType').textContent = Array.isArray(plant.plant_type) ? plant.plant_type.join(', ') : (plant.plant_type || '-');

      document.getElementById('modalWildlife').textContent = (plant.wildlife_ecosystem_benefits || plant.wildlife_benefits || []).join(' · ') || 'Provides nectar, pollen, and shelter for native pollinators and wildlife.';"""

    modal_pop_replacement = """      document.getElementById('modalSociability').textContent = getPlantSociability(plant);
      document.getElementById('modalHabitat').textContent = plant.native_environment || '-';
      document.getElementById('modalPlantType').textContent = Array.isArray(plant.plant_type) ? plant.plant_type.join(', ') : (plant.plant_type || '-');

      const maintLvl = getPlantMaintenanceLevel(plant);
      const maintGuide = getPlantMaintenanceGuide(plant);
      const maintCol = maintLvl === 'Low' ? '#10b981' : (maintLvl === 'Medium' ? '#f59e0b' : '#ef4444');

      const modalMaintLevel = document.getElementById('modalMaintenanceLevel');
      if (modalMaintLevel) modalMaintLevel.textContent = maintLvl + ' Maintenance';

      const modalMaintBadge = document.getElementById('modalMaintenanceBadge');
      if (modalMaintBadge) {
        modalMaintBadge.textContent = maintLvl + ' Maintenance';
        modalMaintBadge.style.borderLeft = `3px solid ${maintCol}`;
        modalMaintBadge.style.color = maintCol;
      }

      const modalMaintSummary = document.getElementById('modalMaintenanceSummary');
      if (modalMaintSummary) modalMaintSummary.textContent = maintGuide.summary || '';

      const modalMaintSpring = document.getElementById('modalMaintSpring');
      if (modalMaintSpring) modalMaintSpring.textContent = maintGuide.spring || '';

      const modalMaintSummer = document.getElementById('modalMaintSummer');
      if (modalMaintSummer) modalMaintSummer.textContent = maintGuide.summer || '';

      const modalMaintFall = document.getElementById('modalMaintFall');
      if (modalMaintFall) modalMaintFall.textContent = maintGuide.fall || '';

      const modalMaintWinter = document.getElementById('modalMaintWinter');
      if (modalMaintWinter) modalMaintWinter.textContent = maintGuide.winter || '';

      const modalMaintDivision = document.getElementById('modalMaintDivision');
      if (modalMaintDivision) modalMaintDivision.textContent = maintGuide.division || '';

      const modalMaintSources = document.getElementById('modalMaintSources');
      if (modalMaintSources) modalMaintSources.textContent = maintGuide.sources || 'Xerces Society, Grow Native!, Missouri Botanical Garden';

      document.getElementById('modalWildlife').textContent = (plant.wildlife_ecosystem_benefits || plant.wildlife_benefits || []).join(' · ') || 'Provides nectar, pollen, and shelter for native pollinators and wildlife.';"""

    if "modalMaintSpring.textContent" not in html:
        assert modal_pop_target in html, "Could not find modal_pop_target in index.html"
        html = html.replace(modal_pop_target, modal_pop_replacement, 1)
        print("Updated openPlantDetail() to populate maintenance guide fields.")
    else:
        print("openPlantDetail() already populates maintenance guide fields.")

    # 12. Update openEditModal() and editPlantForm submit
    edit_modal_prep_target = """      document.getElementById('editHeight').value = getPlantHeight(plant);
      document.getElementById('editSociability').value = getPlantSociability(plant);"""

    edit_modal_prep_replacement = """      document.getElementById('editHeight').value = getPlantHeight(plant);
      document.getElementById('editSociability').value = getPlantSociability(plant);
      const editMaint = document.getElementById('editMaintenanceLevel');
      if (editMaint) editMaint.value = getPlantMaintenanceLevel(plant);"""

    if "editMaint.value = getPlantMaintenanceLevel(plant)" not in html:
        assert edit_modal_prep_target in html, "Could not find edit_modal_prep_target in index.html"
        html = html.replace(edit_modal_prep_target, edit_modal_prep_replacement, 1)
        print("Updated openEditModal() to set editMaintenanceLevel.")
    else:
        print("openEditModal() already sets editMaintenanceLevel.")

    edit_submit_target = """          height_display: document.getElementById('editHeight').value.trim(),
          sociability: document.getElementById('editSociability').value,"""

    edit_submit_replacement = """          height_display: document.getElementById('editHeight').value.trim(),
          sociability: document.getElementById('editSociability').value,
          maintenance_level: document.getElementById('editMaintenanceLevel')?.value || 'Low',"""

    if "maintenance_level: document.getElementById('editMaintenanceLevel')" not in html:
        assert edit_submit_target in html, "Could not find edit_submit_target in index.html"
        html = html.replace(edit_submit_target, edit_submit_replacement, 1)
        print("Updated editPlantForm submit to save maintenance_level.")
    else:
        print("editPlantForm submit already saves maintenance_level.")

    # 13. Update addPlantForm submit
    add_submit_target = """      const sociability = document.getElementById('addSociability').value;
      const wildlife = document.getElementById('addWildlife').value.split(',').map(s => s.trim()).filter(Boolean);"""

    add_submit_replacement = """      const sociability = document.getElementById('addSociability').value;
      const maintLevel = document.getElementById('addMaintenanceLevel')?.value || 'Low';
      const wildlife = document.getElementById('addWildlife').value.split(',').map(s => s.trim()).filter(Boolean);"""

    if "const maintLevel = document.getElementById('addMaintenanceLevel')" not in html:
        assert add_submit_target in html, "Could not find add_submit_target in index.html"
        html = html.replace(add_submit_target, add_submit_replacement, 1)
        print("Updated addPlantForm submit to extract maintLevel.")
    else:
        print("addPlantForm submit already extracts maintLevel.")

    add_plant_obj_target = """        sociability: sociability,
        wildlife_ecosystem_benefits: wildlife.length > 0 ? wildlife : ['Provides nectar and shelter for native wildlife.'],"""

    add_plant_obj_replacement = """        sociability: sociability,
        maintenance_level: maintLevel,
        maintenance_guide: {
          summary: `${maintLevel} Maintenance native species.`,
          level: maintLevel,
          spring: 'Wait until daytime temperatures consistently exceed 50°F before cutting back dead foliage. Leave 8 to 18 inches of standing stems for native bee nesting.',
          summer: 'Minimal irrigation required once established; monitor moisture during dry spells.',
          fall: 'Leave standing stems and seedheads for overwintering birds and beneficial insects.',
          winter: 'Preserve snow cover and natural leaf mulch around root zones.',
          division: 'Divide in early spring if needed.',
          sources: 'Xerces Society for Invertebrate Conservation, Grow Native! (Missouri Prairie Foundation), Missouri Botanical Garden'
        },
        wildlife_ecosystem_benefits: wildlife.length > 0 ? wildlife : ['Provides nectar and shelter for native wildlife.'],"""

    if "maintenance_level: maintLevel," not in html:
        assert add_plant_obj_target in html, "Could not find add_plant_obj_target in index.html"
        html = html.replace(add_plant_obj_target, add_plant_obj_replacement, 1)
        print("Updated addPlantForm newPlant object with maintenance fields.")
    else:
        print("addPlantForm already sets maintenance fields.")

    # 14. Update toggleStagedPlant()
    toggle_staged_target = """          layer: getPlantLayer(plant),
          sociability: getPlantSociability(plant),
          environment: plant.native_environment || '',
          target_area: defaultArea"""

    toggle_staged_replacement = """          layer: getPlantLayer(plant),
          sociability: getPlantSociability(plant),
          maintenance_level: getPlantMaintenanceLevel(plant),
          maintenance_guide: getPlantMaintenanceGuide(plant),
          environment: plant.native_environment || '',
          target_area: defaultArea"""

    if "maintenance_level: getPlantMaintenanceLevel(plant)" not in html:
        assert toggle_staged_target in html, "Could not find toggle_staged_target in index.html"
        html = html.replace(toggle_staged_target, toggle_staged_replacement, 1)
        print("Updated toggleStagedPlant() to store maintenance_level and maintenance_guide.")
    else:
        print("toggleStagedPlant() already stores maintenance fields.")

    # 15. Update downloadDocxReport() to inject maintenance recommendations
    docx_target = """                // Botanical bullet point 2: Bloom, Sun & Moisture
                const bloomColors = (master && (master.bloom_color || master.bloomColor)) || [];
                const bloomSeasons = (master && (master.bloom_period || master.bloom_season || master.bloomSeason)) || [];
                let bloomInfo = 'Seasonal interest';
                if (bloomColors.length > 0 || bloomSeasons.length > 0) {
                  bloomInfo = [bloomColors.join(', '), bloomSeasons.length ? `(${bloomSeasons.join(', ')})` : ''].filter(Boolean).join(' ');
                }
                const sunVal = staged.sun || (master && (master.light_requirements || []).join(', ')) || 'Sun to Part Sun';
                const moistVal = staged.moisture || (master && (master.moisture_requirements || []).join(', ')) || 'Average';

                plantBlocks += `
<w:p>
    <w:pPr>
        <w:ind w:left="720" w:hanging="360"/>
        <w:spacing w:after="60"/>
    </w:pPr>
    <w:r><w:t>• </w:t></w:r>
    <w:r><w:rPr><w:b/></w:rPr><w:t>Bloom: </w:t></w:r>
    <w:r><w:t>${escapeXml(bloomInfo)} | </w:t></w:r>
    <w:r><w:rPr><w:b/></w:rPr><w:t>Sun/Moisture: </w:t></w:r>
    <w:r><w:t>${escapeXml(sunVal)} / ${escapeXml(moistVal)}</w:t></w:r>
</w:p>`;"""

    docx_replacement = """                // Botanical bullet point 2: Bloom, Sun & Moisture
                const bloomColors = (master && (master.bloom_color || master.bloomColor)) || [];
                const bloomSeasons = (master && (master.bloom_period || master.bloom_season || master.bloomSeason)) || [];
                let bloomInfo = 'Seasonal interest';
                if (bloomColors.length > 0 || bloomSeasons.length > 0) {
                  bloomInfo = [bloomColors.join(', '), bloomSeasons.length ? `(${bloomSeasons.join(', ')})` : ''].filter(Boolean).join(' ');
                }
                const sunVal = staged.sun || (master && (master.light_requirements || []).join(', ')) || 'Sun to Part Sun';
                const moistVal = staged.moisture || (master && (master.moisture_requirements || []).join(', ')) || 'Average';

                plantBlocks += `
<w:p>
    <w:pPr>
        <w:ind w:left="720" w:hanging="360"/>
        <w:spacing w:after="60"/>
    </w:pPr>
    <w:r><w:t>• </w:t></w:r>
    <w:r><w:rPr><w:b/></w:rPr><w:t>Bloom: </w:t></w:r>
    <w:r><w:t>${escapeXml(bloomInfo)} | </w:t></w:r>
    <w:r><w:rPr><w:b/></w:rPr><w:t>Sun/Moisture: </w:t></w:r>
    <w:r><w:t>${escapeXml(sunVal)} / ${escapeXml(moistVal)}</w:t></w:r>
</w:p>`;

                // Botanical bullet point 3: Maintenance Level & Ecological Care Timings
                const reportMaintLvl = staged.maintenance_level || (master && (master.maintenance_level || master.maintenanceLevel)) || 'Low';
                const reportMaintGuide = staged.maintenance_guide || (master && master.maintenance_guide) || {};
                let reportMaintSummary = '';
                if (reportMaintGuide && typeof reportMaintGuide === 'object' && reportMaintGuide.summary) {
                  reportMaintSummary = `${reportMaintGuide.summary} Spring (50°F+ cutback): ${reportMaintGuide.spring || ''} | Fall: ${reportMaintGuide.fall || ''}`;
                } else {
                  reportMaintSummary = 'Spring cutback at sustained 50°F+ to protect stem-nesting bees; leave 8–18 in stems and retain seedheads for songbirds.';
                }

                plantBlocks += `
<w:p>
    <w:pPr>
        <w:ind w:left="720" w:hanging="360"/>
        <w:spacing w:after="60"/>
    </w:pPr>
    <w:r><w:t>• </w:t></w:r>
    <w:r><w:rPr><w:b/><w:color w:val="2D5A27"/></w:rPr><w:t>Maintenance (${escapeXml(reportMaintLvl)}): </w:t></w:r>
    <w:r><w:t>${escapeXml(reportMaintSummary)}</w:t></w:r>
</w:p>`;"""

    if "Botanical bullet point 3: Maintenance Level" not in html:
        assert docx_target in html, "Could not find docx_target in index.html"
        html = html.replace(docx_target, docx_replacement, 1)
        print("Updated downloadDocxReport() to include maintenance recommendations.")
    else:
        print("downloadDocxReport() already includes maintenance recommendations.")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("\nSuccessfully patched index.html with all Maintenance Level and Care Guide features!")

if __name__ == '__main__':
    patch_index_html()
