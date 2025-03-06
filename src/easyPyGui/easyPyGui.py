import tkinter as tk  # Used only as a fallback reference


class GlobalWindow:
    """
    GlobalWindow holds the main window parameters:
    - window_name: Title of the window (str, supports python/web).
    - root: The actual GUI root object. For tkinter, this is a tk.Tk() instance;
            for HTML, it is an HTML string.
    - programming_language: Supported languages include 'python' or 'web'.
    - gui_library: Supported libraries include 'tkinter' for python and 'html' for web.
    - widgets_table: A dictionary mapping widget uid to (name, widget instance).
    """

    def __init__(self, name, programming_language="python", gui_library="tkinter"):
        self.window_name = name
        self.programming_language = programming_language
        self.gui_library = gui_library
        self.widgets_table = {}  # Format: {uid: (widget_name, widget_object)}

        # Delegate window initialization to the appropriate backend.
        if self.programming_language == "python" and self.gui_library == "tkinter":
            from . import pythontkinter as backend

            self.root = backend.init_window(name)
        elif self.programming_language == "web" and self.gui_library == "html":
            from . import webhtml as backend

            self.root = backend.init_window(name)
        else:
            raise ValueError(
                f"Unsupported combination: {self.programming_language} with {self.gui_library}"
            )

    def add_widget(self, widget):
        if widget.uid in self.widgets_table:
            raise ValueError(f"Widget with uid {widget.uid} already exists.")
        self.widgets_table[widget.uid] = (widget.name, widget)

    def show(self):
        # Delegate display to the appropriate backend.
        if self.programming_language == "python" and self.gui_library == "tkinter":
            from . import pythontkinter as backend

            backend.display_window(self.root)
        elif self.programming_language == "web" and self.gui_library == "html":
            from . import webhtml as backend

            backend.display_window(self.root)
        else:
            print(
                f"Display not implemented for {self.programming_language} and {self.gui_library}."
            )


class Widget:
    """
    Widget holds individual widget data:
    - uid: A unique identifier (int).
    - name: Widget name (str, e.g., for python: widget name; for web: widget identifier).
    - root: The GUI root object (tk.Tk() instance for tkinter or HTML document string for web).
    - parent: The uid of the parent widget (None if top-level).
    - code: The widget code in HTML or Python as a string.
    """

    uid_counter = 1

    def __init__(self, name, code, parent=None, root=None):
        self.uid = Widget.uid_counter
        Widget.uid_counter += 1

        self.name = name
        self.code = code
        self.parent = parent
        self.root = root  # Tkinter's root or HTML container

    def render(self):
        # For now, simply print the widget details.
        print(f"Rendering widget {self.name} (UID: {self.uid})")
        print(self.code)


# Library-level globals and functions
global_gui = {
    "programming_language": None,
    "gui_library": None,
}


def setgui(language, gui):
    """
    Set the global GUI configuration.
    - language: 'python' or 'web'
    - gui: 'tkinter' (for python) or 'html' (for web)
    """
    supported_languages = ["python", "web"]
    supported_gui = ["tkinter", "html"]

    if language not in supported_languages:
        raise ValueError(
            "Unsupported programming language. Supported: "
            + ", ".join(supported_languages)
        )
    if gui not in supported_gui:
        raise ValueError(
            "Unsupported GUI library. Supported: " + ", ".join(supported_gui)
        )

    # Enforce matching pairs.
    if language == "python" and gui != "tkinter":
        raise ValueError("For 'python', the supported GUI library is 'tkinter'.")
    if language == "web" and gui != "html":
        raise ValueError("For 'web', the supported GUI library is 'html'.")

    global_gui["programming_language"] = language
    global_gui["gui_library"] = gui
    return (language, gui)


def create_window(name, layout=None):
    """
    Create a GlobalWindow instance with the given name and an optional layout.
    'layout' should be a list of widget definitions (dict with keys 'name' and 'code').
    """
    win = GlobalWindow(
        name,
        programming_language=global_gui["programming_language"],
        gui_library=global_gui["gui_library"],
    )
    if layout:
        for widget_def in layout:#TODO New Logic
            widget = Widget(
                widget_def.get("name", "Unnamed"),
                widget_def.get("code", ""),
                parent=None,
                root=win.root,
            )
            win.add_widget(widget)
    return win


# Expose the API
__all__ = ["setgui", "create_window", "GlobalWindow", "Widget"]
