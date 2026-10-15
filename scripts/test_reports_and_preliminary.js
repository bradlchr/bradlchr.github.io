const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const htmlPath = path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');

function assert(cond, msg) {
  if (!cond) {
    console.error('ASSERTION FAILED:', msg);
    process.exit(1);
  }
}

// 1. Extract embeddedMasterPlants JSON
const masterStart = html.indexOf('<script type="application/json" id="embeddedMasterPlants">');
const masterEnd = html.indexOf('</script>', masterStart);
assert(masterStart !== -1 && masterEnd !== -1, 'embeddedMasterPlants JSON block should exist in index.html');
const masterJsonStr = html.slice(masterStart + '<script type="application/json" id="embeddedMasterPlants">'.length, masterEnd).trim();
const masterPlants = JSON.parse(masterJsonStr);
assert(Array.isArray(masterPlants) && masterPlants.length > 80, 'masterPlants should have > 80 species');

// Verify no duplicate consecutive links remain in embeddedMasterPlants
let dupConsecutiveCount = 0;
for (const p of masterPlants) {
  const checkStr = [p.advisor_description || '', p.wildlife_detail?.host_insects || '', p.wildlife_detail?.wildlife_users || ''].join(' ');
  if (/\(\[([^\]]+)\]\(([^)]+)\)\)\s*\(\[([^\]]+)\]\(\2\)\)/.test(checkStr)) {
    dupConsecutiveCount++;
  }
}
assert(dupConsecutiveCount === 0, `Expected 0 duplicate consecutive citations in embeddedMasterPlants, found ${dupConsecutiveCount}`);
console.log('✓ Test 1 Passed: embeddedMasterPlants has 0 duplicate consecutive citations across all', masterPlants.length, 'plants.');

// 2. Load report_template.docx XML and media files
const templatePath = path.join(__dirname, '..', 'report_template.docx');
const templateFiles = JSON.parse(execSync(`python3 -c '
import zipfile, json, base64
z = zipfile.ZipFile(${JSON.stringify(templatePath)}, "r")
out = {"text": {}, "binary": {}}
for name in ["word/document.xml", "word/_rels/document.xml.rels", "word/footnotes.xml", "word/_rels/footnotes.xml.rels"]:
    if name in z.namelist():
        out["text"][name] = z.read(name).decode("utf-8")
for name in ["word/media/image1.jpg", "media/image3.jpg"]:
    if name in z.namelist():
        out["binary"][name] = base64.b64encode(z.read(name)).decode("ascii")
print(json.dumps(out))
'`, { maxBuffer: 50 * 1024 * 1024 }).toString());

let capturedDocxZip = null;
class MockJSZip {
  constructor(initialFiles = {}) {
    this.files = { ...(initialFiles.text || initialFiles) };
    this.binaryFiles = { ...(initialFiles.binary || {}) };
  }
  static async loadAsync() {
    return new MockJSZip(templateFiles);
  }
  file(name, content) {
    if (content !== undefined) {
      this.files[name] = content;
      return this;
    }
    if (name in this.binaryFiles) {
      const b64 = this.binaryFiles[name];
      const buf = Buffer.from(b64, 'base64');
      return {
        async: async (fmt) => {
          if (fmt === 'base64') return b64;
          if (fmt === 'uint8array') return new Uint8Array(buf);
          return buf;
        }
      };
    }
    if (!(name in this.files)) return null;
    const val = this.files[name];
    return { async: async () => val };
  }
  async generateAsync() {
    capturedDocxZip = this.files;
    return Buffer.from('mock-docx');
  }
}

// 3. Set up mock globals and extract functions from index.html
const mockElements = {
  preliminaryReportModal: { open: false, showModal() { this.open = true; }, close() { this.open = false; } },
  preliminaryReportPreviewFrame: { srcdoc: '', contentWindow: { focus() {}, print() {} } },
  embeddedMasterPlants: { textContent: masterJsonStr }
};

