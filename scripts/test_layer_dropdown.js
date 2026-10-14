/**
 * Test verifying the Architecture Layer Dropdown functionality in Garden Planner
 */
const fs = require('fs');

const indexHtml = fs.readFileSync('index.html', 'utf8');

// 1. Verify plannerLayerSelect exists in HTML
if (!indexHtml.includes('id="plannerLayerSelect"')) {
  console.error("FAIL: plannerLayerSelect element missing in index.html");
  process.exit(1);
}

// 2. Verify label for plannerLayerSelect exists
if (!indexHtml.includes('for="plannerLayerSelect"')) {
  console.error("FAIL: label for plannerLayerSelect missing in index.html");
  process.exit(1);
}

// 3. Verify event listener for plannerLayerSelect exists
if (!indexHtml.includes("document.getElementById('plannerLayerSelect')?.addEventListener('change'")) {
  console.error("FAIL: change listener for plannerLayerSelect missing in index.html");
  process.exit(1);
}

// 4. Verify state has activePlannerLayer
if (!indexHtml.includes('activePlannerLayer: null')) {
  console.error("FAIL: activePlannerLayer missing in state definition");
  process.exit(1);
}

// 5. Verify renderAreaRecommendations populates layerSelect and computes layersToRender
if (!indexHtml.includes('availableLayers.filter(l => l === currentSelection)')) {
  console.error("FAIL: layersToRender filtering missing in renderAreaRecommendations");
  process.exit(1);
}

// 6. Verify layer navigation footer buttons
if (!indexHtml.includes('plannerPrevLayerBtn') || !indexHtml.includes('plannerNextLayerBtn')) {
  console.error("FAIL: layer navigation buttons missing in renderAreaRecommendations");
  process.exit(1);
}

// 7. Verify dynamic Add All button text and delegation
if (!indexHtml.includes("addAllLayerToConsultation(activeLayer, profile.name)")) {
  console.error("FAIL: addTopRecommendedToConsultation missing delegation to activeLayer");
  process.exit(1);
}

console.log("✓ All Architecture Layer Dropdown tests passed successfully!");
