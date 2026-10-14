# Deep Roots Nature Advisors - Kansas City Native Plant Database
### *Deep Roots Database*

A multi-platform, production-grade ecological conservation planning application and plant intelligence database built for **Deep Roots Nature Advisors** in the Greater Kansas City region.

Available across platforms:
- 🌐 **Web Application**: [`index.html`](./index.html), hosted live on GitHub Pages at [**bradlchr.github.io**](https://bradlchr.github.io/).
- 💻 **Interactive Code Documentation**: [**`docs.html`**](https://bradlchr.github.io/docs.html) (Live Interactive Portal) and [**`CODE_DOCUMENTATION.md`**](./CODE_DOCUMENTATION.md) — Full technical manual detailing the architecture, technologies used, security, OpenXML pipeline, and reference of all 118 functions.
- 📱 **Native Android & ChromeOS Application**: Pre-compiled [`DeepRootsAdvisor-debug.apk`](./DeepRootsAdvisor-debug.apk) (20 MB), built with Kotlin, Jetpack Compose, and Material 3 Adaptive WindowSizeClass.
- 📄 **Official Word Report Generator**: Integrates the official Deep Roots Word template ([`report_template.docx`](./report_template.docx)) to output genuine, formatted `.docx` consultation reports.
- 📖 **User Guide**: [**Web Application User Guide (`USER_GUIDE.md`)**](./USER_GUIDE.md) — Step-by-step field guide for searching plants, configuring garden zones, and exporting reports.
- ♿ **ADA & WCAG 2.1 AA Compliance Documentation**: Detailed standards mapping, assistive technology testing, and implementation guide at [**`ADA_COMPLIANCE.md`**](./ADA_COMPLIANCE.md).
- 📊 **Program Manager Presentation**: Executive briefing deck at [**`PRESENTATION.md`**](./PRESENTATION.md) (or [**`program_manager_presentation.md`**](./program_manager_presentation.md)) and interactive browser slide deck at [**`presentation.html`**](./presentation.html).

Nature Advisors use the **Deep Roots Database** in the office and out in the field to research native species, evaluate site conditions, curate plant palettes into personalized client reports, and synchronize botanical records in real time via Cloud Firestore.

---

## 🌟 Key Features & Capabilities

### 1. 185 Curated Kansas City Native Plant Species
- **Authoritative Heartland Taxonomy**: Scientific binomials, regional common aliases, native habitats (*Prairie*, *Savannah/Woodland*, *Forest*, *Cliff/Glade*, *Stream Edge/Wetland*).
- **Physical Characteristics & Architecture**: Mature height brackets (`< 1 ft`, `1–3 ft`, `3–6 ft`, `6–15 ft`, `15+ ft`), plant types (*Wildflower*, *Grass*, *Sedge*, *Shrub*, *Tree*, *Vine*, *Fern*), and ecological layers (*Canopy*, *Understory*, *Structural*, *Herbaceous*, *Groundcover*).
- **Phenology & Dynamic Bloom Color Mesh Gradients**: 11 native bloom colors (*Yellow*, *White*, *Purple*, *Pink*, *Blue*, *Orange*, *Red*, *Lavender*, *Cream*, *Greenish*, *Brown/Tan*) with seasonal bloom months. Plant cards render luminous background gradients matching flower colors with frosted glass styling (`backdrop-filter: blur(12px)`).
- **Flagship Conservation Programs**:
  - **⭐ Deep Roots Sweet 16**: 16 high-yield, resilient pollinator species selected for heartland landscapes.
  - **🌿 KC Keystone Species**: Vital ecological host plants (e.g., *Quercus*, *Asclepias*, *Solidago*, *Symphyotrichum*) supporting local biodiversity.
- **Sociability Taxonomy**: *Less Social / Solitary*, *Moderate Spreading*, and *Highly Social / Matrix Groundcover*.
- **Objective Scientific Summaries & Direct Inline Citations**: 2-sentence botanical descriptions completely free of subjective puffery or promotional descriptors (eliminating terms like "exquisite" or "stately"), detailing mature dimensions, leaf form, inflorescence morphology, and soil adaptability. Every factual statement is immediately followed by a direct Markdown link to authoritative sources ([Missouri Botanical Garden PlantFinder](https://www.missouribotanicalgarden.org/PlantFinder/), [Illinois Wildflowers](https://www.illinoiswildflowers.info/), and [Grow Native!](https://grownative.org)).
- **3-Tier Maintenance Taxonomy & Dynamic Seasonal Care**:
  - 🟢 **Low Maintenance (169 species / 91.4%)**: Self-sufficient native perennials, grasses, and trees requiring minimal care once established (conservation spring cutback after sustained 50°F+ temperatures).
  - 🟡 **Medium Maintenance (5 species / 2.7%)**: Species requiring targeted mid-season cultural care (moisture oversight, disease monitoring, cane rejuvenation: *Lobelia cardinalis*, *Cornus florida*, *Phlox paniculata*, *Asimina triloba*, *Sambucus canadensis*).
  - 🔴 **High Maintenance (11 species / 5.9%)**: **Super aggressive spreaders in garden settings** (*Conoclinium coelestinum*, *Oenothera speciosa*, *Anemone canadensis*, *Passiflora incarnata*, *Helianthus salicifolius*, *Chasmanthium latifolium*, *Achillea millefolium*, *Monarda fistulosa*, *Matteuccia struthiopteris*, *Prunus americana*, *Coreopsis palmata*). In residential borders and cultivated garden beds, these demand active seasonal containment (annual boundary spading, digging out runners, pulling aggressive self-sown seedlings, or installing physical root barriers) to prevent taking over beds and displacing companion perennials.
  - **Strict Actionable Seasonal Tiles**: Maintenance guides strictly feature `Spring`, `Summer`, `Fall`, `Winter`, and `Division` cards, omitting inactive seasons completely.
- **Enhanced Wildlife & Ecological Hosts**: Details specific host insect species (caterpillars, butterflies, moths, specialist bees) with direct inline links to Butterflies and Moths of North America (BAMONA) and Xerces Society, as well as specific wildlife foragers with links to Illinois Wildflowers.
- **Missouri Botanical Garden PlantFinder Specimen Photography**: Clean, high-resolution specimen photography with verified attribution and direct links to PlantFinder records.

---

### 2. Native Advisor Authentication & Role-Based Access Control (RBAC)
Replaces third-party Google Sign-In with an integrated, standalone Nature Advisor identity system:
- **Read-Only Guest Mode**: Public visitors and unauthenticated users can freely search, filter, and inspect all 185 plant records. To prevent confusion, the report staging drawer and staging buttons are hidden for guests, presenting a clean botanical catalog.
- **Three Access Tiers**:
  - **Guests (Unauthenticated)**: Read-only botanical discovery and detail views. No staging or catalog modification capabilities.
  - **Nature Advisors (`user`)**: Full plant staging, multi-consultation management, client report creation, and collaborative botanical editing (edits synchronize directly to Cloud Firestore with author attribution). In the Database Sync dialog, advisors can pull fresh data without risk of overwriting the master catalog.
  - **Program Administrators (`admin`)**: All advisor privileges plus:
    - Provisioning new Nature Advisors and issuing temporary credentials.
    - **Central Consultation Reports Repository**: View, search, filter, and re-generate Word reports for any advisor across the organization.
    - **Report Deletion**: Delete reports authored by any user from Cloud Firestore across all collection paths.
    - **Master Catalog Governance**: Exclusive permissions to upload the master catalog to Firestore, reset local edits to pristine defaults, and import JSON backups.
- **Advisor Types**:
  - `Advisor in Training`
  - `Advisor`
  - `Senior Advisor`
  - `Program Manager`
- **Canonical Username Schema**: Enforces `<first>.<last>` with automatic numerical collision handling (e.g., `chris.bradley`, `chris1.bradley`, `chris2.bradley`).
- **Secure Provisioning Workflow**: Generates secure temporary passwords upon provisioning. New advisors are automatically prompted to set a permanent, strong password upon their initial login.
- **Default Administrator Setup**:
  - **Name**: Chris Bradley
  - **Username**: `chris.bradley`
  - **Email**: `ctbbradley@gmail.com`
  - **Role**: `admin`
  - **Advisor Type**: `Advisor in Training`
  - *Note: Initial administrative credentials are provisioned securely out-of-band by the Program Manager or set during initial initialization. No credentials are stored in public documentation.*

---

### 3. Author Attribution on Plant Edits
- Every plant created or updated tracks the advisor who performed the change:
  - `last_edited_by_user_id`
  - `last_edited_by_user_name`
  - `last_edited_by_user_email`
  - `last_edited_timestamp`
- **Live UI Display**: Plant detail views prominently display:
  > *Last edited by: [Advisor Name] ([Advisor Email])*
- Edits synchronize in real time to Cloud Firestore and update local offline caches.

---

### 4. Interactive Plant Editor (with Bloom Color & Season)
- Accessible by signed-in Nature Advisors directly from the plant detail view.
- Supports editing:
  - Common Names & Scientific Binomial
  - Official Plant Profile URL
  - Advisor Description (≤ 3 lines)
  - Light & Soil Moisture Requirements
  - Mature Height Bracket & Sociability
  - **Bloom Colors** (e.g. `Purple, Yellow, White`)
  - **Bloom Season** (e.g. `Summer, Fall`)
  - Image URL & Photographer Attribution
- Saving immediately updates the card's background mesh gradient, bloom indicator dots, and Cloud Firestore catalog.

---

### 5. Name Display & Sorting Toggle
- Interactive toggle in the top control bar and sidebar:
  - **Common Name First**: Displays the common name as the primary bold heading and the scientific name in italics beneath.
  - **Scientific Name First**: Displays the botanical scientific name as the primary italicized serif heading and the common name beneath.
- Dynamically updates all plant cards, the plant detail modal, and the consultation report staging drawer.
- Automatically keeps sorting aligned (Common A–Z vs Scientific A–Z) while allowing independent sorting by Height, Keystone status, or Staging frequency.

---

### 6. Client Consultation Reports & Custom Garden Areas
- **Multi-Consultation Switcher**: Allows advisors to create, rename, switch between, and persist multiple active client consultations.
- **Custom Garden Areas (Planting Zones)**:
  - Dynamically define and rename property zones (e.g., *Area 1: Front Porch*, *Area 2: Front Sidewalk/Mailbox*, *Area 3: Backyard Shade Garden*, or custom additions).
  - Staged plants are assigned to specific areas, which propagate directly into the report Table of Contents and formatted area recommendation blocks.
- **Per-User Cloud Firestore Sync**: Reports are saved against the authenticated advisor's account in Cloud Firestore under `/users/{username}/reports/{reportId}` as well as the central `/reports/{reportId}` collection.
- **Central Consultation Reports Repository (Admin Tab)**:
  - Accessible to Program Administrators via the Admin Console (**Repository** tab).
  - **Cross-Advisor Discovery**: Aggregates all reports across Kansas City with live search by client name, advisor, address, or plant species.
  - **Live Filter & Sort**: Filter by specific advisor and sort by Newest, Oldest, Client A–Z, or Most Staged Plants.
  - **Instant `.docx` Re-generation**: Re-generate and download official Word documents on demand for any historical consultation report.
  - **Inspection & Workspace Loading**: Inspect garden zones, staged palettes, and notes, or load any report directly into the active editing workspace.
  - **Administrative Report Deletion**: Permanently delete obsolete or test reports from Cloud Firestore across all document paths.
- **Alternative Export Formats**: Formatted Markdown clipboard export (`Copy Markdown`) and standalone HTML reports.

---

### 7. Invasive Species Field Guide & Vetted Contractor Directory
- **Catalog Switcher**: Toggle instantly between **🌿 Native Plants (185)** and **⚠️ Invasive Species (10)**.
- **10 Curated Kansas City Invasive Threats**: Bush Honeysuckle, Japanese Honeysuckle, Wintercreeper, English Ivy, Callery/Bradford Pear, Multiflora Rose, Garlic Mustard, Tree of Heaven, Autumn Olive, and Privet.
- **Identification & Eradication Cues**: Phenological indicators, bark textures, leaf arrangements, and MDC cut-stump/herbicide removal tips.
- **Staging Invasives**: Add invasive species to consultation drafts with tailored observation and treatment notes.
- **Vetted Local Contractors Directory**: Interactive modal directory featuring 10 vetted Kansas City invasive removal and habitat restoration contractors directly from the official template (Belfield Botanica Co., Bluestem Habitat Restoration, Bur Oak Ventures, Habitat Architects, Kansas Property Services, Orris Horticulture, Otto’s Environmental Improvements, Polli-Native, Rogue Natives, and the Grow Native! Professional Resource Guide).

---

### 8. Dynamic Word Report Generation (`.docx`) & Directive Compliance
- **Official Deep Roots Template ([`report_template.docx`](./report_template.docx))**: Built using client-side `JSZip` without requiring external server dependencies.
- **Directive & Red Text Processing**:
  - **Red Instruction Removal**: Automatically removes all instructional red text paragraphs intended for Nature Advisors.
  - **Invasive Logic**:
    - **Invasive-Free Landscape (Case A)**: When no invasives are present, outputs the official congratulations text and the Big Three vigilance list (Bush Honeysuckle, Japanese Honeysuckle, Wintercreeper, English Ivy), cleanly deleting Case B.
    - **Invasives Found (Case B)**: When invasives are found on site, outputs *"We found the following invasive plants in your landscape during our visit:"* with staged species and custom notes, followed by the *"More Information"* paragraph recommending vigilance for the remaining Big Three, cleanly deleting Case A.
  - **Wildlife Stewardship Toggles**: Selectively includes or removes Bird Nest Box, Bird Bath, Bat Box, and Native Bee Habitat sections.
  - **Stormwater Management Toggles**: Selectively includes or removes Johnson County (*Contain The Rain*), Wyandotte County (*Unified Government*), and Rainwater Harvesting sections.
  - **(IF Discussed) Heading Cleanup**: Strips placeholder markers from active headings.
- **OpenXML Reverse Offset Splicing**: Paragraphs are evaluated and spliced from highest offset to lowest offset (backwards), ensuring 100% XML validity and zero document corruption.

---

### 9. Cloud Architecture & Zero-Trust Security
- **Cloud Firestore Database**: `deep-roots-nature-advisors` in project `deep-roots-nature-advisors`.
- **Public Read Access**: Shared native plant catalog (`/plants/{plantId}`) is open for community and client reading without requiring Google OAuth tokens.
- **Security Rules ([`firestore.rules`](./firestore.rules))**:
  - Enforces schema validation for plants, user accounts, and consultation reports.
  - Author attribution integrity checks.
  - Admin-only access to user role modification and account deletion.
  - Restricted report modification to authenticated user paths (`/users/{username}/reports/{reportId}`).

---

### 10. ADA Title III & WCAG 2.1 Level AA Accessibility
- **Skip Navigation**: Accessible bypass link (`#skip-to-content`) allowing screen reader and keyboard users to bypass header chrome directly to the botanical catalog.
- **Dynamic Text Scaling**: Native font scaling preference (`100%`, `115%`, `130%`, `145%`) with fluid rem layouts, persisted across browser sessions.
- **High-Contrast Focus System**: High-visibility `:focus-visible` styling (`3px solid #15803d` with `3px` offset) across all interactive cards, filters, buttons, and inputs.
- **Live Screen Reader Announcements**: Accessible live region (`#a11yAnnouncer` with `aria-live="polite"`) delivering real-time status updates on catalog filtering, staging events, and modal dialogs.
- **Accessible Modal Dialogs**: Full keyboard focus trapping, Escape key dismissals, backdrop inerting, and automatic focus restoration to triggering elements.
- **Motion & Contrast**: Full support for `prefers-reduced-motion: reduce` and verified contrast meeting or exceeding WCAG AA 4.5:1 standards.
- Detailed implementation breakdown and assistive technology testing report: [**`ADA_COMPLIANCE.md`**](./ADA_COMPLIANCE.md).

---

## 📂 Project Directory Structure

```
Deep Roots Database/
├── index.html                                  # Standalone Single-File Web Application
├── presentation.html                           # Interactive Web Presentation Deck
├── PRESENTATION.md                             # Program Manager Executive Presentation Briefing
├── program_manager_presentation.md             # Program Manager Executive Presentation (canonical copy)
├── ADA_COMPLIANCE.md                           # ADA Title III & WCAG 2.1 AA Compliance Documentation
├── report_template.docx                        # Official Deep Roots Word Document Template (1.4 MB)
├── DeepRootsAdvisor-debug.apk                  # Pre-compiled Android Debug APK (20 MB)
├── firestore.rules                             # Hardened Cloud Firestore Security Rules
├── README.md                                   # Project documentation
├── implementation_plan.md                      # Web & system implementation specification
├── mobile_architecture_plan.md                 # Mobile architecture specification
├── android/                                    # Native Android Project (Kotlin / Jetpack Compose)
│   ├── app/src/main/
│   │   ├── java/org/deeproots/advisor/
│   │   │   ├── auth/
│   │   │   │   └── AuthManager.kt              # RBAC authentication & password hashing
│   │   │   ├── data/
│   │   │   │   ├── PlantRepository.kt          # Room database, caching, & report storage
│   │   │   │   ├── CloudPlantSyncEngine.kt     # Firestore catalog synchronization
│   │   │   │   └── FirestoreUserSyncEngine.kt  # User roster & consultation reports sync
│   │   │   ├── sync/
│   │   │   │   ├── ReportSyncManager.kt        # Two-way Firestore consultation report sync
│   │   │   │   └── TemplateReportGenerator.kt  # Official .docx Word report builder
│   │   │   ├── ui/
│   │   │   │   ├── DeepRootsApp.kt             # Main navigation & top app bar
│   │   │   │   ├── PlantViewModel.kt           # State management & reactive flows
│   │   │   │   └── components/                 # Modals, plant cards, staging pane, filters
│   │   └── assets/report_template.docx         # Bundled Word report template
│   └── gradlew                                 # Gradle wrapper script
└── scripts/
    └── build_single_file_html.py               # Single-file HTML compiler script
```

---

## 🚀 Running the Application

### 1. Web Application (Zero-Build)
- Open `index.html` in any web browser, or access the live GitHub Pages deployment at:
  > **[https://bradlchr.github.io/](https://bradlchr.github.io/)**

### 2. Android Application
- Download [`DeepRootsAdvisor-debug.apk`](./DeepRootsAdvisor-debug.apk) directly or from [bradlchr.github.io/DeepRootsAdvisor-debug.apk](https://bradlchr.github.io/DeepRootsAdvisor-debug.apk).
- To compile from source:
  ```bash
  cd android
  ./gradlew assembleDebug --no-daemon
  ```
  The compiled APK will be at `android/app/build/outputs/apk/debug/DeepRootsAdvisor-debug.apk`.

---

## 🌿 Authoritative Data Sources & Partners
- **Deep Roots KC** (`deeproots.org`) - Heartland native plant conservation, Sweet 16, and KC Keystones programs.
- **Grow Native! / Missouri Prairie Foundation** (`grownative.org`) - Midwestern native plant resources, cultivation guides, and nursery listings.
- **Missouri Botanical Garden** (`missouribotanicalgarden.org`) - Comprehensive botanical taxonomy and photographic documentation.
- **Lady Bird Johnson Wildflower Center** (`wildflower.org`) - North American native plant database.
