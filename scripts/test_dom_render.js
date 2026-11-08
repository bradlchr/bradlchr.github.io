/**
 * Test verifying that renderPlannerRecommendations runs without throwing DOMException
 */
const fs = require('fs');

const indexHtml = fs.readFileSync('index.html', 'utf8');

// Verify that '#plannerGrid_' no longer appears in querySelector
if (indexHtml.includes('querySelector(`#plannerGrid_') || indexHtml.includes('querySelector("#plannerGrid_') || indexHtml.includes("querySelector('#plannerGrid_")) {
  console.error("FAIL: index.html still has querySelector on plannerGrid ID!");
  process.exit(1);
}

// Verify that safe grid selector is used
if (!indexHtml.includes("layerBox.querySelector('.planner-layer-cards-grid')")) {
  console.error("FAIL: index.html missing layerBox.querySelector('.planner-layer-cards-grid')");
  process.exit(1);
}

// Verify window exports
const exportsToCheck = [
  'window.openGardenPlanner = openGardenPlanner',
  'window.resetPlannerFiltersToBroad = resetPlannerFiltersToBroad',
  'window.addTopRecommendedToConsultation = addTopRecommendedToConsultation',
  'window.addAllLayerToConsultation = addAllLayerToConsultation',
  'window.addPlantToAreaConsultation = addPlantToAreaConsultation',
  'window.removePlantFromAreaConsultation = removePlantFromAreaConsultation'
];

for (const exp of exportsToCheck) {
  if (!indexHtml.includes(exp)) {
    console.error(`FAIL: index.html missing export: ${exp}`);
    process.exit(1);
  }
}

console.log("✓ All querySelector safety checks and window export checks passed.");
