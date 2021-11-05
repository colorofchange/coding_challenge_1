export const $saveAKButton = document.getElementById( "save-ak-mailer" );
export const $savedInAkBanner = document.getElementById( "ak-save-banner" );
let $akMailerLink = ( <HTMLAnchorElement>document.getElementById( "ak-mailer-link" ) )?.href;
const $mailingForm = <HTMLFormElement> document.getElementById( "form_wrapper" );
export const akid = $mailingForm?.dataset.akid;

export function hide( ...elements:any[] ) {
  elements.forEach( ( el ) => {
    if ( el ) {
      el.classList.add( "hide" );
    }
  } );
}

export function show( ...elements:any[] ) {
  elements.forEach( ( el ) => {
    if ( el ) {
      el.classList.remove( "hide" );
    }
  } );
}

export function addSavedToAKBanner( mailerId:string | undefined ) {
  if ( mailerId ) {
    $akMailerLink = `https://act.colorofchange.org/mailings/drafts/${mailerId}`;
    show( $savedInAkBanner );
  }
}

export function getTags( getFullList: boolean, tagType:string ) {
  if ( getFullList ) {
    return Promise.resolve( $.ajax( {
      url: "/tags?full=1",
      type: "GET"
    } ) );
  }

  return Promise.resolve( $.ajax( {
    url: `/tags?tag_type=${tagType}`,
    type: "GET"
  } ) );
}
export function getUser() {
  return Promise.resolve( $.ajax( {
    url: "/users",
    type: "GET"
  } ) );
}
function split( val:string ) {
  return val.split( /,\s*/ );
}
function extractLast( term:string ) {
  return split( term ).pop();
}
export function getTagType() {
  return document.getElementById( "active_tagType" )?.dataset.tagtype;
}

export function saveInAK() {
  $.ajax( {
    method: "POST",
    contentType: "application/x-www-form-urlencoded",
    url: "/save-ak-mailer",
    data: {
      csrfmiddlewaretoken: $( "input[name=\"csrfmiddlewaretoken\"]" ).val(),
      mailing_id: $mailingForm.dataset.mailingid
    }
  } ).done( ( response ) => {
    let savedAKButtonText = $saveAKButton?.textContent;
    if ( !akid ) {
      // @ts-expect-error
      const confetti = new ConfettiGenerator();
      addSavedToAKBanner( response );
      confetti.render();
      setTimeout( () => confetti.clear(), 3000 );
    } else {
      savedAKButtonText = "Saved!";
      setTimeout( () => {
        savedAKButtonText = "Save in AK";
      }, 1500 );
    }
  } );
}

export function addAutocomplete( id:string, sourceFunc:any, args:any ) {
  const data = sourceFunc( args[ "get_full_list" ], args[ "tag_type" ] );
  data.then( ( items:any ) => {
    $( `#${id}` ).on( "keydown", function( event ) {
      // @ts-expect-error
      if ( event.keyCode === $.ui.keyCode.TAB &&

      // @ts-expect-error
          $( this ).autocomplete( "instance" ).menu.active ) {
        event.preventDefault();
      }
    } )

    // @ts-expect-error
      .autocomplete( {
        minLength: 0,
        source( request:any, response:any ) {
        // delegate back to autocomplete, but extract the last term
          // @ts-expect-error
          response( $.ui.autocomplete.filter(
            items, extractLast( request.term )
          ) );
        },
        focus() {
        // prevent value inserted on focus
          return false;
        },
        select( e:Event, ui:any ) {
          const terms = split( this.value );

          // remove the current input
          terms.pop();

          // add the selected item
          terms.push( ui.item.value );

          // add placeholder to get the comma-and-space at the end
          terms.push( "" );
          this.value = terms.join( ", " );
          return false;
        }
      } ).focus( function() {
      // @ts-expect-error
        $( this ).autocomplete( "search" );
      } );
  } );
}
