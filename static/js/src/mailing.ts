import resizeUploadedCkImage from "./drag-and-drop.js";
import { createTagElement } from "./create-tag-element.js";
import { openModal, addTagModalButton, changeActiveTagType, $tagModalSearch, $activeTagType, $openTagModalButton, closeModal, generateCustomTagOption } from "./tag-modal.js";
import { getTags, addAutocomplete, hide, show, saveInAK, addSavedToAKBanner, $saveAKButton, akid } from "./scripts.js";
import { $addSubjectButton, totalInitialSubjects as hasInitialSubjectField } from "./handle-multiple-subjects.js";
import { $validationWarningCloseButton, closeValidationWarning, $tagList, openValidationWarning, validation } from "./validation.js";

const $emailClientNavbar = document.querySelector(".email-client_navbar");
const $saveButton = document.getElementById("saveCloseModal");
const $templateImages = [...document.querySelectorAll(".template__image")];
const $templateSelect = <HTMLSelectElement>document.getElementById("id_template");
const $loadingSpinner = document.querySelector(".fa-spinner");
const $previewImages = [...document.querySelectorAll(".preview--image")];
const $gmailPreviewImage = document.getElementById("preview-GMAIL");
const $visiblePreviewImage = document.querySelector(".preview--image:not([style=\"display: none;\"])");

/** Handles which email client preview is shown */
const handleLitmusEmailClientDisplay = (e: Event) => {
  const $emailClientClicked = <HTMLElement>e.target;
  const $emailClientImage = document.getElementById(`preview-${$emailClientClicked?.id}`);
  console.log($emailClientImage);
  const $emailClients = Array.from((<HTMLElement>$emailClientNavbar).children);
  $emailClients.forEach(($client) => $client.classList.remove("active"));
  hide(...$previewImages);
  show($emailClientImage);
  $emailClientClicked?.classList.add("active");
};

show($gmailPreviewImage);
addSavedToAKBanner(akid);
addTagModalButton();

if (!hasInitialSubjectField) {
  $addSubjectButton?.click();
}

if ($visiblePreviewImage) {
  hide($loadingSpinner);
}

$(() => {
  // function wrapper needed as iframe contents have to be fully loaded.
  CKEDITOR.instances.id_body.on("fileUploadResponse", () => setTimeout(resizeUploadedCkImage, 1000));
});

addAutocomplete("tag-modal-search", getTags, {
  get_full_list: false,
  tag_type: "OWN"
});

if ($tagList) {
  Array.from($tagList?.children).forEach(($tag) => {
    const tagType = (<HTMLElement>$tag).dataset.tagtype;
    const tagName = (<HTMLInputElement>document.getElementById(`id_tag_${tagType?.toLowerCase()}`))?.value;
    createTagElement(tagName, tagType);
  });
}

$tagModalSearch?.addEventListener("keyup", (e) => {
  const whatsTyped = (<HTMLInputElement>e.target).value;
  const $customTagOption = document.getElementById("customTag");
  if ($customTagOption) {
    show($customTagOption);
    $customTagOption.textContent = whatsTyped;
  } else {
    generateCustomTagOption(whatsTyped);
  }
});

document.addEventListener("click", (e) => {
  // dropdown element can't be targeted directly b/c it is added via in the '.autocomplete()' dependency
  const $clicked = <HTMLElement>e.target;
  const $customTagOption = document.getElementById("customTag");
  hide($customTagOption); // mimic standard dropdown
  if ($clicked.classList.contains("ui-menu-item-wrapper") || $customTagOption === $clicked) {
    createTagElement($clicked.textContent, $activeTagType?.dataset.tagtype);
    $tagModalSearch.value = "";
  }
});

$saveAKButton?.addEventListener("click", () => (validation.check() ? saveInAK : openValidationWarning(validation.error)));
$validationWarningCloseButton?.addEventListener("click", closeValidationWarning);
$saveButton?.addEventListener("click", closeModal);
$tagList?.addEventListener("click", (e) => changeActiveTagType(e));
$emailClientNavbar?.addEventListener("click", (e) => handleLitmusEmailClientDisplay(e));

$openTagModalButton.addEventListener("click", (e) => {
  e.preventDefault();
  openModal();
});

$templateSelect?.addEventListener("change", () => {
  const selectedOption = $templateSelect?.selectedOptions[0]?.textContent;
  (<HTMLImageElement>$templateImages[0]).src = `/static/images/template_images/${selectedOption}-preview.png`;
});

// @ts-ignore
$(".preview").magnificPopup({
  delegate: "a",
  type: "image",
  gallery: { enabled: true }
});
