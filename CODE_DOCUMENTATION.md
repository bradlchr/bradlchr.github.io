# Deep Roots Database - Codebase Architecture & Technical Reference Manual

A comprehensive technical manual and function-by-function guide for the **Deep Roots Kansas City Native Plant Database** codebase (`index.html`).

Live Interactive Documentation: [**bradlchr.github.io/docs.html**](https://bradlchr.github.io/docs.html)  
Application Deployment: [**bradlchr.github.io**](https://bradlchr.github.io/)  
Primary Code Repository: [**github.com/bradlchr/deep-roots-nature-advisors**](https://github.com/bradlchr/deep-roots-nature-advisors)

---

## 🏛️ 1. Overall System Architecture

The Deep Roots Database application is constructed as an **offline-first, zero-build, reactive single-page web application** paired with a companion native **Android/ChromeOS** client.

```
+-----------------------------------------------------------------------------------------+
|                                    CLIENT BROWSER                                       |
|                                                                                         |
|  +--------------------+     +------------------------+     +-------------------------+  |
|  |   Core Runtime     | <-> |   Reactive UI & Views  | <-> |  Client-Side Engines    |  |
|  |   - Central State  |     |   - Catalog Grid       |     |  - OpenXML Word Builder |  |
|  |   - Event System   |     |   - Staging Drawer     |     |  - SHA-256 RBAC Auth    |  |
|  |   - Local Caches   |     |   - Admin Repository   |     |  - Color Mesh Gradient  |  |
|  +--------------------+     +------------------------+     +-------------------------+  |
|            ^                                                            |               |
+------------|------------------------------------------------------------|---------------+
             |                                                            |
             v                                                            v
+-------------------------+                                 +-----------------------------+
|    BROWSER STORAGE      |                                 |   OFFICIAL CLIENT EXPORTS   |
|   (localStorage API)    |                                 |                             |
| - dr_consultations      |                                 | - Microsoft Word (.docx)    |
| - dr_users_roster       |                                 | - Formatted Markdown        |
| - dr_custom_plants      |                                 | - Standalone HTML Reports   |
| - dr_text_scale         |                                 +-----------------------------+
+-------------------------+                                               ^
             ^                                                            |
             |                                                            |
             v                                                            |
+-------------------------------------------------------------------------|---------------+
|                       GOOGLE CLOUD FIRESTORE (REST API v1)                              |
|                                                                                         |
|  - /plants/{plantId}            -> 185 Master botanical records + live advisor edits    |
|  - /users/{username}            -> Nature Advisor profiles, credentials, security salts |
|  - /reports/{reportId}          -> Central organization consultation repository         |
|  - /users/{username}/reports/*  -> User-scoped personal consultation backups            |
+-----------------------------------------------------------------------------------------+
```

### Architectural Pillars:
1. **Zero-Build Distribution**: The complete web client runs directly from raw standards-compliant HTML5, CSS3, and ES6+ JavaScript. No node compilation, bundling, or minification is required to deploy or execute.
2. **Offline-First Resilience**: All critical client consultation data, garden areas, staged native palettes, advisor preferences, and local customizations persist in `localStorage`.
3. **Direct Cloud Mesh**: Client browsers communicate directly with Google Cloud Firestore via HTTPS REST endpoints without intermediate middleware servers.
4. **Client-Side OpenXML Synthesis**: Generates authentic, enterprise-grade Microsoft Word `.docx` documents in memory using client-side ZIP decompression and reverse-offset XML splicing.

---

## 🛠️ 2. Technology Stack & Dependencies

| Layer | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Language** | Vanilla JavaScript | ECMAScript 2022+ | Core reactive state, UI manipulation, cryptographic hashing, and REST dispatch. |
| **Styling** | Modern CSS3 | Custom Properties | Fluid rem layouts, dynamic theme tokens, glassmorphism (`backdrop-filter`), and CSS mesh gradients. |
| **Document Engine**| `JSZip` | v3.10.1 (CDN) | Client-side unpack, modification, and repack of OpenXML `.docx` templates. |
| **Cryptography** | Web Crypto API | `window.crypto` | Cryptographically random salt generation and SHA-256 password hashing. |
| **Cloud Storage** | Google Cloud Firestore | REST API v1 | Serverless document storage for plants, users, and consultation reports. |
| **Iconography** | Lucide Icons | v0.344.0 (CDN) | Accessible SVG iconography rendered dynamically via `lucide.createIcons()`. |
| **Typography** | Plus Jakarta Sans & Inter | Google Fonts | High-legibility typography with JetBrains Mono for data displays. |
| **Native Mobile** | Android SDK & Compose | Kotlin / Compose | Material 3 adaptive UI, Room local database, and WorkManager background sync. |

---

## 🔒 3. Three-Tier Role-Based Access Control (RBAC)

The application enforces a 3-tier authorization model:

```
+-----------------------------------------------------------------------------------+
| GUEST (Unauthenticated)                                                           |
| - Read-only botanical catalog browsing (185 native species, 10 invasives)         |
| - Search, filter, and sort by ecological requirements                             |
| - View vetted contractor directory and plant details                              |
| - STAGING DRAWER & EDITING CONTROLS ARE HIDDEN                                    |
+-----------------------------------------------------------------------------------+
                                         │  Sign In with Username & Password
                                         ▼
+-----------------------------------------------------------------------------------+
| NATURE ADVISOR (role: 'user')                                                     |
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
+-----------------------------------------------------------------------------------+
```

---

## 📄 4. OpenXML Word Report Generation Engine

The `.docx` generator (`downloadDocxReport`) transforms the official 1.4 MB Microsoft Word template into a finalized client deliverable without backend servers:

### Processing Pipeline:
1. **Archive Decompression**: `JSZip.loadAsync()` unzips `report_template.docx` and extracts `word/document.xml`.
2. **Directive Stripping**: Uses regex to identify all instructional paragraphs styled with red text (`w:color w:val="FF0000"`).
3. **Invasive Logic Branching**:
   - **Case A (Invasive-Free)**: Retains congratulations text and Big Three vigilance links; purges Case B.
   - **Case B (Invasives Found)**: Replaces placeholder lists with staged species and removal notes; appends remaining Big Three advice; purges Case A.
4. **Wildlife & Stormwater Splicing**: Evaluates consultation toggles (Nest Boxes, Bird Baths, Bat Boxes, Bee Habitat, Johnson County, Wyandotte County, Rainwater Harvesting) and slices unselected sections out of the document.
5. **Reverse-Offset Splicing**: Splicing operations occur in reverse order (highest byte offset to lowest). This ensures subsequent character positions remain intact, preventing document corruption.
6. **Dynamic Recommendation Injection**: Formats styled plant cards grouped by garden area with Grow Native! hyperlinks, botanical bullet points, and customized advisor planting instructions.
7. **Archive Generation & Download**: Compresses the updated XML into a binary blob and initiates client browser download.

---

## ☁️ 5. Google Cloud Firestore Document Schema

All cloud operations target project `deep-roots-nature-advisors`:

### Collections & Document Paths:
- **`/plants/{plantId}`**: Master botanical catalog.
  - Fields: `scientific_name`, `common_names`, `native_environment`, `plant_type`, `mature_height`, `advisor_description`, `bloom_color`, `bloom_period`, `light_requirements`, `moisture_requirements`, `sociability`, `updated_by`, `last_edited_by_user_name`.
- **`/users/{username}`**: Nature Advisor roster records.
  - Fields: `username`, `firstName`, `lastName`, `email`, `phoneNumber`, `advisorType`, `role` (`user` | `admin`), `passwordHash`, `salt`, `isTemporaryPassword`.
- **`/reports/{reportId}`**: Top-level consultation repository.
  - Fields: `id`, `client_name`, `client_address`, `consultation_date`, `advisor_name`, `username`, `garden_areas`, `staged_recommendations`, `staged_invasives`, `report_options`, `last_modified`.
- **`/users/{username}/reports/{reportId}`**: User-scoped consultation subcollection.
- **`/plant_approvals/{approvalId}`**: Dedicated collection for pending and historical plant approval requests (edits and new species additions).
- **`/plants/_approval_{approvalId}`**: Fallback cloud sync path for plant approval requests.
- **`/plants/_report_{username}_{reportId}`**: Fallback consultation storage path.

---

## 🌸 6. Missouri Botanical Garden PlantFinder & Image Engine

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

## 📚 8. Exhaustive Function Reference (129 Functions)

Below is the complete reference of all 118 functions declared in `index.html`, organized by functional subsystem:

### Module 10: Missouri Botanical Garden Gallery & Approval Workflow (11 Functions)

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

### Module 1: Core & Utilities (4 Functions)

#### `escapeHtml(str)`
- **Line**: 3841 | **Async**: No
- **Parameters**: `str` (String)
- **Description**: Replaces HTML-sensitive characters (`&`, `<`, `>`, `"`, `'`) with entity equivalents to prevent cross-site scripting (XSS) when constructing innerHTML strings.

#### `escapeXml(str)`
- **Line**: 3851 | **Async**: No
- **Parameters**: `str` (String)
- **Description**: Escapes XML reserved characters for safe insertion inside OpenXML Word tags.

#### `formatTimeAgo(timestamp)`
- **Line**: 5277 | **Async**: No
- **Parameters**: `timestamp` (Number)
- **Description**: Returns friendly relative elapsed time descriptions (e.g., "Just now", "4m ago", "2h ago", "5d ago").

#### `getActiveUsername()`
- **Line**: 5290 | **Async**: No
- **Parameters**: None
- **Description**: Returns the active authenticated advisor's username, or `"guest"` if unauthenticated.

---

### Module 2: Botanical Taxonomy & Helpers (10 Functions)

#### `shouldShowScientificFirst()`
- **Line**: 4578 | **Async**: No
- **Parameters**: None
- **Description**: Checks user display preference (`dr_name_display_pref`) to determine whether scientific names precede common names.

#### `isSweet16(plant)`
- **Line**: 4592 | **Async**: No
- **Parameters**: `plant` (Object)
- **Description**: Returns `true` if the plant is designated as a Deep Roots Sweet 16 heartland pollinator species.

#### `isKcKeystone(plant)`
- **Line**: 4601 | **Async**: No
- **Parameters**: `plant` (Object)
- **Description**: Returns `true` if the plant is a recognized Kansas City Keystone ecological host species.

#### `getPlantUrl(p)`
- **Line**: 6873 | **Async**: No
- **Parameters**: `p` (Object)
- **Description**: Resolves the plant's official Grow Native! profile URL or generates a slug-based fallback.

#### `getPlantHeight(p)`
- **Line**: 6885 | **Async**: No
- **Parameters**: `p` (Object)
- **Description**: Formats and returns the standardized mature height bracket display string.

#### `getPlantLayer(p)`
- **Line**: 6894 | **Async**: No
- **Parameters**: `p` (Object)
- **Description**: Returns the architectural layer of the plant (Canopy, Understory, Structural, Seasonal, or Groundcover).

#### `getPlantDesc(p)`
- **Line**: 6898 | **Async**: No
- **Parameters**: `p` (Object)
- **Description**: Retrieves the concise 3-line advisor field description.

#### `getPlantSociability(p)`
- **Line**: 6902 | **Async**: No
- **Parameters**: `p` (Object)
- **Description**: Retrieves the Curious by Nature matrix sociability behavior (Solitary, Moderate, Highly Social).

#### `getBloomColorAccent(colorName, isDark)`
- **Line**: 8437 | **Async**: No
- **Parameters**: `colorName` (String), `isDark` (Boolean)
- **Description**: Maps bloom color names to high-contrast calibrated RGB/HEX values.

#### `getBloomCardGradient(bloomColors, isDark)`
- **Line**: 8476 | **Async**: No
- **Parameters**: `bloomColors` (Array), `isDark` (Boolean)
- **Description**: Synthesizes radiant radial/linear CSS background mesh gradients matching seasonal flower colors.

---

### Module 3: Authentication, Security & RBAC (22 Functions)

#### `hashPassword(password, salt)`
- **Line**: 4609 | **Async**: Yes
- **Parameters**: `password` (String), `salt` (String)
- **Description**: Computes a SHA-256 cryptographic digest combining salt and password via the Web Crypto API.

#### `generateSalt()`
- **Line**: 4617 | **Async**: No
- **Parameters**: None
- **Description**: Generates a 16-byte random hex salt using `window.crypto.getRandomValues()`.

#### `isPasswordStrong(pw)`
- **Line**: 4623 | **Async**: No
- **Parameters**: `pw` (String)
- **Description**: Verifies password complexity requirements (≥8 chars, uppercase, lowercase, numeric digits).

#### `generateCanonicalUsername(firstName, lastName, existingUsers)`
- **Line**: 4631 | **Async**: No
- **Parameters**: `firstName` (String), `lastName` (String), `existingUsers` (Array)
- **Description**: Creates canonical `<first>.<last>` usernames with automatic numerical collision handling.

#### `generateTemporaryPassword()`
- **Line**: 4650 | **Async**: No
- **Parameters**: None
- **Description**: Produces a cryptographically random 10-character temporary password for newly provisioned advisors.

#### `loadUsersCache()`
- **Line**: 4661 | **Async**: No
- **Parameters**: None
- **Description**: Retrieves and parses the local advisor roster cache stored in `localStorage` (`dr_users_roster`).

#### `saveUsersCache(users)`
- **Line**: 4669 | **Async**: No
- **Parameters**: `users` (Array)
- **Description**: Commits the advisor roster array to `localStorage`.

#### `userToFirestoreDoc(u)`
- **Line**: 4681 | **Async**: No
- **Parameters**: `u` (Object)
- **Description**: Formats an internal advisor object into a Cloud Firestore REST document payload.

#### `parseFirestoreUser(doc)`
- **Line**: 4703 | **Async**: No
- **Parameters**: `doc` (Object)
- **Description**: Converts a Firestore user document response into an internal Nature Advisor record.

#### `syncUserToFirestore(user)`
- **Line**: 4735 | **Async**: Yes
- **Parameters**: `user` (Object)
- **Description**: Dispatches an authenticated PATCH request to synchronize an advisor profile to Firestore.

#### `fetchAllRemoteUsers()`
- **Line**: 4758 | **Async**: Yes
- **Parameters**: None
- **Description**: Fetches all advisor accounts from Firestore `/users` and updates the local roster cache.

#### `initAdvisorAuth()`
- **Line**: 4800 | **Async**: Yes
- **Parameters**: None
- **Description**: Initializes auth on app startup, seeds default administrators, and validates active sessions.

#### `getUserInitials(u)`
- **Line**: 4876 | **Async**: No
- **Parameters**: `u` (Object)
- **Description**: Extracts two-letter initials from an advisor's full name for header avatar badges.

#### `userRecordToProfile(u)`
- **Line**: 4908 | **Async**: No
- **Parameters**: `u` (Object)
- **Description**: Sanitizes a user record into a safe, client-facing profile omitting password hashes.

#### `loginAdvisor(usernameOrEmail, password)`
- **Line**: 5009 | **Async**: Yes
- **Parameters**: `usernameOrEmail` (String), `password` (String)
- **Description**: Authenticates an advisor, verifies salt hashes, initializes consultations, and renders UI.

#### `signOutAdvisor()`
- **Line**: 5062 | **Async**: Yes
- **Parameters**: None
- **Description**: Terminates active session, clears auth storage, restores text scaling, and activates guest mode.

#### `changeAdvisorPassword(newPassword)`
- **Line**: 5080 | **Async**: Yes
- **Parameters**: `newPassword` (String)
- **Description**: Updates an advisor's password, generating fresh salt/hash and syncing to Cloud Firestore.

#### `provisionAdvisor(firstName, lastName, email, phoneNumber, advisorType, role)`
- **Line**: 5110 | **Async**: Yes
- **Parameters**: Six advisor registration parameters
- **Description**: Administrator function to provision a new Nature Advisor and issue temporary credentials.

#### `resetAdvisorPassword(username)`
- **Line**: 5151 | **Async**: Yes
- **Parameters**: `username` (String)
- **Description**: Admin utility to generate a temporary password reset token for an advisor.

#### `toggleAdvisorRole(username)`
- **Line**: 5177 | **Async**: Yes
- **Parameters**: `username` (String)
- **Description**: Admin privilege to toggle an advisor's system role between `user` and `admin`.

#### `updateAdvisorUser(username, updates)`
- **Line**: 5202 | **Async**: Yes
- **Parameters**: `username` (String), `updates` (Object)
- **Description**: Commits administrative updates to an advisor profile (phone, email, role, type) to cloud and cache.

#### `openEditUserModal(username)`
- **Line**: 8004 | **Async**: No
- **Parameters**: `username` (String)
- **Description**: Opens the admin advisor record modal dialog pre-filled with the selected user's metadata.

---

### Module 4: Botanical Catalog, Filtering & Grid UI (12 Functions)

#### `loadMasterPlants()`
- **Line**: 6907 | **Async**: No
- **Parameters**: None
- **Description**: Loads the 185 baseline heartland native plant species from memory into active catalog state.

#### `applyCustomEditsToPlants()`
- **Line**: 6949 | **Async**: No
- **Parameters**: None
- **Description**: Merges local advisor plant customizations (`dr_custom_plants`) into active species records.


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

#### `applyFilters()`
- **Line**: 8158 | **Async**: No
- **Parameters**: None
- **Description**: Filters the catalog against search queries, light, moisture, height, layers, and badges.

#### `sortPlants()`
- **Line**: 8268 | **Async**: No
- **Parameters**: None
- **Description**: Sorts filtered plants by common name, scientific name, height, or flagship program priority.

#### `renderActiveFilterTags()`
- **Line**: 8307 | **Async**: No
- **Parameters**: None
- **Description**: Renders interactive, dismissible active filter tag chips above the catalog grid.

#### `resetAllFilters()`
- **Line**: 8371 | **Async**: No
- **Parameters**: None
- **Description**: Resets all active search inputs and filter chips, restoring the full catalog view.

#### `renderGrid()`
- **Line**: 8405 | **Async**: No
- **Parameters**: None
- **Description**: Renders the main catalog plant card grid with photo badges, actions, and bloom gradients.

#### `createPlantCard(plant)`
- **Line**: 8532 | **Async**: No
- **Parameters**: `plant` (Object)
- **Description**: Creates the DOM element for an individual plant card with adaptive actions for guests and advisors.

#### `openPlantDetail(plant)`
- **Line**: 8821 | **Async**: No
- **Parameters**: `plant` (Object)
- **Description**: Opens the botanical detail modal showing descriptions, cultural requirements, and wildlife benefits.

#### `openEditModal(plant)`
- **Line**: 8918 | **Async**: No
- **Parameters**: `plant` (Object)
- **Description**: Opens the plant record editor modal allowing advisors to customize descriptions and bloom data.

#### `updateHeaderInfo()`
- **Line**: 7146 | **Async**: No
- **Parameters**: None
- **Description**: Refreshes species counters, sync times, and synchronizes the header auth bar.

#### `renderAuthUser()`
- **Line**: 7181 | **Async**: No
- **Parameters**: None
- **Description**: Renders header user controls (avatar for advisors, sign-in for guests) and enforces guest staging drawer restrictions.

---

### Module 5: Invasive Species Guide & Contractors (9 Functions)

#### `setCatalogMode(mode)`
- **Line**: 5699 | **Async**: No
- **Parameters**: `mode` (String: `'native'` | `'invasive'`)
- **Description**: Toggles active catalog view between 185 Native Plants and 10 High-Threat Invasive Species.

#### `renderInvasiveGrid(searchTerm)`
- **Line**: 5729 | **Async**: No
- **Parameters**: `searchTerm` (String)
- **Description**: Renders the 10 invasive species cards with threat badges, phenology, and MDC control advice.

#### `openInvasiveDetailModal(plant)`
- **Line**: 5918 | **Async**: No
- **Parameters**: `plant` (Object)
- **Description**: Opens the invasive identification modal with MDC control instructions and high-res photos.

#### `openInvasiveLightbox(plant, initialIdx)`
- **Line**: 6052 | **Async**: No
- **Parameters**: `plant` (Object), `initialIdx` (Number)
- **Description**: Launches the full-screen photo gallery lightbox for an invasive species.

#### `renderSlide(idx)`
- **Line**: 6080 | **Async**: No
- **Parameters**: `idx` (Number)
- **Description**: Displays a specific photo slide with caption and attribution inside the invasive lightbox.

#### `toggleStagedInvasive(plant)`
- **Line**: 6219 | **Async**: No
- **Parameters**: `plant` (Object)
- **Description**: Stages or removes an invasive species in the active report and auto-enables the invasive presence option.

#### `persistStagedInvasives()`
- **Line**: 6246 | **Async**: No
- **Parameters**: None
- **Description**: Commits staged invasive species to `localStorage`.

#### `renderStagedInvasives()`
- **Line**: 6289 | **Async**: No
- **Parameters**: None
- **Description**: Renders the staged invasives list in the drawer with editable observation and removal notes.

#### `openContractorsModal()`
- **Line**: 4479 | **Async**: No
- **Parameters**: None
- **Description**: Opens the modal directory featuring 10 vetted Kansas City invasive removal and habitat contractors.

---

### Module 6: Consultation Workspace & Garden Areas (17 Functions)

#### `persistConsultations()`
- **Line**: 5294 | **Async**: No
- **Parameters**: None
- **Description**: Saves the consultations array to `localStorage` under `dr_consultations`.

#### `updateConsultationCounts()`
- **Line**: 5300 | **Async**: No
- **Parameters**: None
- **Description**: Recalculates consultation totals and updates badges across the application.

#### `initConsultations()`
- **Line**: 5460 | **Async**: Yes
- **Parameters**: None
- **Description**: Loads consultation drafts from `localStorage` and synchronizes with the advisor's cloud reports.

#### `saveActiveConsultation(syncToCloud = false)`
- **Line**: 5539 | **Async**: No
- **Parameters**: `syncToCloud` (Boolean)
- **Description**: Serializes active consultation form inputs, garden areas, staged species, and options into state.

#### `switchActiveConsultation(targetId, skipSaveCurrent = false)`
- **Line**: 5562 | **Async**: No
- **Parameters**: `targetId` (String), `skipSaveCurrent` (Boolean)
- **Description**: Switches the active staging workspace to another client draft, repopulating drawer forms.

#### `updateConsultationOption(consultation)`
- **Line**: 5634 | **Async**: No
- **Parameters**: `consultation` (Object)
- **Description**: Syncs wildlife structure and stormwater cost-share options into a consultation draft.

#### `createNewConsultation(options = {})`
- **Line**: 5646 | **Async**: No
- **Parameters**: `options` (Object)
- **Description**: Creates a new client consultation draft with default garden areas and switches workspace to it.

#### `persistReportOptions()`
- **Line**: 6261 | **Async**: No
- **Parameters**: None
- **Description**: Persists consultation report customization options to `localStorage`.

#### `syncReportOptionsUI()`
- **Line**: 6273 | **Async**: No
- **Parameters**: None
- **Description**: Updates checkbox toggle inputs in the staging drawer to match active consultation options.

#### `renderGardenAreasManager()`
- **Line**: 6365 | **Async**: No
- **Parameters**: None
- **Description**: Renders the garden areas panel in the staging drawer, supporting renaming, adding, and deleting zones.

#### `persistGardenAreas()`
- **Line**: 6440 | **Async**: No
- **Parameters**: None
- **Description**: Commits custom garden planting zones to `localStorage` and the active consultation object.

#### `duplicateConsultation(consultationId)`
- **Line**: 6452 | **Async**: No
- **Parameters**: `consultationId` (String)
- **Description**: Clones an existing consultation draft and loads the duplicated draft into the active workspace.

#### `deleteConsultation(consultationId)`
- **Line**: 6475 | **Async**: Yes
- **Parameters**: `consultationId` (String)
- **Description**: Deletes a consultation locally and deletes documents from Cloud Firestore across all storage paths.

#### `renderConsultationSwitcher()`
- **Line**: 6529 | **Async**: No
- **Parameters**: None
- **Description**: Populates the consultation selector dropdown in the staging drawer with all available drafts.

#### `renderConsultationsModalList(filterQuery = '')`
- **Line**: 6573 | **Async**: No
- **Parameters**: `filterQuery` (String)
- **Description**: Renders the searchable list of client consultations inside the All Consultations dialog.

#### `openConsultationsManagerModal()`
- **Line**: 6658 | **Async**: No
- **Parameters**: None
- **Description**: Opens the consultation management dialog.

#### `renderStaging()`
- **Line**: 8716 | **Async**: No
- **Parameters**: None
- **Description**: Renders staged native plants in the drawer, grouped under their assigned garden planting zones.

---

### Module 7: Plant Staging Drawer UI (4 Functions)

#### `toggleStagedPlant(plant)`
- **Line**: 8652 | **Async**: No
- **Parameters**: `plant` (Object)
- **Description**: Adds or removes a native plant from the active consultation report.

#### `saveStaging()`
- **Line**: 8690 | **Async**: No
- **Parameters**: None
- **Description**: Commits staged plants to `localStorage` and updates active consultation draft.

#### `updateStagedBadge()`
- **Line**: 8704 | **Async**: No
- **Parameters**: None
- **Description**: Updates the numeric pill badge on the Selected Plants header button.

#### `formatAreaHeadingLabel(idx, rawName)`
- **Line**: 9528 | **Async**: No
- **Parameters**: `idx` (Number), `rawName` (String)
- **Description**: Cleans and formats garden area titles for inclusion in official Word report headings.

---

### Module 8: Cloud Firestore Sync & Database Governance (8 Functions)

#### `getFirestoreBaseUrl()`
- **Line**: 4673 | **Async**: No
- **Parameters**: None
- **Description**: Constructs the base Firestore REST API endpoint URL using active project and database IDs.

#### `tryLiveSyncFromDatabase(showNotification = false)`
- **Line**: 6962 | **Async**: Yes
- **Parameters**: `showNotification` (Boolean)
- **Description**: Queries Firestore for remote botanical updates and synchronizes changes into local storage.

#### `queryFirestoreDb(targetDb)`
- **Line**: 6989 | **Async**: Yes
- **Parameters**: `targetDb` (String)
- **Description**: Dispatches HTTP requests to Firestore to retrieve all documents from the plants collection.

#### `replaceWithRemotePlants(remoteList)`
- **Line**: 7060 | **Async**: No
- **Parameters**: `remoteList` (Array)
- **Description**: Replaces local plant catalog definitions with verified remote master records from cloud.

#### `parseFirestoreValue(val)`
- **Line**: 7069 | **Async**: No
- **Parameters**: `val` (Object)
- **Description**: Recursively unwraps Firestore typed values (`stringValue`, `integerValue`, `booleanValue`, `mapValue`, `arrayValue`).

#### `parseFirestoreDoc(doc)`
- **Line**: 7089 | **Async**: No
- **Parameters**: `doc` (Object)
- **Description**: Converts a raw Firestore document response into a native botanical plant object.

#### `saveCurrentReportToCloud()`
- **Line**: 6673 | **Async**: Yes
- **Parameters**: None
- **Description**: Saves the active consultation to Firestore under user subcollections and the top-level repository.

#### `renderSyncModal()`
- **Line**: 7155 | **Async**: No
- **Parameters**: None
- **Description**: Updates sync metrics in the Database Sync modal and enforces admin-only visibility on governance tools.

---

### Module 9: Central Consultation Reports Repository (Admin) (8 Functions)

#### `parseFirestoreReportDoc(doc, fallbackUsername = '')`
- **Line**: 5308 | **Async**: No
- **Parameters**: `doc` (Object), `fallbackUsername` (String)
- **Description**: Transforms a Firestore report document into an internal consultation report model.

#### `fetchRemoteConsultations(username)`
- **Line**: 5412 | **Async**: Yes
- **Parameters**: `username` (String)
- **Description**: Fetches all saved consultation reports belonging to a specific advisor username from Firestore.

#### `fetchAllAdvisorReports()`
- **Line**: 7356 | **Async**: Yes
- **Parameters**: None
- **Description**: Aggregates consultation reports across all advisors, collections, and fallback locations for the repository.

#### `addReport(r)`
- **Line**: 7360 | **Async**: No
- **Parameters**: `r` (Object)
- **Description**: Deduplicates and registers a consultation report into the central repository dataset.

#### `updateAdminReportsBadge(count)`
- **Line**: 7349 | **Async**: No
- **Parameters**: `count` (Number)
- **Description**: Updates the repository report counter badge in the Admin Console and profile menu.

#### `renderAdminReportsRepository(searchQuery = '', advisorFilter = '', sortOrder = 'newest')`
- **Line**: 7462 | **Async**: No
- **Parameters**: Three search and sorting parameters
- **Description**: Renders the central consultation report repository grid with search, advisor filters, and sorting.

#### `openAdminReportDetailModal(report)`
- **Line**: 7671 | **Async**: No
- **Parameters**: `report` (Object)
- **Description**: Opens the administrative inspection dialog for a selected report showing garden areas and options.

#### `adminDeleteConsultationReport(report)`
- **Line**: 7839 | **Async**: Yes
- **Parameters**: `report` (Object)
- **Description**: Admin capability to permanently delete any advisor's consultation report across all Cloud Firestore endpoints.

---

### Module 10: Admin Console & Roster Panel (4 Functions)

#### `loadReportIntoWorkspace(report)`
- **Line**: 7809 | **Async**: No
- **Parameters**: `report` (Object)
- **Description**: Loads a historical consultation report from the repository directly into the active editing workspace.

#### `openAdminConsoleModal(initialTab = 'roster')`
- **Line**: 7940 | **Async**: No
- **Parameters**: `initialTab` (String)
- **Description**: Opens the Program Administrator management dialog, gating access to authenticated admins.

#### `switchAdminTab(tab)`
- **Line**: 7953 | **Async**: No
- **Parameters**: `tab` (String: `'roster'` | `'provision'` | `'reports'`)
- **Description**: Switches between Admin Console tabs: Advisor Roster, Provision New Advisor, and Consultation Repository.

#### `renderAdminRoster(searchQuery = '')`
- **Line**: 8053 | **Async**: No
- **Parameters**: `searchQuery` (String)
- **Description**: Renders the table of registered Nature Advisors with role toggles, password reset triggers, and metadata.

#### `updateCanonicalPreview()`
- **Line**: 7995 | **Async**: No
- **Parameters**: None
- **Description**: Live preview helper in the provision form showing the generated `<first>.<last>` username as names are typed.

---

### Module 11: Word Report Generator & OpenXML Splicing (7 Functions)

#### `getUnobservedBigThree(stagedInvasives)`
- **Line**: 9057 | **Async**: No
- **Parameters**: `stagedInvasives` (Array)
- **Description**: Identifies which of the Big Three invasive threats were not observed on site for vigilance advice.

#### `generateMarkdownReport()`
- **Line**: 9081 | **Async**: No
- **Parameters**: None
- **Description**: Generates an email-friendly structured Markdown representation of the consultation report.

#### `buildHtmlReport()`
- **Line**: 9206 | **Async**: No
- **Parameters**: None
- **Description**: Builds a standalone styled HTML report ready for printing or direct client review.

#### `downloadDocxReport(customReport = null)`
- **Line**: 9347 | **Async**: Yes
- **Parameters**: `customReport` (Object | null)
- **Description**: Main OpenXML report compiler. Injects client data, garden areas, and staged palettes into the official Word template.

#### `findParagraphStart(xml, pos)`
- **Line**: 9403 | **Async**: No
- **Parameters**: `xml` (String), `pos` (Number)
- **Description**: Scans backwards from a match position to find the enclosing `<w:p>` OpenXML start tag.

#### `findParagraphEnd(xml, pos)`
- **Line**: 9409 | **Async**: No
- **Parameters**: `xml` (String), `pos` (Number)
- **Description**: Scans forward from a match position to locate the closing `</w:p>` OpenXML end tag.

---

### Module 12: Accessibility, Dialogs & Theming (13 Functions)

#### `getUserTextScale()`
- **Line**: 4927 | **Async**: No
- **Parameters**: None
- **Description**: Retrieves the active font scaling key (`'standard'`, `'large'`, `'xlarge'`, `'huge'`) from preferences.

#### `setUserTextScale(scaleKey, persistUser = true)`
- **Line**: 4938 | **Async**: No
- **Parameters**: `scaleKey` (String), `persistUser` (Boolean)
- **Description**: Applies dynamic text scaling to the document root element and persists to user storage.

#### `updateTextScaleUI(scaleKey)`
- **Line**: 4965 | **Async**: No
- **Parameters**: `scaleKey` (String)
- **Description**: Updates active button states in the text size preferences modal dialog.

#### `openTextSizeModal()`
- **Line**: 4994 | **Async**: No
- **Parameters**: None
- **Description**: Opens the accessible font size adjustment dialog.

#### `announceToScreenReader(msg, immediate = false)`
- **Line**: 6816 | **Async**: No
- **Parameters**: `msg` (String), `immediate` (Boolean)
- **Description**: Dispatches polite screen reader status announcements to the `aria-live` accessibility announcer region.

#### `openLoginModal()`
- **Line**: 7242 | **Async**: No
- **Parameters**: None
- **Description**: Opens the Nature Advisor sign-in dialog.

#### `openUserProfileModal()`
- **Line**: 7253 | **Async**: No
- **Parameters**: None
- **Description**: Opens the Nature Advisor profile modal showing user metadata, role badge, and quick management links.

#### `openChangePasswordModal(isFirstLogin = false)`
- **Line**: 7301 | **Async**: No
- **Parameters**: `isFirstLogin` (Boolean)
- **Description**: Opens the password update modal dialog, enforcing mandatory changes for first-time logins.

#### `updatePasswordStrengthUI(pw)`
- **Line**: 7324 | **Async**: No
- **Parameters**: `pw` (String)
- **Description**: Audits a prospective password and updates live requirement checkmark badges in the password form.

#### `setReqState(elementId, isValid)`
- **Line**: 7336 | **Async**: No
- **Parameters**: `elementId` (String), `isValid` (Boolean)
- **Description**: Toggles checkmark/cross indicators for individual password complexity criteria.

#### `setupEventListeners()`
- **Line**: 10242 | **Async**: No
- **Parameters**: None
- **Description**: Binds DOM event listeners across all top header controls, drawers, modals, filters, and forms.

#### `updateThemeIcon(t)`
- **Line**: 10259 | **Async**: No
- **Parameters**: `t` (String: `'dark'` | `'light'`)
- **Description**: Synchronizes the theme toggle button icon (sun or moon) with the active dark/light mode state.

---

## ♿ 7. ADA Title III & WCAG 2.1 AA Accessibility Conformance

The application meets or exceeds WCAG 2.1 Level AA criteria:
- **Skip Navigation Link**: Accessible bypass link (`#skip-to-content`) allowing assistive technology users to skip header navigation directly to main content.
- **Dynamic Text Scaling (100%–145%)**: Implements fluid root `rem` scaling without horizontal viewport clipping or component breakage. Persisted across sessions and linked to advisor profiles.
- **Live Screen Reader Announcer**: Dedicated `#a11yAnnouncer` region with `aria-live="polite"` transmitting live announcements for catalog filter updates, report staging, and dialog state changes.
- **Accessible Dialog Trapping**: Native `<dialog>` elements with full keyboard focus trapping, Escape key dismissals, backdrop inerting, and automatic focus restoration upon modal close.
- **High-Contrast Focus Indicators**: High-visibility focus styling (`3px solid #15803d` with `3px` offset) across all interactive cards, filters, buttons, and inputs.
- Full testing audit and assistive technology breakdown available at [`ADA_COMPLIANCE.md`](./ADA_COMPLIANCE.md).

---

*Authored for Deep Roots Nature Advisors · Published on GitHub Pages: [bradlchr.github.io/docs.html](https://bradlchr.github.io/docs.html)*
