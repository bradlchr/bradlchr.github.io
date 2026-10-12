# Deep Roots Nature Advisors - Kansas City Native Plant Database
### *Deep Roots Database*

Global web portal and distribution site for the **Deep Roots Nature Advisors - Kansas City Native Plant Database** (or **Deep Roots Database** for short), serving Greater Kansas City ecological landscape advisors, botanists, and homeowners.

- 🌐 **Live Web Application**: [**https://bradlchr.github.io/**](https://bradlchr.github.io/)
- 📱 **Download Android App (APK)**: [**Download DeepRootsAdvisor-debug.apk**](https://bradlchr.github.io/DeepRootsAdvisor-debug.apk) (20 MB)
- 📄 **Source Repository**: [github.com/bradlchr/deep-roots-nature-advisors](https://github.com/bradlchr/deep-roots-nature-advisors)

---

## 🌟 Platform Highlights

### 1. 185 Kansas City Native Plant Species
- Complete botanical taxonomy, 5 mature height brackets, 7 plant types, and 5 ecological layers.
- **Dynamic Bloom Color Mesh Gradients**: Real-time card background color gradients matching 11 heartland bloom colors.
- **Flagship Conservation Programs**: ⭐ Deep Roots Sweet 16 & 🌿 KC Keystone Species.
- **Author Attribution**: Live tracking of plant creators and editors (*"Last edited by: [Advisor]"*).
- **Interactive Plant Editor**: Supports editing taxonomy, descriptions, requirements, and **Bloom Color & Bloom Season**.
- **Display Name Toggle**: Seamlessly switch between **Common Name First** and **Scientific Name First** across all cards, modals, and report stages.

### 2. Native Advisor Authentication & RBAC
- **Read-Only Guest Browsing**: Public visitors can search and explore the full catalog without signing in.
- **Roles**:
  - `user` (Nature Advisor): Stage species, switch between consultations, create reports, edit botanical entries.
  - `admin` (Program Administrator): Provision new advisors, assign roles, reset passwords.
- **Advisor Types**: `Advisor in Training`, `Advisor`, `Senior Advisor`, `Program Manager`.
- **Pre-Seeded Default Administrator**:
  - **Username**: `chris.bradley`
  - **Password**: `deeproots_admin`
  - **Email**: `ctbbradley@gmail.com`
  - **Role**: `admin`

### 3. Consultation Reports & Official Word (.docx) Generation
- **Multi-Consultation Switcher**: Manage drafts and switch between multiple client consultations.
- **Cloud Firestore Storage**: Reports save directly to `/users/{username}/reports/{id}`.
- **Real Word Document (.docx)**: Uses the official Deep Roots template (`report_template.docx`) via JSZip to output genuine Office Open XML `.docx` files formatted with client info, visit date, custom site analysis, grouped recommendation blocks, botanical bullets, and external Grow Native! hyperlinks.

---

## 🌿 Data Citations
- **Deep Roots KC** (`deeproots.org`)
- **Grow Native! / Missouri Prairie Foundation** (`grownative.org`)
- **Missouri Botanical Garden** (`missouribotanicalgarden.org`)
