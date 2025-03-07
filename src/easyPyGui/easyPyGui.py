import tkinter as tk


class Widget:
    """
    A class representing a generic GUI widget.

    Attributes:
        uid (int): Unique identifier for each widget.
        key (str): A unique key for quick access.
        root_widget (tk.Widget): The actual tkinter widget instance.
        parent_name (str): The name of the parent window or frame.
        child_widgets (list): A list to store child widgets if the widget is a container.
    """

    _uid_counter = 1  # Class-level counter to assign unique IDs

    def __init__(self, widget_type, key=None, **kwargs):
        """
        Initializes a new Widget instance.

        Args:
            widget_type (str): The type of tkinter widget (e.g., "Label", "Button").
            key (str): A unique key for the widget.
            **kwargs: Additional arguments needed for widget creation.
        """
        self.uid = Widget._uid_counter
        Widget._uid_counter += 1

        self.type = widget_type
        self.args = kwargs
        self.key = key if key else f"widget_{self.uid}"
        self.parent_name = ""
        self.child_widgets = []  # For container widgets that hold child widgets
        self.root_widget = None  # Will later hold the actual tkinter widget instance


class Window:
    """
    Class representing a GUI window using tkinter.

    Attributes:
        title (str): The title of the window.
        uid (int): Unique identifier for the window.
        root (tk.Tk or tk.Toplevel): The main tkinter window or a child window.
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
        self.root.protocol("WM_DELETE_WINDOW", self.hide)

    def _initialize_layout(self):
        """Create and pack widgets based on the given layout."""
        for wg in self.layout:
            if wg.type == "Label":
                if "text" not in wg.args:
                    raise ValueError("Label widget must have a 'text' argument")
                text_value = wg.args.pop("text")
                wg.root_variable = tk.StringVar()
                wg.root_variable.set(text_value)
                wg.root_widget = tk.Label(
                    self.root,
                    textvariable=wg.root_variable,
                    **(wg.args if wg.args else {}),
                )
                wg.root_widget.pack()
                self.child_widgets.append([wg.uid, wg.root_widget, wg.root_variable])

            elif wg.type == "TextField":
                if "text" not in wg.args:
                    raise ValueError("TextField widget must have a 'text' argument")
                text_value = wg.args.pop("text")
                wg.root_variable = tk.StringVar()
                wg.root_variable.set(text_value)
                wg.root_widget = tk.Entry(
                    self.root,
                    textvariable=wg.root_variable,
                    **(wg.args if wg.args else {}),
                )
                wg.root_widget.pack()
                self.child_widgets.append([wg.uid, wg.root_widget, wg.root_variable])

            elif wg.type == "TextArea":
                if "text" not in wg.args:
                    raise ValueError("TextArea widget must have a 'text' argument")
                text_value = wg.args.pop("text")
                wg.root_widget = tk.Text(self.root, **(wg.args if wg.args else {}))
                wg.root_widget.insert(tk.INSERT, text_value)
                wg.root_widget.pack()
                self.child_widgets.append([wg.uid, wg.root_widget, None])

            elif wg.type == "Button":
                if "text" not in wg.args:
                    raise ValueError("Button widget must have a 'text' argument")
                if "command" not in wg.args:
                    raise ValueError("Button widget must have a 'command' argument")
                text_value = wg.args.pop("text")
                wg.root_widget = tk.Button(
                    self.root, text=text_value, **(wg.args if wg.args else {})
                )
                wg.root_widget.pack()
                self.child_widgets.append([wg.uid, wg.root_widget,None])

            elif wg.type == "CheckBox":
                if "text" not in wg.args:
                    raise ValueError("CheckBox widget must have a 'text' argument")
                text_value = wg.args.pop("text")
                wg.root_variable = tk.BooleanVar()
                checked = wg.args.pop("checked", False)
                wg.root_variable.set(checked)
                wg.root_widget = tk.Checkbutton(
                    self.root,
                    text=text_value,
                    variable=wg.root_variable,
                    **(wg.args if wg.args else {}),
                )
                wg.root_widget.pack()
                self.child_widgets.append([wg.uid, wg.root_widget, wg.root_variable])

            elif wg.type == "RadioButton":
                if "options" not in wg.args:
                    raise ValueError(
                        "RadioButton widget must have an 'options' argument"
                    )
                options = wg.args.pop("options")
                # Optional: use 'group' if provided (for logical grouping)
                group = wg.args.pop("group", None)
                wg.root_variable = tk.StringVar()
                # Set default value to the first option
                first_value = next(iter(options.values()))
                wg.root_variable.set(first_value)
                # Create a container frame to hold radio buttons
                frame = tk.Frame(self.root)
                frame.pack()
                wg.radio_buttons = []
                for label, value in options.items():
                    rb = tk.Radiobutton(
                        frame,
                        text=label,
                        variable=wg.root_variable,
                        value=value,
                        **(wg.args if wg.args else {}),
                    )
                    rb.pack(anchor=tk.W)
                    wg.radio_buttons.append(rb)
                wg.root_widget = frame
                self.child_widgets.append(
                    [wg.uid, wg.root_widget, wg.root_variable, wg.radio_buttons]
                )

            elif wg.type == "ListBox":
                if "items" not in wg.args:
                    raise ValueError("ListBox widget must have an 'items' argument")
                items = wg.args.pop("items")
                wg.root_widget = tk.Listbox(self.root, **(wg.args if wg.args else {}))
                for item in items:
                    wg.root_widget.insert(tk.END, item)
                wg.root_widget.pack()
                self.child_widgets.append([wg.uid, wg.root_widget])

            # Debug print for widget type and key
            print(wg.type, wg.key)

    def hide(self):
        self.hidden = True
        self.root.withdraw()

    def show(self):
        """Show the window and start the tkinter main loop."""
        if self.hidden:
            self.root.deiconify()
            self.hidden = False
        # Uncomment the following line if you want the main loop to run here:
        # self.root.mainloop()


# Factory functions for creating widgets
def Label(text, key=None, **kwargs):
    return Widget("Label", key=key, text=text, **kwargs)


def TextField(default_text, key=None, **kwargs):
    return Widget("TextField", key=key, text=default_text, **kwargs)


def TextArea(default_text, key=None, size=(100, 100), **kwargs):
    return Widget(
        "TextArea", key=key, text=default_text, width=size[0], height=size[1], **kwargs
    )


def Button(text, key=None, **kwargs):
    return Widget("Button", key=key, text=text, **kwargs)


def CheckBox(text, checked=False, key=None, **kwargs):
    return Widget("CheckBox", key=key, text=text, checked=checked, **kwargs)


def RadioButton(options, key=None, group=None, **kwargs):
    if group:
        kwargs["group"] = group
    return Widget("RadioButton", key=key, options=options, **kwargs)


def ListBox(items, key=None, **kwargs):
    return Widget("ListBox", key=key, items=items, **kwargs)


# Example usage: creating a layout with the new widget types.
layout1 = [
    Label("Label 1", anchor=tk.CENTER),  # Unique label text
    TextField("Sample text", font=("calibre", 10, "bold")),
    TextArea("This is a text area"),
    Button("Click Me", key="btn1", command=lambda: print("Button Clicked")),
    RadioButton(
        options={
            "RadioButton 1": "1",
            "RadioButton 2": "2",
            "RadioButton 3": "3",
            "RadioButton 4": "4",
            "RadioButton 5": "5",
        },
        key="radio1",
        group="group1",
    ),
    CheckBox("Accept Terms", checked=True, key="chk1"),
    ListBox(["Item 1", "Item 2", "Item 3"], key="list1", selectmode=tk.SINGLE),
]

# Create the window and show it
# win = Window("My GUI Window", layout=layout1, hidden=False)
# win.root.mainloop()
