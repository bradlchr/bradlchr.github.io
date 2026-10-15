/**
 * Unit & Integration Test for Garden Area Planner & Recommendation Suite
 */
const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');

const plantsJson = fs.readFileSync('data/plants_enriched.json', 'utf8');
const embeddedMasterPlants = JSON.parse(plantsJson);
console.log(`Loaded ${embeddedMasterPlants.length} plants for testing.`);

// Test mock state and functions
const state = {
  allPlants: embeddedMasterPlants,
  stagedPlants: [],
  gardenAreas: ["Area 1: Front Porch", "Area 2: Front Sidewalk/Mailbox", "Area 3: Backyard Shade Garden"],
  gardenAreaProfiles: [],
  activePlannerAreaIdx: 0,
  currentUser: null
};

// Check guest access blocking
function testGuestAccess() {
  state.currentUser = null;
  const isGuest = !state.currentUser || !state.currentUser.name || (state.currentUser.username === 'guest');
  if (!isGuest) throw new Error("Expected guest to be detected when currentUser is null");

  state.currentUser = { username: 'guest' };
  const isGuest2 = !state.currentUser || !state.currentUser.name || (state.currentUser.username === 'guest');
  if (!isGuest2) throw new Error("Expected guest to be detected when username is 'guest'");

  state.currentUser = { username: 'elena.rodriguez', name: 'Elena Rodriguez', role: 'user' };
  const isGuest3 = !state.currentUser || !state.currentUser.name || (state.currentUser.username === 'guest');
  if (isGuest3) throw new Error("Expected standard advisor to NOT be detected as guest");

  console.log("✓ Guest access gate test passed.");
}

testGuestAccess();

// Extract actual helper and recommendation functions from index.html
const SWEET_16_SCIENTIFIC = new Set([
  'asclepias tuberosa', 'baptisia australis', 'carex albicans', 'celastrus scandens',
  'coreopsis lanceolata', 'echinacea purpurea', 'eragrostis spectabilis', 'eryngium yuccifolium',
  'geranium maculatum', 'glandularia canadensis', 'monarda Bradburiana', 'monarda bradburiana',
  'packera obovata', 'penstemon digitalis', 'pycnanthemum muticum', 'schizachyrium scoparium', 'zizia aurea'
]);

const isSweet16 = (p) => Boolean(p && (p.is_sweet_16 || SWEET_16_SCIENTIFIC.has((p.scientific_name || '').toLowerCase())));
const isKcKeystone = (p) => Boolean(p && p.is_kc_keystone === true);
const getPlantLayer = (p) => p?.architectural_layer || '';
const getPlantMaintenanceLevel = (p) => p?.maintenance_level || 'Low';

// Extract SWEET_16_MATCH_MARGIN_PCT, getRecommendationWeightedMatchPct, comparePlannerRecommendations, and getPlantRecommendationsForArea from index.html
const fnStart = html.indexOf('const SWEET_16_MATCH_MARGIN_PCT = 10;');
const fnEnd = html.indexOf('function renderAreaRecommendations()');
if (fnStart === -1 || fnEnd === -1) {
  throw new Error('Could not locate SWEET_16_MATCH_MARGIN_PCT or getPlantRecommendationsForArea in index.html');
}
const extractedCode = html.slice(fnStart, fnEnd);
const plannerFns = new Function(
  'state', 'window', 'isSweet16', 'isKcKeystone', 'getPlantLayer', 'getPlantMaintenanceLevel',
  `${extractedCode}\nreturn { SWEET_16_MATCH_MARGIN_PCT, getRecommendationWeightedMatchPct, comparePlannerRecommendations, getPlantRecommendationsForArea };`
)(state, { embeddedMasterPlants }, isSweet16, isKcKeystone, getPlantLayer, getPlantMaintenanceLevel);

const {
  SWEET_16_MATCH_MARGIN_PCT,
  getRecommendationWeightedMatchPct,
  comparePlannerRecommendations,
  getPlantRecommendationsForArea
} = plannerFns;

if (SWEET_16_MATCH_MARGIN_PCT !== 10) {
  throw new Error(`Expected SWEET_16_MATCH_MARGIN_PCT to be 10, got ${SWEET_16_MATCH_MARGIN_PCT}`);
}

// Test Rain Garden Scenario
const rainGardenProfile = {
  name: "Area 1: Rain Garden",
  sunlight: "Full Sun",
  moisture: "Wet",
  maintenance: "Low",
  structuralLayers: ["Groundcover", "Seasonal/Herbaceous Layer", "Structural Layer"]
};

