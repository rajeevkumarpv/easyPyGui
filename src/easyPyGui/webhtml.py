def init_window(name: str):
    """
    Initialize a web HTML page with a given title.
    (web, html)
    :param name: Page title.
    :return: A string representing the initial part of the HTML document.
    """
    html_template = (
        f"<!DOCTYPE html>\n<html>\n<head>\n<title>{name}</title>\n</head>\n<body>\n"
    )
    return html_template


def create_widget(widget_def: dict):
    """
    Create an HTML widget from a widget definition.
    (web, html)
    widget_def should contain 'name' and 'code', where code is HTML code.
    :param widget_def: Dictionary containing widget definition.
    :return: A string containing the widget HTML.
    """
    return widget_def.get("code", "")


def display_window(html_content: str):
    """
    Finalize and display the HTML page.
    (web, html)
    :param html_content: The HTML content to display.
    :return: A full HTML page string.
    """
    html_end = "\n</body>\n</html>"
    full_page = html_content + html_end
    # For prototyping purposes, simply print the HTML.
    print(full_page)
    return full_page
