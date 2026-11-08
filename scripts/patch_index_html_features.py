#!/usr/bin/env python3
"""
scripts/patch_index_html_features.py

Patches index.html:
1. Modal HTML:
   - Updates modalWildlife to a styled div for rich formatting.
   - Updates modalMaintenanceGrid to be dynamic (rendering only seasons with actions).
   - Wraps division card in modalDivisionContainer.
2. Adds renderRichMarkdownText helper for rich text and clickable links.
3. Updates openPlantDetail(plant) to render:
   - modalAdvisorDesc with clickable links via renderRichMarkdownText.
   - modalMaintenanceGrid dynamically for only non-empty seasons.
   - modalWildlife with host insects, wildlife, and source links.
4. Updates downloadDocxReport to output actionable maintenance and wildlife bullets.
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update modalWildlife and modalMaintenance in modal HTML
old_modal_wildlife_maint = '''      <!-- Wildlife & Keystone Interactions -->
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
        </div>'''

new_modal_wildlife_maint = '''      <!-- Wildlife & Keystone Interactions -->
      <div style="background:var(--bg-base);padding:14px;border-radius:var(--radius-md);">
        <div style="font-size:11px;font-weight:800;text-transform:uppercase;color:var(--accent-keystone);margin-bottom:6px;">Wildlife &amp; Ecological Value</div>
        <div id="modalWildlife" style="font-size:13px;line-height:1.6;color:var(--text-secondary);"></div>
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
        
        <div id="modalMaintenanceGrid" style="display:grid;grid-template-columns:repeat(auto-fit, minmax(220px, 1fr));gap:10px;margin-top:10px;">
          <!-- Dynamically injected season cards only when actions exist -->
        </div>

        <div id="modalDivisionContainer" style="background:var(--bg-surface);padding:10px;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);margin-top:10px;">
          <strong style="font-size:12px;color:var(--text-main);display:flex;align-items:center;gap:4px;margin-bottom:4px;">
            <i data-lucide="git-branch" style="width:12px;height:12px;"></i> Root Division &amp; Propagation
          </strong>
          <p id="modalMaintDivision" style="font-size:12px;line-height:1.4;color:var(--text-secondary);margin:0;"></p>
        </div>'''

if old_modal_wildlife_maint in html:
    html = html.replace(old_modal_wildlife_maint, new_modal_wildlife_maint)
    print("Successfully patched modal HTML markup.")
else:
    print("WARNING: Could not find old_modal_wildlife_maint in index.html")

# 2. Add renderRichMarkdownText helper function
old_helpers = '''    function escapeXml(str) {
      if (str === null || str === undefined) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&apos;');
    }'''

new_helpers = '''    function escapeXml(str) {
      if (str === null || str === undefined) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&apos;');
    }

    function renderRichMarkdownText(str) {
      if (!str) return '';
      let s = escapeHtml(str);
      // Markdown bold: **text**
      s = s.replace(/\\*\\*([^*]+)\\*\\*/g, '<strong style="color:var(--text-main);font-weight:700;">$1</strong>');
      // Markdown italics: *text*
      s = s.replace(/(^|[^*])\\*([^*]+)\\*([^*]|$)/g, '$1<em>$2</em>$3');
      // Markdown links: [text](url)
      s = s.replace(/\\[([^\\]]+)\\]\\((https?:\\/\\/[^\\s\\)]+)\\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" style="color:var(--primary);text-decoration:underline;font-weight:600;">$1</a>');
      // Paragraph spacing
      s = s.replace(/\\n\\n/g, '<div style="margin-top:8px;"></div>');
      s = s.replace(/\\n/g, '<br>');
      return s;
    }'''

if old_helpers in html:
    html = html.replace(old_helpers, new_helpers)
    print("Successfully added renderRichMarkdownText helper.")
else:
    print("WARNING: Could not find old_helpers in index.html")

# 3. Update openPlantDetail(plant)
old_open_detail = '''      document.getElementById('modalAdvisorDesc').textContent = getPlantDesc(plant);
      document.getElementById('modalLight').textContent = (plant.light_requirements || []).join(', ') || '-';
      document.getElementById('modalMoisture').textContent = (plant.moisture_requirements || []).join(', ') || '-';
      document.getElementById('modalHeight').textContent = getPlantHeight(plant);
      document.getElementById('modalSoil').textContent = (plant.soil_requirements || []).join(', ') || '-';
      document.getElementById('modalBloomPeriod').textContent = (plant.bloom_period || []).join(', ') || '-';
      document.getElementById('modalBloomColor').textContent = (plant.bloom_color || plant.bloom_colors || []).join(', ') || '-';
      document.getElementById('modalLayer').textContent = getPlantLayer(plant);
      document.getElementById('modalSociability').textContent = getPlantSociability(plant);
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

      document.getElementById('modalWildlife').textContent = (plant.wildlife_ecosystem_benefits || plant.wildlife_benefits || []).join(' · ') || 'Provides nectar, pollen, and shelter for native pollinators and wildlife.';'''

new_open_detail = '''      document.getElementById('modalAdvisorDesc').innerHTML = renderRichMarkdownText(getPlantDesc(plant));
      document.getElementById('modalLight').textContent = (plant.light_requirements || []).join(', ') || '-';
      document.getElementById('modalMoisture').textContent = (plant.moisture_requirements || []).join(', ') || '-';
      document.getElementById('modalHeight').textContent = getPlantHeight(plant);
      document.getElementById('modalSoil').textContent = (plant.soil_requirements || []).join(', ') || '-';
      document.getElementById('modalBloomPeriod').textContent = (plant.bloom_period || []).join(', ') || '-';
      document.getElementById('modalBloomColor').textContent = (plant.bloom_color || plant.bloom_colors || []).join(', ') || '-';
      document.getElementById('modalLayer').textContent = getPlantLayer(plant);
      document.getElementById('modalSociability').textContent = getPlantSociability(plant);
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

      // Dynamically render cards ONLY for seasons with actionable maintenance
      const maintGrid = document.getElementById('modalMaintenanceGrid');
      if (maintGrid) {
        let gridHtml = '';
        if (maintGuide.spring && maintGuide.spring.trim()) {
          gridHtml += `
            <div style="background:var(--bg-surface);padding:10px;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
              <strong style="font-size:12px;color:var(--primary);display:flex;align-items:center;gap:4px;margin-bottom:4px;">
                <i data-lucide="flower" style="width:12px;height:12px;"></i> Spring (50°F+ Cutback)
              </strong>
              <p style="font-size:12px;line-height:1.4;color:var(--text-secondary);margin:0;">${escapeHtml(maintGuide.spring)}</p>
            </div>`;
        }
        if (maintGuide.summer && maintGuide.summer.trim()) {
          gridHtml += `
            <div style="background:var(--bg-surface);padding:10px;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
              <strong style="font-size:12px;color:#d97706;display:flex;align-items:center;gap:4px;margin-bottom:4px;">
                <i data-lucide="sun" style="width:12px;height:12px;"></i> Summer Care
              </strong>
              <p style="font-size:12px;line-height:1.4;color:var(--text-secondary);margin:0;">${escapeHtml(maintGuide.summer)}</p>
            </div>`;
        }
        if (maintGuide.fall && maintGuide.fall.trim()) {
          gridHtml += `
            <div style="background:var(--bg-surface);padding:10px;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
              <strong style="font-size:12px;color:#b45309;display:flex;align-items:center;gap:4px;margin-bottom:4px;">
                <i data-lucide="leaf" style="width:12px;height:12px;"></i> Fall Timing
              </strong>
              <p style="font-size:12px;line-height:1.4;color:var(--text-secondary);margin:0;">${escapeHtml(maintGuide.fall)}</p>
            </div>`;
        }
        if (maintGuide.winter && maintGuide.winter.trim()) {
          gridHtml += `
            <div style="background:var(--bg-surface);padding:10px;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
              <strong style="font-size:12px;color:#2563eb;display:flex;align-items:center;gap:4px;margin-bottom:4px;">
                <i data-lucide="snowflake" style="width:12px;height:12px;"></i> Winter Protection
              </strong>
              <p style="font-size:12px;line-height:1.4;color:var(--text-secondary);margin:0;">${escapeHtml(maintGuide.winter)}</p>
            </div>`;
        }
        maintGrid.innerHTML = gridHtml;
      }

      // Root Division Card
      const divContainer = document.getElementById('modalDivisionContainer');
      const modalMaintDivision = document.getElementById('modalMaintDivision');
      if (divContainer && modalMaintDivision) {
        if (maintGuide.division && maintGuide.division.trim()) {
          divContainer.style.display = 'block';
          modalMaintDivision.textContent = maintGuide.division;
        } else {
          divContainer.style.display = 'none';
        }
      }

      const modalMaintSources = document.getElementById('modalMaintSources');
      if (modalMaintSources) modalMaintSources.textContent = maintGuide.sources || 'Xerces Society, Grow Native!, Missouri Botanical Garden';

      // Enhanced Wildlife and Ecological Value rendering
      const modalWildlife = document.getElementById('modalWildlife');
      if (modalWildlife) {
        if (plant.wildlife_ecological_value) {
          modalWildlife.innerHTML = renderRichMarkdownText(plant.wildlife_ecological_value);
        } else if (plant.wildlife_detail && plant.wildlife_detail.host_insects) {
          const wd = plant.wildlife_detail;
          const wmd = `**Host Plant Value:** ${wd.host_insects}\\n\\n**Wildlife & Ecological Interactions:** ${wd.wildlife_users || 'Supports native pollinators and birds.'}\\n\\n**Scientific Sources:** ${wd.sources || '[Xerces Society](https://xerces.org), [MDC](https://mdc.mo.gov)'}`;
          modalWildlife.innerHTML = renderRichMarkdownText(wmd);
        } else {
          modalWildlife.textContent = (plant.wildlife_ecosystem_benefits || plant.wildlife_benefits || []).join(' · ') || 'Provides nectar, pollen, and shelter for native pollinators and wildlife.';
        }
      }'''

if old_open_detail in html:
    html = html.replace(old_open_detail, new_open_detail)
    print("Successfully patched openPlantDetail in index.html.")
else:
    print("WARNING: Could not find old_open_detail in index.html")

# 4. Update downloadDocxReport
old_docx_maint = '''                // Botanical bullet point 3: Maintenance Level & Ecological Care Timings
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
</w:p>`;'''

new_docx_maint = '''                // Botanical bullet point 3: Maintenance Level & Actionable Timings
                const reportMaintLvl = staged.maintenance_level || (master && (master.maintenance_level || master.maintenanceLevel)) || 'Low';
                const reportMaintGuide = staged.maintenance_guide || (master && master.maintenance_guide) || {};
                let reportMaintSummary = '';
                if (reportMaintGuide && typeof reportMaintGuide === 'object' && reportMaintGuide.summary) {
                  const parts = [reportMaintGuide.summary];
                  if (reportMaintGuide.spring) parts.push(`Spring: ${reportMaintGuide.spring}`);
                  if (reportMaintGuide.summer) parts.push(`Summer: ${reportMaintGuide.summer}`);
                  if (reportMaintGuide.fall) parts.push(`Fall: ${reportMaintGuide.fall}`);
                  if (reportMaintGuide.winter) parts.push(`Winter: ${reportMaintGuide.winter}`);
                  if (reportMaintGuide.division) parts.push(`Division: ${reportMaintGuide.division}`);
                  reportMaintSummary = parts.join(' | ');
                } else {
                  reportMaintSummary = 'Spring cutback at sustained 50°F+ to protect stem-nesting bees; leave 8–18 in stems and retain seedheads for songbirds.';
                }

                plantBlocks += `
<w:p>
    <w:pPr>
        <w:ind w:left="720" w:hanging="360"/>
        <w:spacing w:after="40"/>
    </w:pPr>
    <w:r><w:t>• </w:t></w:r>
    <w:r><w:rPr><w:b/><w:color w:val="2D5A27"/></w:rPr><w:t>Maintenance (${escapeXml(reportMaintLvl)}): </w:t></w:r>
    <w:r><w:t>${escapeXml(reportMaintSummary)}</w:t></w:r>
</w:p>`;

                // Botanical bullet point 4: Wildlife & Host Insect Value
                let wildlifeReportText = '';
                if (master && master.wildlife_detail && master.wildlife_detail.host_insects) {
                  wildlifeReportText = `Host value: ${master.wildlife_detail.host_insects} Wildlife supported: ${master.wildlife_detail.wildlife_users || 'Native songbirds and pollinators'}.`;
                } else if (master && master.wildlife_ecosystem_benefits) {
                  wildlifeReportText = master.wildlife_ecosystem_benefits.join(' · ');
                }
                if (wildlifeReportText) {
                  plantBlocks += `
<w:p>
    <w:pPr>
        <w:ind w:left="720" w:hanging="360"/>
        <w:spacing w:after="60"/>
    </w:pPr>
    <w:r><w:t>• </w:t></w:r>
    <w:r><w:rPr><w:b/><w:color w:val="2D5A27"/></w:rPr><w:t>Wildlife &amp; Host Value: </w:t></w:r>
    <w:r><w:t>${escapeXml(wildlifeReportText)}</w:t></w:r>
</w:p>`;
                }'''

if old_docx_maint in html:
    html = html.replace(old_docx_maint, new_docx_maint)
    print("Successfully patched downloadDocxReport in index.html.")
else:
    print("WARNING: Could not find old_docx_maint in index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved updated index.html successfully.")