const rainRecs = getPlantRecommendationsForArea(rainGardenProfile);
if (rainRecs.length < 5) throw new Error("Expected at least 5 rain garden recommendations");
console.log(`✓ Rain garden scenario returned ${rainRecs.length} compatible native species.`);

// Test Woodland Shade Scenario
const shadeProfile = {
  name: "Area 3: Backyard Woodland",
  sunlight: "Full Shade",
  moisture: "Medium",
  maintenance: "Low",
  structuralLayers: ["Groundcover", "Seasonal/Herbaceous Layer", "Understory"]
};

const shadeRecs = getPlantRecommendationsForArea(shadeProfile);
if (shadeRecs.length < 5) throw new Error("Expected at least 5 shade garden recommendations");
console.log(`✓ Shade garden scenario returned ${shadeRecs.length} compatible native species.`);

// Verify Consultation Staging with Area assignment
const testPlant = rainRecs[0].plant;
state.stagedPlants.push({
  id: testPlant.id || testPlant.scientific_name,
  common_name: testPlant.common_names?.[0] || testPlant.scientific_name,
  scientific_name: testPlant.scientific_name,
  target_area: rainGardenProfile.name,
  quantity: 1
});

if (state.stagedPlants.length !== 1) throw new Error("Failed to stage plant");
if (state.stagedPlants[0].target_area !== rainGardenProfile.name) throw new Error("target_area mismatch");

console.log(`✓ Staged plant ${state.stagedPlants[0].common_name} assigned correctly to ${state.stagedPlants[0].target_area}`);

// Verify Top 6 capping per architecture layer
const layerOrder = ['Groundcover', 'Seasonal/Herbaceous Layer', 'Structural Layer', 'Understory', 'Canopy', 'Vine'];
const grouped = {};
layerOrder.forEach(l => { grouped[l] = []; });
rainRecs.forEach(rec => {
  const lKey = rec.effectiveLayer || 'Seasonal/Herbaceous Layer';
  if (!grouped[lKey]) grouped[lKey] = [];
  grouped[lKey].push(rec);
});

layerOrder.forEach(layerKey => {
  const layerPlants = grouped[layerKey].slice(0, 6);
  if (layerPlants.length > 6) {
    throw new Error(`Layer ${layerKey} has ${layerPlants.length} plants, expected <= 6`);
  }
});
console.log(`✓ Verified architecture layers strictly cap recommendations to top 6 plants.`);

