# Deep Roots Nature Advisors - Web Application User Guide
### *Deep Roots Database Quick Start & Field Guide*

Welcome to the **Deep Roots Nature Advisors - Kansas City Native Plant Database** (short name: **Deep Roots Database**). This guide walks you through using the web application at [**https://bradlchr.github.io/**](https://bradlchr.github.io/) to research native species, conduct client property assessments, set up custom planting zones, and generate official branded Word (`.docx`) consultation reports.

---

## 🚀 Quick Start Overview

| Step | Action | Outcome |
| :--- | :--- | :--- |
| **1. Access** | Visit [**bradlchr.github.io**](https://bradlchr.github.io/) | Browse full catalog as Guest or click **Sign In** as an Advisor |
| **2. Discover** | Search 185 KC species & apply ecological filters | Instant filtered plant grid with bloom color mesh gradients |
| **3. Consult** | Open consultation drawer & name Garden Areas | Define custom planting zones (e.g., *Front Porch*, *Backyard Shade*) |
| **4. Stage** | Click **+ Add to Report** & assign to Garden Areas | Curate tailored plant palettes with quantities & site notes |
| **5. Export** | Click **Download Official Word Report (.docx)** | Complete, formatted Word document ready for client delivery |

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

## 📋 2. Setting Up a Client Consultation

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

## 🏡 3. Setting Up Garden Areas (Planting Zones)

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

## 🌸 4. Staging Plants & Assigning to Garden Areas

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

## 📄 5. Generating & Downloading the Client Report

### Official Word Document (`.docx`)
1. Click **Download Official Word Report (.docx)** at the bottom of the consultation drawer.
2. The application automatically takes the official Deep Roots Microsoft Word template and:
   - Fills in client details, address, date of visit, and advisor names.
   - Formats your customized Site Overview and Strategy intro.
   - Updates the Table of Contents with your named Garden Areas.
   - Formats professional plant recommendation cards grouped by Garden Area, complete with Grow Native! hyperlinks, botanical bullet points, bloom seasons, and your custom site notes.
   - Downloads a genuine, non-corrupt `.docx` file ready for Microsoft Word or Google Docs.

### Copy Markdown Report
- Click **Copy Markdown** to copy a clean, structured text version of the consultation report for quick email drafting or notes.

### Cloud Synchronization
- Click **Save Report to Advisor Profile** to back up and sync your active consultation draft directly to Cloud Firestore.
- Consultations persist safely in local storage and across advisor sign-ins.

---

## ✏️ 6. Editing Botanical Records (Advisors)

Advisors can update species records to reflect regional field observations:
1. Sign in to your advisor account.
2. Click the edit pencil icon on any plant card.
3. Update descriptions, height brackets, sociability, and select **Bloom Colors** and **Bloom Seasons** using interactive chips.
4. Save changes. Plant cards immediately update with the new bloom mesh gradient, and the edit is logged with author attribution (*"Last edited by: [Your Name]"*).

---

## 👥 7. Program Administrator Functions

Advisors with the `admin` role can manage the advisor roster:
1. Click your name / avatar in the top right and select **Admin Panel**.
2. **Provision New Advisors**:
   - Enter First and Last Name (generates canonical `<first>.<last>` username).
   - Select Advisor Type: `Advisor in Training`, `Advisor`, `Senior Advisor`, or `Program Manager`.
   - Issue a temporary password.
3. **First-Login Security**:
   - When a newly provisioned advisor signs in for the first time, the app automatically prompts them to set a permanent, strong password before accessing the system.