global.window = {
  JSZip: MockJSZip,
  lucide: { createIcons: () => {} }
};
global.JSZip = MockJSZip;
global.URL = { createObjectURL: () => 'blob:mock' };
global.Blob = class { constructor(parts, opts) { this.parts = parts; this.opts = opts; } };
global.navigator = { clipboard: { writeText: async () => {} } };
global.localStorage = {
  store: {},
  getItem(k) { return this.store[k] || null; },
  setItem(k, v) { this.store[k] = String(v); }
};
global.document = {
  getElementById: (id) => mockElements[id] || null,
  createElement: () => ({ style: {}, click() {} }),
  body: { appendChild() {}, removeChild() {} }
};
global.fetch = async (url) => {
  if (String(url).includes('report_template.docx')) {
    return { ok: true, arrayBuffer: async () => Buffer.from('template') };
  }
  return { ok: false };
};

global.escapeHtml = (s) => String(s || '')
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');
global.showToast = () => {};
global.persistReportOptions = () => {};
global.saveStaging = () => {};
global.getPlantUrl = (p) => (p && (p.plant_url || p.url)) || 'https://grownative.org';
global.isKcSweet16Plant = (p) => Boolean(p && (p.is_sweet_16 || p.kc_sweet_16 || p.scientific_name === 'Zizia aurea'));

const state = {
  allPlants: [],
  customPlants: {},
  invasivePlants: [],
  stagedPlants: [],
  stagedInvasives: [],
  gardenAreas: [],
  gardenAreaProfiles: {},
  clientMeta: {},
  reportOptions: {},
  currentUser: { name: 'Bradford Advisor' }
};
global.state = state;

// Extract canonical overlay block and report generator block from index.html
const overlayStart = html.indexOf('function getEmbeddedMasterMap()');
const overlayEnd = html.indexOf('async function loadMasterPlants()');
assert(overlayStart !== -1 && overlayEnd !== -1, 'Could not locate canonical overlay block in index.html');

const reportStart = html.indexOf('const BIG_THREE_DATA = {');
const reportEnd = html.indexOf('// Setup Event Listeners\n    function setupEventListeners()');
assert(reportStart !== -1 && reportEnd !== -1, 'Could not locate report generator block in index.html');

eval(
  html.slice(overlayStart, overlayEnd) + '\n' +
  html.slice(reportStart, reportEnd) + '\n' +
  'global.overlayCanonicalMasterFields = overlayCanonicalMasterFields;\n' +
  'global.refreshStagedPlantsFromCatalog = refreshStagedPlantsFromCatalog;\n' +
  'global.resolveReportPlantRecord = resolveReportPlantRecord;\n' +
  'global.formatConciseMaintenanceForReport = formatConciseMaintenanceForReport;\n' +
  'global.formatConciseWildlifeForReport = formatConciseWildlifeForReport;\n' +
  'global.generateMarkdownReport = generateMarkdownReport;\n' +
  'global.buildHtmlReport = buildHtmlReport;\n' +
  'global.generatePreliminaryReportHtml = generatePreliminaryReportHtml;\n' +
  'global.openPreliminaryReport = openPreliminaryReport;\n' +
  'global.ensureDeepRootsBrandAssets = ensureDeepRootsBrandAssets;\n' +
  'global.generatePreliminaryReportPdfFile = generatePreliminaryReportPdfFile;\n' +
  'global.sharePreliminaryReport = sharePreliminaryReport;\n' +
  'global.downloadDocxReport = downloadDocxReport;\n'
);

const goldenAlex = masterPlants.find(p => p.scientific_name === 'Zizia aurea');
const blackEyedSusan = masterPlants.find(p => p.scientific_name === 'Rudbeckia hirta');
assert(goldenAlex && blackEyedSusan, 'Golden Alexanders and Black-Eyed Susan should exist in masterPlants');

