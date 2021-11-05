import os


def make_template(template_name):
    template_name = template_name.replace(" ", "-")
    f = open(f"templates/email/{template_name}.html", "x")
    f.write("<html><div class='body-text'></div></html>")
    f.close()


def delete_template(template_name):
    template_name = template_name.replace(" ", "-")
    os.remove(f"templates/email/{template_name}.html")
