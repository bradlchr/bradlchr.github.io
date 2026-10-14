/**
 * test_planner_cleanup.js
 * Verification test for simplified and decluttered Garden Planner UI
 */
const fs = require('fs');

const indexHtml = fs.readFileSync('index.html', 'utf8');

function assert(condition, message) {
  if (!condition) {
    console.error(`❌ FAIL: ${message}`);
    process.exit(1);
  }
  console.log(`✓ ${message}`);
}

console.log("\n==================== TEST SUITE: PLANNER CLEANUP & SIMPLIFICATION ====================");

// 1. Verify redundant conditions panel in sidebar is REMOVED
console.log("\n--- Checking Removal of Redundant Left Sidebar Characteristics ---");
assert(!indexHtml.includes('id="plannerConditionsPanel"'), "plannerConditionsPanel removed from index.html");
assert(!indexHtml.includes('id="plannerSunChips"'), "plannerSunChips removed from left sidebar");
assert(!indexHtml.includes('id="plannerMoistureChips"'), "plannerMoistureChips removed from left sidebar");
assert(!indexHtml.includes('id="plannerSoilTextureSelect"'), "plannerSoilTextureSelect removed from left sidebar");
assert(!indexHtml.includes('id="plannerMaintChips"'), "plannerMaintChips removed from left sidebar");
assert(!indexHtml.includes('id="plannerColorChips"'), "plannerColorChips removed from left sidebar");
assert(!indexHtml.includes('id="plannerLayerCheckboxes"'), "plannerLayerCheckboxes removed from left sidebar");
assert(!indexHtml.includes('id="plannerAreaNotesInput"'), "plannerAreaNotesInput removed from left sidebar");

// 2. Verify modal conditions editor is intact
console.log("\n--- Checking Conditions Editor Modal Remains Intact ---");
assert(indexHtml.includes('id="plannerAreaConditionsModal"'), "plannerAreaConditionsModal exists for editing conditions");
assert(indexHtml.includes('id="modalSunChips"'), "modalSunChips exists inside modal");
assert(indexHtml.includes('id="modalMoistChips"'), "modalMoistChips exists inside modal");
assert(indexHtml.includes('id="modalSoilTextureSelect"'), "modalSoilTextureSelect exists inside modal");
assert(indexHtml.includes('id="modalMaintChips"'), "modalMaintChips exists inside modal");
assert(indexHtml.includes('id="modalColorChips"'), "modalColorChips exists inside modal");
assert(indexHtml.includes('id="modalLayerCheckboxes"'), "modalLayerCheckboxes exists inside modal");
assert(indexHtml.includes('id="modalAreaNotesInput"'), "modalAreaNotesInput exists inside modal");

// 3. Verify clean sidebar components
console.log("\n--- Checking Simplified Sidebar Components ---");
assert(indexHtml.includes('id="plannerAreasRoster"'), "plannerAreasRoster exists in left sidebar");
assert(indexHtml.includes('id="plannerAddAreaBtn"'), "plannerAddAreaBtn exists in left sidebar");
assert(indexHtml.includes('id="plannerRestartWizardBtn"'), "plannerRestartWizardBtn exists in left sidebar");
assert(indexHtml.includes('.planner-area-edit-btn'), "planner-area-edit-btn exists on each area card");

// 4. Verify clean header and plant cards
console.log("\n--- Checking Header and Plant Card Improvements ---");
assert(indexHtml.includes('id="plannerHeaderEditBtn"'), "plannerHeaderEditBtn exists in header criteria strip");
assert(indexHtml.includes('.planner-match-pill'), "planner-match-pill CSS exists for plant cards");
assert(indexHtml.includes('Add Top 6 / Layer to Report'), "Concise Add Top text is configured");

console.log("\n✅ ALL PLANNER CLEANUP & SIMPLIFICATION CHECKS PASSED!\n");
