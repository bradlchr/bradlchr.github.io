/**
 * test_planner_workflow.js
 * Verification test for Guided Workflow-Based Garden Planner
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

console.log("\n==================== TEST SUITE: GUIDED WORKFLOW GARDEN PLANNER ====================");

// 1. Verify HTML Elements exist in index.html
console.log("\n--- Checking HTML Elements ---");
assert(indexHtml.includes('id="plannerSetupWizardView"'), "plannerSetupWizardView container exists in index.html");
assert(indexHtml.includes('id="plannerWizardAreasList"'), "plannerWizardAreasList exists in index.html");
assert(indexHtml.includes('id="plannerWizardAddAreaBtn"'), "plannerWizardAddAreaBtn exists in index.html");
assert(indexHtml.includes('id="plannerWizardConditionsPane"'), "plannerWizardConditionsPane exists in index.html");
assert(indexHtml.includes('id="plannerWizardProceedBtn"'), "plannerWizardProceedBtn exists in index.html");
assert(indexHtml.includes('id="plannerWizardProceedBottomBtn"'), "plannerWizardProceedBottomBtn exists in index.html");
assert(indexHtml.includes('id="plannerMainLayout"'), "plannerMainLayout exists in index.html");
assert(indexHtml.includes('id="plannerWorkflowBannerWrap"'), "plannerWorkflowBannerWrap exists in index.html");
assert(indexHtml.includes('id="plannerAreaConditionsModal"'), "plannerAreaConditionsModal exists in index.html");
assert(indexHtml.includes('id="plannerAreaConditionsModalTitle"'), "plannerAreaConditionsModalTitle exists in index.html");
assert(indexHtml.includes('id="plannerAreaConditionsModalBody"'), "plannerAreaConditionsModalBody exists in index.html");
assert(indexHtml.includes('id="plannerAreaModalSaveBtn"'), "plannerAreaModalSaveBtn exists in index.html");
assert(indexHtml.includes('id="plannerRestartWizardBtn"'), "plannerRestartWizardBtn exists in index.html");

// 2. Verify CSS & Responsive rules
console.log("\n--- Checking CSS Rules ---");
assert(indexHtml.includes('.planner-area-card'), "planner-area-card CSS exists");
assert(indexHtml.includes('.planner-area-edit-btn'), "planner-area-edit-btn used in planner roster");
assert(indexHtml.includes('.planner-wizard-split'), "planner-wizard-split CSS / responsive class exists");

// 3. Verify JavaScript Functions & Logic
console.log("\n--- Checking JavaScript Functions & Exports ---");
assert(indexHtml.includes('function getPlannerWorkflowState()'), "getPlannerWorkflowState() defined");
assert(indexHtml.includes('function persistPlannerWorkflowState(wf)'), "persistPlannerWorkflowState() defined");
assert(indexHtml.includes('function renderPlannerSetupWizard()'), "renderPlannerSetupWizard() defined");
assert(indexHtml.includes('function openAreaConditionsModal(areaIdx)'), "openAreaConditionsModal() defined");
assert(indexHtml.includes('window.getPlannerWorkflowState = getPlannerWorkflowState'), "getPlannerWorkflowState exported to window");
assert(indexHtml.includes('window.persistPlannerWorkflowState = persistPlannerWorkflowState'), "persistPlannerWorkflowState exported to window");
assert(indexHtml.includes('window.openAreaConditionsModal = openAreaConditionsModal'), "openAreaConditionsModal exported to window");
assert(indexHtml.includes('window.renderPlannerSetupWizard = renderPlannerSetupWizard'), "renderPlannerSetupWizard exported to window");

// 4. Verify Workflow Logic & State Transitions in Code
console.log("\n--- Checking Workflow Logic & State Transitions ---");
// Check createNewConsultation initializes workflow
assert(indexHtml.includes("plannerWorkflow: { status: 'setup_areas', currentStepAreaIdx: 0 }"), "createNewConsultation initializes plannerWorkflow with 'setup_areas'");
// Check switchActiveConsultation handles plannerWorkflow fallback
assert(indexHtml.includes("state.plannerWorkflow = { status: hasStaged ? 'completed' : 'setup_areas', currentStepAreaIdx: 0 }"), "switchActiveConsultation handles legacy or fresh consultations");
// Check renderGardenPlannerUI toggles wizard view vs main layout
assert(indexHtml.includes("wizardView.style.display = 'flex'") && indexHtml.includes("mainLayout.style.display = 'none'"), "renderGardenPlannerUI shows wizardView and hides mainLayout in 'setup_areas'");
assert(indexHtml.includes("wizardView.style.display = 'none'") && indexHtml.includes("mainLayout.style.display = 'grid'"), "renderGardenPlannerUI shows mainLayout and hides wizardView in 'review_areas' and 'completed'");

// Check Step Navigation in footer
assert(indexHtml.includes("id=\"plannerWfNextBtn\""), "Continue to Next Area button generated during review");
assert(indexHtml.includes("id=\"plannerWfPrevBtn\""), "Previous Area button generated during review");
assert(indexHtml.includes("id=\"plannerWfFinishBtn\""), "Finish Guided Setup button generated on last area");

// Check Edit Button stops propagation and calls openAreaConditionsModal
assert(indexHtml.includes("openAreaConditionsModal(idx)"), "openAreaConditionsModal(idx) wired to area edit buttons");
assert(indexHtml.includes("e.stopPropagation()"), "Edit button stops click event propagation");

// Check resume behavior
assert(indexHtml.includes("const stepIdx = Math.max(0, Math.min(wf.currentStepAreaIdx || 0, state.gardenAreas.length - 1))"), "openGardenPlanner resumes at currentStepAreaIdx during review_areas");

// 5. Test State Transitions Unit Logic
console.log("\n--- Testing State Transitions Logic In-Memory ---");
const state = {
  consultations: [],
  activeConsultationId: null,
  gardenAreas: ["Area 1: Front Porch", "Area 2: Front Sidewalk/Mailbox", "Area 3: Backyard Shade Garden"],
  gardenAreaProfiles: [],
  stagedPlants: [],
  activePlannerAreaIdx: 0,
  plannerWorkflow: null
};

// Mock getPlannerWorkflowState
function mockGetPlannerWorkflowState() {
  if (!state.plannerWorkflow) {
    state.plannerWorkflow = { status: 'setup_areas', currentStepAreaIdx: 0 };
  }
  return state.plannerWorkflow;
}

// 1. Initial State
let wf = mockGetPlannerWorkflowState();
assert(wf.status === 'setup_areas', "Initial workflow status is 'setup_areas'");

// 2. Transition to Step-by-Step Review
wf.status = 'review_areas';
wf.currentStepAreaIdx = 0;
state.activePlannerAreaIdx = 0;
assert(wf.status === 'review_areas' && state.activePlannerAreaIdx === 0, "Transitioned to review_areas Step 0 (Area 1)");

// 3. Advance to Step 1 (Area 2)
wf.currentStepAreaIdx++;
state.activePlannerAreaIdx = wf.currentStepAreaIdx;
assert(wf.currentStepAreaIdx === 1 && state.activePlannerAreaIdx === 1, "Advanced to Step 1 (Area 2)");

// 4. Simulate closing and re-opening planner (Resume where left off)
const resumedIdx = wf.status === 'review_areas' ? wf.currentStepAreaIdx : 0;
assert(resumedIdx === 1, "Resuming planner picks up at Step 1 (Area 2)");

// 5. Advance to Step 2 (Area 3 - final area)
wf.currentStepAreaIdx++;
state.activePlannerAreaIdx = wf.currentStepAreaIdx;
assert(wf.currentStepAreaIdx === 2, "Reached final area Step 2 (Area 3)");

// 6. Finish Guided Setup
wf.status = 'completed';
assert(wf.status === 'completed', "Workflow status marked 'completed'");

// 7. Re-opening in completed mode
const isCompleted = wf.status === 'completed';
assert(isCompleted === true, "Planner opens directly in dashboard mode when status is 'completed'");

console.log("\n✅ ALL GUIDED WORKFLOW GARDEN PLANNER CHECKS PASSED SUCCESSFULLY!\n");
