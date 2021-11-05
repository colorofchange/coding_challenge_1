import { hide, show } from "./scripts.js";

const templateTypes = ["default", "fundraising"]; // TODO - make dynamic
const prev = document.getElementById("prev");
const next = document.getElementById("next");
const $templateWrapper = document.querySelector(".template__wrapper");
const $templateSelector = <HTMLElement>document.getElementById("select-template");
const scrollWidth = 536;

const loadTemplates = (templateType: string = "default") => {
  $.ajax({
    method: "POST",
    contentType: "application/x-www-form-urlencoded",
    url: "/filter-templates",
    data: {
      csrfmiddlewaretoken: $("input[name=\"csrfmiddlewaretoken\"]").val(),
      template_type: templateType
    }
  }).done((response) => {
    response.forEach((template: any) => {
      const dashTemplateName = template.name.replace(" ", "-").toLowerCase();
      $(".template__wrapper").append(
        `<div class="template hide" data-template-type="${template.template_type}">
         <span class="template--title">${template.name}</span>
         <a href ='/new/${dashTemplateName}'>
         <img class="template__image" src = "/static/images/template_images/${dashTemplateName}-preview.png"/>
        </a>
        </div>`
      );
    });
  });
};

const filterTemplates = (target: HTMLSelectElement, templates: any[]) => {
  templates.forEach((template) => {
    show(template, $templateWrapper);
    if (target.value !== template.dataset.templateType) {
      hide(template);
    }
  });
};

templateTypes.forEach(loadTemplates);

$templateSelector.addEventListener("change", (e) => {
  const $templates = Array.from(document.querySelectorAll(".template"));
  filterTemplates(<HTMLSelectElement>e.target, $templates);
});

const scrollTemplates = (direction: string) => {
  if ($templateWrapper) {
    if (direction === "prev") {
      const x = $templateWrapper.scrollLeft - scrollWidth;
      if (x >= 0) {
        $templateWrapper.scrollTo(x, 0);
      }
    } else if (direction === "next") {
      const x = $templateWrapper.scrollLeft + scrollWidth;
      if (x < $templateWrapper.scrollWidth) {
        $templateWrapper.scrollTo(x, 0);
      }
    }
  }
};

prev?.addEventListener("click", () => scrollTemplates("prev"));
next?.addEventListener("click", () => scrollTemplates("next"));
