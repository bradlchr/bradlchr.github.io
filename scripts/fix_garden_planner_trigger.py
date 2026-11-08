#!/usr/bin/env python3
"""
Fix garden planner button triggers and initialization across all test files:
1. Add onclick="openGardenPlanner()" to #gardenPlannerHeaderBtn
2. Export window.openGardenPlanner and window.openPlannerGuestGatewayModal
3. Wrap openGardenPlanner and openPlannerGuestGatewayModal in robust try/catch with fallback
4. Ensure initApp runs whether document.readyState is 'loading', 'interactive', or 'complete'
5. Add onclick to drawer and profile planner buttons
"""

import sys

FILES_TO_PATCH = [
    'index.html',
    'test.html',
    'test/index.html',
    '/home/droid/.cache/bradlchr.github.io/test.html',
    '/home/droid/.cache/bradlchr.github.io/test/index.html',
    '/home/droid/.cache/deep-roots-nature-advisors/index.html'
]

def patch_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Skipping {filepath}: {e}")
        return

    # 1. Update button in header to include onclick="openGardenPlanner()" and type="button"
    old_btn = '<button id="gardenPlannerHeaderBtn" class="btn btn-planner"'
    new_btn = '<button id="gardenPlannerHeaderBtn" type="button" class="btn btn-planner" onclick="openGardenPlanner()"'
    if old_btn in content and 'onclick="openGardenPlanner()"' not in content:
        content = content.replace(old_btn, new_btn, 1)
        print(f"  ✓ Added onclick to header button in {filepath}")

    # 2. Update staging drawer button to include onclick
    old_staging_btn = '<button type="button" id="openPlannerFromStagingBtn" class="btn-text-action"'
    new_staging_btn = '<button type="button" id="openPlannerFromStagingBtn" onclick="closeDrawer(); openGardenPlanner();" class="btn-text-action"'
    if old_staging_btn in content and 'onclick="closeDrawer(); openGardenPlanner();"' not in content:
        content = content.replace(old_staging_btn, new_staging_btn, 1)
        print(f"  ✓ Added onclick to staging drawer button in {filepath}")

    # 3. Update profile tile button to include onclick
    old_profile_btn = '<button id="profileOpenPlannerBtn" type="button" class="profile-tile-btn">'
    new_profile_btn = '<button id="profileOpenPlannerBtn" type="button" onclick="document.getElementById(\'userProfileModal\')?.close(); openGardenPlanner();" class="profile-tile-btn">'
    if old_profile_btn in content and 'onclick="document.getElementById' not in content:
        content = content.replace(old_profile_btn, new_profile_btn, 1)
        print(f"  ✓ Added onclick to profile tile button in {filepath}")

    # 4. Robust openGardenPlanner with try/catch, fallback, and window export
    old_open_planner_signature = '    function openGardenPlanner(targetAreaIdx = null) {'
    new_open_planner = '''    function openGardenPlanner(targetAreaIdx = null) {
      try {
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
          if (typeof modal.showModal === 'function') {
            modal.showModal();
          } else {
            modal.setAttribute('open', '');
          }
          if (window.lucide) lucide.createIcons();
        }
      } catch (err) {
        console.error("Error opening garden planner:", err);
        showToast("Error opening Garden Planner: " + err.message, "danger");
      }
    }
    window.openGardenPlanner = openGardenPlanner;

    function openPlannerGuestGatewayModal() {
      try {
        const modal = document.getElementById('plannerGuestModal');
        if (modal) {
          if (typeof modal.showModal === 'function') {
            modal.showModal();
          } else {
            modal.setAttribute('open', '');
          }
          if (window.lucide) lucide.createIcons();
        } else {
          openLoginModal();
        }
      } catch (err) {
        console.error("Error opening guest gateway modal:", err);
        openLoginModal();
      }
    }
    window.openPlannerGuestGatewayModal = openPlannerGuestGatewayModal;'''

    # Replace the old function definitions
    if 'window.openGardenPlanner = openGardenPlanner;' not in content:
        # find old openGardenPlanner and openPlannerGuestGatewayModal
        start_p = content.find('    function openGardenPlanner(targetAreaIdx = null) {')
        end_p = content.find('    function initGardenAreaProfiles() {', start_p)
        if start_p != -1 and end_p != -1:
            content = content[:start_p] + new_open_planner + '\n\n' + content[end_p:]
            print(f"  ✓ Upgraded openGardenPlanner & window exports in {filepath}")

    # 5. Make App Initialization readyState resilient
    old_init = '''    // App Initialization
    window.addEventListener('DOMContentLoaded', () => {
      try { loadMasterPlants(); } catch(e) { console.error('loadMasterPlants error:', e); }
      try { setupEventListeners(); } catch(e) { console.error('setupEventListeners error:', e); }
      try { initAdvisorAuth(); } catch(e) { console.error('initAdvisorAuth error:', e); }
      try { renderGardenAreasManager(); } catch(e) { console.error('renderGardenAreasManager error:', e); }
      try { renderStagedInvasives(); } catch(e) { console.error('renderStagedInvasives error:', e); }
      try { renderStaging(); } catch(e) { console.error('renderStaging error:', e); }
      try { syncReportOptionsUI(); } catch(e) { console.error('syncReportOptionsUI error:', e); }
      if (window.lucide) {
        try { lucide.createIcons(); } catch(e) {}
      }
    });'''

    new_init = '''    // App Initialization
    function initializeApplication() {
      try { loadMasterPlants(); } catch(e) { console.error('loadMasterPlants error:', e); }
      try { setupEventListeners(); } catch(e) { console.error('setupEventListeners error:', e); }
      try { initAdvisorAuth(); } catch(e) { console.error('initAdvisorAuth error:', e); }
      try { renderGardenAreasManager(); } catch(e) { console.error('renderGardenAreasManager error:', e); }
      try { renderStagedInvasives(); } catch(e) { console.error('renderStagedInvasives error:', e); }
      try { renderStaging(); } catch(e) { console.error('renderStaging error:', e); }
      try { syncReportOptionsUI(); } catch(e) { console.error('syncReportOptionsUI error:', e); }
      if (window.lucide) {
        try { lucide.createIcons(); } catch(e) {}
      }
    }

    if (document.readyState === 'loading') {
      window.addEventListener('DOMContentLoaded', initializeApplication);
    } else {
      initializeApplication();
    }'''

    if old_init in content:
        content = content.replace(old_init, new_init, 1)
        print(f"  ✓ Patched resilient readyState initialization in {filepath}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Completed patching {filepath}")

def main():
    for f in FILES_TO_PATCH:
        print(f"Patching {f}...")
        patch_file(f)

if __name__ == '__main__':
    main()
