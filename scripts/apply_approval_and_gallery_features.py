#!/usr/bin/env python3
"""
Applies native plant gallery, lightbox, and 2-tier approval workflow to index.html.
"""
import sys

def apply_updates():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update state definition to include plantApprovals
    old_state = "      stagedInvasives: JSON.parse(localStorage.getItem('dr_staged_invasives') || '[]'),\n      reportOptions: JSON.parse"
    new_state = "      stagedInvasives: JSON.parse(localStorage.getItem('dr_staged_invasives') || '[]'),\n      plantApprovals: JSON.parse(localStorage.getItem('dr_plant_approvals') || '[]'),\n      reportOptions: JSON.parse"
    if old_state in content:
        content = content.replace(old_state, new_state, 1)
        print("Updated state definition")
    else:
        print("Warning: old_state pattern not found!")

    # 2. Update loadMasterPlants to check cache MOBOT validity and fetch plant approvals
    old_load = """      // 1. Initial load from local Firestore cache or embedded master catalog
      const cached = localStorage.getItem('dr_firestore_cache_plants');
      if (cached) {
        try {
          const parsedCache = JSON.parse(cached);
          if (Array.isArray(parsedCache) && parsedCache.length > 50) {
            state.allPlants = parsedCache;
            document.getElementById('dbEngineTxt').textContent = 'Cloud Firestore (Cached)';
          }
        } catch (e) {}
      }"""

    new_load = """      // 1. Initial load from local Firestore cache or embedded master catalog
      const raw = document.getElementById('embeddedMasterPlants')?.textContent;
      let embeddedList = [];
      if (raw) {
        try { embeddedList = JSON.parse(raw); } catch (e) {}
      }

      const cached = localStorage.getItem('dr_firestore_cache_plants');
      if (cached) {
        try {
          const parsedCache = JSON.parse(cached);
          const hasMobot = parsedCache.some(p => p.plantfinder_url || (p.images && p.images.some(img => img.url && img.url.includes('mobot.org'))));
          if (hasMobot && Array.isArray(parsedCache) && parsedCache.length > 50) {
            state.allPlants = parsedCache;
            document.getElementById('dbEngineTxt').textContent = 'Cloud Firestore (Cached)';
          }
        } catch (e) {}
      }

      if (!state.allPlants || state.allPlants.length === 0) {
        state.allPlants = embeddedList;
      }"""

    if old_load in content:
        content = content.replace(old_load, new_load, 1)
        print("Updated loadMasterPlants cache check")
    else:
        print("Warning: old_load pattern not found!")

    # Also in loadMasterPlants, fetch approvals:
    old_load_end = """      // 3. Attempt live sync from database endpoints
      await tryLiveSyncFromDatabase(false);

      applyFilters();
      updateHeaderInfo();
    }"""

    new_load_end = """      // 3. Attempt live sync from database endpoints
      await tryLiveSyncFromDatabase(false);

      try {
        fetchPlantApprovalsFromFirestore().then(() => {
          updateApprovalBadges();
          if (state.catalogMode === 'native') applyFilters();
        }).catch(() => {});
      } catch(e) {}

      applyFilters();
      updateHeaderInfo();
    }"""

    if old_load_end in content:
        content = content.replace(old_load_end, new_load_end, 1)
        print("Updated loadMasterPlants end to fetch approvals")
    else:
        print("Warning: old_load_end pattern not found!")

    # 3. Update renderAuthUser to show/hide openAddPlantBtn and update approvals badge
    old_auth_user = """        const firstName = u.name.split(' ')[0];
        const isAdmin = u.isAdmin;
        container.innerHTML = `
          <button id="userProfileBtn" class="btn btn-secondary user-profile-header-btn" style="padding:4px 10px;gap:8px;" title="View Advisor Profile (${escapeHtml(u.name)})">
            ${u.photoURL ? `<img src="${u.photoURL}" style="width:24px;height:24px;border-radius:50%;object-fit:cover;">` : `
              <div class="user-avatar-initials" style="width:24px;height:24px;border-radius:50%;background:var(--primary);color:#fff;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;">
                ${getUserInitials(u)}
              </div>
            `}
            <span class="user-profile-name" style="font-size:12px;font-weight:700;">${firstName}</span>
            ${isAdmin ? `<span class="role-badge admin profile-header-role-badge" style="font-size:10px;padding:1px 6px;">Admin</span>` : ''}
          </button>
        `;
        document.getElementById('userProfileBtn').addEventListener('click', openUserProfileModal);"""

    new_auth_user = """        const firstName = u.name.split(' ')[0];
        const isAdmin = u.isAdmin;
        container.innerHTML = `
          <button id="userProfileBtn" class="btn btn-secondary user-profile-header-btn" style="padding:4px 10px;gap:8px;" title="View Advisor Profile (${escapeHtml(u.name)})">
            ${u.photoURL ? `<img src="${u.photoURL}" style="width:24px;height:24px;border-radius:50%;object-fit:cover;">` : `
              <div class="user-avatar-initials" style="width:24px;height:24px;border-radius:50%;background:var(--primary);color:#fff;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;">
                ${getUserInitials(u)}
              </div>
            `}
            <span class="user-profile-name" style="font-size:12px;font-weight:700;">${firstName}</span>
            ${isAdmin ? `<span class="role-badge admin profile-header-role-badge" style="font-size:10px;padding:1px 6px;">Admin</span>` : ''}
          </button>
        `;
        document.getElementById('userProfileBtn').addEventListener('click', openUserProfileModal);

        const addPlantBtn = document.getElementById('openAddPlantBtn');
        if (addPlantBtn) addPlantBtn.style.display = 'inline-flex';
        updateApprovalBadges();"""

    if old_auth_user in content:
        content = content.replace(old_auth_user, new_auth_user, 1)
        print("Updated renderAuthUser signed-in branch")
    else:
        print("Warning: old_auth_user pattern not found!")

    old_auth_guest = """        container.innerHTML = `
          <button id="headerSignInBtn" class="btn btn-secondary" style="font-weight:700;">
            <i data-lucide="user-check"></i>
            <span class="btn-text-long">Advisor Sign In</span>
            <span class="btn-text-short">Sign In</span>
          </button>
        `;"""

    new_auth_guest = """        const addPlantBtn = document.getElementById('openAddPlantBtn');
        if (addPlantBtn) addPlantBtn.style.display = 'none';

        container.innerHTML = `
          <button id="headerSignInBtn" class="btn btn-secondary" style="font-weight:700;">
            <i data-lucide="user-check"></i>
            <span class="btn-text-long">Advisor Sign In</span>
            <span class="btn-text-short">Sign In</span>
          </button>
        `;"""

    if old_auth_guest in content:
        content = content.replace(old_auth_guest, new_auth_guest, 1)
        print("Updated renderAuthUser guest branch")
    else:
        print("Warning: old_auth_guest pattern not found!")

    # 4. Update openUserProfileModal to show profileAddPlantBtn and openAdminApprovalsBtn
    old_profile_modal = """      const adminBtn = document.getElementById('openAdminConsoleBtn');
      if (adminBtn) {
        adminBtn.style.display = u.isAdmin ? 'inline-flex' : 'none';
      }

      updateTextScaleUI(getUserTextScale());"""

    new_profile_modal = """      const profileAddPlantBtn = document.getElementById('profileAddPlantBtn');
      if (profileAddPlantBtn) {
        profileAddPlantBtn.style.display = 'inline-flex';
      }

      const openApprovalsBtn = document.getElementById('openAdminApprovalsBtn');
      if (openApprovalsBtn) {
        openApprovalsBtn.style.display = u.isAdmin ? 'inline-flex' : 'none';
        if (u.isAdmin) {
          updateApprovalBadges();
        }
      }

      const adminBtn = document.getElementById('openAdminConsoleBtn');
      if (adminBtn) {
        adminBtn.style.display = u.isAdmin ? 'inline-flex' : 'none';
      }

      updateTextScaleUI(getUserTextScale());"""

    if old_profile_modal in content:
        content = content.replace(old_profile_modal, new_profile_modal, 1)
        print("Updated openUserProfileModal")
    else:
        print("Warning: old_profile_modal pattern not found!")

    # 5. Update switchAdminTab to handle 'approvals' tab
    old_switch_tab = """    function switchAdminTab(tab) {
      const rosterTabBtn = document.getElementById('adminRosterTabBtn');
      const provisionTabBtn = document.getElementById('adminProvisionTabBtn');
      const reportsTabBtn = document.getElementById('adminReportsTabBtn');
      const rosterPanel = document.getElementById('adminRosterPanel');
      const provisionPanel = document.getElementById('adminProvisionPanel');
      const reportsPanel = document.getElementById('adminReportsPanel');

      if (tab === 'roster') {
        rosterTabBtn.classList.add('active');
        provisionTabBtn.classList.remove('active');
        reportsTabBtn?.classList.remove('active');
        rosterPanel.style.display = 'block';
        provisionPanel.style.display = 'none';
        if (reportsPanel) reportsPanel.style.display = 'none';
        renderAdminRoster(document.getElementById('adminRosterSearchInput')?.value || '');
      } else if (tab === 'provision') {
        provisionTabBtn.classList.add('active');
        rosterTabBtn.classList.remove('active');
        reportsTabBtn?.classList.remove('active');
        rosterPanel.style.display = 'none';
        provisionPanel.style.display = 'block';
        if (reportsPanel) reportsPanel.style.display = 'none';
        updateCanonicalPreview();
      } else if (tab === 'reports') {
        reportsTabBtn?.classList.add('active');
        rosterTabBtn.classList.remove('active');
        provisionTabBtn.classList.remove('active');
        rosterPanel.style.display = 'none';
        provisionPanel.style.display = 'none';
        if (reportsPanel) reportsPanel.style.display = 'block';
        fetchAllAdvisorReports().then(() => {
          renderAdminReportsRepository(
            document.getElementById('adminReportsSearchInput')?.value || '',
            document.getElementById('adminReportsAdvisorFilter')?.value || '',
            document.getElementById('adminReportsSortSelect')?.value || 'newest'
          );
        });
      }
      if (window.lucide) lucide.createIcons();
    }"""

    new_switch_tab = """    function switchAdminTab(tab) {
      const rosterTabBtn = document.getElementById('adminRosterTabBtn');
      const provisionTabBtn = document.getElementById('adminProvisionTabBtn');
      const reportsTabBtn = document.getElementById('adminReportsTabBtn');
      const approvalsTabBtn = document.getElementById('adminApprovalsTabBtn');
      const rosterPanel = document.getElementById('adminRosterPanel');
      const provisionPanel = document.getElementById('adminProvisionPanel');
      const reportsPanel = document.getElementById('adminReportsPanel');
      const approvalsPanel = document.getElementById('adminApprovalsPanel');

      if (tab === 'roster') {
        rosterTabBtn.classList.add('active');
        provisionTabBtn.classList.remove('active');
        reportsTabBtn?.classList.remove('active');
        approvalsTabBtn?.classList.remove('active');
        rosterPanel.style.display = 'block';
        provisionPanel.style.display = 'none';
        if (reportsPanel) reportsPanel.style.display = 'none';
        if (approvalsPanel) approvalsPanel.style.display = 'none';
        renderAdminRoster(document.getElementById('adminRosterSearchInput')?.value || '');
      } else if (tab === 'provision') {
        provisionTabBtn.classList.add('active');
        rosterTabBtn.classList.remove('active');
        reportsTabBtn?.classList.remove('active');
        approvalsTabBtn?.classList.remove('active');
        rosterPanel.style.display = 'none';
        provisionPanel.style.display = 'block';
        if (reportsPanel) reportsPanel.style.display = 'none';
        if (approvalsPanel) approvalsPanel.style.display = 'none';
        updateCanonicalPreview();
      } else if (tab === 'reports') {
        reportsTabBtn?.classList.add('active');
        rosterTabBtn.classList.remove('active');
        provisionTabBtn.classList.remove('active');
        approvalsTabBtn?.classList.remove('active');
        rosterPanel.style.display = 'none';
        provisionPanel.style.display = 'none';
        if (reportsPanel) reportsPanel.style.display = 'block';
        if (approvalsPanel) approvalsPanel.style.display = 'none';
        fetchAllAdvisorReports().then(() => {
          renderAdminReportsRepository(
            document.getElementById('adminReportsSearchInput')?.value || '',
            document.getElementById('adminReportsAdvisorFilter')?.value || '',
            document.getElementById('adminReportsSortSelect')?.value || 'newest'
          );
        });
      } else if (tab === 'approvals') {
        approvalsTabBtn?.classList.add('active');
        rosterTabBtn.classList.remove('active');
        provisionTabBtn.classList.remove('active');
        reportsTabBtn?.classList.remove('active');
        rosterPanel.style.display = 'none';
        provisionPanel.style.display = 'none';
        if (reportsPanel) reportsPanel.style.display = 'none';
        if (approvalsPanel) approvalsPanel.style.display = 'block';
        fetchPlantApprovalsFromFirestore().then(() => {
          renderAdminApprovals(document.getElementById('adminApprovalsSearchInput')?.value || '');
        });
      }
      if (window.lucide) lucide.createIcons();
    }"""

    if old_switch_tab in content:
        content = content.replace(old_switch_tab, new_switch_tab, 1)
        print("Updated switchAdminTab")
    else:
        print("Warning: old_switch_tab pattern not found!")

    # 6. Update createPlantCard with photo count badge and pending approval badge
    old_card_media = """          <div class="card-media">
            ${imgUrl ? `<img src="${imgUrl}" alt="${commonName}" loading="lazy" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1598880940371-c756e015fea1?auto=format&fit=crop&w=600&q=80';">` : `
              <div class="card-placeholder">
                <i data-lucide="sprout" style="width:36px;height:36px;"></i>
                <span style="font-size:11px;">Botanical Record</span>
              </div>
            `}
            <div class="card-badges">
              ${isSweet16(plant) ? `<span class="badge-sweet16">⭐ Sweet 16</span>` : ''}
              ${isKcKeystone(plant) ? `<span class="badge-keystone">🌿 Keystone</span>` : ''}
            </div>
            ${layerStr ? `<span class="badge-layer">${layerStr}</span>` : ''}
          </div>"""

    new_card_media = """          <div class="card-media">
            ${imgUrl ? `<img src="${imgUrl}" alt="${commonName}" loading="lazy" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1598880940371-c756e015fea1?auto=format&fit=crop&w=600&q=80';">` : `
              <div class="card-placeholder">
                <i data-lucide="sprout" style="width:36px;height:36px;"></i>
                <span style="font-size:11px;">Botanical Record</span>
              </div>
            `}
            ${(plant.images && plant.images.length > 1) ? `
              <span class="card-photo-count-badge" style="position:absolute;bottom:6px;right:6px;background:rgba(0,0,0,0.72);color:#fff;font-size:10px;font-weight:700;padding:2px 7px;border-radius:12px;display:flex;align-items:center;gap:4px;backdrop-filter:blur(3px);z-index:2;" title="${plant.images.length} botanical photos courtesy Missouri Botanical Garden PlantFinder">
                <i data-lucide="camera" style="width:11px;height:11px;"></i>
                <span>${plant.images.length}</span>
              </span>
            ` : ''}
            ${(state.plantApprovals || []).some(a => a.status === 'pending' && (a.plant_id === plant.id || a.scientific_name === plant.scientific_name)) ? `
              <span style="position:absolute;top:6px;left:6px;background:#f59e0b;color:#1e293b;font-size:10px;font-weight:800;padding:2px 6px;border-radius:4px;display:flex;align-items:center;gap:3px;box-shadow:0 2px 4px rgba(0,0,0,0.3);z-index:2;" title="Proposed edits are pending Administrator approval">
                <i data-lucide="clock" style="width:10px;height:10px;"></i>
                <span>Pending Review</span>
              </span>
            ` : ''}
            <div class="card-badges">
              ${isSweet16(plant) ? `<span class="badge-sweet16">⭐ Sweet 16</span>` : ''}
              ${isKcKeystone(plant) ? `<span class="badge-keystone">🌿 Keystone</span>` : ''}
            </div>
            ${layerStr ? `<span class="badge-layer">${layerStr}</span>` : ''}
          </div>"""

    if old_card_media in content:
        content = content.replace(old_card_media, new_card_media, 1)
        print("Updated createPlantCard media section")
    else:
        print("Warning: old_card_media pattern not found!")

    # 7. Add renderPlantGallery and openPlantLightbox before openPlantDetail
    # and update openPlantDetail to call renderPlantGallery and toggle pending approval notice
    old_detail_start = """    // Plant Detail Modal
    function openPlantDetail(plant) {
      state.activeModalPlant = plant;
      const modal = document.getElementById('plantDetailModal');
      const showSciFirst = shouldShowScientificFirst();
      const commonName = (plant.common_names && plant.common_names[0]) || plant.scientific_name;
      const primaryName = showSciFirst ? (plant.scientific_name || commonName) : commonName;
      const secondaryName = showSciFirst ? commonName : (plant.scientific_name || '');

      const modalCommon = document.getElementById('modalCommonName');
      const modalSci = document.getElementById('modalSciName');
      if (modalCommon) {
        modalCommon.textContent = primaryName;
        modalCommon.style.fontStyle = showSciFirst ? 'italic' : 'normal';
      }
      if (modalSci) {
        modalSci.textContent = secondaryName;
        modalSci.style.fontStyle = showSciFirst ? 'normal' : 'italic';
      }
      
      const badgeContainer = document.getElementById('modalBadges');
      if (badgeContainer) {
        let bHtml = '';
        if (isSweet16(plant)) bHtml += '<span class="badge-sweet16" style="font-size:11px;padding:3px 9px;">⭐ Deep Roots Sweet 16</span>';
        if (isKcKeystone(plant)) bHtml += '<span class="badge-keystone" style="font-size:11px;padding:3px 9px;">🌿 KC Keystone Species</span>';
        badgeContainer.innerHTML = bHtml;
        badgeContainer.style.display = bHtml ? 'flex' : 'none';
      }
      
      const img = document.getElementById('modalImg');
      const imgAttr = document.getElementById('modalImgAttr');
      if (plant.images && plant.images[0] && plant.images[0].url) {
        img.src = plant.images[0].url;
        img.onerror = function() {
          this.onerror = null;
          this.src = 'https://images.unsplash.com/photo-1598880940371-c756e015fea1?auto=format&fit=crop&w=800&q=80';
        };
        img.style.display = 'block';
        imgAttr.textContent = `Photo: ${plant.images[0].attribution_name || plant.images[0].source || 'Missouri Botanical Garden / Grow Native!'} ${plant.images[0].license ? '· ' + plant.images[0].license : ''}`;
      } else {
        img.style.display = 'none';
        imgAttr.textContent = 'Botanical record';
      }"""

    new_detail_start = """    // Botanical Multi-Image Gallery & Fullscreen Lightbox
    function renderPlantGallery(plant) {
      const container = document.getElementById('modalPlantGalleryContainer');
      if (!container) return;

      const images = (plant.images && Array.isArray(plant.images) && plant.images.length > 0) ? plant.images : [];
      const plantfinderUrl = plant.plantfinder_url || (images[0] && images[0].source_url) || getPlantUrl(plant);

      if (images.length === 0) {
        container.innerHTML = `
          <div style="background:var(--bg-base);border:1px dashed var(--border-subtle);border-radius:var(--radius-md);padding:24px;text-align:center;margin-bottom:14px;">
            <i data-lucide="sprout" style="width:36px;height:36px;color:var(--text-muted);margin:0 auto 8px auto;display:block;"></i>
            <p style="font-size:13px;color:var(--text-muted);margin:0;">Botanical Record · No specimen imagery cataloged yet</p>
          </div>
        `;
        if (window.lucide) lucide.createIcons();
        return;
      }

      const isMobot = images.some(img => (img.attribution_name && img.attribution_name.includes('Missouri Botanical Garden')) || (img.license && img.license.includes('Missouri Botanical Garden')) || (img.url && img.url.includes('mobot.org')));
      const sourceCredit = isMobot ? 'Courtesy Missouri Botanical Garden PlantFinder' : (images[0].attribution_name || images[0].source || 'Missouri Botanical Garden PlantFinder');

      container.innerHTML = `
        <div style="margin-bottom:16px;">
          <div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.04em;color:var(--text-secondary);margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px;">
            <div style="display:flex;align-items:center;gap:6px;">
              <i data-lucide="camera" style="width:14px;height:14px;color:var(--primary);"></i>
              <span>Botanical Photo Gallery (${images.length})</span>
            </div>
            <a href="${plantfinderUrl}" target="_blank" rel="noopener noreferrer" style="font-size:11px;color:var(--primary);font-weight:600;text-transform:none;display:inline-flex;align-items:center;gap:4px;text-decoration:none;" title="Open Missouri Botanical Garden PlantFinder profile for ${escapeHtml(plant.scientific_name)}">
              <span>${sourceCredit}</span>
              <i data-lucide="external-link" style="width:11px;height:11px;"></i>
            </a>
          </div>

          <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(130px, 1fr));gap:10px;">
            ${images.map((img, idx) => {
              const thumbUrl = img.thumbnail_url || (img.url && img.url.includes('/large960/') ? img.url.replace('/large960/', '/small240/') : img.url);
              const label = img.label || (idx === 0 ? 'Specimen' : `View ${idx + 1}`);
              const credit = img.license || img.attribution_name || 'Courtesy Missouri Botanical Garden PlantFinder';
              const linkUrl = img.source_url || plantfinderUrl;

              return `
                <div class="native-gallery-photo-card" data-idx="${idx}" tabindex="0" role="button" aria-label="View photo ${idx + 1}: ${escapeHtml(label)} in full size" style="border-radius:var(--radius-md);overflow:hidden;border:1px solid var(--border-subtle);background:var(--bg-base);cursor:pointer;transition:transform 0.15s,box-shadow 0.15s;outline:none;" title="Click to view full-size photo">
                  <div style="height:115px;overflow:hidden;background:#051b11;position:relative;">
                    <img src="${thumbUrl}" alt="${escapeHtml(label)} - ${escapeHtml(plant.common_names?.[0] || plant.scientific_name)}" style="width:100%;height:100%;object-fit:cover;transition:transform 0.2s;" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1598880940371-c756e015fea1?auto=format&fit=crop&w=400&q=80';">
                    <span style="position:absolute;bottom:5px;right:5px;background:rgba(0,0,0,0.72);color:#fff;font-size:9px;padding:2px 6px;border-radius:4px;display:flex;align-items:center;gap:3px;backdrop-filter:blur(2px);">
                      <i data-lucide="maximize-2" style="width:10px;height:10px;"></i>
                      <span>Full size</span>
                    </span>
                  </div>
                  <div style="padding:7px 8px;">
                    <span style="font-weight:700;font-size:11px;color:var(--primary);display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${escapeHtml(label)}</span>
                    <div style="font-size:9px;color:var(--text-secondary);margin-top:4px;border-top:1px dashed var(--border-subtle);padding-top:4px;line-height:1.2;">
                      <a href="${linkUrl}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation();" style="color:inherit;text-decoration:none;display:inline-flex;align-items:center;gap:2px;" title="View on Missouri Botanical Garden PlantFinder">
                        <span>${escapeHtml(credit)}</span>
                        <i data-lucide="external-link" style="width:8px;height:8px;"></i>
                      </a>
                    </div>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      `;

      container.querySelectorAll('.native-gallery-photo-card').forEach(card => {
        const handler = () => {
          const idx = parseInt(card.getAttribute('data-idx'), 10) || 0;
          openPlantLightbox(plant, idx);
        };
        card.addEventListener('click', handler);
        card.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            handler();
          }
        });
      });

      if (window.lucide) lucide.createIcons();
    }
    window.renderPlantGallery = renderPlantGallery;

    function openPlantLightbox(plant, initialIdx = 0) {
      let modal = document.getElementById('plantLightboxModal');
      if (!modal) {
        modal = document.createElement('dialog');
        modal.id = 'plantLightboxModal';
        modal.setAttribute('aria-modal', 'true');
        modal.setAttribute('aria-label', 'Full size botanical photo preview');
        modal.className = 'lightbox-dialog';
        modal.style.cssText = 'max-width: 95vw; width: 920px; max-height: 94vh; border: 1px solid rgba(255,255,255,0.18); border-radius: var(--radius-lg); padding: 0; box-shadow: 0 25px 60px rgba(0,0,0,0.85); background: #07130c; color: #f8fafc; overflow: hidden;';
        document.body.appendChild(modal);

        modal.addEventListener('click', (e) => {
          if (e.target === modal) modal.close();
        });
      }

      const images = (plant.images && plant.images.length > 0) ? plant.images : [{
        url: 'https://images.unsplash.com/photo-1598880940371-c756e015fea1?auto=format&fit=crop&w=800&q=80',
        label: 'Botanical Record',
        caption: plant.common_names?.[0] || plant.scientific_name,
        attribution_name: 'Courtesy Missouri Botanical Garden PlantFinder',
        license: 'Courtesy Missouri Botanical Garden PlantFinder',
        source_name: 'Missouri Botanical Garden PlantFinder',
        source_url: plant.plantfinder_url || getPlantUrl(plant)
      }];

      let currentIdx = Math.max(0, Math.min(initialIdx, images.length - 1));

      function renderSlide(idx) {
        currentIdx = idx;
        const img = images[currentIdx];
        const hasPrev = images.length > 1;
        const hasNext = images.length > 1;
        const plantfinderUrl = img.source_url || plant.plantfinder_url || getPlantUrl(plant);
        const credit = img.license || img.attribution_name || 'Courtesy Missouri Botanical Garden PlantFinder';
        const label = img.label || (currentIdx === 0 ? 'Specimen' : `View ${currentIdx + 1}`);

        let fullResUrl = img.url;
        if (fullResUrl && fullResUrl.includes('/small240/')) {
          fullResUrl = fullResUrl.replace('/small240/', '/large960/');
        }

        modal.innerHTML = `
          <div style="padding: 12px 18px; border-bottom: 1px solid rgba(255,255,255,0.12); display: flex; align-items: center; justify-content: space-between; background: #0c1e13;">
            <div style="display: flex; align-items: center; gap: 10px; overflow: hidden;">
              <span style="font-size: 16px;">🌿</span>
              <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                <span style="font-weight: 800; font-size: 15px; color: #86efac;">${escapeHtml(plant.common_names?.[0] || plant.scientific_name)}</span>
                <span style="font-style: italic; color: #a7f3d0; font-size: 12px; margin-left: 6px;">(${escapeHtml(plant.scientific_name)})</span>
              </div>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="font-size: 12px; font-weight: 700; color: #d1fae5; background: rgba(255,255,255,0.1); padding: 3px 8px; border-radius: 999px;">
                Photo ${currentIdx + 1} of ${images.length}
              </span>
              <a href="${plantfinderUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-secondary btn-sm" style="background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.2); color: #86efac; font-size: 11px; padding: 4px 8px; display: inline-flex; align-items: center; gap: 4px; text-decoration: none;" title="Open original plant info page on Missouri Botanical Garden PlantFinder">
                <i data-lucide="external-link" style="width: 12px; height: 12px;"></i>
                <span class="hide-mobile">MBG PlantFinder</span>
              </a>
              <button type="button" class="btn-icon" id="closePlantLightboxBtn" aria-label="Close photo preview" style="border: none; background: transparent; cursor: pointer; color: #cbd5e1; padding: 4px;" title="Close full size view">
                <i data-lucide="x" style="width: 20px; height: 20px;"></i>
              </button>
            </div>
          </div>

          <div style="position: relative; background: #030a06; display: flex; align-items: center; justify-content: center; min-height: 320px; max-height: 62vh; padding: 12px; overflow: hidden;">
            <img src="${fullResUrl}" alt="${escapeHtml(label)} - ${escapeHtml(plant.common_names?.[0] || plant.scientific_name)}" style="max-width: 100%; max-height: 60vh; object-fit: contain; border-radius: 6px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); user-select: none;" onerror="this.onerror=null; this.src='${img.url}';">

            ${hasPrev ? `
              <button type="button" id="plantLightboxPrevBtn" class="btn-icon" aria-label="Previous photo" style="position: absolute; left: 14px; top: 50%; transform: translateY(-50%); width: 40px; height: 40px; border-radius: 50%; background: rgba(12,30,19,0.85); border: 1px solid rgba(255,255,255,0.25); color: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.5); z-index: 5;" title="Previous Photo (Left Arrow)">
                <i data-lucide="chevron-left" style="width: 22px; height: 22px;"></i>
              </button>
            ` : ''}

            ${hasNext ? `
              <button type="button" id="plantLightboxNextBtn" class="btn-icon" aria-label="Next photo" style="position: absolute; right: 14px; top: 50%; transform: translateY(-50%); width: 40px; height: 40px; border-radius: 50%; background: rgba(12,30,19,0.85); border: 1px solid rgba(255,255,255,0.25); color: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.5); z-index: 5;" title="Next Photo (Right Arrow)">
                <i data-lucide="chevron-right" style="width: 22px; height: 22px;"></i>
              </button>
            ` : ''}
          </div>

          <div style="padding: 12px 18px; border-top: 1px solid rgba(255,255,255,0.1); background: #0a1910; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
            <div>
              <span style="font-weight: 700; font-size: 13px; color: #f0fdf4;">${escapeHtml(label)}</span>
              ${img.caption ? `<span style="font-size: 12px; color: #a7f3d0; margin-left: 6px;">· ${escapeHtml(img.caption)}</span>` : ''}
              <div style="font-size: 11px; color: #86efac; margin-top: 2px;">
                <span>${escapeHtml(credit)}</span>
              </div>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
              <a href="${plantfinderUrl}" target="_blank" rel="noopener noreferrer" style="font-size: 12px; color: #6ee7b7; text-decoration: underline; display: inline-flex; align-items: center; gap: 4px;">
                <span>View info on Missouri Botanical Garden</span>
                <i data-lucide="external-link" style="width: 12px; height: 12px;"></i>
              </a>
              <button type="button" class="btn btn-secondary btn-sm" id="plantLightboxCloseBtn" style="background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.2); color: #fff;">Close</button>
            </div>
          </div>
        `;

        modal.querySelector('#closePlantLightboxBtn')?.addEventListener('click', () => modal.close());
        modal.querySelector('#plantLightboxCloseBtn')?.addEventListener('click', () => modal.close());
        modal.querySelector('#plantLightboxPrevBtn')?.addEventListener('click', () => {
          renderSlide((currentIdx - 1 + images.length) % images.length);
        });
        modal.querySelector('#plantLightboxNextBtn')?.addEventListener('click', () => {
          renderSlide((currentIdx + 1) % images.length);
        });

        if (window.lucide) lucide.createIcons();
      }

      const keyHandler = (e) => {
        if (!modal.open) {
          window.removeEventListener('keydown', keyHandler);
          return;
        }
        if (e.key === 'ArrowLeft' && images.length > 1) {
          renderSlide((currentIdx - 1 + images.length) % images.length);
        } else if (e.key === 'ArrowRight' && images.length > 1) {
          renderSlide((currentIdx + 1) % images.length);
        } else if (e.key === 'Escape') {
          modal.close();
          window.removeEventListener('keydown', keyHandler);
        }
      };
      window.addEventListener('keydown', keyHandler);
      modal.addEventListener('close', () => window.removeEventListener('keydown', keyHandler), { once: true });

      renderSlide(currentIdx);
      modal.showModal();
    }
    window.openPlantLightbox = openPlantLightbox;

    // Plant Detail Modal
    function openPlantDetail(plant) {
      state.activeModalPlant = plant;
      const modal = document.getElementById('plantDetailModal');
      const showSciFirst = shouldShowScientificFirst();
      const commonName = (plant.common_names && plant.common_names[0]) || plant.scientific_name;
      const primaryName = showSciFirst ? (plant.scientific_name || commonName) : commonName;
      const secondaryName = showSciFirst ? commonName : (plant.scientific_name || '');

      const modalCommon = document.getElementById('modalCommonName');
      const modalSci = document.getElementById('modalSciName');
      if (modalCommon) {
        modalCommon.textContent = primaryName;
        modalCommon.style.fontStyle = showSciFirst ? 'italic' : 'normal';
      }
      if (modalSci) {
        modalSci.textContent = secondaryName;
        modalSci.style.fontStyle = showSciFirst ? 'normal' : 'italic';
      }
      
      const badgeContainer = document.getElementById('modalBadges');
      if (badgeContainer) {
        let bHtml = '';
        if (isSweet16(plant)) bHtml += '<span class="badge-sweet16" style="font-size:11px;padding:3px 9px;">⭐ Deep Roots Sweet 16</span>';
        if (isKcKeystone(plant)) bHtml += '<span class="badge-keystone" style="font-size:11px;padding:3px 9px;">🌿 KC Keystone Species</span>';
        badgeContainer.innerHTML = bHtml;
        badgeContainer.style.display = bHtml ? 'flex' : 'none';
      }

      // Check if there is an active pending approval for this plant
      const pendingApproval = (state.plantApprovals || []).find(a => a.status === 'pending' && (a.plant_id === plant.id || a.scientific_name === plant.scientific_name));
      const alertEl = document.getElementById('modalPendingApprovalAlert');
      if (alertEl) {
        if (pendingApproval) {
          alertEl.style.display = 'block';
          const txtEl = document.getElementById('modalPendingApprovalTxt');
          if (txtEl) {
            txtEl.textContent = `Proposed edits submitted by ${escapeHtml(pendingApproval.submitted_by_name || 'an advisor')} are pending Administrator review.`;
          }
        } else {
          alertEl.style.display = 'none';
        }
      }

      // Render Multi-Image Gallery Courtesy Missouri Botanical Garden PlantFinder
      renderPlantGallery(plant);
      const img = document.getElementById('modalImg');
      if (img) img.style.display = 'none';
      const imgAttr = document.getElementById('modalImgAttr');
      if (imgAttr) imgAttr.style.display = 'none';"""

    if old_detail_start in content:
        content = content.replace(old_detail_start, new_detail_start, 1)
        print("Updated openPlantDetail with renderPlantGallery and lightbox")
    else:
        print("Warning: old_detail_start pattern not found!")

    # 8. Update openEditModal and editPlantForm submit handler, add openAddPlantModal and addPlantForm
    old_edit_block = """    // Edit Plant Modal
    function openEditModal(plant) {
      if (!state.currentUser) {
        showToast("Please sign in as an advisor to edit plant records.", "warning");
        openLoginModal();
        return;
      }
      document.getElementById('editPlantId').value = plant.id || plant.scientific_name;
      document.getElementById('editCommonName').value = plant.common_names?.[0] || '';
      document.getElementById('editSciName').value = plant.scientific_name || '';
      document.getElementById('editOfficialUrl').value = getPlantUrl(plant);
      document.getElementById('editAdvisorDesc').value = getPlantDesc(plant);
      document.getElementById('editLight').value = (plant.light_requirements || []).join(', ');
      document.getElementById('editMoisture').value = (plant.moisture_requirements || []).join(', ');
      document.getElementById('editHeight').value = getPlantHeight(plant);
      document.getElementById('editSociability').value = getPlantSociability(plant);
      const colors = plant.bloom_color || plant.bloomColor || plant.bloom_colors || [];
      document.getElementById('editBloomColor').value = Array.isArray(colors) ? colors.join(', ') : String(colors || '');
      const seasons = plant.bloom_period || plant.bloomSeason || plant.bloom_seasons || [];
      document.getElementById('editBloomPeriod').value = Array.isArray(seasons) ? seasons.join(', ') : String(seasons || '');
      document.getElementById('editImageUrl').value = plant.images?.[0]?.url || '';
      document.getElementById('editImageAttr').value = plant.images?.[0]?.attribution_name || plant.images?.[0]?.source || '';
      
      document.getElementById('editPlantModal').showModal();
    }

    document.getElementById('editPlantForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!state.currentUser) {
        showToast("Please sign in as an advisor to edit plant records.", "warning");
        openLoginModal();
        return;
      }

      const id = document.getElementById('editPlantId').value;
      const plant = state.allPlants.find(p => p.id === id || p.scientific_name === id);
      if (plant) {
        const edits = {
          common_names: [document.getElementById('editCommonName').value],
          scientific_name: document.getElementById('editSciName').value,
          plant_url: document.getElementById('editOfficialUrl').value,
          advisor_description: document.getElementById('editAdvisorDesc').value,
          light_requirements: document.getElementById('editLight').value.split(',').map(s => s.trim()).filter(Boolean),
          moisture_requirements: document.getElementById('editMoisture').value.split(',').map(s => s.trim()).filter(Boolean),
          height_display: document.getElementById('editHeight').value,
          sociability: document.getElementById('editSociability').value,
          bloom_color: document.getElementById('editBloomColor').value.split(',').map(s => s.trim()).filter(Boolean),
          bloomColor: document.getElementById('editBloomColor').value.split(',').map(s => s.trim()).filter(Boolean),
          bloom_period: document.getElementById('editBloomPeriod').value.split(',').map(s => s.trim()).filter(Boolean),
          bloomSeason: document.getElementById('editBloomPeriod').value.split(',').map(s => s.trim()).filter(Boolean),
          last_edited_by_user_id: state.currentUser.id || state.currentUser.username,
          last_edited_by_user_name: state.currentUser.name || `${state.currentUser.firstName} ${state.currentUser.lastName}`,
          last_edited_by_user_email: state.currentUser.email || '',
          last_edited_timestamp: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          updated_by: state.currentUser.name || state.currentUser.username
        };

        const imgUrl = document.getElementById('editImageUrl').value;
        if (imgUrl) {
          edits.images = [{
            url: imgUrl,
            attribution_name: document.getElementById('editImageAttr').value,
            caption: edits.scientific_name
          }];
        }

        Object.assign(plant, edits);
        state.customPlants[id] = edits;
        localStorage.setItem('dr_custom_plants', JSON.stringify(state.customPlants));

        // Save to Firestore
        try {
          const pId = localStorage.getItem('dr_firestore_project_id') || 'deep-roots-nature-advisors';
          let dId = localStorage.getItem('dr_firestore_database_id');
          if (!dId || dId === '(default)') dId = 'deep-roots-nature-advisors';
          const firestoreUrl = `https://firestore.googleapis.com/v1/projects/${pId}/databases/${dId}/documents/plants/${encodeURIComponent(plant.id || plant.scientific_name)}`;
          fetch(firestoreUrl, {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              fields: {
                scientific_name: { stringValue: edits.scientific_name },
                common_names: { arrayValue: { values: edits.common_names.map(c => ({ stringValue: c })) } },
                plant_url: { stringValue: edits.plant_url },
                advisor_description: { stringValue: edits.advisor_description },
                height_display: { stringValue: edits.height_display },
                bloom_color: { arrayValue: { values: (edits.bloom_color || []).map(c => ({ stringValue: String(c) })) } },
                bloom_period: { arrayValue: { values: (edits.bloom_period || []).map(s => ({ stringValue: String(s) })) } },
                light_requirements: { arrayValue: { values: (edits.light_requirements || []).map(s => ({ stringValue: String(s) })) } },
                moisture_requirements: { arrayValue: { values: (edits.moisture_requirements || []).map(s => ({ stringValue: String(s) })) } },
                sociability: { stringValue: edits.sociability || '' },
                last_edited_by_user_id: { stringValue: edits.last_edited_by_user_id },
                last_edited_by_user_name: { stringValue: edits.last_edited_by_user_name },
                last_edited_by_user_email: { stringValue: edits.last_edited_by_user_email },
                last_edited_timestamp: { stringValue: edits.last_edited_timestamp },
                updated_at: { stringValue: edits.updated_at },
                updated_by: { stringValue: edits.updated_by }
              }
            })
          }).catch(() => {});
        } catch (e) {}

        applyFilters();
        updateHeaderInfo();
        showToast(`Saved changes for ${plant.common_names[0]}! (Author: ${edits.last_edited_by_user_name})`);
      }
      document.getElementById('editPlantModal').close();
    });"""

    new_edit_block = """    // ==================== Plant Firestore & Approval Synchronization Engine ====================
    async function syncPlantToFirestore(plant) {
      try {
        const pId = localStorage.getItem('dr_firestore_project_id') || 'deep-roots-nature-advisors';
        let dId = localStorage.getItem('dr_firestore_database_id');
        if (!dId || dId === '(default)') dId = 'deep-roots-nature-advisors';
        const docId = encodeURIComponent(plant.id || plant.scientific_name);
        const firestoreUrl = `https://firestore.googleapis.com/v1/projects/${pId}/databases/${dId}/documents/plants/${docId}`;
        
        const docFields = {
          scientific_name: { stringValue: plant.scientific_name || '' },
          common_names: { arrayValue: { values: (plant.common_names || []).map(c => ({ stringValue: String(c) })) } },
          plant_url: { stringValue: getPlantUrl(plant) },
          advisor_description: { stringValue: getPlantDesc(plant) },
          height_display: { stringValue: getPlantHeight(plant) },
          bloom_color: { arrayValue: { values: (plant.bloom_color || plant.bloomColor || []).map(c => ({ stringValue: String(c) })) } },
          bloom_period: { arrayValue: { values: (plant.bloom_period || plant.bloomSeason || []).map(s => ({ stringValue: String(s) })) } },
          light_requirements: { arrayValue: { values: (plant.light_requirements || []).map(s => ({ stringValue: String(s) })) } },
          moisture_requirements: { arrayValue: { values: (plant.moisture_requirements || []).map(s => ({ stringValue: String(s) })) } },
          sociability: { stringValue: getPlantSociability(plant) },
          last_edited_by_user_id: { stringValue: plant.last_edited_by_user_id || '' },
          last_edited_by_user_name: { stringValue: plant.last_edited_by_user_name || '' },
          last_edited_by_user_email: { stringValue: plant.last_edited_by_user_email || '' },
          last_edited_timestamp: { stringValue: plant.last_edited_timestamp || new Date().toISOString() },
          updated_at: { stringValue: plant.updated_at || new Date().toISOString() },
          updated_by: { stringValue: plant.updated_by || 'Nature Advisor' }
        };

        if (plant.plantfinder_url) {
          docFields.plantfinder_url = { stringValue: plant.plantfinder_url };
        }
        if (plant.native_environment) {
          docFields.native_environment = { stringValue: plant.native_environment };
        }
        if (plant.architectural_layer) {
          docFields.architectural_layer = { stringValue: plant.architectural_layer };
        }
        if (plant.plant_type) {
          const pt = Array.isArray(plant.plant_type) ? plant.plant_type : [plant.plant_type];
          docFields.plant_type = { arrayValue: { values: pt.map(t => ({ stringValue: String(t) })) } };
        }
        if (plant.images && Array.isArray(plant.images) && plant.images.length > 0) {
          docFields.images = {
            arrayValue: {
              values: plant.images.slice(0, 15).map(img => ({
                mapValue: {
                  fields: {
                    url: { stringValue: img.url || '' },
                    thumbnail: { stringValue: img.thumbnail_url || img.thumbnail || '' },
                    attribution_name: { stringValue: img.attribution_name || img.attribution || 'Courtesy Missouri Botanical Garden PlantFinder' },
                    license: { stringValue: img.license || 'Courtesy Missouri Botanical Garden PlantFinder' },
                    caption: { stringValue: img.caption || '' },
                    attribution_url: { stringValue: img.source_url || plant.plantfinder_url || '' }
                  }
                }
              }))
            }
          };
        }

        await fetch(firestoreUrl, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ fields: docFields })
        });
      } catch (err) {
        console.warn('Firestore plant sync notice:', err);
      }
    }

    async function savePlantApprovalToFirestore(approval) {
      if (!approval || !approval.id) return;
      try {
        const pId = localStorage.getItem('dr_firestore_project_id') || 'deep-roots-nature-advisors';
        let dId = localStorage.getItem('dr_firestore_database_id');
        if (!dId || dId === '(default)') dId = 'deep-roots-nature-advisors';

        const jsonPayload = JSON.stringify(approval);
        const fields = {
          id: { stringValue: approval.id },
          type: { stringValue: approval.type || 'edit' },
          status: { stringValue: approval.status || 'pending' },
          plant_id: { stringValue: approval.plant_id || '' },
          scientific_name: { stringValue: approval.scientific_name || '' },
          common_name: { stringValue: approval.common_name || '' },
          submitted_by_id: { stringValue: approval.submitted_by_id || '' },
          submitted_by_name: { stringValue: approval.submitted_by_name || '' },
          submitted_by_email: { stringValue: approval.submitted_by_email || '' },
          submitted_at: { stringValue: approval.submitted_at || '' },
          reviewed_by_id: { stringValue: approval.reviewed_by_id || '' },
          reviewed_by_name: { stringValue: approval.reviewed_by_name || '' },
          reviewed_at: { stringValue: approval.reviewed_at || '' },
          raw_json: { stringValue: jsonPayload }
        };

        const primaryUrl = `https://firestore.googleapis.com/v1/projects/${pId}/databases/${dId}/documents/plant_approvals/${encodeURIComponent(approval.id)}`;
        fetch(primaryUrl, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ fields })
        }).catch(() => {});

        const fallbackUrl = `https://firestore.googleapis.com/v1/projects/${pId}/databases/${dId}/documents/plants/_approval_${encodeURIComponent(approval.id)}`;
        fetch(fallbackUrl, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            fields: {
              ...fields,
              scientific_name: { stringValue: `_approval_${approval.id}` }
            }
          })
        }).catch(() => {});
      } catch (e) {
        console.warn('savePlantApprovalToFirestore notice:', e);
      }
    }

    async function fetchPlantApprovalsFromFirestore() {
      const mergedMap = new Map();
      (state.plantApprovals || []).forEach(a => {
        if (a && a.id) mergedMap.set(a.id, a);
      });

      const pId = localStorage.getItem('dr_firestore_project_id') || 'deep-roots-nature-advisors';
      let dId = localStorage.getItem('dr_firestore_database_id');
      if (!dId || dId === '(default)') dId = 'deep-roots-nature-advisors';

      try {
        const url = `https://firestore.googleapis.com/v1/projects/${pId}/databases/${dId}/documents/plant_approvals?pageSize=200`;
        const res = await fetch(url);
        if (res.ok) {
          const data = await res.json();
          for (const doc of data.documents || []) {
            const rawJson = doc.fields?.raw_json?.stringValue;
            if (rawJson) {
              try {
                const parsed = JSON.parse(rawJson);
                if (parsed && parsed.id) mergedMap.set(parsed.id, parsed);
              } catch (e) {}
            }
          }
        }
      } catch (err) {}

      try {
        const url = `https://firestore.googleapis.com/v1/projects/${pId}/databases/${dId}/documents/plants?pageSize=300`;
        const res = await fetch(url);
        if (res.ok) {
          const data = await res.json();
          for (const doc of data.documents || []) {
            const docId = doc.name ? doc.name.split('/').pop() : '';
            if (docId.startsWith('_approval_')) {
              const rawJson = doc.fields?.raw_json?.stringValue;
              if (rawJson) {
                try {
                  const parsed = JSON.parse(rawJson);
                  if (parsed && parsed.id) mergedMap.set(parsed.id, parsed);
                } catch (e) {}
              }
            }
          }
        }
      } catch (err) {}

      state.plantApprovals = Array.from(mergedMap.values()).sort((a, b) => {
        return new Date(b.submitted_at || 0) - new Date(a.submitted_at || 0);
      });
      localStorage.setItem('dr_plant_approvals', JSON.stringify(state.plantApprovals));
      updateApprovalBadges();
      return state.plantApprovals;
    }

    function updateApprovalBadges() {
      const pendingCount = (state.plantApprovals || []).filter(a => a.status === 'pending').length;
      const b1 = document.getElementById('adminApprovalsTabBadge');
      if (b1) b1.textContent = pendingCount;
      const b2 = document.getElementById('profileApprovalsCount');
      if (b2) b2.textContent = pendingCount;
    }

    // ==================== Edit Plant Modal & Role-Aware Workflow ====================
    function openEditModal(plant) {
      if (!state.currentUser) {
        showToast("Please sign in as an advisor to edit plant records.", "warning");
        openLoginModal();
        return;
      }
      document.getElementById('editPlantId').value = plant.id || plant.scientific_name;
      document.getElementById('editCommonName').value = plant.common_names?.[0] || '';
      document.getElementById('editSciName').value = plant.scientific_name || '';
      document.getElementById('editOfficialUrl').value = getPlantUrl(plant);
      document.getElementById('editAdvisorDesc').value = getPlantDesc(plant);
      document.getElementById('editLight').value = (plant.light_requirements || []).join(', ');
      document.getElementById('editMoisture').value = (plant.moisture_requirements || []).join(', ');
      document.getElementById('editHeight').value = getPlantHeight(plant);
      document.getElementById('editSociability').value = getPlantSociability(plant);
      const colors = plant.bloom_color || plant.bloomColor || plant.bloom_colors || [];
      document.getElementById('editBloomColor').value = Array.isArray(colors) ? colors.join(', ') : String(colors || '');
      const seasons = plant.bloom_period || plant.bloomSeason || plant.bloom_seasons || [];
      document.getElementById('editBloomPeriod').value = Array.isArray(seasons) ? seasons.join(', ') : String(seasons || '');
      document.getElementById('editImageUrl').value = plant.images?.[0]?.url || '';
      document.getElementById('editImageAttr').value = plant.images?.[0]?.attribution_name || plant.images?.[0]?.license || 'Courtesy Missouri Botanical Garden PlantFinder';
      
      const notice = document.getElementById('editApprovalNotice');
      const submitBtn = document.getElementById('editPlantSubmitBtn');
      const isAdmin = Boolean(state.currentUser && state.currentUser.isAdmin);

      if (notice) {
        if (isAdmin) {
          notice.style.background = 'rgba(21,128,61,0.1)';
          notice.style.color = '#15803d';
          notice.innerHTML = '🛡️ <strong>Administrator Mode:</strong> Edits saved here will immediately update the master database and synchronize across all devices.';
        } else {
          notice.style.background = 'var(--primary-subtle)';
          notice.style.color = 'var(--primary-dark)';
          notice.innerHTML = 'ℹ️ <strong>Advisor Mode:</strong> Edits will be submitted to the <strong>Admin Approval Inbox</strong> for review before being applied to the master catalog.';
        }
      }

      if (submitBtn) {
        submitBtn.textContent = isAdmin ? 'Save to Master Catalog' : 'Submit Changes for Approval';
      }

      document.getElementById('editPlantModal').showModal();
    }

    document.getElementById('editPlantForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!state.currentUser) {
        showToast("Please sign in as an advisor to edit plant records.", "warning");
        openLoginModal();
        return;
      }

      const id = document.getElementById('editPlantId').value;
      const plant = state.allPlants.find(p => p.id === id || p.scientific_name === id);
      if (plant) {
        const edits = {
          common_names: [document.getElementById('editCommonName').value.trim()],
          scientific_name: document.getElementById('editSciName').value.trim(),
          plant_url: document.getElementById('editOfficialUrl').value.trim(),
          advisor_description: document.getElementById('editAdvisorDesc').value.trim(),
          light_requirements: document.getElementById('editLight').value.split(',').map(s => s.trim()).filter(Boolean),
          moisture_requirements: document.getElementById('editMoisture').value.split(',').map(s => s.trim()).filter(Boolean),
          height_display: document.getElementById('editHeight').value.trim(),
          sociability: document.getElementById('editSociability').value,
          bloom_color: document.getElementById('editBloomColor').value.split(',').map(s => s.trim()).filter(Boolean),
          bloomColor: document.getElementById('editBloomColor').value.split(',').map(s => s.trim()).filter(Boolean),
          bloom_period: document.getElementById('editBloomPeriod').value.split(',').map(s => s.trim()).filter(Boolean),
          bloomSeason: document.getElementById('editBloomPeriod').value.split(',').map(s => s.trim()).filter(Boolean),
          last_edited_by_user_id: state.currentUser.id || state.currentUser.username,
          last_edited_by_user_name: state.currentUser.name || `${state.currentUser.firstName} ${state.currentUser.lastName}`.trim() || state.currentUser.username,
          last_edited_by_user_email: state.currentUser.email || '',
          last_edited_timestamp: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          updated_by: state.currentUser.name || state.currentUser.username
        };

        const imgUrl = document.getElementById('editImageUrl').value.trim();
        if (imgUrl) {
          const imgAttr = document.getElementById('editImageAttr').value.trim() || 'Courtesy Missouri Botanical Garden PlantFinder';
          const newImg = {
            url: imgUrl,
            thumbnail_url: imgUrl,
            attribution_name: imgAttr,
            license: 'Courtesy Missouri Botanical Garden PlantFinder',
            caption: edits.scientific_name,
            source_name: 'Missouri Botanical Garden PlantFinder',
            source_url: edits.plant_url || plant.plantfinder_url || getPlantUrl(plant)
          };
          edits.images = [newImg, ...(plant.images || []).filter(im => im.url !== imgUrl)];
        }

        const isAdmin = Boolean(state.currentUser && state.currentUser.isAdmin);

        if (isAdmin) {
          Object.assign(plant, edits);
          state.customPlants[id] = edits;
          localStorage.setItem('dr_custom_plants', JSON.stringify(state.customPlants));
          syncPlantToFirestore(plant);
          applyFilters();
          updateHeaderInfo();
          showToast(`Saved changes for ${plant.common_names[0]} to master catalog!`, "success");
        } else {
          const approval = {
            id: 'appr-' + Date.now() + '-' + Math.random().toString(36).substr(2, 6),
            type: 'edit',
            status: 'pending',
            plant_id: plant.id || plant.scientific_name,
            scientific_name: edits.scientific_name,
            common_name: edits.common_names[0] || (plant.common_names && plant.common_names[0]) || edits.scientific_name,
            submitted_by_id: state.currentUser.id || state.currentUser.username,
            submitted_by_name: state.currentUser.name || state.currentUser.username,
            submitted_by_email: state.currentUser.email || '',
            submitted_at: new Date().toISOString(),
            changes: edits,
            original: {
              scientific_name: plant.scientific_name,
              common_names: plant.common_names || [],
              plant_url: getPlantUrl(plant),
              advisor_description: getPlantDesc(plant),
              height_display: getPlantHeight(plant),
              bloom_color: plant.bloom_color || plant.bloomColor || [],
              bloom_period: plant.bloom_period || plant.bloomSeason || [],
              light_requirements: plant.light_requirements || [],
              moisture_requirements: plant.moisture_requirements || [],
              sociability: getPlantSociability(plant),
              images: plant.images || []
            }
          };

          state.plantApprovals = state.plantApprovals || [];
          state.plantApprovals.unshift(approval);
          localStorage.setItem('dr_plant_approvals', JSON.stringify(state.plantApprovals));
          savePlantApprovalToFirestore(approval);
          updateApprovalBadges();
          applyFilters();
          showToast(`Proposed edits for ${approval.common_name} submitted to Admin Approval Inbox!`, "success");
        }
      }
      document.getElementById('editPlantModal').close();
    });

    // ==================== Add Plant Modal & Role-Aware Submission ====================
    function openAddPlantModal() {
      if (!state.currentUser) {
        showToast("Please sign in as an advisor or administrator to contribute plant records.", "warning");
        openLoginModal();
        return;
      }
      const modal = document.getElementById('addPlantModal');
      const form = document.getElementById('addPlantForm');
      if (!modal || !form) return;
      form.reset();

      const notice = document.getElementById('addApprovalNotice');
      const submitBtn = document.getElementById('addPlantSubmitBtn');
      const isAdmin = Boolean(state.currentUser && state.currentUser.isAdmin);

      if (notice) {
        if (isAdmin) {
          notice.style.background = 'rgba(21,128,61,0.1)';
          notice.style.color = '#15803d';
          notice.innerHTML = '🛡️ <strong>Administrator Mode:</strong> New species added here will be immediately published to the master catalog.';
        } else {
          notice.style.background = 'var(--primary-subtle)';
          notice.style.color = 'var(--primary-dark)';
          notice.innerHTML = 'ℹ️ <strong>Advisor Mode:</strong> Proposed species will be submitted to the <strong>Admin Approval Inbox</strong> for verification before landing in the master database.';
        }
      }

      if (submitBtn) {
        submitBtn.textContent = isAdmin ? 'Add to Master Catalog' : 'Submit for Approval';
      }

      modal.showModal();
      if (window.lucide) lucide.createIcons();
    }
    window.openAddPlantModal = openAddPlantModal;

    document.getElementById('addPlantForm')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!state.currentUser) {
        showToast("Please sign in to contribute plants.", "warning");
        openLoginModal();
        return;
      }

      const commonName = document.getElementById('addCommonName').value.trim();
      const sciName = document.getElementById('addSciName').value.trim();
      if (!commonName || !sciName) {
        showToast("Common name and Scientific name are required.", "warning");
        return;
      }

      const plantType = document.getElementById('addPlantType').value;
      const layer = document.getElementById('addLayer').value;
      const habitat = document.getElementById('addHabitat').value;
      const height = document.getElementById('addHeight').value.trim();
      const light = document.getElementById('addLight').value.split(',').map(s => s.trim()).filter(Boolean);
      const moisture = document.getElementById('addMoisture').value.split(',').map(s => s.trim()).filter(Boolean);
      const soil = document.getElementById('addSoil').value.split(',').map(s => s.trim()).filter(Boolean);
      const bloomColor = document.getElementById('addBloomColor').value.split(',').map(s => s.trim()).filter(Boolean);
      const bloomPeriod = document.getElementById('addBloomPeriod').value.split(',').map(s => s.trim()).filter(Boolean);
      const sociability = document.getElementById('addSociability').value;
      const wildlife = document.getElementById('addWildlife').value.split(',').map(s => s.trim()).filter(Boolean);
      const plantUrl = document.getElementById('addPlantUrl').value.trim() || 'https://www.missouribotanicalgarden.org/PlantFinder/PlantFinderSearch.aspx';
      const imageUrl = document.getElementById('addImageUrl').value.trim();
      const imageAttr = document.getElementById('addImageAttr').value.trim() || 'Courtesy Missouri Botanical Garden PlantFinder';
      const advisorDesc = document.getElementById('addAdvisorDesc').value.trim();

      const newId = 'dr-kc-custom-' + Date.now();
      const images = [];
      if (imageUrl) {
        images.push({
          url: imageUrl,
          thumbnail_url: imageUrl,
          attribution_name: imageAttr,
          license: 'Courtesy Missouri Botanical Garden PlantFinder',
          label: 'Specimen',
          caption: `${sciName} (${commonName})`,
          source_name: 'Missouri Botanical Garden PlantFinder',
          source_url: plantUrl
        });
      }

      const newPlant = {
        id: newId,
        scientific_name: sciName,
        common_names: [commonName],
        plant_type: [plantType],
        architectural_layer: layer,
        native_environment: habitat,
        height_display: height || '2–4 ft',
        light_requirements: light.length > 0 ? light : ['Full Sun', 'Part Sun'],
        moisture_requirements: moisture.length > 0 ? moisture : ['Medium'],
        soil_requirements: soil.length > 0 ? soil : ['Loam'],
        bloom_color: bloomColor,
        bloomColor: bloomColor,
        bloom_period: bloomPeriod,
        bloomSeason: bloomPeriod,
        sociability: sociability,
        wildlife_ecosystem_benefits: wildlife.length > 0 ? wildlife : ['Provides nectar and shelter for native wildlife.'],
        plant_url: plantUrl,
        plantfinder_url: plantUrl,
        advisor_description: advisorDesc,
        images: images,
        is_sweet16: false,
        is_kc_keystone: false,
        created_at: new Date().toISOString(),
        created_by: state.currentUser.name || state.currentUser.username,
        last_edited_by_user_id: state.currentUser.id || state.currentUser.username,
        last_edited_by_user_name: state.currentUser.name || state.currentUser.username,
        last_edited_timestamp: new Date().toISOString()
      };

      const isAdmin = Boolean(state.currentUser && state.currentUser.isAdmin);

      if (isAdmin) {
        state.allPlants.push(newPlant);
        state.customPlants[newId] = newPlant;
        localStorage.setItem('dr_custom_plants', JSON.stringify(state.customPlants));
        syncPlantToFirestore(newPlant);
        applyFilters();
        updateHeaderInfo();
        showToast(`Added ${commonName} directly to the master catalog!`, "success");
      } else {
        const approval = {
          id: 'appr-' + Date.now() + '-' + Math.random().toString(36).substr(2, 6),
          type: 'add',
          status: 'pending',
          plant_id: newId,
          scientific_name: sciName,
          common_name: commonName,
          submitted_by_id: state.currentUser.id || state.currentUser.username,
          submitted_by_name: state.currentUser.name || state.currentUser.username,
          submitted_by_email: state.currentUser.email || '',
          submitted_at: new Date().toISOString(),
          changes: newPlant
        };

        state.plantApprovals = state.plantApprovals || [];
        state.plantApprovals.unshift(approval);
        localStorage.setItem('dr_plant_approvals', JSON.stringify(state.plantApprovals));
        savePlantApprovalToFirestore(approval);
        updateApprovalBadges();
        showToast(`New plant proposal for ${commonName} submitted to Admin Approval Inbox!`, "success");
      }

      document.getElementById('addPlantModal').close();
    });

    // ==================== Admin Approval Inbox Panel & Review Actions ====================
    function renderAdminApprovals(filterTerm = '') {
      const container = document.getElementById('adminApprovalsList');
      if (!container) return;

      const term = (filterTerm || '').toLowerCase().trim();
      let list = state.plantApprovals || [];

      if (term) {
        list = list.filter(item => {
          const common = (item.common_name || '').toLowerCase();
          const sci = (item.scientific_name || '').toLowerCase();
          const author = (item.submitted_by_name || '').toLowerCase();
          return common.includes(term) || sci.includes(term) || author.includes(term);
        });
      }

      updateApprovalBadges();

      if (list.length === 0) {
        container.innerHTML = `
          <div style="background:var(--bg-base);border:1px dashed var(--border-subtle);border-radius:var(--radius-md);padding:36px 20px;text-align:center;">
            <i data-lucide="inbox" style="width:36px;height:36px;color:var(--text-muted);margin:0 auto 10px auto;display:block;"></i>
            <h4 style="font-size:15px;font-weight:700;margin:0 0 4px 0;">All Clear! No Pending Approvals</h4>
            <p style="font-size:12px;color:var(--text-muted);margin:0;">When advisors submit plant edits or new species, they will appear here for administrator review.</p>
          </div>
        `;
        if (window.lucide) lucide.createIcons();
        return;
      }

      container.innerHTML = list.map(item => {
        const isPending = item.status === 'pending';
        const isEdit = item.type === 'edit';
        const dateStr = item.submitted_at ? new Date(item.submitted_at).toLocaleString() : 'Recent';
        
        let statusBadge = '';
        if (item.status === 'pending') {
          statusBadge = '<span style="background:#fef3c7;color:#92400e;font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px;display:inline-flex;align-items:center;gap:4px;"><i data-lucide="clock" style="width:11px;height:11px;"></i> Pending Review</span>';
        } else if (item.status === 'approved') {
          statusBadge = '<span style="background:#dcfce7;color:#166534;font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px;display:inline-flex;align-items:center;gap:4px;"><i data-lucide="check-circle" style="width:11px;height:11px;"></i> Approved</span>';
        } else {
          statusBadge = '<span style="background:#fee2e2;color:#991b1b;font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px;display:inline-flex;align-items:center;gap:4px;"><i data-lucide="x-circle" style="width:11px;height:11px;"></i> Denied</span>';
        }

        const typeBadge = isEdit 
          ? '<span style="background:var(--primary-subtle);color:var(--primary-dark);font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px;">Edit Proposal</span>'
          : '<span style="background:#dbeafe;color:#1e40af;font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px;">New Plant Addition</span>';

        let diffHtml = '';
        if (isEdit && item.changes) {
          const ch = item.changes;
          const orig = item.original || {};
          const rows = [];
          
          if (ch.common_names && JSON.stringify(ch.common_names) !== JSON.stringify(orig.common_names)) {
            rows.push(`<div><strong>Common Name:</strong> <del style="color:var(--text-muted);">${escapeHtml((orig.common_names || []).join(', '))}</del> ➔ <span style="color:#15803d;font-weight:700;">${escapeHtml(ch.common_names.join(', '))}</span></div>`);
          }
          if (ch.scientific_name && ch.scientific_name !== orig.scientific_name) {
            rows.push(`<div><strong>Scientific Name:</strong> <del style="color:var(--text-muted);">${escapeHtml(orig.scientific_name || '')}</del> ➔ <span style="color:#15803d;font-weight:700;">${escapeHtml(ch.scientific_name)}</span></div>`);
          }
          if (ch.advisor_description && ch.advisor_description !== orig.advisor_description) {
            rows.push(`<div><strong>Advisor Description:</strong><div style="font-size:11px;color:#15803d;background:rgba(21,128,61,0.06);padding:6px;border-radius:4px;margin-top:2px;">${escapeHtml(ch.advisor_description)}</div></div>`);
          }
          if (ch.height_display && ch.height_display !== orig.height_display) {
            rows.push(`<div><strong>Height:</strong> <del style="color:var(--text-muted);">${escapeHtml(orig.height_display || '-')}</del> ➔ <span style="color:#15803d;font-weight:700;">${escapeHtml(ch.height_display)}</span></div>`);
          }
          if (ch.light_requirements && JSON.stringify(ch.light_requirements) !== JSON.stringify(orig.light_requirements)) {
            rows.push(`<div><strong>Light:</strong> <del style="color:var(--text-muted);">${escapeHtml((orig.light_requirements || []).join(', '))}</del> ➔ <span style="color:#15803d;font-weight:700;">${escapeHtml(ch.light_requirements.join(', '))}</span></div>`);
          }
          if (ch.moisture_requirements && JSON.stringify(ch.moisture_requirements) !== JSON.stringify(orig.moisture_requirements)) {
            rows.push(`<div><strong>Moisture:</strong> <del style="color:var(--text-muted);">${escapeHtml((orig.moisture_requirements || []).join(', '))}</del> ➔ <span style="color:#15803d;font-weight:700;">${escapeHtml(ch.moisture_requirements.join(', '))}</span></div>`);
          }
          if (ch.bloom_color && JSON.stringify(ch.bloom_color) !== JSON.stringify(orig.bloom_color)) {
            rows.push(`<div><strong>Bloom Color:</strong> <del style="color:var(--text-muted);">${escapeHtml((orig.bloom_color || []).join(', '))}</del> ➔ <span style="color:#15803d;font-weight:700;">${escapeHtml(ch.bloom_color.join(', '))}</span></div>`);
          }
          if (ch.images && ch.images[0] && ch.images[0].url) {
            rows.push(`<div><strong>Photo:</strong> <a href="${ch.images[0].url}" target="_blank" rel="noopener noreferrer" style="color:var(--primary);text-decoration:underline;">View Submitted Photo</a> · <span style="font-size:11px;color:var(--text-secondary);">${escapeHtml(ch.images[0].attribution_name || 'Credit')}</span></div>`);
          }
          diffHtml = rows.length > 0 ? rows.join('<div style="height:6px;"></div>') : '<p style="font-size:11px;color:var(--text-muted);margin:0;">General field edits</p>';
        } else if (!isEdit && item.changes) {
          const p = item.changes;
          diffHtml = `
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:11px;color:var(--text-main);">
              <div><strong>Type:</strong> ${escapeHtml(Array.isArray(p.plant_type) ? p.plant_type.join(', ') : (p.plant_type || '-'))}</div>
              <div><strong>Layer:</strong> ${escapeHtml(p.architectural_layer || '-')}</div>
              <div><strong>Environment:</strong> ${escapeHtml(p.native_environment || '-')}</div>
              <div><strong>Height:</strong> ${escapeHtml(p.height_display || '-')}</div>
              <div><strong>Light:</strong> ${escapeHtml((p.light_requirements || []).join(', '))}</div>
              <div><strong>Moisture:</strong> ${escapeHtml((p.moisture_requirements || []).join(', '))}</div>
            </div>
            ${p.advisor_description ? `<div style="font-size:11px;margin-top:6px;background:rgba(21,128,61,0.06);padding:6px;border-radius:4px;"><strong>Description:</strong> ${escapeHtml(p.advisor_description)}</div>` : ''}
            ${p.images && p.images[0] ? `<div style="margin-top:6px;font-size:11px;"><a href="${p.images[0].url}" target="_blank" rel="noopener noreferrer" style="color:var(--primary);text-decoration:underline;">View Attached Photo</a> (Credit: ${escapeHtml(p.images[0].attribution_name || 'Courtesy Missouri Botanical Garden PlantFinder')})</div>` : ''}
          `;
        }

        return `
          <div class="approval-card" style="border:1px solid var(--border-subtle);border-radius:var(--radius-md);background:var(--bg-surface);padding:14px;display:flex;flex-direction:column;gap:10px;">
            <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:8px;flex-wrap:wrap;">
              <div>
                <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
                  ${typeBadge}
                  ${statusBadge}
                  <h4 style="font-size:14px;font-weight:800;margin:0;color:var(--text-main);">${escapeHtml(item.common_name)}</h4>
                  <span style="font-style:italic;color:var(--text-muted);font-size:12px;">(${escapeHtml(item.scientific_name)})</span>
                </div>
                <div style="font-size:11px;color:var(--text-secondary);margin-top:4px;">
                  Submitted by <strong>${escapeHtml(item.submitted_by_name || 'Advisor')}</strong> (${escapeHtml(item.submitted_by_email || 'No email')}) on ${dateStr}
                </div>
              </div>

              ${isPending ? `
                <div style="display:flex;align-items:center;gap:8px;">
                  <button type="button" class="btn btn-secondary btn-sm" onclick="denyPlantChange('${item.id}')" style="color:#b91c1c;border-color:rgba(185,28,28,0.3);font-size:11px;padding:4px 10px;display:inline-flex;align-items:center;gap:4px;">
                    <i data-lucide="x" style="width:12px;height:12px;"></i>
                    <span>Deny</span>
                  </button>
                  <button type="button" class="btn btn-primary btn-sm" onclick="approvePlantChange('${item.id}')" style="background:#15803d;border-color:#15803d;font-size:11px;padding:4px 12px;display:inline-flex;align-items:center;gap:4px;">
                    <i data-lucide="check" style="width:12px;height:12px;"></i>
                    <span>Approve &amp; Apply</span>
                  </button>
                </div>
              ` : `
                <div style="font-size:11px;color:var(--text-muted);">
                  ${item.reviewed_by_name ? `Reviewed by ${escapeHtml(item.reviewed_by_name)} on ${new Date(item.reviewed_at).toLocaleDateString()}` : ''}
                </div>
              `}
            </div>

            <div style="background:var(--bg-base);border-radius:var(--radius-sm);padding:10px;font-size:12px;border-left:3px solid var(--primary);">
              ${diffHtml}
            </div>
          </div>
        `;
      }).join('');

      if (window.lucide) lucide.createIcons();
    }
    window.renderAdminApprovals = renderAdminApprovals;

    async function approvePlantChange(approvalId) {
      if (!state.currentUser || !state.currentUser.isAdmin) {
        showToast("Administrator privileges required to approve catalog changes.", "danger");
        return;
      }

      const approval = (state.plantApprovals || []).find(a => a.id === approvalId);
      if (!approval || approval.status !== 'pending') return;

      const reviewerName = state.currentUser.name || state.currentUser.username;
      approval.status = 'approved';
      approval.reviewed_by_id = state.currentUser.id || state.currentUser.username;
      approval.reviewed_by_name = reviewerName;
      approval.reviewed_at = new Date().toISOString();

      if (approval.type === 'edit') {
        const targetPlant = state.allPlants.find(p => p.id === approval.plant_id || p.scientific_name === approval.scientific_name);
        if (targetPlant && approval.changes) {
          Object.assign(targetPlant, approval.changes);
          targetPlant.updated_at = new Date().toISOString();
          targetPlant.updated_by = `Approved by ${reviewerName} (Sub: ${approval.submitted_by_name})`;
          
          state.customPlants[targetPlant.id || targetPlant.scientific_name] = approval.changes;
          localStorage.setItem('dr_custom_plants', JSON.stringify(state.customPlants));
          syncPlantToFirestore(targetPlant);
        }
      } else if (approval.type === 'add') {
        const newPlant = approval.changes;
        if (newPlant) {
          newPlant.updated_by = `Approved by ${reviewerName} (Sub: ${approval.submitted_by_name})`;
          state.allPlants.push(newPlant);
          state.customPlants[newPlant.id] = newPlant;
          localStorage.setItem('dr_custom_plants', JSON.stringify(state.customPlants));
          syncPlantToFirestore(newPlant);
        }
      }

      localStorage.setItem('dr_plant_approvals', JSON.stringify(state.plantApprovals));
      savePlantApprovalToFirestore(approval);

      renderAdminApprovals(document.getElementById('adminApprovalsSearchInput')?.value || '');
      updateApprovalBadges();
      applyFilters();
      updateHeaderInfo();

      showToast(`Approved changes for ${approval.common_name}! Catalog updated.`, "success");
    }
    window.approvePlantChange = approvePlantChange;

    async function denyPlantChange(approvalId) {
      if (!state.currentUser || !state.currentUser.isAdmin) {
        showToast("Administrator privileges required.", "danger");
        return;
      }

      const approval = (state.plantApprovals || []).find(a => a.id === approvalId);
      if (!approval || approval.status !== 'pending') return;

      if (!confirm(`Are you sure you want to deny proposed changes for "${approval.common_name}"?`)) {
        return;
      }

      approval.status = 'denied';
      approval.reviewed_by_id = state.currentUser.id || state.currentUser.username;
      approval.reviewed_by_name = state.currentUser.name || state.currentUser.username;
      approval.reviewed_at = new Date().toISOString();

      localStorage.setItem('dr_plant_approvals', JSON.stringify(state.plantApprovals));
      savePlantApprovalToFirestore(approval);

      renderAdminApprovals(document.getElementById('adminApprovalsSearchInput')?.value || '');
      updateApprovalBadges();
      showToast(`Changes for ${approval.common_name} were denied.`, "info");
    }
    window.denyPlantChange = denyPlantChange;"""

    if old_edit_block in content:
        content = content.replace(old_edit_block, new_edit_block, 1)
        print("Updated editPlantModal, added addPlantModal & admin approvals engine")
    else:
        print("Warning: old_edit_block pattern not found!")

    # 9. Update setupEventListeners to wire approvals buttons & tabs
    old_events = """      // Admin Management Tabs & Actions
      document.getElementById('adminRosterTabBtn')?.addEventListener('click', () => switchAdminTab('roster'));
      document.getElementById('adminProvisionTabBtn')?.addEventListener('click', () => switchAdminTab('provision'));
      document.getElementById('adminReportsTabBtn')?.addEventListener('click', () => switchAdminTab('reports'));"""

    new_events = """      // Admin Management Tabs & Actions
      document.getElementById('adminRosterTabBtn')?.addEventListener('click', () => switchAdminTab('roster'));
      document.getElementById('adminProvisionTabBtn')?.addEventListener('click', () => switchAdminTab('provision'));
      document.getElementById('adminReportsTabBtn')?.addEventListener('click', () => switchAdminTab('reports'));
      document.getElementById('adminApprovalsTabBtn')?.addEventListener('click', () => switchAdminTab('approvals'));

      document.getElementById('adminApprovalsSearchInput')?.addEventListener('input', (e) => {
        renderAdminApprovals(e.target.value);
      });

      document.getElementById('adminApprovalsRefreshBtn')?.addEventListener('click', async () => {
        const btn = document.getElementById('adminApprovalsRefreshBtn');
        const icon = btn?.querySelector('i');
        if (icon) icon.classList.add('spin');
        try {
          await fetchPlantApprovalsFromFirestore();
          renderAdminApprovals(document.getElementById('adminApprovalsSearchInput')?.value || '');
          showToast('Approval inbox refreshed from cloud!', 'success');
        } catch (err) {
          showToast(`Refresh error: ${err.message}`, 'danger');
        } finally {
          if (icon) icon.classList.remove('spin');
        }
      });

      document.getElementById('openAdminApprovalsBtn')?.addEventListener('click', () => {
        document.getElementById('userProfileModal')?.close();
        openAdminConsoleModal('approvals');
      });

      document.getElementById('openAddPlantBtn')?.addEventListener('click', () => {
        openAddPlantModal();
      });

      document.getElementById('profileAddPlantBtn')?.addEventListener('click', () => {
        document.getElementById('userProfileModal')?.close();
        openAddPlantModal();
      });"""

    if old_events in content:
        content = content.replace(old_events, new_events, 1)
        print("Updated setupEventListeners with approvals & add plant handlers")
    else:
        print("Warning: old_events pattern not found!")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Finished updates to index.html!")

if __name__ == '__main__':
    apply_updates()
