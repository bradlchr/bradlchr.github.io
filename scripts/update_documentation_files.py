#!/usr/bin/env python3
"""
Updates CODE_DOCUMENTATION.md and docs.html with the Missouri Botanical Garden PlantFinder
integration, English Ivy correction, and the 2-tier approval workflow.
"""

def update_code_documentation():
    with open('CODE_DOCUMENTATION.md', 'r', encoding='utf-8') as f:
        doc = f.read()

    # 1. Update RBAC section in CODE_DOCUMENTATION.md
    old_advisor_rbac = """| NATURE ADVISOR (role: 'user')                                                     |
| - All Guest capabilities                                                          |
| - Full consultation staging drawer & custom garden zones (planting areas)         |
| - Generate and download official Word consultation reports (.docx)                |
| - Edit botanical species records (syncs to Cloud Firestore with attribution)      |
| - Pull fresh data from master database in Database Sync modal                     |
+-----------------------------------------------------------------------------------+
                                         │  Admin Role Assigned
                                         ▼
+-----------------------------------------------------------------------------------+
| PROGRAM ADMINISTRATOR (role: 'admin')                                             |
| - All Nature Advisor capabilities                                                 |
| - Central Consultation Reports Repository (inspect any advisor's reports)         |
| - Instant on-demand Word (.docx) regeneration for any historical report           |
| - Delete consultation reports across all Cloud Firestore paths                    |
| - Provision new Nature Advisors and issue temporary passwords                     |
| - Master Catalog Governance: Upload baseline, reset local edits, import JSON      |
+-----------------------------------------------------------------------------------+"""

    new_advisor_rbac = """| NATURE ADVISOR (role: 'user')                                                     |
| - All Guest capabilities                                                          |
| - Full consultation staging drawer & custom garden zones (planting areas)         |
| - Generate and download official Word consultation reports (.docx)                |
| - Propose botanical record edits (submitted to Admin Approval Inbox)              |
| - Propose new native species additions (submitted to Admin Approval Inbox)        |
| - Pull fresh data from master database in Database Sync modal                     |
+-----------------------------------------------------------------------------------+
                                         │  Admin Role Assigned
                                         ▼
+-----------------------------------------------------------------------------------+
| PROGRAM ADMINISTRATOR (role: 'admin')                                             |
| - All Nature Advisor capabilities                                                 |
| - Plant Approval Inbox: Review, approve, or deny proposed edits & new species     |
| - Direct master catalog editing and instant plant additions without gating        |
| - Central Consultation Reports Repository (inspect any advisor's reports)         |
| - Instant on-demand Word (.docx) regeneration for any historical report           |
| - Delete consultation reports across all Cloud Firestore paths                    |
| - Provision new Nature Advisors and issue temporary passwords                     |
| - Master Catalog Governance: Upload baseline, reset local edits, import JSON      |
+-----------------------------------------------------------------------------------+"""

    if old_advisor_rbac in doc:
        doc = doc.replace(old_advisor_rbac, new_advisor_rbac, 1)
        print("Updated RBAC in CODE_DOCUMENTATION.md")

    # 2. Update Firestore schema section in CODE_DOCUMENTATION.md
    old_schema = """- **`/users/{username}/reports/{reportId}`**: User-scoped consultation subcollection.
- **`/plants/_report_{username}_{reportId}`**: Fallback consultation storage path."""

    new_schema = """- **`/users/{username}/reports/{reportId}`**: User-scoped consultation subcollection.
- **`/plant_approvals/{approvalId}`**: Dedicated collection for pending and historical plant approval requests (edits and new species additions).
- **`/plants/_approval_{approvalId}`**: Fallback cloud sync path for plant approval requests.
- **`/plants/_report_{username}_{reportId}`**: Fallback consultation storage path."""

    if old_schema in doc:
        doc = doc.replace(old_schema, new_schema, 1)
        print("Updated Firestore schema in CODE_DOCUMENTATION.md")

    # 3. Add new section for Missouri Botanical Garden Gallery & Approval Workflow before Section 6
    old_sec6 = "## 📚 6. Exhaustive Function Reference (118 Functions)"
    new_features_sec = """## 🌸 6. Missouri Botanical Garden PlantFinder & Image Engine

The native plant catalog integrates high-resolution botanical photography sourced directly from the **Missouri Botanical Garden PlantFinder** (MOBOT), providing authentic identification imagery for 179 Kansas City native species:

### Key Image Engine Features:
1. **Authentic Taxonomy Mapping**: 179 regional species are mapped to official MOBOT Taxon IDs and Kemper Center codes using Wikidata Property `P6034`.
2. **High-Resolution Multi-Image Galleries**: Over 1,231 specimen photos are indexed across flower close-ups, whole-plant growth habits, foliage detail, fall color, and winter architecture.
3. **Mandatory Attribution & Linkbacks**: Every single photograph displays the required credit: `"Courtesy Missouri Botanical Garden PlantFinder"` and provides a direct hyperlink back to the plant's dedicated information page on `missouribotanicalgarden.org`.
4. **Fullscreen Botanical Lightbox**: Native plants feature an interactive modal lightbox supporting high-resolution image rendering (`large960`), slide navigation, keyboard shortcuts (Left/Right arrows, Escape), and specimen labels.
5. **English Ivy (*Hedera helix*) Correction**: Corrected previous misidentified ground ivy imagery with verified Bugwood / Invasive.org specimens showing juvenile lobed leaves, adult flowering stems, tree-girdling vines, and ecological infestations.

---

## ⚖️ 7. Two-Tier Database Change Approval Workflow

To safeguard the integrity of the master botanical database, the system enforces a strict two-tier approval workflow for all catalog modifications:

```
+-----------------------------------------------------------------------+
| NATURE ADVISOR PROPOSES CHANGE                                        |
| 1. Advisor edits an existing plant record OR adds a new plant record. |
| 2. Changes are packaged into an Approval Proposal object.             |
| 3. Proposal is stored locally & synced to Firestore:                  |
|    - /plant_approvals/{approvalId}                                    |
|    - /plants/_approval_{approvalId} (fallback)                        |
| 4. Plant displays "Pending Review" badge in catalog grid & modal.     |
+-----------------------------------------------------------------------+
                                    │
                                    ▼
+-----------------------------------------------------------------------+
| ADMINISTRATOR REVIEW & DECISION                                       |
| 1. Admin opens "Approval Inbox" tab in Administration Console.        |
| 2. Admin inspects side-by-side field diffs (Old vs New values).       |
| 3. Action options:                                                    |
|    • APPROVE: Changes applied to master catalog, saved to custom      |
|      plants cache, and patched directly to master Firestore /plants/. |
|    • DENY: Changes rejected, reviewer audit notes recorded.           |
| 4. Status synchronized across all connected client devices.           |
+-----------------------------------------------------------------------+
```

---

## 📚 8. Exhaustive Function Reference (129 Functions)"""

    if old_sec6 in doc:
        doc = doc.replace(old_sec6, new_features_sec, 1)
        print("Added MOBOT & Approval sections to CODE_DOCUMENTATION.md")

    # Add the 11 new functions to Section 8 in CODE_DOCUMENTATION.md
    new_funcs_doc = """### Module 10: Missouri Botanical Garden Gallery & Approval Workflow (11 Functions)

#### `renderPlantGallery(plant)`
- **Async**: No
- **Parameters**: `plant` (Object)
- **Description**: Renders the multi-image botanical photo gallery into the plant detail modal. Displays specimen cards, photo count badge, mandatory credit "Courtesy Missouri Botanical Garden PlantFinder", and direct linkbacks to each species' MOBOT profile.

#### `openPlantLightbox(plant, initialIdx = 0)`
- **Async**: No
- **Parameters**: `plant` (Object), `initialIdx` (Number, default `0`)
- **Description**: Opens a high-resolution, accessible fullscreen modal lightbox displaying authentic MOBOT photography with previous/next slide navigation, keyboard arrow support, credit banner, and direct links to the official PlantFinder page.

#### `openAddPlantModal()`
- **Async**: No
- **Parameters**: None
- **Description**: Opens the Kansas City Native Plant contribution modal. Dynamically adjusts guidance notices and submit button labels depending on whether the user is an Administrator (direct addition) or an Advisor (submission for approval).

#### `renderAdminApprovals(filterTerm = '')`
- **Async**: No
- **Parameters**: `filterTerm` (String, optional)
- **Description**: Renders all pending, approved, and denied plant change requests in the Administrator Approval Inbox. Generates side-by-side field diffs for edits and full specification checklists for new plant additions.

#### `approvePlantChange(approvalId)`
- **Async**: Yes
- **Parameters**: `approvalId` (String)
- **Description**: Administrator action to approve a pending change request. Automatically updates the plant in the active catalog, persists edits to local storage, syncs to master Cloud Firestore `/plants/`, marks approval status as approved, and refreshes the catalog grid.

#### `denyPlantChange(approvalId)`
- **Async**: Yes
- **Parameters**: `approvalId` (String)
- **Description**: Administrator action to deny a proposed edit or new plant contribution with confirmation, marking the approval request as denied and archiving it in Firestore.

#### `syncPlantToFirestore(plant)`
- **Async**: Yes
- **Parameters**: `plant` (Object)
- **Description**: Formats and serializes a native plant record into a Firestore document structure and issues an HTTP PATCH request to update the master record at `/plants/{plantId}`.

#### `savePlantApprovalToFirestore(approval)`
- **Async**: Yes
- **Parameters**: `approval` (Object)
- **Description**: Dual-writes a plant approval request to the primary collection `/plant_approvals/{id}` and fallback sync document `/plants/_approval_{id}`.

#### `fetchPlantApprovalsFromFirestore()`
- **Async**: Yes
- **Parameters**: None
- **Description**: Scans Firestore `/plant_approvals` and fallback `plants/` collections for approval requests, deduplicates them, updates the local cache, and refreshes approval badges.

#### `deletePlantApprovalFromFirestore(approvalId)`
- **Async**: Yes
- **Parameters**: `approvalId` (String)
- **Description**: Permanently purges a plant approval document from both primary and fallback collections in Cloud Firestore.

#### `updateApprovalBadges()`
- **Async**: No
- **Parameters**: None
- **Description**: Calculates the number of pending plant approval requests in `state.plantApprovals` and updates the numeric count badges on the Administrator Approval tab and User Profile drawer.

---
"""

    if "### Module 1: Core & Utilities" in doc:
        doc = doc.replace("### Module 1: Core & Utilities", new_funcs_doc + "\n### Module 1: Core & Utilities", 1)
        print("Added new functions to function reference in CODE_DOCUMENTATION.md")

    with open('CODE_DOCUMENTATION.md', 'w', encoding='utf-8') as f:
        f.write(doc)
    print("CODE_DOCUMENTATION.md updated successfully!")


