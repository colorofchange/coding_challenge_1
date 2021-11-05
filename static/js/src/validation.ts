import { show, hide } from "./scripts.js";

export const $tagList = document.getElementById( "taglist" );
export const $validationWarningCloseButton = document.getElementById( "validation-error-popup__button" );
const $fromLine = <HTMLInputElement>document.getElementById( "id_from_line" );
const $validationErrorPopup = document.getElementById( "validation-error-popup" );
const warningText = {
  tags: "You must input all required tags before saving your mailer.",
  fromLine: "You must input a from line before saving your mailer.",
  body: "You must input body text before saving your mailer."
};

export const openValidationWarning = ( error: string ) => {
  let validationErrorText = $validationErrorPopup?.querySelector( "p" )?.textContent;
  validationErrorText = error;
  show( $validationErrorPopup );
};

export const closeValidationWarning = () => hide( $validationErrorPopup );

/** returns false if failed */
export const validateCKeditor = () => {
  const $CKeditorIframe = <HTMLIFrameElement>document.querySelector( ".cke_wysiwyg_frame" );
  const $CKIframeDocument = $CKeditorIframe.contentDocument || $CKeditorIframe.contentWindow?.document;
  const $CKIframeHTML = $CKIframeDocument?.firstChild;
  const $CKIframeBody = $CKIframeHTML?.childNodes[1];
  return !!$CKIframeBody?.textContent;
};

/** returns false if failed */
export const checkAllRequiredTagsFilled = (): boolean => {
  const fields = $tagList ? Array.from( $tagList.children ) : null;
  fields?.map( ( $tagType ) => {
    const $currentTagType = ( <HTMLElement>$tagType ).dataset.tagtype;
    const $hiddenTagTypeField = <HTMLInputElement>document.getElementById( `id_tag_${$currentTagType?.toLowerCase()}` );
    if ( $currentTagType !== "OTH" && $currentTagType !== "HELP" && $hiddenTagTypeField.value === "" ) {
      return true;
    }
    return false;
  } );
  return !fields?.filter( ( field ) => field ).length;
};

/** NOTE: .check() only returns one error at a time */
export const validation = {
  error: "",
  check: () => {
    if ( !validateCKeditor() ) {
      validation.error = warningText.body;
    } else if ( !$fromLine ) {
      validation.error = warningText.fromLine;
    } else if ( !checkAllRequiredTagsFilled() ) {
      validation.error = warningText.tags;
    } else {
      return true;
    }
    return false;
  }
};
