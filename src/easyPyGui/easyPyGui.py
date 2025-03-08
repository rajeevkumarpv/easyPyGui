import tkinter as tk
import config as gv

widget_types = {
    "Label": 1,
    "Button": 2,
    "TextField": 3,
    "TextArea": 4,
    "ListBox": 5,
    "Radio": 6,
    "CheckBox": 7,
    "Frame": 8,
}

# Store in tables using widget_uid as the primary key
gv.TABLE_WINDOWS = {}
gv.TABLE_WIDGETS = {}
gv.TABLE_FRAMES = {}


class Widget:
    """
    A class representing a UI widget in the EasyPyGui framework.

    Attributes:
        widget_uid (int): Unique identifier for the widget (auto-incremented).
        key (str): A key to reference the widget in the application.
        widget_type (str): The type of the widget (e.g., button, textbox).
        row (int): The grid row position of the widget.
        column (int): The grid column position of the widget.
        sticky (str): Defines how the widget expands (e.g., "N", "E", "S", "W").
        extra_arguments (dict): Additional configuration options for the widget.
        parent_root (object): The parent container (window or frame) of the widget.
        root (object): The widget's root instance in Tkinter.
        values (list): A dynamic list for storing widget-related values.
    """

    _uid_counter = 0  # Internal counter for widget_uid

    def __init__(
        self,
        widget_type=None,
        key=None,
        row: int = 0,
        column: int = 0,
        sticky: str = "N",
        **kwargs,
    ):
        """Initialize a Widget instance with an auto-incremented UID."""
        Widget._uid_counter += 1
        self.widget_uid = Widget._uid_counter

        # Assign key based on provided key or 'text' argument
        if key is None and "text" in kwargs:
            self.key = kwargs["text"]
        elif key:
            self.key = key
        else:
            self.key = f"widget_{self.widget_uid}"

        self.widget_type = widget_types[widget_type]
        self.row = row
        self.column = column
        self.sticky = sticky
        self.extra_arguments = kwargs  # Store additional arguments
        self.parent_root = None  # Window or frame container
        self.root = None  # Widget's root instance
        self.in_frame = False  # check if widget is part of frame
        self.values = []  # Dynamic values
        self.event = None  # Event placeholder
        self.value = None  # Event-generated value (e.g., selected list index)

        # Store the widget in the gv.TABLE_WIDGETS dictionary
        gv.TABLE_WIDGETS[self.widget_uid] = {
            "widget_self": self,
            "widget_uid": self.widget_uid,
            "key": self.key,
            "parent_root": self.parent_root,
            "self_root": self.parent_root,
            "widget_type": self.widget_type,
            "in_frame": self.in_frame,
            "row": self.row,
            "column": self.column,
            "sticky": self.sticky,
            "extra_arguments": self.extra_arguments,
            "event": self.event,
            "value": self.value,
        }

    def __repr__(self):
        """Return a string representation of the Widget instance."""
        return (
            f"Widget({self.widget_uid}, {self.key}, {self.widget_type}, "
            f"row={self.row}, column={self.column}, sticky={self.sticky}, extra={self.extra_arguments})"
        )


class Window:
    """
    A class representing a window in the EasyPyGui framework.

    Attributes:
        uid (int): Unique identifier for the window.
        title (str): The title of the window.
        layout (list): The layout of widgets inside the window.
        size (tuple): The size of the window (width, height).
        hidden (bool): Whether the window is initially hidden.
        root (tk.Tk or tk.Toplevel): The root instance of the window.
        child_widgets (list): A list of widgets contained in the window.
    """

    _uid_counter = 1
    _root_instance = None

    def __init__(self, title, layout=None, size=(100, 100), hidden=True):
        """Initialize a Window instance."""
        self.title = title
        self.window_uid = Window._uid_counter
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

        self.child_widget_uids = []
        self.layout = layout if layout else []
        #populate tables
        self.init_layout(layout=layout)

    def init_layout(self, layout,parent='window'):
        child_uids=[]
        for row in layout:#widget collection
            for col in row:#frame layout or widget
                if col.widget_type == 8: 
                    frame_child_uids=self.init_layout(col.extra_arguments['layout'],parent='frame')
                    gv.TABLE_FRAMES[self.window_uid] = {
                        "key": col.key,
                        "frame_uid": col.widget_uid,
                        "title": self.title,
                        "window_uid": self.window_uid,
                        "child_widgets_uids": frame_child_uids,
                    }
                    child_uids.append(col.widget_uid)
                else:
                    child_uids.append(col.widget_uid)
        if parent!='window':
            return child_uids
        gv.TABLE_WINDOWS[self.window_uid] = {
                    "title": self.title,
                    "window_root": self.root,
                    "window_uid": self.window_uid,
                    "child_widgets_uids": child_uids,
                }



        


def Label(text, key=None, **kwargs):
    return Widget(widget_type="Label", key=key, text=text, **kwargs)


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
    return Widget("Radio", key=key, options=options, **kwargs)


def ListBox(items, key=None, **kwargs):
    return Widget("ListBox", key=key, items=items, **kwargs)


def Frame(text, key, **kwargs):
    # Use "layout" or "values" to define nested layouts.
    child_widgets = []
    for widget in kwargs["layout"]:
        widget = widget[0]  # NOTE nested frames
        widget.in_frame = True
        widget_uid = widget.widget_uid
        gv.TABLE_WIDGETS[widget_uid]["in_frame"] = True

        child_widgets.append(widget_uid)
    # key is used instead of uid
    # gv.TABLE_FRAMES[key] = {
    #     "title": text,
    #     "window_uid": None,
    #     "child_widget_uids": child_widgets,
    # }
    if text is not None:
        return Widget("Frame", key=key, text=text, **kwargs)
    else:
        return Widget("Frame", key=key, **kwargs)
