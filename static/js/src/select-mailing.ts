import { addAutocomplete, getTags, getUser, show, hide } from "./scripts.js";

const $filterBtn = <HTMLButtonElement>document.getElementById("filter-btn");
const $filterType = <HTMLSelectElement>document.getElementById("filter-type");
const $tagInput = <HTMLInputElement>document.getElementById("tag_input");
const $userInput = <HTMLInputElement>document.getElementById("user_input");
const $rightWrapper = $(".wrapper__right");

addAutocomplete("tag_input", getTags, { get_full_list: true });
addAutocomplete("user_input", getUser, { get_full_list: true });

const filterMailings = () => {
  $.ajax({
    method: "POST",
    contentType: "application/x-www-form-urlencoded",
    url: "/filter-mailings",
    data: {
      csrfmiddlewaretoken: $("input[name=\"csrfmiddlewaretoken\"]").val(),
      type: $filterType.value,
      value: $(".filters:visible").val()

    }
  }).done((response) => {
    $rightWrapper.empty();
    response.forEach((mailing: any) => {
      const date = new Date(response[mailing].updated_date);
      $rightWrapper.append(
        `<div class="exist-mailing">
            <span class="exist-mailing--date">
            ${`${date.toLocaleDateString("default", { month: "long" })} ${date.getDate()}, ${date.getFullYear()}`}
            </span>
            <a class="exist-mailing--title" href="mailings/${response[mailing].id}">${response[mailing].subjects__subject}</a>
            <div class="exist-mailing--tags">
              <span class="exist-mailing--tags-owner">Owner</span>
              <span class="exist-mailing--tags-helper">Helper</span>
              <span class="exist-mailing--tags-dept">Dept</span>
              <span class="exist-mailing--tags-issue">Issue</span>
              <span class="exist-mailing--tags-ask">Ask</span>
              <span class="exist-mailing--tags-entity">Entity</span>
              <span class="exist-mailing--tags-targeting">Targeting</span>
              <span class="exist-mailing--tags-camp">Camp</span>
              <span class="exist-mailing--tags-other">Other</span>
            </div>
        </div>`
      );
    });
  });
};

$filterType?.addEventListener("change", () => {
  hide($tagInput, $userInput);
  $filterType.value === "Tag" ? show($tagInput) : show($userInput);
});

$filterBtn?.addEventListener("click", filterMailings);
