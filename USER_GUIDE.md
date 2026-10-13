# Deep Roots Nature Advisors - Web Application User Guide
### *Deep Roots Database Quick Start & Field Guide*

Welcome to the **Deep Roots Nature Advisors - Kansas City Native Plant Database** (short name: **Deep Roots Database**). This guide walks you through using the web application at [**https://bradlchr.github.io/**](https://bradlchr.github.io/) to research native species, identify and stage invasive plant threats, conduct client property assessments, configure garden planting zones, and generate official branded Word (`.docx`) consultation reports.

---

## 🚀 Quick Start Overview

| Step | Action | Outcome |
| :--- | :--- | :--- |
| **1. Access** | Visit [**bradlchr.github.io**](https://bradlchr.github.io/) | Browse full catalog as Guest or click **Sign In** as an Advisor |
| **2. Discover** | Search 185 KC native species or flip to 10 High-Threat Invasives | Filtered plant cards with bloom color gradients or invasive removal tips |
| **3. Consult** | Open consultation drawer & name Garden Areas | Define custom planting zones (e.g., *Front Porch*, *Backyard Shade*) |
| **4. Stage** | Add native plants & invasive species with site notes | Curate tailored plant recommendations and flag invasive sightings |
| **5. Customize** | Toggle Wildlife Stewardship & Stormwater County options | Enable/disable nest boxes, bird baths, bat boxes, county cost-share |
| **6. Export** | Click **Download Official Word Report (.docx)** | Tailored Word document ready for client delivery (all red instructions removed) |

> 💡 **Developer & System Architecture**: For an interactive breakdown of the system architecture, OpenXML Word pipeline, and reference of all 118 functions, visit [**bradlchr.github.io/docs.html**](https://bradlchr.github.io/docs.html) or read [**`CODE_DOCUMENTATION.md`**](./CODE_DOCUMENTATION.md).

---

## 🌿 1. Browsing & Filtering Kansas City Native Plants

### Search Bar
- Type any botanical name (e.g., *Echinacea*, *Asclepias*), common alias (e.g., *Purple Coneflower*, *Butterfly Milkweed*), or ecological tag (e.g., *Keystone*, *Monarch*, *Rain Garden*).

### Ecological Filter Chips
- **Native Environment**: Prairie, Savannah/Woodland, Forest, Cliff/Glade, Stream Edge/Wetland.
- **Sun & Light**: Full Sun, Part Sun, Part Shade, Full Shade.
- **Soil Moisture**: Dry, Medium-Dry, Medium, Medium-Wet, Wet.
- **Mature Height**: `< 1 ft`, `1–3 ft`, `3–6 ft`, `6–15 ft`, `15+ ft`.
- **Architectural Layer**: Canopy, Understory, Structural Layer, Seasonal Layer, Groundcover.
- **Curious by Nature Sociability**: Solitary / Less Social, Moderate Spreading, Highly Social / Matrix.
- **Flagship Badges**:
  - ⭐ **Deep Roots Sweet 16**: High-performance pollinator workhorses.
  - 🌿 **KC Keystone Species**: Heartland ecosystem powerhouses.

### Display Preference (Common vs. Scientific Name)
- In the top header bar (or sidebar on mobile), toggle between **Common Name First** and **Scientific Name First**.
- Changing this setting automatically re-sorts and re-indexes the entire plant directory.

### Plant Cards
- **Dynamic Bloom Gradients**: Luminous card backgrounds dynamically match the plant’s real bloom colors.
- **Copy Summary**: Click **Copy** to grab the concise 3-line advisor description to your clipboard.
- **Plant Detail Modal**: Click on any card image or title to view high-resolution photography, companion plants, Grow Native! links, and full botanical citations.

---

## ⚠️ 2. Invasive Species Field Guide & Removal Contractors

Kansas City landscapes frequently harbor aggressive non-native species that outcompete native plants. Deep Roots Database features a dedicated **Invasive Species Field Guide**:

### Switching to Invasive Mode
- Click the **⚠️ Invasive Species (10)** button in the top navigation bar.
- The catalog flips from native plants to the 10 most damaging invasive species in the KC region (Bush Honeysuckle, Japanese Honeysuckle, Wintercreeper, English Ivy, Callery/Bradford Pear, Multiflora Rose, Garlic Mustard, Tree of Heaven, Autumn Olive, and Privet).

### Invasive Plant Cards
- **How to Identify**: Visual identification cues including bark textures, leaf arrangements, berries, and spring/autumn phenology.
- **Removal Tips**: Mechanical and cut-stump herbicide treatments recommended by the Missouri Department of Conservation (MDC).
- **MDC Guide**: Direct external link to official MDC problem plant control guides.
- **+ Add to Report**: Stages the invasive species in the active consultation report with editable removal notes.

### Vetted Removal & Habitat Contractors Directory
- Click **View Removal Professionals (10)** in the banner or on any invasive card.
- Opens a curated directory of 10 vetted local ecological contractors specializing in invasive plant eradication, cut-stump treatment, forestry mulching, and natural resources management in the Greater Kansas City area:
  1. **Belfield Botanica Co.** – (913) 660-2420 | `BelfieldBotanica@gmail.com`
  2. **Bluestem Habitat Restoration** – (816) 714-8342 | `bluestemhabitatrestoration@gmail.com`
  3. **Bur Oak Ventures** – (816) 974-3462 | `kyle@buroakventures.com`
  4. **Habitat Architects** – (816) 645-0026
  5. **Kansas Property Services** – (785) 845-4072 | `kansaspropertyservices@gmail.com`
  6. **Orris Horticulture** – (573) 355-0786 / (816) 785-3773 | `travis@orrishorticulture.com`, `iris@orrishorticulture.com`
  7. **Otto’s Environmental Improvements** – (816) 652-6886
  8. **Polli-Native** – (913) 701-4565 | `Paul@atgib.com`, `nanette@atgib.com`
  9. **Rogue Natives** – (913) 244-7327 | `roguenativesllc@gmail.com`
  10. **Grow Native! Professional Resource Guide** – Statewide directory link (`grownative.org/resource-guide/`).

---

## 📋 3. Setting Up a Client Consultation

1. **Open Consultation Drawer**:
   - Click the green **Selected Plants** button in the top navigation bar.
2. **Consultation Switcher**:
   - The top dropdown displays your active consultation draft.
   - Click **+ New** to start a fresh consultation for a new client.
   - Click **All Consultations** to search, switch between, duplicate, or delete saved client consultations.
3. **Client Information Form**:
   - **Client Name**: (e.g., *Eleanor Vance*)
   - **Project Address**: (e.g., *4520 Rockhill Rd, Kansas City, MO*)
   - **Consultation Date**: Defaults to today’s date.
   - **Nature Advisor Name**: Auto-filled when signed in.
   - **Advisor Overview & Site Strategy**: Enter high-level observations regarding site soils, microclimates, drainage, and landowner conservation goals.

---

## 🏡 4. Setting Up Garden Areas (Planting Zones)

Each property consultation is divided into specific planting zones so recommendations are practical and organized for the client.

1. In the consultation drawer, locate the **Garden Areas** panel directly below the Client Information form.
2. Default areas are provided:
   - *Area 1: Front Porch*
   - *Area 2: Front Sidewalk/Mailbox*
   - *Area 3: Backyard Shade Garden*
3. **Customize Area Names**:
   - Click any area text box to rename it (e.g., change *Area 1: Front Porch* to *Area 1: Downspout Rain Garden*).
   - Any plants already assigned to that area automatically update.
4. **Add More Areas**:
   - Click **+ Add Area** to append additional planting zones (*Area 4*, *Area 5*, etc.).
5. **Delete an Area**:
   - Click the trash icon next to an area. Staged plants will automatically reassign to the first available area.

---

## 🌸 5. Staging Plants & Assigning to Garden Areas

1. **Add Plants to Report**:
   - On any plant card in the main catalog, click **+ Add to Report** (or from the plant detail modal).
   - A toast notification confirms which area the plant was added to.
2. **Assign to a Garden Area**:
   - In the consultation drawer, find the plant under **Selected Plants**.
   - Use the **Area:** dropdown to assign the plant to the intended garden zone (e.g., assign *Wild Columbine* to *Area 3: Backyard Shade Garden*).
3. **Specify Quantities & Site Notes**:
   - Adjust quantities using the `+` and `-` steppers.
   - In the **Specific location / planting notes** field, enter custom advice for the client (e.g., *"Cluster 5 along the north foundation wall where downspout overflow stays damp"*).

---

## ⚙️ 6. Consultation Options & Report Toggles

The consultation drawer provides dynamic toggles to customize the report based on landowner preferences:

### Invasive Species Present on Property
- **Auto-Toggle**: Adding any invasive plant from the Invasive Field Guide automatically turns this toggle **ON**.
- **Manual Toggle**: Can also be manually toggled ON or OFF.
- **When OFF (Invasive-Free Landscape)**:
  - Generates the official *"Congratulations on an invasive-free landscape!"* section with links to the Big Three vigilance list (Bush Honeysuckle, Japanese Honeysuckle, Wintercreeper, English Ivy).
  - Case B text and placeholder plants are completely removed.
- **When ON (Invasives Found)**:
  - Generates *"We found the following invasive plants in your landscape during our visit:"* with your staged species and tailored removal notes.
  - Automatically appends a *"More Information"* paragraph advising vigilance for whichever of the Big Three were *not* found on the property.
  - Case A text is completely removed.

### Wildlife Stewardship Structure Toggles
Select which habitat structures to include in the client deliverable:
- **Include Bird Nest Box Section** *(Default: ON)*
- **Include Bird Bath Section** *(Default: ON)*
- **Include Bat Box Section** *(Default: OFF)*
- **Include Bee Habitat Section** *(Default: ON)*
*(If all four wildlife options are turned off, the entire Wildlife Stewardship chapter is cleanly omitted.)*

### Stormwater Management & County Cost-Share Toggles
- **Johnson County, KS (*Contain The Rain*)** *(Default: OFF)*: Includes cost-share reimbursement information for Johnson County homeowners (rain gardens, rain barrels).
- **Wyandotte County, KS (*Unified Government Stormwater*)** *(Default: OFF)*: Includes cost-share grant details for Wyandotte County homeowners.
- **Include Rainwater Harvesting Section** *(Default: ON)*: Includes best-practice guidance for rain barrels, overflow, winterization, and mosquito prevention.

---

## 📄 7. Generating & Downloading the Client Report

### Official Word Document (`.docx`)
1. Click **Download Official Word Report (.docx)** at the bottom of the consultation drawer.
2. The application dynamically processes the official Deep Roots Microsoft Word template:
   - Fills in client details, address, date of visit, and advisor names.
   - Formats your customized Site Overview and Strategy intro.
   - Updates the Table of Contents with your custom Garden Areas.
   - Formats professional plant recommendation cards grouped by Garden Area, complete with Grow Native! hyperlinks, botanical bullet points, bloom seasons, and your custom site notes.
   - Applies your Invasive Species and Wildlife/Stormwater toggles.
   - **Removes all red instructional text** from the template, producing a clean, final deliverable ready for client presentation.
   - Downloads a genuine, non-corrupt `.docx` file ready for Microsoft Word or Google Docs.

### Copy Markdown Report
- Click **Copy Markdown** to copy a clean, structured text version of the consultation report for quick email drafting or notes.

### Cloud Synchronization
- Click **Save Report to Advisor Profile** to back up and sync your active consultation draft directly to Cloud Firestore.
- Consultations persist safely in local storage and across advisor sign-ins.

---

## ✏️ 8. Editing Botanical Records (Advisors)

Advisors can update species records to reflect regional field observations:
1. Sign in to your advisor account.
2. Click the edit pencil icon on any plant card.
3. Update descriptions, height brackets, sociability, and select **Bloom Colors** and **Bloom Seasons** using interactive chips.
4. Save changes. Plant cards immediately update with the new bloom mesh gradient, and the edit is logged with author attribution (*"Last edited by: [Your Name]"*).

---

## 👥 9. Program Administrator Functions

Advisors with the `admin` role possess organization-wide management tools accessible via the avatar menu (**Admin Console**) and the Database Sync dialog:

### 9.1 Provisioning & Managing Nature Advisors
1. Open your profile menu in the top right and select **Admin Console** (or open the **Advisor Roster** tab).
2. **Search Roster**: Filter advisors by name, email, phone, or username.
3. **Provision New Advisors**:
   - Enter First Name and Last Name (the system automatically generates the canonical `<first>.<last>` username).
   - Enter Email, Phone, and select Advisor Type (`Advisor in Training`, `Advisor`, `Senior Advisor`, or `Program Manager`).
   - Assign System Role (`user` for Nature Advisors, `admin` for Program Administrators).
   - Click **Provision Advisor & Generate Temp Password**.
4. **First-Login Security**:
   - When a newly provisioned advisor signs in for the first time, the application automatically forces them to set a permanent, strong password (minimum 8 characters, uppercase, lowercase, numbers) before accessing staging features.

### 9.2 Central Consultation Reports Repository
Advisors with the `admin` role can oversee all consultations conducted across the region:
1. Open the **Admin Console** and select the **Consultation Repository** tab.
2. **Search & Filter**: Search by client name, advisor name/username, property address, plant species, or notes. Use the advisor dropdown to isolate reports by specific team members.
3. **Inspect & View**: Click **View** on any report card to review full site strategy, garden planting zones, staged native palettes, and invasive species observations.
4. **Re-generate Word Document (`.docx`)**: Click **Regenerate .docx** directly from the report card or inspection modal to generate and download an official formatted Word document.
5. **Load into Workspace**: Click **Load into Workspace** to clone or edit the report in your active staging drawer.
6. **Administrative Report Deletion**:
   - Click the red trash icon on any report card or **Delete Report** in the inspection modal.
   - Prompts for confirmation with the client name and author.
   - Permanently deletes the report from Cloud Firestore across all document paths (`/reports`, `/plants/_report_*`, and `/users/{username}/reports`), purging local caches and updating repository counters.

### 9.3 Master Catalog Governance (Database Sync Dialog)
To protect data integrity, destructive master database operations in the **Shared Master Database** dialog (`#syncModal`) are strictly limited to Program Administrators:
- **Pull Fresh Data from Master Database**: Available to all signed-in advisors to pull latest updates.
- **Upload Master Plant Catalog to Firestore** *(Admin Only)*: Batches all 185 baseline species definitions to the remote Firestore master catalog.
- **Reset Local Edits to Clean Master Catalog** *(Admin Only)*: Clears local customizations and restores the pristine default botanical catalog.
- **Import Plants JSON (Android Backup)** *(Admin Only)*: Imports JSON backup files from native Android app backups.

---

## 🔒 10. Access Permissions Summary

| Feature / Action | Guest (Public) | Nature Advisor (`user`) | Program Administrator (`admin`) |
| :--- | :---: | :---: | :---: |
| **Browse 185 Native Species & 10 Invasives** | ✅ | ✅ | ✅ |
| **Search, Filter & Sort Botanical Records** | ✅ | ✅ | ✅ |
| **View Plant Details & Grow Native! Profiles** | ✅ | ✅ | ✅ |
| **View Vetted Invasive Removal Contractors** | ✅ | ✅ | ✅ |
| **Consultation Staging Drawer & Garden Areas** | ❌ (Hidden) | ✅ | ✅ |
| **Add Native / Invasive Species to Report** | ❌ (Hidden) | ✅ | ✅ |
| **Generate & Download Word Reports (.docx)** | ❌ | ✅ | ✅ |
| **Edit Plant Details (Syncs to Firestore)** | ❌ | ✅ | ✅ |
| **View Central Reports Repository** | ❌ | ❌ | ✅ |
| **Delete Other Advisors' Reports** | ❌ | ❌ | ✅ |
| **Provision & Manage Advisor Roster** | ❌ | ❌ | ✅ |
| **Upload / Reset / Import Master Catalog** | ❌ | ❌ | ✅ |
