import { addAutocomplete, getTags, getTagType, hide, show } from "./scripts.js";
import { $tagList } from "./validation.js";

export const $activeTagType = document.getElementById( "active_tagType" );
export const $openTagModalButton = document.createElement( "button" );
export const $tagModalSearch = <HTMLInputElement>document.getElementById( "tag-modal-search" );
const $modalOverlay = document.querySelector( ".modal__wrapper" );
const $tagModal = document.querySelector( ".tag_modal" );
const $ckBodyArea = document.querySelector( ".django-ckeditor-widget" );
const $searchWrapper = document.querySelector( ".search__wrapper" );
const handleKeyDown = ( e:KeyboardEvent ) => { if ( e.key === "Escape" ) { closeModal(); } };

const handleModalOverlayClick = () => {
  document.querySelector( ".modal__wrapper" )?.addEventListener( "click", ( e ) => {
    if ( e.target === $modalOverlay ) { closeModal(); }
  } );
};

export const closeModal = () => {
  $modalOverlay?.removeEventListener( "click", handleModalOverlayClick, true );
  document.removeEventListener( "keydown", ( e ) => handleKeyDown( e ), true );
  hide( $tagModal, $modalOverlay );
};

export const openModal = () => {
  $modalOverlay?.addEventListener( "click", handleModalOverlayClick, true );
  document.addEventListener( "keydown", ( e ) => handleKeyDown( e ), true );
  show( $tagModal, $modalOverlay );
};

/**
 * Handles clicks on the tag types inside the tag modal ('Owner', 'Helper', etc)
 */
export const changeActiveTagType = ( e:Event ) => {
  const $selectedTag = <HTMLElement>e.target;
  let tagTypeText = $activeTagType?.textContent;

  if ( $selectedTag?.classList.contains( "modal__left-tag" ) && $activeTagType ) {
    $tagList?.childNodes.forEach( ( $tag ) => ( ( <HTMLElement>$tag ).classList ? ( <HTMLElement>$tag ).classList.remove( "activeTag" ) : "" ) );
    tagTypeText = $selectedTag.firstChild?.textContent;
    $tagModalSearch.placeholder = `Search for ${$selectedTag.firstChild?.textContent?.toLowerCase()} tags`;
    $activeTagType.dataset.tagtype = $selectedTag.dataset.tagtype;
    $selectedTag.classList.add( "activeTag" );
    addAutocomplete( "tag-modal-search", getTags, { get_full_list: false, tag_type: getTagType() } );
  }
};

/**
 * adds Tag Modal Button to form
 */
export const addTagModalButton = () => {
  $openTagModalButton.id = "openTagModal";
  $openTagModalButton.textContent = "Manage Tags";
  $ckBodyArea?.append( $openTagModalButton );
};

/**
 * For tag types that allow the creation of new tags
 */
export const generateCustomTagOption = ( whatsTyped:string ) => {
  const $customTagOption = document.createElement( "option" );
  $customTagOption.id = "customTag";
  $searchWrapper?.appendChild( $customTagOption );
  $customTagOption.textContent = whatsTyped;
};
