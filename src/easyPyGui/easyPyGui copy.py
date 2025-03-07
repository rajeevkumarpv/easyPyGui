import tkinter as tk


class Widget:
    """
    A class representing a generic GUI widget.

    Attributes:
        uid (int): Unique identifier for each widget.
        key (str): A unique key for quick access.
        root_widget (tk.Widget): The actual tkinter widget instance.
        parent_name (str): The name of the parent window or frame.
        child_widgets (list): A list to store child widgets if the widget is a container (like a Frame).
    """

    _uid_counter = 1  # Class-level counter to assign unique IDs

    def __init__(self, widget_type, key=None, **kwargs):
        """
        Initializes a new Widget instance.

        Args:
        widget_type (str): The type of tkinter widget (e.g., "label", "button", "frame").
        *args: Additional arguments. By convention, the second argument (if provided)
                is treated as the widget's key.
        """
        self.uid = Widget._uid_counter
        Widget._uid_counter += 1

        self.type = widget_type
        self.args = kwargs
        self.key = key if key else f"widget_{self.uid}"
        self.parent_name = ""
        self.child_widgets = []  # To store child widgets if this widget is a container
        self.root_widget = None  # Will later hold the actual tkinter widget instance


class Window:
    """
    Class representing a GUI window using tkinter.

    Attributes:
        title (str): The title of the window.
        uid (int): Unique identifier for the window.
        root (tk.Tk): The tkinter root instance.
        child_widgets (list): List of child widget instances added to the window.
        hidden (bool): Whether the window is initially hidden.
        layout (list): A list defining the configuration of child widgets.
    """

    _uid_counter = 1  # Class-level UID counter
    _root_instance = None  # Class-level variable to hold the first Tk instance

    def __init__(self, title, layout=None, hidden=True):
        self.title = title
        self.uid = Window._uid_counter
        Window._uid_counter += 1

        if Window._root_instance is None:
            self.root = tk.Tk()
            Window._root_instance = self.root
        else:
            self.root = tk.Toplevel(Window._root_instance)

        self.root.title(self.title)
        self.hidden = hidden
        if self.hidden:
            self.root.withdraw()

        self.child_widgets = []
        self.layout = layout if layout else []
        self._initialize_layout()
        self.root.protocol("WM_DELETE_WINDOW", self.hide)#TODO onclose
    def _initialize_layout(self):
        """Create and pack widgets based on the given layout."""
        for wg in self.layout:
            if wg.type == "Label":
                if "text" not in wg.args:
                    raise ValueError("Label widget must have a 'text' argument")

                text_value = wg.args.pop(
                    "text"
                )  # Remove 'text' from dict,it helps duplicate key problem
                wg.root_variable = tk.StringVar()
                wg.root_variable.set(text_value)

                # Pass remaining args if any
                wg.root_widget = tk.Label(
                    self.root,
                    textvariable=wg.root_variable,
                    **wg.args if wg.args else {},
                )
                wg.root_widget.pack()
                self.child_widgets.append(
                    [wg.uid, wg.root_widget, wg.root_variable]
                )  # Use a list instead of a set
            if wg.type == "TextField":
                if "text" not in wg.args:
                    raise ValueError("Label widget must have a 'text' argument")

                text_value = wg.args.pop(
                    "text"
                )  # Remove 'text' from dict,it helps duplicate key problem
                wg.root_variable = tk.StringVar()
                wg.root_variable.set(text_value)

                # Pass remaining args if any
                wg.root_widget = tk.Entry(
                    self.root,
                    textvariable=wg.root_variable,
                    **wg.args if wg.args else {},
                )
                wg.root_widget.pack()
                self.child_widgets.append(
                    [wg.uid, wg.root_widget, wg.root_variable]
                )  # Use a list instead of a set
            if wg.type == "TextArea":
                if "text" not in wg.args:
                    raise ValueError("Label widget must have a 'text' argument")

                text_value = wg.args.pop(
                    "text"
                )  # Remove 'text' from dict,it helps duplicate key problem
                wg.root_variable = None
                # wg.root_variable.set(text_value)

                # Pass remaining args if any
                wg.root_widget = tk.Text(
                    self.root,
                    **wg.args if wg.args else {},
                )
                wg.root_widget.insert(tk.INSERT,text_value)
                wg.root_widget.pack()
                self.child_widgets.append(
                    [wg.uid, wg.root_widget, wg.root_variable]
                )  # Use a list instead of a set

            print(wg.type, wg.key)
    def hide(self):
        self.hidden = True
        self.root.withdraw()
    def show(self):
        """Show the window and start the tkinter main loop."""
        if self.hidden:
            self.root.deiconify()
            self.hidden = False
        # self.root.mainloop()


def Label(text, key=None, **kwargs):
    return Widget("Label", key=key, text=text, **kwargs)


def TextField(default_text, key=None, **kwargs):
    return Widget("TextField", key=key, text=default_text, **kwargs)


def TextArea(default_text, key=None, size=(100, 100), **kwargs):
    return Widget(
        "TextArea", key=key, text=default_text, width=size[0], height=size[1], **kwargs
    )
