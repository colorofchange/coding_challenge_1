/**
 * Handles logic for determining when to replace a tag vs add it in addition to existing
 * Additionally, effectively 'autosaves' values in tag modal
 *
 * @param {HTMLElement} $tagType - The tag type DOM element
 * @param {string} $tag - The new tag element to be added to the $tagType
 * @param {string} tagTypeName - The name of the tag type ('OWN', 'HELP', etc)
 * @param {string} tagName - The name or "value" of the tag
 */
export const handleTagAddition = (
  $tagType:HTMLElement,
  $tag:HTMLSpanElement,
  tagTypeName:string|undefined,
  tagName:string
) => {
  const $hiddenTagTypeField = <HTMLInputElement>document.getElementById( `id_tag_${tagTypeName?.toLowerCase()}` );
  let $hiddenFieldValue = $hiddenTagTypeField.value;
  if ( $tagType?.childElementCount ) {
    if ( !$hiddenFieldValue.includes( tagName ) ) {
      if ( tagTypeName === "HELP" || tagTypeName === "OTH" ) {
        $tagType.appendChild( $tag );
        $hiddenTagTypeField.value += `, ${tagName}`;
      } else {
        $tagType.lastChild?.replaceWith( $tag );
        $hiddenFieldValue = tagName;
      }
    }
  } else {
    if ( tagName ) {
      $tagType.appendChild( $tag );
    }
    $hiddenFieldValue = tagName;
  }
};

/**
 * Also auto-updates form with values in tag modal
 *
 * @param {HTMLElement} $tagToRemove - The $tag element in the DOM to remove
 * @param {string} tagTypeName - The name of the tag type ('OWN', 'HELP', etc)
 */
export const handleTagRemoval = ( $tagToRemove:HTMLElement|null, tagTypeName:string|undefined ) => {
  const $hiddenTagTypeField = <HTMLInputElement>document.getElementById( `id_tag_${tagTypeName?.toLowerCase()}` );
  $hiddenTagTypeField.value = $hiddenTagTypeField.value.replace( `${$tagToRemove?.firstChild?.textContent}, `, "" );
  $tagToRemove?.remove();
};

/**
 * Adds tag element to the DOM, with an interactive close feature
 *
 * NOTE: Only creates one element per call
 *
 * @param {string | any} tagName - The name or "value" of the tag
 * @param {string} tagType - The type of the tag to create
 */
export const createTagElement = ( tagName:any, tagType:string|undefined ) => {
  const $currentTagType = <HTMLElement>document.querySelector( `[data-tagtype=${tagType}` );
  const $tag = document.createElement( "span" );
  const $removeTagButton = document.createElement( "span" );
  $tag.classList.add( `${tagType}_tag`, "tag" );
  $removeTagButton.classList.add( "remove_tag" );
  $tag.textContent = tagName;
  $removeTagButton.textContent = "X";
  $tag.appendChild( $removeTagButton );

  handleTagAddition( $currentTagType, $tag, tagType, tagName );
  $removeTagButton.addEventListener( "click", ( e ) => (
    handleTagRemoval( ( <HTMLElement>e.target ).parentElement, tagType ) ) );
};