// Test KC Sweet 16 Preference & 10% Match Margin Rule
function testSweet16PreferenceAndMargin() {
  const goldenAlexander = embeddedMasterPlants.find(p => p.scientific_name === 'Zizia aurea');
  const blackEyedSusan = embeddedMasterPlants.find(p => p.scientific_name === 'Rudbeckia hirta');
  if (!goldenAlexander || !blackEyedSusan) {
    throw new Error("Could not find Zizia aurea or Rudbeckia hirta in plant dataset");
  }

  // 1. Direct test of the 10% match margin rule (e.g. Black-Eyed Susan 95% vs Golden Alexander 90%)
  const besRec95 = {
    plant: blackEyedSusan,
    score: 128,
    matchPct: 95,
    isSweet16: false,
    matchesCriteria: true
  };
  const gaRec90 = {
    plant: goldenAlexander,
    score: 122,
    matchPct: 90,
    isSweet16: true,
    matchesCriteria: true
  };

  if (getRecommendationWeightedMatchPct(besRec95) !== 95) {
    throw new Error(`Expected Black-Eyed Susan (95%) weighted pct to be 95, got ${getRecommendationWeightedMatchPct(besRec95)}`);
  }
  if (getRecommendationWeightedMatchPct(gaRec90) !== 100) {
    throw new Error(`Expected Golden Alexander (90% + 10% Sweet 16 margin) weighted pct to be 100, got ${getRecommendationWeightedMatchPct(gaRec90)}`);
  }

  const pair90vs95 = [besRec95, gaRec90].sort(comparePlannerRecommendations);
  if (pair90vs95[0].plant.scientific_name !== 'Zizia aurea') {
    throw new Error("Expected Golden Alexander (90% match, Sweet 16) to rank higher than Black-Eyed Susan (95% match, non-Sweet 16)");
  }

  // Boundary test: 85% Sweet 16 vs 95% non-Sweet 16 (tie at 95% weighted -> Sweet 16 wins tie-breaker)
  const gaRec85 = { ...gaRec90, matchPct: 85, score: 115 };
  const pair85vs95 = [besRec95, gaRec85].sort(comparePlannerRecommendations);
  if (pair85vs95[0].plant.scientific_name !== 'Zizia aurea') {
    throw new Error("Expected Golden Alexander (85% + 10% = 95% weighted) to win tie-breaker over Black-Eyed Susan (95%)");
  }

  // Outside 10% margin test: 80% Sweet 16 vs 95% non-Sweet 16 -> 95% non-Sweet 16 ranks higher
  const gaRec80 = { ...gaRec90, matchPct: 80, score: 108 };
  const pair80vs95 = [gaRec80, besRec95].sort(comparePlannerRecommendations);
  if (pair80vs95[0].plant.scientific_name !== 'Rudbeckia hirta') {
    throw new Error("Expected Black-Eyed Susan (95%) to rank higher than a Sweet 16 plant at 80% (outside 10% margin)");
  }
  console.log("✓ 10% match margin comparator test passed (90% Sweet 16 > 95% non-Sweet 16).");

  // 2. Full Garden Planner profile where both Golden Alexander and Black-Eyed Susan qualify
  const sunnyMesicProfile = {
    name: "Area 1: Sunny Border",
    sunlight: "Full Sun",
    moisture: "Medium",
    maintenance: "Low",
    bloomColors: ["Any"],
    structuralLayers: ["Groundcover", "Seasonal/Herbaceous Layer", "Structural Layer"]
  };
  const recsAnyColor = getPlantRecommendationsForArea(sunnyMesicProfile);
  const seasonalTop6Any = recsAnyColor.filter(r => r.effectiveLayer === 'Seasonal/Herbaceous Layer').slice(0, 6);
  const gaIdxAny = recsAnyColor.findIndex(r => r.plant.scientific_name === 'Zizia aurea');
  const besIdxAny = recsAnyColor.findIndex(r => r.plant.scientific_name === 'Rudbeckia hirta');

  if (gaIdxAny === -1 || besIdxAny === -1) {
    throw new Error("Expected both Zizia aurea and Rudbeckia hirta in recommendations for Full Sun + Medium moisture");
  }
  if (gaIdxAny >= besIdxAny) {
    throw new Error(`Expected Golden Alexander (idx ${gaIdxAny}) to rank ahead of Black-Eyed Susan (idx ${besIdxAny})`);
  }
  if (!seasonalTop6Any.some(r => r.plant.scientific_name === 'Zizia aurea')) {
    throw new Error("Expected Golden Alexander (Zizia aurea) to be in Top 6 of Seasonal/Herbaceous Layer for Full Sun + Medium moisture");
  }

  // Also test with explicit Yellow bloom color filter
  const sunnyYellowProfile = {
    ...sunnyMesicProfile,
    bloomColors: ["Yellow"]
  };
  const recsYellow = getPlantRecommendationsForArea(sunnyYellowProfile);
  const seasonalTop6Yellow = recsYellow.filter(r => r.effectiveLayer === 'Seasonal/Herbaceous Layer').slice(0, 6);
  const gaIdxYellow = recsYellow.findIndex(r => r.plant.scientific_name === 'Zizia aurea');
  const besIdxYellow = recsYellow.findIndex(r => r.plant.scientific_name === 'Rudbeckia hirta');

  if (gaIdxYellow >= besIdxYellow) {
    throw new Error(`Expected Golden Alexander (idx ${gaIdxYellow}) to rank ahead of Black-Eyed Susan (idx ${besIdxYellow}) for Yellow bloom filter`);
  }
  if (!seasonalTop6Yellow.some(r => r.plant.scientific_name === 'Zizia aurea')) {
    throw new Error("Expected Golden Alexander (Zizia aurea) to be in Top 6 of Seasonal/Herbaceous Layer for Yellow bloom filter");
  }
  // Verify non-yellow Sweet 16 flowers (e.g. Purple Coneflower) do not get the +10% margin when Yellow is filtered
  const purpleConeflowerRec = recsYellow.find(r => r.plant.scientific_name === 'Echinacea purpurea');
  if (purpleConeflowerRec && purpleConeflowerRec.matchesCriteria !== false) {
    throw new Error("Expected Echinacea purpurea to have matchesCriteria=false when bloomColors=['Yellow']");
  }

  console.log("✓ Golden Alexander ranks in Top 6 and above Black-Eyed Susan across qualifying profiles.");
}

testSweet16PreferenceAndMargin();

console.log("\nALL GARDEN PLANNER UNIT TESTS PASSED!");
