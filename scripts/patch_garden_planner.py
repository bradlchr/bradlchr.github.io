#!/usr/bin/env python3
"""
Patch index.html to add the Garden Area Planner & Recommendation Suite:
- Accessible to all authenticated users (Advisors, Senior Advisors, Program Managers, Admins)
- Protected from Guest users via friendly Advisor Access Gateway dialog
- Multi-zone garden setup: Soil type/moisture, sunlight, bloom color preference, maintenance level, and structural layers
- Ecological recommendation engine scoring and categorization by structural layers
- Full consultation staging review and 1-click add to consultation report
"""

import sys
import re

INDEX_PATH = 'index.html'

def patch_index_html():
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. CSS STYLES
    css_target = '/* Toasts */'
    if '.btn-planner' not in content:
        planner_css = '''    /* Garden Area Planner & Recommendation Suite Styles */
    .btn-planner {
      background: var(--primary-light);
      color: var(--primary-dark);
      border: 1px solid var(--primary-border);
      font-weight: 700;
      gap: 6px;
      transition: all 0.15s ease;
    }
    .btn-planner:hover {
      background: var(--primary);
      color: #ffffff;
      border-color: var(--primary);
      box-shadow: 0 2px 8px rgba(35, 92, 54, 0.25);
    }
    .btn-planner:active {
      transform: translateY(1px);
    }
    [data-theme="dark"] .btn-planner {
      background: rgba(35, 92, 54, 0.25);
      color: #a7f3d0;
      border-color: rgba(52, 211, 153, 0.35);
    }
    [data-theme="dark"] .btn-planner:hover {
      background: var(--primary);
      color: #ffffff;
    }

    .planner-chips-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
    }
    .planner-chip {
      padding: 7px 9px;
      font-size: 11px;
      font-weight: 600;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-subtle);
      background: var(--bg-base);
      color: var(--text-secondary);
      cursor: pointer;
      text-align: left;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 5px;
      user-select: none;
    }
    .planner-chip:hover {
      border-color: var(--primary-border);
      color: var(--primary);
      background: var(--bg-surface-elevated);
    }
    .planner-chip.active {
      background: var(--primary-light);
      border-color: var(--primary);
      color: var(--primary-dark);
      font-weight: 800;
      box-shadow: 0 1px 4px rgba(35, 92, 54, 0.15);
    }
    [data-theme="dark"] .planner-chip.active {
      background: rgba(35, 92, 54, 0.3);
      color: #6ee7b7;
      border-color: #059669;
    }

    .planner-color-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
    }
    .planner-color-chip {
      padding: 4px 9px;
      font-size: 11px;
      font-weight: 600;
      border-radius: 20px;
      border: 1px solid var(--border-subtle);
      background: var(--bg-base);
      color: var(--text-secondary);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.15s ease;
      user-select: none;
    }
    .planner-color-chip:hover {
      border-color: var(--primary-border);
      color: var(--text-main);
    }
    .planner-color-chip.active {
      background: var(--primary-light);
      border-color: var(--primary);
      color: var(--primary-dark);
      font-weight: 800;
    }
    [data-theme="dark"] .planner-color-chip.active {
      background: rgba(35, 92, 54, 0.3);
      color: #6ee7b7;
      border-color: #059669;
    }
    .color-dot {
      width: 9px;
      height: 9px;
      border-radius: 50%;
      display: inline-block;
      flex-shrink: 0;
    }

    .planner-checkbox-label {
      display: flex;
      align-items: flex-start;
      gap: 8px;
      font-size: 11.5px;
      color: var(--text-secondary);
      cursor: pointer;
      margin-bottom: 6px;
      line-height: 1.35;
      user-select: none;
      padding: 4px 6px;
      border-radius: var(--radius-sm);
      transition: background 0.12s ease;
    }
    .planner-checkbox-label:hover {
      background: var(--bg-surface-elevated);
      color: var(--text-main);
    }
    .planner-checkbox-label input {
      margin-top: 2px;
      accent-color: var(--primary);
      cursor: pointer;
    }

    .planner-area-card {
      padding: 8px 10px;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-subtle);
      background: var(--bg-base);
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      user-select: none;
    }
    .planner-area-card:hover {
      border-color: var(--primary-border);
      background: var(--bg-surface-elevated);
    }
    .planner-area-card.active {
      background: var(--primary-light);
      border-color: var(--primary);
      box-shadow: 0 2px 8px rgba(35, 92, 54, 0.12);
    }
    [data-theme="dark"] .planner-area-card.active {
      background: rgba(35, 92, 54, 0.25);
      border-color: #059669;
    }

    .planner-layer-box {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      overflow: hidden;
      margin-bottom: 16px;
    }
    .planner-layer-header {
      padding: 10px 14px;
      background: var(--bg-surface-elevated);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
    }
    .planner-layer-cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 12px;
      padding: 14px;
    }
    .planner-plant-card {
      background: var(--bg-base);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 10px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 8px;
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    .planner-plant-card:hover {
      border-color: var(--primary-border);
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
    }
    .planner-plant-card.is-staged {
      border-color: var(--primary);
      background: var(--primary-light);
    }
    [data-theme="dark"] .planner-plant-card.is-staged {
      background: rgba(35, 92, 54, 0.2);
      border-color: #059669;
    }

    @media (max-width: 900px) {
      .planner-layout {
        grid-template-columns: 1fr !important;
        display: flex !important;
        flex-direction: column !important;
        overflow-y: auto !important;
      }
      .planner-sidebar {
        border-right: none !important;
        border-bottom: 1px solid var(--border-subtle) !important;
        max-height: 48vh;
      }
    }

'''
        content = content.replace(css_target, planner_css + css_target, 1)
        print("✓ Injected Garden Planner CSS")

    # 2. HEADER BUTTON
    header_target = '<button id="reportDrawerBtn"'
    if 'id="gardenPlannerHeaderBtn"' not in content:
        header_btn_html = '''      <!-- Garden Area Planner & Recommendation Suite Trigger (All users except guest) -->
      <button id="gardenPlannerHeaderBtn" class="btn btn-planner" aria-label="Garden Area Planner & Ecological Plant Recommendations" title="Garden Area Planner & Plant Recommendations">
        <i data-lucide="layout-grid"></i>
        <span class="btn-text-long">Garden Planner</span>
        <span class="btn-text-short">Planner</span>
      </button>

      '''
        content = content.replace(header_target, header_btn_html + header_target, 1)
        print("✓ Injected Garden Planner Header Button")

    # 3. STAGING DRAWER BUTTON
    staging_target = '<button type="button" id="addGardenAreaBtn"'
    if 'id="openPlannerFromStagingBtn"' not in content:
        staging_btn_html = '''<button type="button" id="openPlannerFromStagingBtn" class="btn-text-action" style="font-size:11px;font-weight:700;color:var(--primary);display:inline-flex;align-items:center;gap:3px;margin-right:6px;" title="Open Garden Area Planner and get plant recommendations for this property">
            <i data-lucide="sparkles" style="width:12px;height:12px;"></i>
            <span>Recommend Plants</span>
          </button>
          '''
        content = content.replace(staging_target, staging_btn_html + staging_target, 1)
        print("✓ Injected Garden Planner Staging Drawer Button")

    # 4. ADVISOR PROFILE MODAL TILE
    profile_tile_target = '<button id="profileOpenSyncBtn"'
    if 'id="profileOpenPlannerBtn"' not in content:
        profile_tile_html = '''<button id="profileOpenPlannerBtn" type="button" class="profile-tile-btn">
          <div class="profile-tile-icon" style="background:rgba(16, 185, 129, 0.1);color:#059669;">
            <i data-lucide="layout-grid" style="width:18px;height:18px;"></i>
          </div>
          <div class="profile-tile-content">
            <div class="profile-tile-title">
              <span>Garden Planner</span>
            </div>
            <div class="profile-tile-desc">Area recommendations</div>
          </div>
        </button>

        '''
        content = content.replace(profile_tile_target, profile_tile_html + profile_tile_target, 1)
        print("✓ Injected Garden Planner Profile Tile")

    # 5. DIALOGS MARKUP (Guest Gateway & Full Planner Modal)
    dialog_target = '<!-- Change / Set Strong Password Dialog -->'
    if 'id="gardenPlannerModal"' not in content:
        dialogs_html = '''  <!-- Garden Planner Guest Access Gate Dialog -->
  <dialog id="plannerGuestModal" aria-modal="true" aria-labelledby="plannerGuestTitle" style="max-width:500px;width:92%;border-radius:var(--radius-lg);padding:0;overflow:hidden;border:1px solid var(--border-subtle);box-shadow:0 24px 48px rgba(0,0,0,0.35);background:var(--bg-surface);">
    <div style="background:linear-gradient(135deg, rgba(27,67,50,0.96), rgba(13,40,24,0.98));padding:26px 22px;color:#fff;text-align:center;position:relative;">
      <button onclick="document.getElementById('plannerGuestModal').close()" class="btn-icon" aria-label="Close dialog" style="position:absolute;top:12px;right:12px;color:rgba(255,255,255,0.75);background:transparent;border:none;cursor:pointer;padding:4px;">
        <i data-lucide="x" style="width:18px;height:18px;"></i>
      </button>
      <div style="width:52px;height:52px;border-radius:50%;background:rgba(255,255,255,0.12);display:flex;align-items:center;justify-content:center;margin:0 auto 12px auto;border:1px solid rgba(255,255,255,0.2);">
        <i data-lucide="layout-grid" style="width:26px;height:26px;color:#6ee7b7;"></i>
      </div>
      <h3 id="plannerGuestTitle" style="font-size:18px;font-weight:800;margin:0 0 6px 0;letter-spacing:-0.02em;">Nature Advisor Access Required</h3>
      <p style="font-size:12.5px;color:#d1fae5;margin:0;line-height:1.45;">
        Garden Area Planning &amp; Ecological Recommendation Suite
      </p>
    </div>
    <div style="padding:22px 24px;color:var(--text-main);">
      <p style="font-size:13.5px;color:var(--text-secondary);line-height:1.55;margin:0 0 16px 0;">
        The <strong>Garden Area Planner</strong> enables Deep Roots Nature Advisors to configure multi-zone residential and commercial planting areas. Based on each zone's specific sunlight, soil moisture, maintenance goals, and structural matrix layers, it automatically calculates and recommends optimal native plant communities.
      </p>
      <div style="background:var(--bg-base);border:1px solid var(--border-subtle);border-radius:var(--radius-md);padding:12px 14px;margin-bottom:20px;display:flex;align-items:flex-start;gap:10px;font-size:12px;color:var(--text-muted);">
        <i data-lucide="lock" style="width:16px;height:16px;color:var(--accent-gold);flex-shrink:0;margin-top:2px;"></i>
        <span>Please sign in with your Nature Advisor account to access this feature and stage plant recommendations into client reports.</span>
      </div>
      <div style="display:flex;gap:10px;justify-content:flex-end;flex-wrap:wrap;">
        <button type="button" onclick="document.getElementById('plannerGuestModal').close()" class="btn btn-secondary" style="font-size:13px;">
          Browse Public Catalog
        </button>
        <button type="button" id="guestGateSignInBtn" class="btn btn-primary" style="font-size:13px;font-weight:700;">
          <i data-lucide="user-check"></i>
          <span>Advisor Sign In</span>
        </button>
      </div>
    </div>
  </dialog>

  <!-- Garden Area Planner & Recommendation Suite Modal -->
  <dialog id="gardenPlannerModal" aria-modal="true" aria-labelledby="gardenPlannerTitle" style="max-width:1280px;width:96%;height:92vh;max-height:920px;border-radius:var(--radius-lg);padding:0;overflow:hidden;border:1px solid var(--border-subtle);box-shadow:0 25px 60px rgba(0,0,0,0.35);background:var(--bg-surface);">
    <div style="display:flex;flex-direction:column;height:100%;min-height:0;">
      <!-- Modal Header -->
      <div class="dialog-header" style="padding:14px 20px;border-bottom:1px solid var(--border-subtle);background:var(--bg-frosted);backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:space-between;gap:12px;flex-shrink:0;">
        <div style="display:flex;align-items:center;gap:10px;min-width:0;">
          <div style="width:36px;height:36px;border-radius:var(--radius-md);background:var(--primary-light);border:1px solid var(--primary-border);display:flex;align-items:center;justify-content:center;color:var(--primary);flex-shrink:0;">
            <i data-lucide="layout-grid" style="width:20px;height:20px;"></i>
          </div>
          <div style="min-width:0;">
            <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
              <h3 id="gardenPlannerTitle" style="font-size:16px;font-weight:800;margin:0;color:var(--text-main);letter-spacing:-0.02em;">
                Garden Area Planner &amp; Ecological Recommendation Suite
              </h3>
              <span id="plannerConsultationBadge" class="badge" style="background:var(--primary-light);color:var(--primary);border:1px solid var(--primary-border);font-size:11px;font-weight:700;">
                <i data-lucide="folder-kanban" style="width:11px;height:11px;vertical-align:-1px;"></i>
                <span id="plannerActiveConsultationName">Active Consultation</span>
              </span>
            </div>
            <p style="font-size:11.5px;color:var(--text-muted);margin:2px 0 0 0;line-height:1.3;">
              Define property planting zones by sun, soil, bloom preferences, and structural layers to generate ecological native plant selections.
            </p>
          </div>
        </div>
        <div style="display:flex;align-items:center;gap:8px;flex-shrink:0;">
          <button type="button" id="plannerOpenDrawerBtn" class="btn btn-secondary btn-sm" title="View Staged Consultation Report" style="font-size:12px;gap:5px;">
            <i data-lucide="clipboard-list" style="width:14px;height:14px;"></i>
            <span>Staging (<span id="plannerStagedCountBadge">0</span>)</span>
          </button>
          <button type="button" onclick="document.getElementById('gardenPlannerModal').close()" class="btn-icon" aria-label="Close Garden Planner">
            <i data-lucide="x"></i>
          </button>
        </div>
      </div>

      <!-- Modal Body (Two-Column Layout) -->
      <div class="planner-layout" style="display:grid;grid-template-columns:360px 1fr;flex:1;min-height:0;overflow:hidden;background:var(--bg-base);">
        
        <!-- Left Column: Garden Areas Selector & Active Area Conditions -->
        <div class="planner-sidebar" style="border-right:1px solid var(--border-subtle);background:var(--bg-surface);overflow-y:auto;display:flex;flex-direction:column;gap:16px;padding:16px;">
          
          <!-- Area Selector Section -->
          <div>
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
              <span style="font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;color:var(--text-muted);">
                Garden Areas (<span id="plannerAreasCount">3</span>)
              </span>
              <button type="button" id="plannerAddAreaBtn" class="btn-text-action" style="font-size:11.5px;font-weight:700;color:var(--primary);display:inline-flex;align-items:center;gap:3px;" title="Add new planting area">
                <i data-lucide="plus" style="width:12px;height:12px;"></i>
                <span>+ Add Area</span>
              </button>
            </div>
            <div id="plannerAreasRoster" style="display:flex;flex-direction:column;gap:6px;">
              <!-- Dynamically populated area cards -->
            </div>
          </div>

          <div style="height:1px;background:var(--border-subtle);"></div>

          <!-- Active Area Conditions Configuration -->
          <div id="plannerConditionsPanel" style="display:flex;flex-direction:column;gap:14px;">
            <!-- Area Name & Controls -->
            <div class="form-group" style="margin-bottom:0;">
              <label for="plannerAreaNameInput" style="font-size:11.5px;font-weight:700;display:flex;justify-content:space-between;align-items:center;">
                <span>Area Name</span>
                <span id="plannerAreaDeleteBtnWrap"></span>
              </label>
              <input type="text" id="plannerAreaNameInput" placeholder="e.g. Area 1: Front Porch & Walkway" style="font-size:13px;padding:7px 10px;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);background:var(--bg-base);color:var(--text-main);">
            </div>

            <!-- Sunlight Condition -->
            <div>
              <label style="font-size:11.5px;font-weight:700;margin-bottom:6px;display:block;color:var(--text-main);">
                <i data-lucide="sun" style="width:12px;height:12px;color:#d97706;vertical-align:-1px;"></i>
                Sunlight Exposure
              </label>
              <div class="planner-chips-grid" id="plannerSunChips">
                <button type="button" class="planner-chip active" data-sun="Full Sun">☀️ Full Sun (6+ hrs)</button>
                <button type="button" class="planner-chip" data-sun="Part Sun / Part Shade">⛅ Part Sun / Shade</button>
                <button type="button" class="planner-chip" data-sun="Full Shade">🌲 Full Shade (&lt;3 hrs)</button>
                <button type="button" class="planner-chip" data-sun="Any">🔄 Any Sunlight</button>
              </div>
            </div>

            <!-- Soil Moisture Condition -->
            <div>
              <label style="font-size:11.5px;font-weight:700;margin-bottom:6px;display:block;color:var(--text-main);">
                <i data-lucide="droplets" style="width:12px;height:12px;color:#0284c7;vertical-align:-1px;"></i>
                Soil Moisture &amp; Drainage
              </label>
              <div class="planner-chips-grid" id="plannerMoistureChips">
                <button type="button" class="planner-chip" data-moist="Dry">🏜️ Dry (Xeric / Fast)</button>
                <button type="button" class="planner-chip active" data-moist="Medium">💧 Medium (Mesic / Avg)</button>
                <button type="button" class="planner-chip" data-moist="Wet">🌊 Wet (Rain Garden / Moist)</button>
                <button type="button" class="planner-chip" data-moist="Any">🔄 Any Moisture</button>
              </div>
            </div>

            <!-- Soil Texture Condition -->
            <div>
              <label style="font-size:11.5px;font-weight:700;margin-bottom:6px;display:block;color:var(--text-main);">
                <i data-lucide="layers" style="width:12px;height:12px;color:#b45309;vertical-align:-1px;"></i>
                Soil Texture
              </label>
              <select id="plannerSoilTextureSelect" style="width:100%;font-size:12px;padding:6px 10px;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);background:var(--bg-base);color:var(--text-main);">
                <option value="Any">Any / Typical Garden Soil</option>
                <option value="Clay">Heavy Clay (Slow drainage)</option>
                <option value="Loam">Rich Loam (Fertile &amp; Organic)</option>
                <option value="Sandy">Sandy / Gravelly (Fast draining)</option>
                <option value="Rocky">Rocky / Limestone Glade</option>
              </select>
            </div>

            <!-- Desired Maintenance Level -->
            <div>
              <label style="font-size:11.5px;font-weight:700;margin-bottom:6px;display:block;color:var(--text-main);">
                <i data-lucide="wrench" style="width:12px;height:12px;color:var(--primary);vertical-align:-1px;"></i>
                Maintenance Level Desired
              </label>
              <div class="planner-chips-grid" id="plannerMaintChips">
                <button type="button" class="planner-chip active" data-maint="Low">🟢 Low (Tough &amp; Self-reliant)</button>
                <button type="button" class="planner-chip" data-maint="Medium">🟡 Medium (Occasional care)</button>
                <button type="button" class="planner-chip" data-maint="Any">🔄 Any Maintenance</button>
              </div>
            </div>

            <!-- Bloom Color Preference -->
            <div>
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <label style="font-size:11.5px;font-weight:700;margin:0;color:var(--text-main);">
                  <i data-lucide="palette" style="width:12px;height:12px;color:#ec4899;vertical-align:-1px;"></i>
                  Bloom Color Preferences
                </label>
                <button type="button" id="plannerAnyColorBtn" style="background:transparent;border:none;color:var(--primary);font-size:11px;cursor:pointer;font-weight:700;">Reset to Any</button>
              </div>
              <div class="planner-color-chips" id="plannerColorChips">
                <button type="button" class="planner-color-chip active" data-color="Any">Any Color</button>
                <button type="button" class="planner-color-chip" data-color="Yellow"><span class="color-dot" style="background:#eab308;"></span>Yellow</button>
                <button type="button" class="planner-color-chip" data-color="Purple"><span class="color-dot" style="background:#a855f7;"></span>Purple / Blue</button>
                <button type="button" class="planner-color-chip" data-color="White"><span class="color-dot" style="background:#ffffff;border:1px solid #cbd5e1;"></span>White</button>
                <button type="button" class="planner-color-chip" data-color="Pink"><span class="color-dot" style="background:#ec4899;"></span>Pink</button>
                <button type="button" class="planner-color-chip" data-color="Red"><span class="color-dot" style="background:#ef4444;"></span>Red</button>
                <button type="button" class="planner-color-chip" data-color="Orange"><span class="color-dot" style="background:#f97316;"></span>Orange</button>
              </div>
            </div>

            <!-- Structural Layers Needed (Ecological Matrix) -->
            <div>
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <label style="font-size:11.5px;font-weight:700;margin:0;color:var(--text-main);">
                  <i data-lucide="layers" style="width:12px;height:12px;color:var(--primary);vertical-align:-1px;"></i>
                  Structural Layers Needed
                </label>
                <button type="button" id="plannerSelectAllLayersBtn" style="background:transparent;border:none;color:var(--primary);font-size:11px;cursor:pointer;font-weight:700;">All Layers</button>
              </div>
              <div class="planner-layer-checkboxes" id="plannerLayerCheckboxes">
                <label class="planner-checkbox-label">
                  <input type="checkbox" data-layer="Groundcover" checked>
                  <span><strong>Groundcover / Living Matrix</strong> (Sedges, creeping forbs &lt;1.5 ft)</span>
                </label>
                <label class="planner-checkbox-label">
                  <input type="checkbox" data-layer="Seasonal/Herbaceous Layer" checked>
                  <span><strong>Seasonal &amp; Mid-Layer Blooms</strong> (Flowers 1.5–3.5 ft)</span>
                </label>
                <label class="planner-checkbox-label">
                  <input type="checkbox" data-layer="Structural Layer" checked>
                  <span><strong>Structural Perennials &amp; Grasses</strong> (Backbone 3–6 ft)</span>
                </label>
                <label class="planner-checkbox-label">
                  <input type="checkbox" data-layer="Understory">
                  <span><strong>Understory Trees &amp; Large Shrubs</strong> (Mid-story &lt;25 ft)</span>
                </label>
                <label class="planner-checkbox-label">
                  <input type="checkbox" data-layer="Canopy">
                  <span><strong>Canopy / Shade Trees</strong> (Overstory trees &gt;25 ft)</span>
                </label>
              </div>
            </div>

            <!-- Area Notes -->
            <div class="form-group" style="margin-bottom:0;">
              <label for="plannerAreaNotesInput" style="font-size:11.5px;font-weight:700;">Area Notes &amp; Ecological Strategy</label>
              <textarea id="plannerAreaNotesInput" rows="2" placeholder="e.g. Near street, receives roof runoff, needs winter interest..." style="font-size:12px;padding:6px 10px;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);background:var(--bg-base);color:var(--text-main);"></textarea>
            </div>

          </div>

        </div>

        <!-- Right Column: Recommendations Review & Batch Add Pane -->
        <div class="planner-content" style="overflow-y:auto;display:flex;flex-direction:column;min-height:0;background:var(--bg-base);">
          
          <!-- Recommendations Header Bar -->
          <div style="padding:14px 20px;border-bottom:1px solid var(--border-subtle);background:var(--bg-surface);display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;flex-shrink:0;">
            <div>
              <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                <h4 id="plannerAreaDisplayTitle" style="font-size:15px;font-weight:800;margin:0;color:var(--text-main);">
                  Area 1: Front Porch &amp; Walkway
                </h4>
                <span id="plannerMatchCountBadge" class="badge" style="background:var(--primary-light);color:var(--primary);border:1px solid var(--primary-border);font-size:11px;font-weight:700;">
                  0 Recommendations
                </span>
              </div>
              <div id="plannerCriteriaPills" style="display:flex;gap:5px;flex-wrap:wrap;margin-top:4px;">
                <!-- Live criteria badges -->
              </div>
            </div>

            <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
              <select id="plannerSortBySelect" style="font-size:12px;padding:6px 10px;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);background:var(--bg-base);color:var(--text-main);" aria-label="Sort recommendations">
                <option value="score">Sort: Best Match Score</option>
                <option value="keystone">Sort: Keystone Species First</option>
                <option value="sweet16">Sort: Sweet 16 First</option>
                <option value="common">Sort: Common Name A-Z</option>
                <option value="height">Sort: Height Low to High</option>
              </select>
              <button type="button" id="plannerAddAllToConsultationBtn" class="btn btn-primary" style="font-size:12px;padding:7px 12px;font-weight:700;display:inline-flex;align-items:center;gap:5px;">
                <i data-lucide="plus-circle" style="width:14px;height:14px;"></i>
                <span>Add Top Recommended to Report</span>
              </button>
            </div>
          </div>

          <!-- Recommendations Body Container -->
          <div id="plannerRecommendationsList" style="flex:1;padding:18px 20px;display:flex;flex-direction:column;gap:18px;overflow-y:auto;">
            <!-- Dynamically populated layer groups and plant cards -->
          </div>

          <!-- Bottom Summary Footer Bar -->
          <div style="padding:10px 20px;background:var(--bg-surface);border-top:1px solid var(--border-subtle);display:flex;align-items:center;justify-content:space-between;gap:12px;font-size:12px;flex-shrink:0;">
            <div style="display:flex;align-items:center;gap:8px;color:var(--text-secondary);">
              <i data-lucide="clipboard-check" style="width:14px;height:14px;color:var(--primary);"></i>
              <span>Consultation Staging: <strong id="plannerCurrentAreaStagedCount" style="color:var(--primary);">0</strong> plants assigned to this area (<span id="plannerTotalStagedCount">0</span> total staged)</span>
            </div>
            <button type="button" id="plannerFinishAndStageBtn" class="btn btn-secondary btn-sm" style="font-size:12px;font-weight:700;">
              <span>Review Consultation Report Drawer &rarr;</span>
            </button>
          </div>

        </div>

      </div>
    </div>
  </dialog>

  '''
        content = content.replace(dialog_target, dialogs_html + dialog_target, 1)
        print("✓ Injected Garden Planner and Guest Dialogs")

    # 6. STATE INITIALIZATION
    state_target = "customPlants: JSON.parse(localStorage.getItem('dr_custom_plants') || '{}'),"
    if 'gardenAreaProfiles' not in content:
        state_snippet = '''gardenAreaProfiles: JSON.parse(localStorage.getItem('dr_garden_area_profiles') || '[]'),
      activePlannerAreaIdx: 0,
      '''
        content = content.replace(state_target, state_snippet + state_target, 1)
        print("✓ Injected gardenAreaProfiles into state")

    # 7. JAVASCRIPT FUNCTIONS (Recommendation Engine & UI)
    js_target = '    // App Initialization'
    if 'function openGardenPlanner(' not in content:
        planner_js = '''    // ==================== Garden Area Planner & Ecological Recommendation Engine ====================
    const PLANNER_LAYER_METADATA = {
      'Groundcover': {
        title: 'Ground Layer / Living Matrix',
        subtitle: 'Sedges, low grasses & creeping groundcovers (< 1.5 ft)',
        desc: 'Suppresses weeds, cools soil, retains moisture, and eliminates the need for repeated wood mulch application.',
        icon: 'sprout',
        color: '#059669',
        badgeBg: 'rgba(5, 150, 105, 0.12)'
      },
      'Seasonal/Herbaceous Layer': {
        title: 'Seasonal & Mid-Layer Forbs',
        subtitle: 'Mid-height wildflowers & blooming perennials (1.5 – 3.5 ft)',
        desc: 'Provides continuous floral succession, nectar, and pollen resources for butterflies, native bees, and hummingbirds.',
        icon: 'flower',
        color: '#ec4899',
        badgeBg: 'rgba(236, 72, 153, 0.12)'
      },
      'Structural Layer': {
        title: 'Structural Perennials & Architectural Grasses',
        subtitle: 'Tall focal flowers & warm-season bunchgrasses (3 – 6+ ft)',
        desc: 'Anchors the bed with architectural form, autumn color, winter interest, and high-value seedheads for songbirds.',
        icon: 'wheat',
        color: '#d97706',
        badgeBg: 'rgba(217, 119, 6, 0.12)'
      },
      'Understory': {
        title: 'Understory Trees & Large Shrubs',
        subtitle: 'Mid-story woody structure & flowering shrubs (< 25 ft)',
        desc: 'Provides critical wildlife nesting cover, structural wind protection, rich berry production, and dappled shade.',
        icon: 'trees',
        color: '#2563eb',
        badgeBg: 'rgba(37, 99, 235, 0.12)'
      },
      'Canopy': {
        title: 'Canopy & Shade Trees',
        subtitle: 'Overstory keystone trees (> 25 ft)',
        desc: 'Top-tier ecological keystone giants that host hundreds of native caterpillar species, provide cooling shade, and sequester carbon.',
        icon: 'tree-pine',
        color: '#15803d',
        badgeBg: 'rgba(21, 128, 61, 0.12)'
      },
      'Vine': {
        title: 'Native Climbers & Vines',
        subtitle: 'Vertical trellis, fence & wall habitat',
        desc: 'Maximizes vertical biodiversity and wall coverage in compact residential footprints.',
        icon: 'activity',
        color: '#7c3aed',
        badgeBg: 'rgba(124, 58, 237, 0.12)'
      }
    };

    function openGardenPlanner(targetAreaIdx = null) {
      // Access Control: Anyone except guest
      const u = state.currentUser;
      const isGuest = !u || !u.name || (u.username === 'guest');
      if (isGuest) {
        openPlannerGuestGatewayModal();
        return;
      }

      initGardenAreaProfiles();

      if (targetAreaIdx !== null && targetAreaIdx >= 0 && targetAreaIdx < state.gardenAreas.length) {
        state.activePlannerAreaIdx = targetAreaIdx;
      } else if (state.activePlannerAreaIdx >= state.gardenAreas.length) {
        state.activePlannerAreaIdx = 0;
      }

      renderGardenPlannerUI();

      const modal = document.getElementById('gardenPlannerModal');
      if (modal) {
        modal.showModal();
        if (window.lucide) lucide.createIcons();
      }
    }

    function openPlannerGuestGatewayModal() {
      const modal = document.getElementById('plannerGuestModal');
      if (modal) {
        modal.showModal();
        if (window.lucide) lucide.createIcons();
      }
    }

    function initGardenAreaProfiles() {
      if (!state.gardenAreas || state.gardenAreas.length === 0) {
        state.gardenAreas = ["Area 1: Front Porch", "Area 2: Front Sidewalk/Mailbox", "Area 3: Backyard Shade Garden"];
      }

      if (!state.gardenAreaProfiles || !Array.isArray(state.gardenAreaProfiles)) {
        state.gardenAreaProfiles = [];
      }

      // Ensure every area in state.gardenAreas has a profile
      state.gardenAreas.forEach((areaName, idx) => {
        let profile = state.gardenAreaProfiles.find(p => p.name === areaName);
        if (!profile) {
          const lower = areaName.toLowerCase();
          let sun = 'Full Sun';
          let moist = 'Medium';
          let layers = ['Groundcover', 'Seasonal/Herbaceous Layer', 'Structural Layer'];
          let maint = 'Low';

          if (lower.includes('shade') || lower.includes('woodland') || lower.includes('tree')) {
            sun = 'Full Shade';
            moist = 'Medium';
            layers = ['Groundcover', 'Seasonal/Herbaceous Layer', 'Understory'];
          } else if (lower.includes('rain') || lower.includes('bioswale') || lower.includes('wet') || lower.includes('drain')) {
            sun = 'Full Sun';
            moist = 'Wet';
            layers = ['Groundcover', 'Seasonal/Herbaceous Layer', 'Structural Layer'];
          } else if (lower.includes('sidewalk') || lower.includes('mailbox') || lower.includes('street') || lower.includes('parkway') || lower.includes('hellstrip')) {
            sun = 'Full Sun';
            moist = 'Dry';
            layers = ['Groundcover', 'Seasonal/Herbaceous Layer', 'Structural Layer'];
            maint = 'Low';
          }

          profile = {
            id: 'area-prof-' + idx + '-' + Date.now(),
            name: areaName,
            sunlight: sun,
            moisture: moist,
            soilTexture: 'Any',
            maintenance: maint,
            bloomColors: ['Any'],
            structuralLayers: layers,
            notes: '',
            sqft: ''
          };
          state.gardenAreaProfiles.push(profile);
        }
      });

      // Filter out stale profiles
      state.gardenAreaProfiles = state.gardenAreaProfiles.filter(p => state.gardenAreas.includes(p.name));
      persistGardenAreaProfiles();
    }

    function persistGardenAreaProfiles() {
      localStorage.setItem('dr_garden_area_profiles', JSON.stringify(state.gardenAreaProfiles));
      if (state.activeConsultationId && state.consultations) {
        const active = state.consultations.find(c => c.id === state.activeConsultationId);
        if (active) {
          active.gardenAreaProfiles = JSON.parse(JSON.stringify(state.gardenAreaProfiles));
          active.lastModified = Date.now();
          persistConsultations();
        }
      }
    }

    function getActivePlannerProfile() {
      initGardenAreaProfiles();
      const areaName = state.gardenAreas[state.activePlannerAreaIdx] || state.gardenAreas[0];
      let prof = state.gardenAreaProfiles.find(p => p.name === areaName);
      if (!prof) {
        prof = state.gardenAreaProfiles[0];
      }
      return prof;
    }

    function renderGardenPlannerUI() {
      initGardenAreaProfiles();
      const activeProf = getActivePlannerProfile();
      if (!activeProf) return;

      // Update Header Badges
      const consultBadge = document.getElementById('plannerActiveConsultationName');
      if (consultBadge) {
        const clientName = state.clientMeta?.name?.trim();
        consultBadge.textContent = clientName ? `Client: ${clientName}` : 'Active Consultation';
      }

      updatePlannerStagedBadges();
      renderPlannerAreasRoster();
      renderPlannerConditionsForm(activeProf);
      renderAreaRecommendations();
    }

    function updatePlannerStagedBadges() {
      const activeProf = getActivePlannerProfile();
      const currentAreaName = activeProf ? activeProf.name : '';
      const stagedList = state.stagedPlants || [];
      const totalStaged = stagedList.length;
      const currentAreaStaged = stagedList.filter(p => (p.target_area || state.gardenAreas[0]) === currentAreaName).length;

      const badgeHeader = document.getElementById('plannerStagedCountBadge');
      if (badgeHeader) badgeHeader.textContent = totalStaged;

      const badgeFooterArea = document.getElementById('plannerCurrentAreaStagedCount');
      if (badgeFooterArea) badgeFooterArea.textContent = currentAreaStaged;

      const badgeFooterTotal = document.getElementById('plannerTotalStagedCount');
      if (badgeFooterTotal) badgeFooterTotal.textContent = totalStaged;
    }

    function renderPlannerAreasRoster() {
      const roster = document.getElementById('plannerAreasRoster');
      const countEl = document.getElementById('plannerAreasCount');
      if (!roster) return;

      countEl.textContent = state.gardenAreas.length;
      roster.innerHTML = '';

      state.gardenAreas.forEach((areaName, idx) => {
        const prof = state.gardenAreaProfiles.find(p => p.name === areaName) || {};
        const plantCount = (state.stagedPlants || []).filter(p => (p.target_area || state.gardenAreas[0]) === areaName).length;
        const isActive = idx === state.activePlannerAreaIdx;

        const card = document.createElement('div');
        card.className = `planner-area-card ${isActive ? 'active' : ''}`;
        card.innerHTML = `
          <div style="display:flex;align-items:center;gap:8px;min-width:0;">
            <i data-lucide="map-pin" style="width:14px;height:14px;color:${isActive ? 'var(--primary)' : 'var(--text-muted)'};flex-shrink:0;"></i>
            <div style="min-width:0;">
              <div style="font-size:12px;font-weight:${isActive ? '800' : '600'};color:var(--text-main);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                ${escapeHtml(areaName)}
              </div>
              <div style="font-size:10px;color:var(--text-muted);display:flex;align-items:center;gap:5px;margin-top:1px;">
                <span>${escapeHtml(prof.sunlight || 'Sun')}</span> &bull; <span>${escapeHtml(prof.moisture || 'Moist')}</span>
              </div>
            </div>
          </div>
          <span class="badge" style="background:${isActive ? 'var(--primary)' : 'var(--border-subtle)'};color:${isActive ? '#fff' : 'var(--text-secondary)'};font-size:10px;font-weight:700;padding:1px 6px;border-radius:10px;flex-shrink:0;">
            ${plantCount}
          </span>
        `;

        card.addEventListener('click', () => {
          if (state.activePlannerAreaIdx !== idx) {
            state.activePlannerAreaIdx = idx;
            renderGardenPlannerUI();
          }
        });

        roster.appendChild(card);
      });

      if (window.lucide) lucide.createIcons();
    }

    function renderPlannerConditionsForm(profile) {
      if (!profile) return;

      // Area Name Input
      const nameInput = document.getElementById('plannerAreaNameInput');
      if (nameInput) {
        nameInput.value = profile.name;
        nameInput.onchange = (e) => {
          const newName = (e.target.value || '').trim() || `Area ${state.activePlannerAreaIdx + 1}`;
          const oldName = profile.name;
          if (newName !== oldName) {
            profile.name = newName;
            state.gardenAreas[state.activePlannerAreaIdx] = newName;
            (state.stagedPlants || []).forEach(p => {
              if (p.target_area === oldName) p.target_area = newName;
            });
            saveStaging();
            persistGardenAreas();
            persistGardenAreaProfiles();
            renderGardenAreasManager();
            renderGardenPlannerUI();
          }
        };
      }

      // Delete Area Button
      const deleteWrap = document.getElementById('plannerAreaDeleteBtnWrap');
      if (deleteWrap) {
        if (state.gardenAreas.length > 1) {
          deleteWrap.innerHTML = `
            <button type="button" class="btn-text-action" style="color:var(--danger);font-size:11px;font-weight:700;" title="Delete this garden area">
              Delete Area
            </button>
          `;
          deleteWrap.querySelector('button')?.addEventListener('click', () => {
            const removingName = profile.name;
            if (confirm(`Remove "${removingName}"? Staged plants will be reassigned to the first remaining area.`)) {
              state.gardenAreas.splice(state.activePlannerAreaIdx, 1);
              state.gardenAreaProfiles = state.gardenAreaProfiles.filter(p => p.name !== removingName);
              const fallbackArea = state.gardenAreas[0];
              (state.stagedPlants || []).forEach(p => {
                if (p.target_area === removingName) p.target_area = fallbackArea;
              });
              state.activePlannerAreaIdx = 0;
              saveStaging();
              persistGardenAreas();
              persistGardenAreaProfiles();
              renderGardenAreasManager();
              renderGardenPlannerUI();
            }
          });
        } else {
          deleteWrap.innerHTML = '';
        }
      }

      // Sunlight Chips
      const sunChips = document.querySelectorAll('#plannerSunChips .planner-chip');
      sunChips.forEach(chip => {
        const val = chip.getAttribute('data-sun');
        chip.classList.toggle('active', profile.sunlight === val);
        chip.onclick = () => {
          profile.sunlight = val;
          persistGardenAreaProfiles();
          renderPlannerConditionsForm(profile);
          renderAreaRecommendations();
        };
      });

      // Moisture Chips
      const moistChips = document.querySelectorAll('#plannerMoistureChips .planner-chip');
      moistChips.forEach(chip => {
        const val = chip.getAttribute('data-moist');
        chip.classList.toggle('active', profile.moisture === val);
        chip.onclick = () => {
          profile.moisture = val;
          persistGardenAreaProfiles();
          renderPlannerConditionsForm(profile);
          renderAreaRecommendations();
        };
      });

      // Soil Texture Select
      const textureSelect = document.getElementById('plannerSoilTextureSelect');
      if (textureSelect) {
        textureSelect.value = profile.soilTexture || 'Any';
        textureSelect.onchange = (e) => {
          profile.soilTexture = e.target.value;
          persistGardenAreaProfiles();
          renderAreaRecommendations();
        };
      }

      // Maintenance Chips
      const maintChips = document.querySelectorAll('#plannerMaintChips .planner-chip');
      maintChips.forEach(chip => {
        const val = chip.getAttribute('data-maint');
        chip.classList.toggle('active', profile.maintenance === val);
        chip.onclick = () => {
          profile.maintenance = val;
          persistGardenAreaProfiles();
          renderPlannerConditionsForm(profile);
          renderAreaRecommendations();
        };
      });

      // Bloom Color Chips
      const colorChips = document.querySelectorAll('#plannerColorChips .planner-color-chip');
      const curColors = profile.bloomColors || ['Any'];
      colorChips.forEach(chip => {
        const val = chip.getAttribute('data-color');
        const isActive = curColors.includes(val);
        chip.classList.toggle('active', isActive);
        chip.onclick = () => {
          if (val === 'Any') {
            profile.bloomColors = ['Any'];
          } else {
            let next = curColors.filter(c => c !== 'Any');
            if (next.includes(val)) {
              next = next.filter(c => c !== val);
            } else {
              next.push(val);
            }
            profile.bloomColors = next.length > 0 ? next : ['Any'];
          }
          persistGardenAreaProfiles();
          renderPlannerConditionsForm(profile);
          renderAreaRecommendations();
        };
      });

      // Structural Layer Checkboxes
      const layerBoxes = document.querySelectorAll('#plannerLayerCheckboxes input[type="checkbox"]');
      const curLayers = profile.structuralLayers || ['Groundcover', 'Seasonal/Herbaceous Layer', 'Structural Layer'];
      layerBoxes.forEach(box => {
        const lKey = box.getAttribute('data-layer');
        box.checked = curLayers.includes(lKey);
        box.onchange = (e) => {
          if (e.target.checked) {
            if (!curLayers.includes(lKey)) curLayers.push(lKey);
          } else {
            const idx = curLayers.indexOf(lKey);
            if (idx >= 0) curLayers.splice(idx, 1);
          }
          profile.structuralLayers = curLayers;
          persistGardenAreaProfiles();
          renderAreaRecommendations();
        };
      });

      // Area Notes
      const notesInput = document.getElementById('plannerAreaNotesInput');
      if (notesInput) {
        notesInput.value = profile.notes || '';
        notesInput.onchange = (e) => {
          profile.notes = e.target.value;
          persistGardenAreaProfiles();
        };
      }
    }

    // Calculate Ecological Native Recommendations
    function getPlantRecommendationsForArea(profile) {
      if (!profile) return [];
      const allPlants = (state.allPlants && state.allPlants.length > 0) ? state.allPlants : (window.embeddedMasterPlants || []);

      const toList = (v) => {
        if (!v) return [];
        if (Array.isArray(v)) return v.map(x => String(x).trim()).filter(Boolean);
        return String(v).split(',').map(x => x.trim()).filter(Boolean);
      };

      const areaSun = profile.sunlight || 'Any';
      const areaMoist = profile.moisture || 'Any';
      const areaTexture = (profile.soilTexture || 'Any').toLowerCase();
      const areaMaint = profile.maintenance || 'Any';
      const areaColors = (profile.bloomColors && profile.bloomColors.length > 0) ? profile.bloomColors.map(c => c.toLowerCase()) : ['any'];
      const areaLayers = (profile.structuralLayers && profile.structuralLayers.length > 0) ? profile.structuralLayers : [];

      const results = [];

      allPlants.forEach(plant => {
        if (plant.is_invasive === true) return;

        let score = 0;
        const reasons = [];
        let isDisqualified = false;

        // 1. Sunlight Compatibility (Max 35 pts)
        const plantSun = toList(plant.light_requirements || plant.sun_exposure).map(s => s.toLowerCase());
        if (areaSun === 'Full Sun') {
          if (plantSun.some(s => s.includes('full sun'))) {
            score += 35;
            reasons.push('☀️ Full Sun Match');
          } else if (plantSun.some(s => s.includes('part sun'))) {
            score += 18;
            reasons.push('⛅ Tolerates Part Sun');
          } else if (plantSun.every(s => s.includes('shade'))) {
            isDisqualified = true;
          } else {
            score += 10;
          }
        } else if (areaSun === 'Part Sun / Part Shade' || areaSun === 'Part Sun' || areaSun === 'Part Shade') {
          if (plantSun.some(s => s.includes('part'))) {
            score += 35;
            reasons.push('⛅ Part Sun/Shade Optimal');
          } else if (plantSun.some(s => s.includes('full sun') || s.includes('shade'))) {
            score += 22;
            reasons.push('🔄 Flexible Sun Tolerance');
          }
        } else if (areaSun === 'Full Shade') {
          if (plantSun.some(s => s.includes('full shade') || s.includes('shade'))) {
            score += 35;
            reasons.push('🌲 Shade Adapted');
          } else if (plantSun.some(s => s.includes('part'))) {
            score += 20;
            reasons.push('⛅ Part Shade Tolerant');
          } else if (plantSun.some(s => s.includes('full sun') && !s.includes('part'))) {
            isDisqualified = true;
          }
        } else {
          score += 30; // Any sun
        }

        if (isDisqualified) return;

        // 2. Moisture Compatibility (Max 30 pts)
        const plantMoist = toList(plant.moisture_requirements || plant.moisture || plant.soil_moisture).map(m => m.toLowerCase());
        if (areaMoist === 'Dry') {
          if (plantMoist.some(m => m.includes('dry'))) {
            score += 30;
            reasons.push('🏜️ Drought Hardy / Dry Soil');
          } else if (plantMoist.some(m => m.includes('medium') && !m.includes('wet'))) {
            score += 15;
          } else if (plantMoist.every(m => m.includes('wet'))) {
            isDisqualified = true;
          }
        } else if (areaMoist === 'Medium') {
          if (plantMoist.some(m => m.includes('medium'))) {
            score += 30;
            reasons.push('💧 Mesic / Average Soil');
          } else if (plantMoist.some(m => m.includes('dry') || m.includes('wet'))) {
            score += 18;
          }
        } else if (areaMoist === 'Wet') {
          if (plantMoist.some(m => m.includes('wet'))) {
            score += 30;
            reasons.push('🌊 Wet Soil / Rain Garden');
          } else if (plantMoist.some(m => m.includes('medium-wet') || m.includes('moist'))) {
            score += 25;
          } else if (plantMoist.every(m => m.includes('dry') && !m.includes('medium'))) {
            isDisqualified = true;
          }
        } else {
          score += 25; // Any moisture
        }

        if (isDisqualified) return;

        // Soil texture bonus
        if (areaTexture !== 'any') {
          const plantSoil = String(plant.soil_requirements || '').toLowerCase();
          if (plantSoil.includes(areaTexture)) {
            score += 6;
            reasons.push(`🌱 Thrives in ${areaTexture}`);
          }
        }

        // 3. Structural Layer Match (Max 25 pts)
        const plantLayer = plant.architectural_layer || getPlantLayer(plant) || 'Seasonal/Herbaceous Layer';
        const plantTypes = toList(plant.plant_type).map(t => t.toLowerCase());

        let effectiveLayer = plantLayer;
        if (plantTypes.includes('tree')) {
          const maxH = parseFloat(plant.mature_height_max) || 0;
          effectiveLayer = maxH > 25 ? 'Canopy' : 'Understory';
        } else if (plantTypes.includes('shrub')) {
          effectiveLayer = 'Understory';
        } else if (plantTypes.includes('sedge') || (plantTypes.includes('grass') && (parseFloat(plant.mature_height_max) || 0) < 2.5)) {
          effectiveLayer = 'Groundcover';
        } else if (plantTypes.includes('grass') && (parseFloat(plant.mature_height_max) || 0) >= 2.5) {
          effectiveLayer = 'Structural Layer';
        } else if (plantTypes.includes('wildflower')) {
          const maxH = parseFloat(plant.mature_height_max) || 0;
          if (maxH < 1.5 || String(plant.growth_habit || '').toLowerCase().includes('groundcover')) {
            effectiveLayer = 'Groundcover';
          } else if (maxH >= 3.5) {
            effectiveLayer = 'Structural Layer';
          } else {
            effectiveLayer = 'Seasonal/Herbaceous Layer';
          }
        } else if (plantTypes.includes('vine')) {
          effectiveLayer = 'Vine';
        }

        if (areaLayers.length > 0) {
          if (areaLayers.includes(effectiveLayer) || areaLayers.includes(plantLayer)) {
            score += 25;
            reasons.push(`🌿 ${effectiveLayer}`);
          } else {
            score -= 25;
          }
        } else {
          score += 15;
        }

        // 4. Maintenance Match (Max 15 pts)
        const plantMaint = (plant.maintenance_level || getPlantMaintenanceLevel(plant) || 'Low').toLowerCase();
        if (areaMaint === 'Low') {
          if (plantMaint.includes('low')) {
            score += 15;
            reasons.push('🟢 Low Maintenance');
          } else if (plantMaint.includes('medium')) {
            score += 5;
          } else {
            score -= 15;
          }
        } else if (areaMaint === 'Medium') {
          if (plantMaint.includes('low') || plantMaint.includes('medium')) {
            score += 15;
          } else {
            score += 5;
          }
        } else {
          score += 12;
        }

        // 5. Bloom Color Match (Max 15 pts)
        const plantColors = toList(plant.bloom_color || plant.flower_color).map(c => c.toLowerCase());
        const isFoliage = plantTypes.some(t => ['grass', 'sedge', 'fern'].includes(t));
        if (areaColors.includes('any')) {
          score += 15;
        } else if (isFoliage) {
          score += 12;
          reasons.push('🌾 Living Matrix Foliage');
        } else if (plantColors.some(pc => areaColors.some(ac => pc.includes(ac)))) {
          score += 15;
          reasons.push('🌸 Color Match');
        } else {
          score += 4;
        }

        // 6. Ecological Superchargers (Bonus 0 - 20 pts)
        if (isKcKeystone(plant)) {
          score += 10;
          reasons.push('⭐ Keystone Species');
        }
        if (isSweet16(plant)) {
          score += 8;
          reasons.push('🏆 Sweet 16');
        }

        if (score >= 50) {
          results.push({
            plant,
            score,
            matchPct: Math.min(100, Math.round((score / 135) * 100)),
            reasons: Array.from(new Set(reasons)),
            effectiveLayer: effectiveLayer || 'Seasonal/Herbaceous Layer'
          });
        }
      });

      return results;
    }

    function renderAreaRecommendations() {
      const listContainer = document.getElementById('plannerRecommendationsList');
      const profile = getActivePlannerProfile();
      if (!listContainer || !profile) return;

      // Update Area Title & Criteria Badges
      const titleEl = document.getElementById('plannerAreaDisplayTitle');
      if (titleEl) titleEl.textContent = profile.name;

      const criteriaPills = document.getElementById('plannerCriteriaPills');
      if (criteriaPills) {
        const layersCount = (profile.structuralLayers || []).length;
        const colorTxt = (profile.bloomColors || ['Any']).join(', ');
        criteriaPills.innerHTML = `
          <span class="badge" style="background:rgba(217,119,6,0.12);color:#b45309;font-size:10.5px;">☀️ ${escapeHtml(profile.sunlight || 'Any Sun')}</span>
          <span class="badge" style="background:rgba(2,132,199,0.12);color:#0284c7;font-size:10.5px;">💧 ${escapeHtml(profile.moisture || 'Any Moisture')}</span>
          <span class="badge" style="background:rgba(35,92,54,0.12);color:var(--primary);font-size:10.5px;">🟢 ${escapeHtml(profile.maintenance || 'Any')} Maint</span>
          <span class="badge" style="background:rgba(236,72,153,0.12);color:#db2777;font-size:10.5px;">🌸 ${escapeHtml(colorTxt)}</span>
          <span class="badge" style="background:var(--border-subtle);color:var(--text-secondary);font-size:10.5px;">🌿 ${layersCount} Layer${layersCount === 1 ? '' : 's'}</span>
        `;
      }

      // Calculate recommendations
      let recommendations = getPlantRecommendationsForArea(profile);

      // Sort
      const sortBy = document.getElementById('plannerSortBySelect')?.value || 'score';
      if (sortBy === 'score') {
        recommendations.sort((a, b) => b.score - a.score);
      } else if (sortBy === 'keystone') {
        recommendations.sort((a, b) => {
          const aKey = isKcKeystone(a.plant) ? 1 : 0;
          const bKey = isKcKeystone(b.plant) ? 1 : 0;
          return (bKey - aKey) || (b.score - a.score);
        });
      } else if (sortBy === 'sweet16') {
        recommendations.sort((a, b) => {
          const aSw = isSweet16(a.plant) ? 1 : 0;
          const bSw = isSweet16(b.plant) ? 1 : 0;
          return (bSw - aSw) || (b.score - a.score);
        });
      } else if (sortBy === 'common') {
        recommendations.sort((a, b) => {
          const aName = a.plant.common_names?.[0] || a.plant.scientific_name;
          const bName = b.plant.common_names?.[0] || b.plant.scientific_name;
          return aName.localeCompare(bName);
        });
      } else if (sortBy === 'height') {
        recommendations.sort((a, b) => {
          const aH = parseFloat(a.plant.mature_height_max) || 0;
          const bH = parseFloat(b.plant.mature_height_max) || 0;
          return aH - bH;
        });
      }

      const matchBadge = document.getElementById('plannerMatchCountBadge');
      if (matchBadge) matchBadge.textContent = `${recommendations.length} Recommended Species`;

      if (recommendations.length === 0) {
        listContainer.innerHTML = `
          <div style="text-align:center;padding:50px 20px;color:var(--text-muted);background:var(--bg-surface);border:1px solid var(--border-subtle);border-radius:var(--radius-md);">
            <i data-lucide="sprout" style="width:36px;height:36px;color:var(--text-muted);margin-bottom:10px;"></i>
            <h5 style="font-size:15px;font-weight:700;margin:0 0 6px 0;color:var(--text-main);">No Exact Matches for this Criteria Combination</h5>
            <p style="font-size:12.5px;max-width:440px;margin:0 auto 14px auto;line-height:1.45;">
              Try setting Sunlight or Moisture to <em>Any</em>, or selecting additional structural layers in the left panel.
            </p>
            <button type="button" class="btn btn-secondary btn-sm" onclick="resetPlannerFiltersToBroad()">
              Broaden Area Conditions
            </button>
          </div>
        `;
        if (window.lucide) lucide.createIcons();
        return;
      }

      // Group recommendations by Layer
      const layerOrder = ['Groundcover', 'Seasonal/Herbaceous Layer', 'Structural Layer', 'Understory', 'Canopy', 'Vine'];
      const grouped = {};
      layerOrder.forEach(l => { grouped[l] = []; });

      recommendations.forEach(rec => {
        const lKey = rec.effectiveLayer || 'Seasonal/Herbaceous Layer';
        if (!grouped[lKey]) grouped[lKey] = [];
        grouped[lKey].push(rec);
      });

      listContainer.innerHTML = '';

      layerOrder.forEach(layerKey => {
        const items = grouped[layerKey];
        if (!items || items.length === 0) return;

        const meta = PLANNER_LAYER_METADATA[layerKey] || {
          title: layerKey,
          subtitle: 'Ecological Planting Layer',
          desc: 'Complementary planting matrix layer.',
          icon: 'layers',
          color: 'var(--primary)',
          badgeBg: 'rgba(35, 92, 54, 0.12)'
        };

        const layerBox = document.createElement('div');
        layerBox.className = 'planner-layer-box';

        layerBox.innerHTML = `
          <div class="planner-layer-header">
            <div style="display:flex;align-items:center;gap:10px;min-width:0;">
              <div style="width:32px;height:32px;border-radius:var(--radius-sm);background:${meta.badgeBg};color:${meta.color};display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <i data-lucide="${meta.icon}" style="width:18px;height:18px;"></i>
              </div>
              <div>
                <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                  <span style="font-size:13.5px;font-weight:800;color:var(--text-main);">${escapeHtml(meta.title)}</span>
                  <span class="badge" style="background:${meta.badgeBg};color:${meta.color};font-size:10.5px;font-weight:700;">
                    ${items.length} species
                  </span>
                </div>
                <div style="font-size:11px;color:var(--text-muted);margin-top:1px;">
                  ${escapeHtml(meta.desc)}
                </div>
              </div>
            </div>
            <button type="button" class="btn btn-secondary btn-sm planner-batch-layer-btn" data-layer="${layerKey}" style="font-size:11.5px;padding:5px 10px;font-weight:700;">
              <i data-lucide="plus" style="width:12px;height:12px;"></i>
              <span>Add All ${escapeHtml(meta.title.split('/')[0].trim())}</span>
            </button>
          </div>
          <div class="planner-layer-cards-grid" id="plannerGrid_${layerKey}">
            <!-- Plant Cards -->
          </div>
        `;

        const grid = layerBox.querySelector(`#plannerGrid_${layerKey}`);
        items.forEach(rec => {
          const card = createPlannerPlantCard(rec, profile);
          grid.appendChild(card);
        });

        // Batch Add for Layer
        layerBox.querySelector('.planner-batch-layer-btn')?.addEventListener('click', () => {
          addAllLayerToConsultation(layerKey, profile.name);
        });

        listContainer.appendChild(layerBox);
      });

      if (window.lucide) lucide.createIcons();
    }

    function createPlannerPlantCard(rec, profile) {
      const plant = rec.plant;
      const commonName = plant.common_names?.[0] || plant.scientific_name;
      const sciName = plant.scientific_name;
      const img = plant.images?.[0] || {};
      const imgUrl = img.url || '';
      const thumbUrl = img.thumbnail || imgUrl || 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 24 24" fill="none" stroke="%23235c36" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>';

      const isStagedInArea = (state.stagedPlants || []).some(p => 
        (p.id === plant.id || p.scientific_name === sciName) && 
        (p.target_area || state.gardenAreas[0]) === profile.name
      );

      const stagedItem = isStagedInArea ? (state.stagedPlants || []).find(p => (p.id === plant.id || p.scientific_name === sciName) && (p.target_area || state.gardenAreas[0]) === profile.name) : null;
      const quantity = stagedItem ? (stagedItem.quantity || 1) : 0;

      const card = document.createElement('div');
      card.className = `planner-plant-card ${isStagedInArea ? 'is-staged' : ''}`;

      const topReasons = rec.reasons.slice(0, 3);

      card.innerHTML = `
        <div style="display:flex;gap:10px;align-items:flex-start;">
          <div style="width:68px;height:68px;border-radius:var(--radius-sm);overflow:hidden;flex-shrink:0;background:#030a06;position:relative;">
            <img src="${thumbUrl}" alt="${escapeHtml(commonName)}" style="width:100%;height:100%;object-fit:cover;" onerror="if(this.src.includes('images/plants/') && !this.src.startsWith('images/plants/')){ this.src='images/plants/' + this.src.split('images/plants/')[1]; } else { this.onerror=null; this.src='${imgUrl}'; }">
            <span class="badge" style="position:absolute;top:3px;left:3px;background:rgba(12,30,19,0.85);color:#a7f3d0;border:1px solid rgba(255,255,255,0.2);font-size:9px;font-weight:800;padding:1px 4px;border-radius:3px;">
              ${rec.matchPct}%
            </span>
          </div>
          <div style="flex:1;min-width:0;">
            <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:4px;">
              <h5 style="font-size:13px;font-weight:800;margin:0;color:var(--text-main);line-height:1.25;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                ${escapeHtml(commonName)}
              </h5>
            </div>
            <div style="font-size:11.5px;font-style:italic;color:var(--text-muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:1px;">
              ${escapeHtml(sciName)}
            </div>
            <div style="display:flex;gap:4px;flex-wrap:wrap;margin-top:4px;">
              ${topReasons.map(r => `<span class="badge" style="font-size:9.5px;padding:1px 5px;background:var(--bg-surface-elevated);color:var(--text-secondary);border:1px solid var(--border-subtle);">${escapeHtml(r)}</span>`).join('')}
            </div>
          </div>
        </div>

        <div style="font-size:11px;color:var(--text-secondary);display:flex;justify-content:space-between;align-items:center;border-top:1px dashed var(--border-subtle);padding-top:6px;margin-top:4px;">
          <span>Height: <strong>${escapeHtml(getPlantHeight(plant) || 'Var')}</strong></span>
          <span>Bloom: <strong>${escapeHtml(plant.bloom_period || 'Seasonal')}</strong></span>
          <button type="button" class="btn-text-action btn-inspect-plant" style="font-size:11px;color:var(--primary);font-weight:700;">Details &rarr;</button>
        </div>

        <div style="display:flex;gap:6px;align-items:center;margin-top:2px;">
          ${isStagedInArea ? `
            <button type="button" class="btn btn-sm btn-primary planner-toggle-btn" style="flex:1;font-size:11.5px;padding:6px 8px;gap:4px;background:#059669;border-color:#059669;" title="In Consultation for this area. Click to increase quantity.">
              <i data-lucide="check" style="width:13px;height:13px;"></i>
              <span>In Report (${quantity}x)</span>
            </button>
            <button type="button" class="btn-icon planner-remove-btn" title="Remove from this area" style="color:var(--danger);padding:5px;border:1px solid var(--border-subtle);border-radius:var(--radius-sm);background:var(--bg-base);">
              <i data-lucide="trash-2" style="width:13px;height:13px;"></i>
            </button>
          ` : `
            <button type="button" class="btn btn-sm btn-secondary planner-toggle-btn" style="flex:1;font-size:11.5px;padding:6px 8px;gap:4px;font-weight:700;">
              <i data-lucide="plus" style="width:13px;height:13px;"></i>
              <span>Add to Consultation</span>
            </button>
          `}
        </div>
      `;

      card.querySelector('.btn-inspect-plant')?.addEventListener('click', (e) => {
        e.stopPropagation();
        openPlantDetail(plant);
      });

      card.querySelector('.planner-toggle-btn')?.addEventListener('click', () => {
        addPlantToAreaConsultation(plant, profile.name, rec.effectiveLayer);
      });

      card.querySelector('.planner-remove-btn')?.addEventListener('click', (e) => {
        e.stopPropagation();
        removePlantFromAreaConsultation(plant, profile.name);
      });

      return card;
    }

    function addPlantToAreaConsultation(plant, areaName, layerName) {
      if (!state.currentUser) {
        showToast("Please sign in as an advisor to stage plants for reports.", "warning");
        openLoginModal();
        return;
      }

      const existing = (state.stagedPlants || []).find(p => 
        (p.id === plant.id || p.scientific_name === plant.scientific_name) && 
        (p.target_area || state.gardenAreas[0]) === areaName
      );

      if (existing) {
        existing.quantity = (existing.quantity || 1) + 1;
        showToast(`Increased ${plant.common_names?.[0] || plant.scientific_name} quantity to ${existing.quantity} for ${areaName}!`);
      } else {
        const meta = PLANNER_LAYER_METADATA[layerName] || {};
        state.stagedPlants.push({
          id: plant.id || plant.scientific_name,
          common_name: plant.common_names?.[0] || plant.scientific_name,
          scientific_name: plant.scientific_name,
          image_url: plant.images?.[0]?.url || '',
          plant_url: getPlantUrl(plant),
          advisor_description: getPlantDesc(plant),
          quantity: 1,
          custom_notes: `Recommended ${meta.title || layerName} for ${areaName}`,
          sun: (plant.light_requirements || []).join(', '),
          moisture: (plant.moisture_requirements || []).join(', '),
          height: getPlantHeight(plant),
          layer: meta.title || getPlantLayer(plant),
          sociability: getPlantSociability(plant),
          maintenance_level: getPlantMaintenanceLevel(plant),
          maintenance_guide: getPlantMaintenanceGuide(plant),
          environment: plant.native_environment || '',
          target_area: areaName
        });
        showToast(`Added ${plant.common_names?.[0] || plant.scientific_name} to ${areaName}!`);
      }

      saveStaging();
      renderStaging();
      renderGrid();
      updatePlannerStagedBadges();
      renderAreaRecommendations();
    }

    function removePlantFromAreaConsultation(plant, areaName) {
      const idx = (state.stagedPlants || []).findIndex(p => 
        (p.id === plant.id || p.scientific_name === plant.scientific_name) && 
        (p.target_area || state.gardenAreas[0]) === areaName
      );
      if (idx >= 0) {
        const removed = state.stagedPlants.splice(idx, 1)[0];
        showToast(`Removed ${removed.common_name} from ${areaName}.`);
        saveStaging();
        renderStaging();
        renderGrid();
        updatePlannerStagedBadges();
        renderAreaRecommendations();
      }
    }

    function addAllLayerToConsultation(layerKey, areaName) {
      const profile = getActivePlannerProfile();
      const recs = getPlantRecommendationsForArea(profile).filter(r => r.effectiveLayer === layerKey);
      let added = 0;

      recs.forEach(({ plant }) => {
        const isStaged = (state.stagedPlants || []).some(p => 
          (p.id === plant.id || p.scientific_name === plant.scientific_name) && 
          (p.target_area || state.gardenAreas[0]) === areaName
        );
        if (!isStaged) {
          const meta = PLANNER_LAYER_METADATA[layerKey] || {};
          state.stagedPlants.push({
            id: plant.id || plant.scientific_name,
            common_name: plant.common_names?.[0] || plant.scientific_name,
            scientific_name: plant.scientific_name,
            image_url: plant.images?.[0]?.url || '',
            plant_url: getPlantUrl(plant),
            advisor_description: getPlantDesc(plant),
            quantity: 1,
            custom_notes: `Recommended ${meta.title || layerKey} for ${areaName}`,
            sun: (plant.light_requirements || []).join(', '),
            moisture: (plant.moisture_requirements || []).join(', '),
            height: getPlantHeight(plant),
            layer: meta.title || getPlantLayer(plant),
            sociability: getPlantSociability(plant),
            maintenance_level: getPlantMaintenanceLevel(plant),
            maintenance_guide: getPlantMaintenanceGuide(plant),
            environment: plant.native_environment || '',
            target_area: areaName
          });
          added++;
        }
      });

      if (added > 0) {
        saveStaging();
        renderStaging();
        renderGrid();
        updatePlannerStagedBadges();
        renderAreaRecommendations();
        showToast(`Added ${added} native plants to ${areaName}!`, 'success');
      } else {
        showToast(`All recommended species in this layer are already staged for ${areaName}.`);
      }
    }

    function addTopRecommendedToConsultation() {
      const profile = getActivePlannerProfile();
      const recs = getPlantRecommendationsForArea(profile);
      if (recs.length === 0) {
        showToast("No recommendations available to add.", "warning");
        return;
      }

      // Add top 6 species across layers
      const topRecs = recs.slice(0, 6);
      let added = 0;
      topRecs.forEach(({ plant, effectiveLayer }) => {
        const isStaged = (state.stagedPlants || []).some(p => 
          (p.id === plant.id || p.scientific_name === plant.scientific_name) && 
          (p.target_area || state.gardenAreas[0]) === profile.name
        );
        if (!isStaged) {
          const meta = PLANNER_LAYER_METADATA[effectiveLayer] || {};
          state.stagedPlants.push({
            id: plant.id || plant.scientific_name,
            common_name: plant.common_names?.[0] || plant.scientific_name,
            scientific_name: plant.scientific_name,
            image_url: plant.images?.[0]?.url || '',
            plant_url: getPlantUrl(plant),
            advisor_description: getPlantDesc(plant),
            quantity: 1,
            custom_notes: `Recommended ${meta.title || effectiveLayer} for ${profile.name}`,
            sun: (plant.light_requirements || []).join(', '),
            moisture: (plant.moisture_requirements || []).join(', '),
            height: getPlantHeight(plant),
            layer: meta.title || getPlantLayer(plant),
            sociability: getPlantSociability(plant),
            maintenance_level: getPlantMaintenanceLevel(plant),
            maintenance_guide: getPlantMaintenanceGuide(plant),
            environment: plant.native_environment || '',
            target_area: profile.name
          });
          added++;
        }
      });

      saveStaging();
      renderStaging();
      renderGrid();
      updatePlannerStagedBadges();
      renderAreaRecommendations();
      showToast(`Staged ${added} top recommended native plants for ${profile.name}!`, 'success');
    }

    function resetPlannerFiltersToBroad() {
      const profile = getActivePlannerProfile();
      if (!profile) return;
      profile.sunlight = 'Any';
      profile.moisture = 'Any';
      profile.maintenance = 'Any';
      profile.bloomColors = ['Any'];
      profile.structuralLayers = ['Groundcover', 'Seasonal/Herbaceous Layer', 'Structural Layer'];
      persistGardenAreaProfiles();
      renderPlannerConditionsForm(profile);
      renderAreaRecommendations();
      showToast("Conditions broadened to Any Sunlight & Any Moisture.");
    }

'''
        content = content.replace(js_target, planner_js + js_target, 1)
        print("✓ Injected Garden Planner JavaScript Logic")

    # 8. EVENT LISTENER BINDINGS in setupEventListeners
    listener_target = "// App Initialization"
    if "document.getElementById('gardenPlannerHeaderBtn')" not in content:
        event_bindings = '''      // Garden Area Planner Triggers
      document.getElementById('gardenPlannerHeaderBtn')?.addEventListener('click', () => openGardenPlanner());
      document.getElementById('openPlannerFromStagingBtn')?.addEventListener('click', () => {
        closeDrawer();
        openGardenPlanner();
      });
      document.getElementById('profileOpenPlannerBtn')?.addEventListener('click', () => {
        document.getElementById('userProfileModal')?.close();
        openGardenPlanner();
      });
      document.getElementById('guestGateSignInBtn')?.addEventListener('click', () => {
        document.getElementById('plannerGuestModal')?.close();
        openLoginModal();
      });
      document.getElementById('plannerOpenDrawerBtn')?.addEventListener('click', () => {
        document.getElementById('gardenPlannerModal')?.close();
        document.getElementById('stagingDrawer')?.classList.add('open');
        document.getElementById('drawerOverlay')?.classList.add('open');
      });
      document.getElementById('plannerFinishAndStageBtn')?.addEventListener('click', () => {
        document.getElementById('gardenPlannerModal')?.close();
        document.getElementById('stagingDrawer')?.classList.add('open');
        document.getElementById('drawerOverlay')?.classList.add('open');
      });
      document.getElementById('plannerAddAreaBtn')?.addEventListener('click', () => {
        const nextNum = state.gardenAreas.length + 1;
        const newAreaName = `Area ${nextNum}: New Planting Zone`;
        state.gardenAreas.push(newAreaName);
        persistGardenAreas();
        initGardenAreaProfiles();
        state.activePlannerAreaIdx = state.gardenAreas.length - 1;
        renderGardenAreasManager();
        renderGardenPlannerUI();
        showToast(`Added ${newAreaName}! Customize its conditions on the left.`);
      });
      document.getElementById('plannerAddAllToConsultationBtn')?.addEventListener('click', () => {
        addTopRecommendedToConsultation();
      });
      document.getElementById('plannerSortBySelect')?.addEventListener('change', () => {
        renderAreaRecommendations();
      });
      document.getElementById('plannerAnyColorBtn')?.addEventListener('click', () => {
        const prof = getActivePlannerProfile();
        if (prof) {
          prof.bloomColors = ['Any'];
          persistGardenAreaProfiles();
          renderPlannerConditionsForm(prof);
          renderAreaRecommendations();
        }
      });
      document.getElementById('plannerSelectAllLayersBtn')?.addEventListener('click', () => {
        const prof = getActivePlannerProfile();
        if (prof) {
          prof.structuralLayers = ['Groundcover', 'Seasonal/Herbaceous Layer', 'Structural Layer', 'Understory', 'Canopy'];
          persistGardenAreaProfiles();
          renderPlannerConditionsForm(prof);
          renderAreaRecommendations();
        }
      });

'''
        # Place before `// App Initialization` inside `setupEventListeners`
        # Let's find the closing brace of `setupEventListeners`
        # In lines 12815-12820:
        # `      });\n    }\n\n    // App Initialization`
        content = content.replace('      // Browse Invasives Button inside Consultation Drawer', event_bindings + '      // Browse Invasives Button inside Consultation Drawer', 1)
        print("✓ Injected Garden Planner Event Listeners")

    # 9. Also add direct planner launcher inside renderGardenAreasManager row
    area_row_target = '<input type="text" class="garden-area-input"'
    if 'planner-row-btn' not in content:
        # add a small sparkles button in each row
        replacement_row = '''<button type="button" class="btn-icon planner-row-btn" data-area-idx="${idx}" title="Get plant recommendations for this area" aria-label="Get plant recommendations for ${escapeHtml(areaName)}" style="color:var(--primary);padding:3px;margin-right:2px;">
            <i data-lucide="sparkles" style="width:13px;height:13px;"></i>
          </button>
          <input type="text" class="garden-area-input"'''
        content = content.replace(area_row_target, replacement_row, 1)

        # and in renderGardenAreasManager, wire up planner-row-btn:
        row_wire_target = "container.appendChild(row);"
        row_wire_code = '''row.querySelector('.planner-row-btn')?.addEventListener('click', () => {
          closeDrawer();
          openGardenPlanner(idx);
        });
        '''
        content = content.replace(row_wire_target, row_wire_code + row_wire_target, 1)
        print("✓ Injected direct planner trigger into garden area rows")

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully patched index.html with Garden Area Planner!")

if __name__ == '__main__':
    patch_index_html()
