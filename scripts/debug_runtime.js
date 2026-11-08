/**
 * Debug runtime errors in test.html
 */
const fs = require('fs');

const html = fs.readFileSync('test.html', 'utf8');

// Simple DOM Mock
const elements = new Map();
class MockElement {
  constructor(id, tag = 'div') {
    this.id = id;
    this.tagName = tag.toUpperCase();
    this.listeners = {};
    this.attributes = {};
    this.style = {};
    this.classList = {
      add: () => {},
      remove: () => {},
      toggle: () => {}
    };
  }
  addEventListener(event, fn) {
    this.listeners[event] = fn;
  }
  setAttribute(k, v) { this.attributes[k] = v; }
  getAttribute(k) { return this.attributes[k] || null; }
  showModal() { this.open = true; }
  close() { this.open = false; }
  querySelectorAll() { return []; }
  querySelector() { return null; }
  appendChild(c) {}
}

const parser = {
  feed(h) {
    const idRegex = /id=["']([^"']+)["']/g;
    let m;
    while ((m = idRegex.exec(h)) !== null) {
      if (!elements.has(m[1])) {
        elements.set(m[1], new MockElement(m[1]));
      }
    }
  }
};
parser.feed(html);
console.log(`Mocked ${elements.size} DOM elements.`);

// Global mocks
global.document = {
  getElementById: (id) => elements.get(id) || null,
  querySelectorAll: (sel) => [],
  querySelector: (sel) => null,
  createElement: (tag) => new MockElement('mock-' + Math.random(), tag),
  body: new MockElement('body', 'body')
};

global.lucide = { createIcons: () => {} };
global.window = {
  addEventListener: (ev, fn) => {},
  matchMedia: () => ({ matches: false }),
  lucide: { createIcons: () => {} }
};

global.localStorage = {
  _data: {},
  getItem: (k) => global.localStorage._data[k] || null,
  setItem: (k, v) => { global.localStorage._data[k] = String(v); },
  removeItem: (k) => { delete global.localStorage._data[k]; }
};

global.navigator = { clipboard: { writeText: async () => {} } };

// Extract script
const scriptStart = html.rfind ? html.rfind('<script>') : html.lastIndexOf('<script>') + 8;
const scriptEnd = html.lastIndexOf('</script>');
const scriptCode = fs.readFileSync("/tmp/module_code.js", "utf8");

console.log("Evaluating scriptCode...");
try {
  eval(scriptCode);
  console.log("✓ Script evaluated without top-level errors.");
} catch (err) {
  console.error("FATAL top-level eval error:", err);
  process.exit(1);
}

// Now test setupEventListeners()
console.log("Calling setupEventListeners()...");
try {
  setupEventListeners();
  console.log("✓ setupEventListeners() completed successfully without errors!");
} catch (err) {
  console.error("FATAL setupEventListeners error:", err);
  process.exit(1);
}

// Now test clicking gardenPlannerHeaderBtn
console.log("Simulating click on gardenPlannerHeaderBtn...");
const plannerBtn = document.getElementById('gardenPlannerHeaderBtn');
if (!plannerBtn) {
  console.error("gardenPlannerHeaderBtn not found in DOM!");
  process.exit(1);
}

if (!plannerBtn.listeners['click']) {
  console.error("gardenPlannerHeaderBtn has NO click listener attached!");
  process.exit(1);
}

try {
  plannerBtn.listeners['click']();
  console.log("✓ gardenPlannerHeaderBtn click listener executed successfully!");
  const guestModal = document.getElementById('plannerGuestModal');
  console.log("Guest modal open state:", guestModal ? guestModal.open : "NOT FOUND");
} catch (err) {
  console.error("FATAL click handler error:", err);
  process.exit(1);
}