const staleIndexDescription = 'STALE MASTER PLANT INDEX DESCRIPTION FROM OLD DOCUMENT THAT SHOULD NOT BE USED.';

(async function runTests() {
  state.allPlants = overlayCanonicalMasterFields(JSON.parse(JSON.stringify(masterPlants)));
  state.clientMeta = {
    name: 'Jane & John Doe',
    address: '1234 Brookside Blvd, Kansas City, MO 64113',
    date: '2026-10-15',
    advisor: 'BradfordAdvisor',
    notes: 'Focus on front porch pollinator curb appeal and backyard shade matrix.'
  };
  state.gardenAreas = [
    'Area 1: Front Porch Sunny Border',
    'Area 2: Backyard Woodland Edge'
  ];
  state.gardenAreaProfiles = {
    'Area 1: Front Porch Sunny Border': {
      name: 'Area 1: Front Porch Sunny Border',
      sun: ['Full Sun', 'Part Sun'],
      moisture: ['Medium', 'Dry'],
      layers: ['Groundcover', 'Mid-layer', 'Structural'],
      maxHeightFt: 4,
      notes: 'South-facing foundation bed along front walkway.'
    },
    'Area 2: Backyard Woodland Edge': {
      name: 'Area 2: Backyard Woodland Edge',
      sun: ['Part Shade', 'Full Shade'],
      moisture: ['Medium'],
      layers: ['Groundcover', 'Mid-layer'],
      maxHeightFt: 3,
      notes: 'Dappled afternoon shade under mature oaks.'
    }
  };
  state.stagedPlants = [
    {
      id: goldenAlex.id,
      common_name: goldenAlex.common_names[0],
      scientific_name: goldenAlex.scientific_name,
      advisor_description: staleIndexDescription,
      plant_url: goldenAlex.plant_url,
      quantity: 5,
      target_area: 'Area 1: Front Porch Sunny Border',
      custom_notes: 'Plant in drifts of 3-5 near front steps.'
    },
    {
      id: blackEyedSusan.id,
      common_name: blackEyedSusan.common_names[0],
      scientific_name: blackEyedSusan.scientific_name,
      advisor_description: staleIndexDescription,
      plant_url: blackEyedSusan.plant_url,
      quantity: 3,
      target_area: 'Area 1: Front Porch Sunny Border',
      custom_notes: ''
    }
  ];

  // Test 2: resolveReportPlantRecord uses updated canonical advisor_description instead of stale description
  const resolvedGA = resolveReportPlantRecord(state.stagedPlants[0]);
  assert(!resolvedGA.advisor_description.includes('STALE MASTER PLANT INDEX'), 'resolveReportPlantRecord must NOT use stale staged advisor_description');
  assert(resolvedGA.advisor_description === goldenAlex.advisor_description, 'resolveReportPlantRecord must use canonical updated advisor_description');
  console.log('✓ Test 2 Passed: resolveReportPlantRecord overrides stale staged description with updated canonical advisor_description.');

  // Test 3: Shortened Maintenance & Wildlife sections
  const maintShort = formatConciseMaintenanceForReport(resolvedGA);
  const maintVisible = maintShort.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
  assert(!maintShort.includes('Requires minimal care once established'), 'Shortened maintenance must omit repetitive summary boilerplate');
  assert(maintVisible.length < 320, `Shortened maintenance visible text should be concise (< 320 chars), got ${maintVisible.length}`);
  const dupCheck = deduplicateMarkdownLinksInBullet('Spring: Cut stems ([Xerces](https://xerces.org/a)) | Winter: Leave stems ([Xerces](https://xerces.org/a))');
  const xercesMatches = dupCheck.match(/https:\/\/xerces\.org\/a/g) || [];
  assert(xercesMatches.length === 1, `Duplicate URLs in the same maintenance bullet must be deduplicated (expected 1, got ${xercesMatches.length})`);

  const wildlifeShort = formatConciseWildlifeForReport(resolvedGA);
  assert(!wildlifeShort.includes('Specialist bees and native pollinators are supported'), 'Shortened wildlife must omit filler sentences');
  assert(wildlifeShort.startsWith('Host:'), 'Shortened wildlife should start with Host:');
  console.log('✓ Test 3 Passed: Maintenance and Wildlife sections are concise and deduplicated.');

  // Test 4: Markdown & HTML Reports have clickable links + numbered Sources Cited at the end
  const mdReport = generateMarkdownReport();
  assert(!mdReport.includes(staleIndexDescription), 'Markdown report must not contain stale description');
  assert(mdReport.includes('## Sources Cited'), 'Markdown report must include ## Sources Cited at the end');
  assert(/1\.\s+"[^"]+"\s+\[https?:\/\//.test(mdReport), 'Markdown Sources Cited must follow numbered citation format');

  const htmlReport = buildHtmlReport();
  assert(!htmlReport.includes(staleIndexDescription), 'HTML report must not contain stale description');
  assert(htmlReport.includes('<h2>Sources Cited</h2>'), 'HTML report must include Sources Cited section');
  assert(htmlReport.includes('id="report-cite-1"'), 'HTML report must include numbered citation anchors');
  console.log('✓ Test 4 Passed: Markdown and HTML reports use updated descriptions, clickable links, and numbered Sources Cited.');

  // Test 5: DOCX Report generation (clickable links + sequential footnotes 1..M in word/footnotes.xml)
  await downloadDocxReport();
  assert(capturedDocxZip, 'downloadDocxReport should generate a DOCX zip archive');
  const docXml = capturedDocxZip['word/document.xml'];
  const fnXml = capturedDocxZip['word/footnotes.xml'];

  assert(!docXml.includes(staleIndexDescription), 'DOCX document.xml must NOT contain stale advisor_description');
  assert(!/\[[^\]]+\]\(https?:\/\/[^)]+\)/.test(docXml), 'DOCX document.xml must NOT contain raw unparsed [Label](url) markdown links');
  assert(docXml.includes('<w:hyperlink r:id='), 'DOCX document.xml must contain <w:hyperlink> elements');

  // Verify footnote references in document.xml are numbered 1..M sequentially in order of appearance
  const docFnRefs = [...docXml.matchAll(/<w:footnoteReference\b[^>]*?\bw:id="(\d+)"[^>]*?\/>/g)].map(m => Number(m[1]));
  assert(docFnRefs.length > 35, `Expected > 35 footnote references in DOCX, found ${docFnRefs.length}`);
  for (let i = 0; i < docFnRefs.length; i++) {
    assert(docFnRefs[i] === i + 1, `Footnote reference at index ${i} should be ${i + 1}, got ${docFnRefs[i]}`);
  }

  // Verify every referenced footnote 1..M exists in word/footnotes.xml and has a valid hyperlink
  const fnIdsInFootnotesXml = [...fnXml.matchAll(/<w:footnote\b[^>]*?\bw:id="(\d+)"/g)].map(m => Number(m[1])).filter(id => id > 0);
  assert(fnIdsInFootnotesXml.length === docFnRefs.length, `word/footnotes.xml count (${fnIdsInFootnotesXml.length}) must match document.xml footnoteRef count (${docFnRefs.length})`);
  assert(fnXml.includes('Black Swallowtail') || fnXml.includes('Butterflies and Moths of North America'), 'word/footnotes.xml must include plant citation titles');
  assert(fnXml.includes('Accessed 15 Oct. 2026.'), 'word/footnotes.xml must format Accessed date matching template pattern');
  console.log(`✓ Test 5 Passed: DOCX report converts all inline source links to <w:hyperlink> + sequential footnotes 1..${docFnRefs.length} in word/footnotes.xml.`);

  // Test 6: Preliminary Report (Deep Roots KC Branded HTML)
  await ensureDeepRootsBrandAssets();
  assert(state.deepRootsBrandAssets && state.deepRootsBrandAssets.loaded, 'Deep Roots brand assets (logo + partner footer) should load from template');
  await openPreliminaryReport();
  assert(mockElements.preliminaryReportModal.open === true, 'openPreliminaryReport should open #preliminaryReportModal');
  const prelimHtml = generatePreliminaryReportHtml(null, { standalone: true });
  assert(prelimHtml.includes('Preliminary Consultation Takeaway'), 'Preliminary report should include takeaway title');
  assert(prelimHtml.includes('#9BBB59'), 'Preliminary report should use official Deep Roots olive-meadow #9BBB59 branding');
  assert(prelimHtml.includes('I. NATURESCAPING'), 'Preliminary report should include Deep Roots NATURESCAPING section header');
  assert(prelimHtml.includes('Jane &amp; John Doe'), 'Preliminary report should include client name');
  assert(prelimHtml.includes('Area 1: Front Porch Sunny Border'), 'Preliminary report should include consulted area name');
  assert(prelimHtml.includes('South-facing foundation bed along front walkway.'), 'Preliminary report should include area strategy notes');
  assert(prelimHtml.includes('★ KC Sweet 16'), 'Preliminary report should highlight KC Sweet 16 plants');
  assert(prelimHtml.includes('Grow Native! Plant Profile ↗'), 'Preliminary report should include clickable plant profile links');
  assert(prelimHtml.includes('@page'), 'Preliminary report should include @page print rules for <= 3 page PDF output');
  assert(!prelimHtml.includes(staleIndexDescription), 'Preliminary report must use updated canonical advisor_description');
  console.log('✓ Test 6 Passed: Preliminary Report takeaway renders with Deep Roots KC branding, consulted areas, and clickable plant links.');

  // Test 7: Preliminary Report PDF Conversion & Share Sheet (Send to Client)
  let sharedPayload = null;
  global.navigator = {
    canShare: () => true,
    share: async (payload) => {
      sharedPayload = payload;
    }
  };
  await sharePreliminaryReport();
  assert(sharedPayload && Array.isArray(sharedPayload.files) && sharedPayload.files.length === 1, 'sharePreliminaryReport must pass a generated PDF file to navigator.share');
  const sharedFile = sharedPayload.files[0];
  assert(sharedFile.name.endsWith('.pdf'), `Shared file must be a .pdf, got ${sharedFile.name}`);
  assert(sharedFile.type === 'application/pdf', `Shared file MIME type must be application/pdf, got ${sharedFile.type}`);

  const pdfPack = generatePreliminaryReportPdfFile();
  const pdfStr = Buffer.from(pdfPack.pdfBytes).toString('latin1');
  assert(pdfStr.startsWith('%PDF-1.4'), 'Generated PDF must have valid %PDF-1.4 header');
  assert(pdfStr.includes('/Subtype /Link'), 'Generated PDF must contain clickable /Subtype /Link URI annotations');
  assert(pdfStr.includes('I. NATURESCAPING - PRELIMINARY PLANT RECOMMENDATIONS'), 'Generated PDF must contain Deep Roots section banner text');
  fs.writeFileSync('/storage/emulated/10/Documents/Antigravity Apps/.gemini/antigravity/brain/7dcb635b-95b1-47f2-ab5a-910bb596b8d2/scratch/sample_preliminary_report.pdf', Buffer.from(pdfPack.pdfBytes));
  console.log('✓ Test 7 Passed: Send to Client converts Preliminary Report to PDF with clickable links and opens share sheet.');

  console.log('\nALL REPORT & PRELIMINARY TAKEAWAY TESTS PASSED SUCCESSFULLY!');
})().catch(err => {
  console.error('Test failed with error:', err);
  process.exit(1);
});
