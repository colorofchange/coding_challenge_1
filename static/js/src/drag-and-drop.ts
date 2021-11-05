/**
 * Resizes Images Added To CKeditor
 */
export default () => {
  const $CKImage = $( "iframe" ).contents().find( ".cke_widget_element" );
  const lastImageIndex = $CKImage.length - 1;
  $CKImage[ lastImageIndex ].setAttribute( "height", "auto" );
  $CKImage[ lastImageIndex ].setAttribute( "width", "500" );
};
