import { hide } from "./scripts.js";

export const $addSubjectButton = document.getElementById("add_subjects");
export const totalInitialSubjects = parseInt((<HTMLInputElement>document.getElementById("id_subjects-TOTAL_FORMS"))?.value, 10);
const subject1ID = "id_subjects-0-";
let $latestSubjectGroup = document.getElementById(`subject-${totalInitialSubjects}`);
const subjectPlaceholder = "Enter a subject line";
const previewTextPlaceholder = "Enter preview text to be shown below the subject.";
const $removeSubjectButton = document.getElementById("delete_subjects");
const $formSet = document.getElementById("form_set");
const $totalFormsElement = (<HTMLInputElement>document.getElementById("id_subjects-TOTAL_FORMS"));
let totalSubjectGroups = parseInt($totalFormsElement?.value, 10);

/**
 * Create new subject line group (subject + preview-text fields)
 */
const generateSubjectLineGroup = () => {
  const $subjectGroup = document.createElement("div");
  $subjectGroup.id = `subject-${totalSubjectGroups + 1}`;
  $subjectGroup.classList.add("subjectGroup");
  $subjectGroup.innerHTML = $("#empty_form").html().replace(/__prefix__/g, totalSubjectGroups.toString());
  const $newSubjectField = (<HTMLInputElement>$subjectGroup.querySelector("[id$=\"subject\"]"));
  const $newPreviewField = (<HTMLInputElement>$subjectGroup.querySelector("[id$=\"preview_text\"]"));

  $newSubjectField.placeholder = subjectPlaceholder;
  $newPreviewField.placeholder = previewTextPlaceholder;

  if ($latestSubjectGroup) {
    const $latestSubjectText = (<HTMLInputElement>$latestSubjectGroup?.querySelector("[id$=\"subject\"]"))?.value;
    const $latestPreviewText = (<HTMLInputElement>$latestSubjectGroup?.querySelector("[id$=\"preview_text\"]"))?.value;

    if ($latestSubjectText) {
      $newSubjectField.value = $latestSubjectText;
      $newPreviewField.value = $latestPreviewText;
    }
  } else {
    const $subject1 = <HTMLInputElement>document.getElementById(`${subject1ID}subject`);
    const $previewText1 = <HTMLInputElement>document.getElementById(`${subject1ID}preview_text`);
    if ($subject1 && $previewText1) {
      $subject1.required = true;
      $previewText1.required = true;
      $subject1.placeholder = subjectPlaceholder;
      $previewText1.placeholder = previewTextPlaceholder;
    }
  }
  return $subjectGroup;
};

$addSubjectButton?.addEventListener("click", () => {
  const $newSubjectGroup = generateSubjectLineGroup();
  $formSet?.append($newSubjectGroup);
  $latestSubjectGroup = $newSubjectGroup;
  $totalFormsElement.value = `${totalSubjectGroups += 1}`;
});

$removeSubjectButton?.addEventListener("click", () => {
  // TODO - seems like this is checking if this is a new mailing or not
  const $subjectGroupToRemove = $latestSubjectGroup;
  let subjectGroupToRemoveCheckbox = (<HTMLInputElement>$subjectGroupToRemove?.querySelector("[id$=\"DELETE\"]"))?.checked;
  if ($latestSubjectGroup?.id !== "subject-1" && totalSubjectGroups !== 1) {
    $subjectGroupToRemove?.remove();
    subjectGroupToRemoveCheckbox = true;
    $latestSubjectGroup = document.getElementById(`subject-${parseInt((<HTMLElement>$latestSubjectGroup)?.id.slice(-1), 10) - 1}`);
    $totalFormsElement.value = `${totalSubjectGroups -= 1}`;
  }
});