def update_docs_html():
    with open('docs.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update nav bar in docs.html
    old_nav = """        <a href="#admin-repo" class="nav-item">
          <i data-lucide="folder-git-2"></i>
          <span>Reports Repository</span>
        </a>
        <a href="#a11y" class="nav-item">"""

    new_nav = """        <a href="#admin-repo" class="nav-item">
          <i data-lucide="folder-git-2"></i>
          <span>Reports Repository</span>
        </a>
        <a href="#botanical-gallery" class="nav-item">
          <i data-lucide="camera"></i>
          <span>MOBOT PlantFinder Gallery</span>
        </a>
        <a href="#approval-workflow" class="nav-item">
          <i data-lucide="inbox"></i>
          <span>Database Approval Inbox</span>
        </a>
        <a href="#a11y" class="nav-item">"""

    if old_nav in html:
        html = html.replace(old_nav, new_nav, 1)
        print("Updated navigation bar in docs.html")

    # 2. Add sections before #a11y in docs.html
    old_a11y_sec = '      <!-- Accessibility & Inclusive UX Engineering -->'
    new_sections = """      <!-- Missouri Botanical Garden PlantFinder Multi-Image Gallery -->
      <section id="botanical-gallery" class="doc-section">
        <div class="section-header">
          <h2 class="section-title"><i data-lucide="camera" style="color:var(--primary);"></i> Missouri Botanical Garden PlantFinder Multi-Image Gallery &amp; Lightbox</h2>
          <span class="nav-badge" style="background:#dcfce7;color:#166534;">179 Species · 1,231 Photos</span>
        </div>
        <p class="section-lead">
          The Kansas City Native Plant Database integrates authentic botanical specimen photography from the <strong>Missouri Botanical Garden PlantFinder</strong> (MOBOT). 179 regional indigenous species feature curated multi-photo galleries with strict attribution and deep linkbacks.
        </p>

        <div class="grid-2col" style="margin-top:16px;">
          <div style="background:var(--bg-base);padding:18px;border-radius:var(--radius-md);border-left:4px solid var(--primary);">
            <h4 style="font-size:14px;font-weight:800;color:var(--primary);margin:0 0 8px 0;display:flex;align-items:center;gap:6px;">
              <i data-lucide="image" style="width:16px;height:16px;"></i>
              <span>High-Resolution Photo Galleries</span>
            </h4>
            <p style="font-size:13px;line-height:1.5;color:var(--text-secondary);margin:0;">
              Over 1,231 specimen photos cover flower close-ups, whole-plant growth forms, leaf morphology, fall color transformations, and winter architecture. Plant cards show photo count badges, and detail modals render interactive thumbnail strips.
            </p>
          </div>

          <div style="background:var(--bg-base);padding:18px;border-radius:var(--radius-md);border-left:4px solid #16a34a;">
            <h4 style="font-size:14px;font-weight:800;color:#16a34a;margin:0 0 8px 0;display:flex;align-items:center;gap:6px;">
              <i data-lucide="external-link" style="width:16px;height:16px;"></i>
              <span>Attribution &amp; Source Linking</span>
            </h4>
            <p style="font-size:13px;line-height:1.5;color:var(--text-secondary);margin:0;">
              Every photograph is credited as <strong>"Courtesy Missouri Botanical Garden PlantFinder"</strong> and includes an outbound link directly to the plant's official information page on <code>missouribotanicalgarden.org</code>.
            </p>
          </div>
        </div>

        <div style="margin-top:16px;background:var(--bg-surface);padding:16px;border-radius:var(--radius-md);border:1px solid var(--border-subtle);">
          <h4 style="font-size:13px;font-weight:800;margin:0 0 6px 0;display:flex;align-items:center;gap:6px;">
            <i data-lucide="maximize-2" style="width:15px;height:15px;color:var(--primary);"></i>
            <span>Accessible Fullscreen Modal Lightbox</span>
          </h4>
          <p style="font-size:12px;color:var(--text-secondary);margin:0;line-height:1.5;">
            Clicking any specimen photo opens <code>openPlantLightbox(plant, idx)</code> with full high-resolution rendering (<code>large960</code>), photo counter, keyboard arrow slide transitions, and screen-reader announcements.
          </p>
        </div>

        <div style="margin-top:14px;background:#fef2f2;border-left:4px solid #ef4444;padding:12px 16px;border-radius:var(--radius-sm);font-size:12px;color:#991b1b;line-height:1.5;">
          <strong>🌿 English Ivy (*Hedera helix*) Invasive Image Correction:</strong> Previous misidentified photos of Ground Ivy (*Glechoma hederacea*) were corrected with verified Bugwood / Invasive.org specimens showing juvenile foliage, mature climbing vines, flowers, and tree-smothering infestations.
        </div>
      </section>

      <!-- Database Change Approval Workflow -->
      <section id="approval-workflow" class="doc-section">
        <div class="section-header">
          <h2 class="section-title"><i data-lucide="inbox" style="color:var(--primary);"></i> Two-Tier Database Change Approval Workflow</h2>
          <span class="nav-badge" style="background:#fef3c7;color:#92400e;">Governance &amp; Quality Control</span>
        </div>
        <p class="section-lead">
          Any plant edits or new plant additions submitted by non-administrator users (Nature Advisors) route to an approval inbox for Administrator review before landing in the master database.
        </p>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px;">
          <div style="background:var(--bg-base);padding:16px;border-radius:var(--radius-md);border:1px solid var(--border-subtle);">
            <div style="font-weight:800;color:var(--primary);font-size:13px;margin-bottom:6px;display:flex;align-items:center;gap:6px;">
              <i data-lucide="user" style="width:14px;height:14px;"></i>
              <span>Nature Advisor Submission Flow</span>
            </div>
            <ul style="font-size:12px;color:var(--text-secondary);padding-left:18px;margin:0;line-height:1.6;">
              <li>Advisor edits a plant record or contributes a new species in "Contribute New Native Plant".</li>
              <li>Proposal is submitted to the Admin Approval Inbox (marked <code>status: 'pending'</code>).</li>
              <li>A <span style="background:#fef3c7;color:#92400e;padding:1px 6px;border-radius:3px;font-weight:700;">Pending Review</span> badge displays on the plant card and detail modal.</li>
            </ul>
          </div>

          <div style="background:var(--bg-base);padding:16px;border-radius:var(--radius-md);border:1px solid var(--border-subtle);">
            <div style="font-weight:800;color:#15803d;font-size:13px;margin-bottom:6px;display:flex;align-items:center;gap:6px;">
              <i data-lucide="shield-check" style="width:14px;height:14px;"></i>
              <span>Administrator Review &amp; Master Apply</span>
            </div>
            <ul style="font-size:12px;color:var(--text-secondary);padding-left:18px;margin:0;line-height:1.6;">
              <li>Administrator opens "Approval Inbox" tab in the Admin Console.</li>
              <li>Inspects side-by-side diffs showing exactly which fields were changed.</li>
              <li>Clicking <strong>"Approve &amp; Apply"</strong> updates the master catalog, saves local edits, and patches Cloud Firestore.</li>
              <li>Clicking <strong>"Deny"</strong> records reviewer notes and rejects the change.</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Accessibility & Inclusive UX Engineering -->"""

    if old_a11y_sec in html:
        html = html.replace(old_a11y_sec, new_sections, 1)
        print("Added new documentation sections to docs.html")

    # 3. Add new functions to FUNCTIONS_CATALOG in docs.html
    new_catalog_entries = """      // Missouri Botanical Garden PlantFinder & Approval Workflow
      { name: "renderPlantGallery", params: "plant", module: "catalog", line: 8996, isAsync: false, desc: "Renders the multi-image botanical photo gallery into the plant detail modal with count badge, credit Courtesy Missouri Botanical Garden PlantFinder, and direct profile links." },
      { name: "openPlantLightbox", params: "plant, initialIdx = 0", module: "catalog", line: 9085, isAsync: false, desc: "Opens a high-resolution, accessible fullscreen modal lightbox displaying authentic MOBOT photography with slide navigation, keyboard shortcuts, and credit banner." },
      { name: "openAddPlantModal", params: "", module: "catalog", line: 9345, isAsync: false, desc: "Opens the native plant contribution dialog with role-aware notices (direct addition for Admins, approval submission for Advisors)." },
      { name: "renderAdminApprovals", params: "filterTerm = ''", module: "admin", line: 9480, isAsync: false, desc: "Renders the list of pending, approved, and denied plant change requests in the Administrator Approval Inbox with side-by-side field diffs." },
      { name: "approvePlantChange", params: "approvalId", module: "admin", line: 9610, isAsync: true, desc: "Administrator action to approve a proposed plant edit or new species, updating the master database and synchronizing across Cloud Firestore." },
      { name: "denyPlantChange", params: "approvalId", module: "admin", line: 9655, isAsync: true, desc: "Administrator action to deny a proposed plant edit or new species with confirmation, archiving the decision in Firestore." },
      { name: "syncPlantToFirestore", params: "plant", module: "sync", line: 9190, isAsync: true, desc: "Serializes a native plant record into a Firestore document structure and executes an HTTP PATCH to update /plants/{plantId}." },
      { name: "savePlantApprovalToFirestore", params: "approval", module: "sync", line: 9270, isAsync: true, desc: "Dual-writes an approval record to /plant_approvals/{id} and fallback sync document /plants/_approval_{id}." },
      { name: "fetchPlantApprovalsFromFirestore", params: "", module: "sync", line: 9310, isAsync: true, desc: "Fetches approval records from Cloud Firestore, merges with local storage, and updates badge counts." },
      { name: "deletePlantApprovalFromFirestore", params: "approvalId", module: "sync", line: 9360, isAsync: true, desc: "Permanently deletes an approval record from Cloud Firestore across primary and fallback paths." },
      { name: "updateApprovalBadges", params: "", module: "admin", line: 9340, isAsync: false, desc: "Calculates the count of pending plant change requests and updates UI badges across the app." },
"""

    if '// Complete catalog of 118 functions from index.html' in html:
        html = html.replace('// Complete catalog of 118 functions from index.html', '// Complete catalog of 129 functions from index.html\n' + new_catalog_entries, 1)
        html = html.replace('Comprehensive Function Reference (118 Functions)', 'Comprehensive Function Reference (129 Functions)')
        html = html.replace('Showing 118 of 118', 'Showing 129 of 129')
        html = html.replace('All Modules (118)', 'All Modules (129)')
        html = html.replace('Admin Repository &amp; Roster (13)', 'Admin Repository &amp; Roster (16)')
        html = html.replace('Catalog &amp; Filtering (22)', 'Catalog &amp; Filtering (25)')
        html = html.replace('Firestore &amp; Master Sync (8)', 'Firestore &amp; Master Sync (12)')
        html = html.replace('118 functions', '129 functions')
        print("Updated FUNCTIONS_CATALOG in docs.html")

    with open('docs.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("docs.html updated successfully!")


if __name__ == '__main__':
    update_code_documentation()
    update_docs_html()
