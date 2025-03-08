import tkinter as tk
from tkinter import ttk
import config as gv

# Updated widget type mapping with additional items.
widget_types = {
    "Label": 1,
    "Button": 2,
    "TextField": 3,
    "TextArea": 4,
    "ListBox": 5,
    "Radio": 6,
    "CheckBox": 7,
    "Frame": 8,
    "Slider": 9,
    "ComboBox": 10,
    "ProgressBar": 11,
    "TreeView": 12,
}

# Store in tables using widget_uid as the primary key
gv.TABLE_WINDOWS = {}
gv.TABLE_WIDGETS = {}
gv.TABLE_FRAMES = {}


class Widget:
    """
    A class representing a UI widget in the EasyPyGui framework.
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
        Widget._uid_counter += 1
        self.widget_uid = Widget._uid_counter

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
        self.extra_arguments = kwargs
        self.parent_root = None  # Window or frame container
        self.root = None  # Tkinter widget instance
        self.in_frame = False
        self.values = []  # Dynamic values for widget
        self.event = None  # Event placeholder
        self.value = None  # Event-generated value

        gv.TABLE_WIDGETS[self.widget_uid] = {
            "widget_self": self,  # widget itself, for purposes like variable values
            "widget_uid": self.widget_uid,
            "key": self.key,
            "parent_root": self.parent_root,
            "self_root": self.parent_root,
            "widget_type": self.widget_type,
            "in_frame": self.in_frame,
            "row": self.row,
            "column": self.column,
            "sticky": self.sticky,
            "extra_arguments": self.extra_arguments,  # not updated to table
            "event": self.event,
            "value": self.value,
        }

    def __repr__(self):
        return (
            f"Widget({self.widget_uid}, {self.key}, {self.widget_type}, "
            f"row={self.row}, column={self.column}, sticky={self.sticky}, extra={self.extra_arguments})"
        )


class Window:
    """
    A class representing a window in the EasyPyGui framework.
    """

    _uid_counter = 1
    _root_instance = None

    def __init__(
        self, title, layout=None, size=(300, 300), resizable=(True, True), hidden=True
    ):
        self.title = title
        self.window_uid = Window._uid_counter
        Window._uid_counter += 1

        if Window._root_instance is None:
            self.root = tk.Tk()
            Window._root_instance = self.root
        else:
            self.root = tk.Toplevel(Window._root_instance)

        self.hidden = hidden
        self.child_widget_uids = []
        self.layout = layout if layout else []
        self.grid_rows = len(layout)
        self.grid_cols = 0

        # Initialize event storage for widget and window events.
        self.last_event = None

        # Store last window state and size for detecting changes.
        self._last_window_state = self.root.state()
        self._last_size = (self.root.winfo_width(), self.root.winfo_height())

        # Bind window-level events.
        self.root.bind("<Configure>", self._on_configure)
        self.root.protocol("WM_DELETE_WINDOW", self._on_exit)

        # Populate tables and assign layout
        self.init_layout(layout=layout)
        self.root.geometry(f"{size[0]}x{size[1]}")
        self.root.title(self.title)
        self.root.resizable(resizable[0], resizable[1])
        self.create_widget(layout=layout, parent_root=self.root, row_no=0, cols_no=0)

    def init_layout(self, layout, parent="window"):
        child_uids = []
        for row in layout:
            cols = 0
            for col in row:
                if col.widget_type == widget_types["Frame"]:
                    frame_child_uids = self.init_layout(
                        col.extra_arguments["layout"], parent="frame"
                    )
                    gv.TABLE_FRAMES[self.window_uid] = {
                        "key": col.key,
                        "frame_uid": col.widget_uid,
                        "title": self.title,
                        "window_uid": self.window_uid,
                        "child_widgets_uids": frame_child_uids,
                    }
                    child_uids.append(col.widget_uid)
                else:
                    cols += 1
                    if cols > self.grid_cols:
                        self.grid_cols = cols
                    child_uids.append(col.widget_uid)
        if parent != "window":
            return child_uids
        gv.TABLE_WINDOWS[self.window_uid] = {
            "window_self": self,
            "title": self.title,
            "window_root": self.root,
            "window_uid": self.window_uid,
            "child_widgets_uids": child_uids,
        }
        # Assign geometry to widgets
        row_no = 0
        for row in layout:
            cols_no = 0
            for col in row:
                if col.widget_type == widget_types["Frame"]:
                    for widget_row in col.extra_arguments["layout"]:
                        for widget in widget_row:
                            widget.row = row_no
                            widget.column = cols_no
                else:
                    col.row = row_no
                    col.column = cols_no
                cols_no += 1
            row_no += 1

    def create_widget(self, layout, parent_root, row_no, cols_no):
        for row in layout:
            _cols_no = cols_no
            for col in row:
                if col.widget_type == widget_types["Frame"]:
                    frame = ttk.Frame(parent_root)
                    frame.grid(column=_cols_no, row=row_no)
                    self.create_widget(
                        col.extra_arguments["layout"], frame, row_no, cols_no
                    )
                else:
                    gv.TABLE_WIDGETS[col.widget_uid]["parent_root"] = parent_root

                    # Create widget based on its type with event binding.
                    if col.widget_type == widget_types["Label"]:
                        widget_instance = ttk.Label(parent_root, **col.extra_arguments)
                        widget_instance.bind(
                            "<Button-1>", lambda e, key=col.key: self._handle_event(key)
                        )
                    elif col.widget_type == widget_types["Button"]:
                        if "command" not in col.extra_arguments:
                            widget_instance = ttk.Button(
                                parent_root,
                                text=col.extra_arguments.get("text", ""),
                                command=lambda key=col.key: self._handle_event(key),
                            )
                        else:
                            orig_cmd = col.extra_arguments["command"]
                            widget_instance = ttk.Button(
                                parent_root,
                                text=col.extra_arguments.get("text", ""),
                                command=lambda key=col.key, orig=orig_cmd: (
                                    orig(),
                                    self._handle_event(key),
                                ),
                            )
                    elif col.widget_type == widget_types["TextField"]:
                        widget_instance = ttk.Entry(parent_root, **col.extra_arguments)
                        widget_instance.bind(
                            "<KeyRelease>",
                            lambda e, key=col.key: self._handle_event(key),
                        )
                    elif col.widget_type == widget_types["TextArea"]:
                        widget_instance = tk.Text(parent_root, **col.extra_arguments)
                        widget_instance.bind(
                            "<KeyRelease>",
                            lambda e, key=col.key: self._handle_event(key),
                        )
                    elif col.widget_type == widget_types["ListBox"]:
                        widget_instance = tk.Listbox(parent_root, **col.extra_arguments)
                        widget_instance.bind(
                            "<<ListboxSelect>>",
                            lambda e, key=col.key: self._handle_event(key),
                        )
                    elif col.widget_type == widget_types["Radio"]:
                        var = tk.StringVar()
                        var.trace(
                            "w", lambda *args, key=col.key: self._handle_event(key)
                        )
                        options = col.extra_arguments.get("options", [])
                        for idx, option in enumerate(options):
                            rb = ttk.Radiobutton(
                                parent_root, text=option, variable=var, value=option
                            )
                            rb.grid(column=_cols_no, row=row_no + idx)
                        widget_instance = rb
                    elif col.widget_type == widget_types["CheckBox"]:
                        if "command" not in col.extra_arguments:
                            widget_instance = ttk.Checkbutton(
                                parent_root,
                                **col.extra_arguments,
                                command=lambda key=col.key: self._handle_event(key),
                            )
                        else:
                            orig_cmd = col.extra_arguments["command"]
                            widget_instance = ttk.Checkbutton(
                                parent_root,
                                **col.extra_arguments,
                                command=lambda key=col.key, orig=orig_cmd: (
                                    orig(),
                                    self._handle_event(key),
                                ),
                            )
                    elif col.widget_type == widget_types["Slider"]:
                        if "command" not in col.extra_arguments:
                            widget_instance = tk.Scale(
                                parent_root,
                                **col.extra_arguments,
                                command=lambda val, key=col.key: self._handle_event(
                                    key
                                ),
                            )
                        else:
                            orig_cmd = col.extra_arguments["command"]
                            widget_instance = tk.Scale(
                                parent_root,
                                **col.extra_arguments,
                                command=lambda val, key=col.key, orig=orig_cmd: (
                                    orig(val),
                                    self._handle_event(key),
                                ),
                            )
                    elif col.widget_type == widget_types["ComboBox"]:
                        widget_instance = ttk.Combobox(
                            parent_root, **col.extra_arguments
                        )
                        widget_instance.bind(
                            "<<ComboboxSelected>>",
                            lambda e, key=col.key: self._handle_event(key),
                        )
                    elif col.widget_type == widget_types["ProgressBar"]:
                        widget_instance = ttk.Progressbar(
                            parent_root, **col.extra_arguments
                        )
                        widget_instance.bind(
                            "<Button-1>", lambda e, key=col.key: self._handle_event(key)
                        )
                    elif col.widget_type == widget_types["TreeView"]:
                        widget_instance = ttk.Treeview(
                            parent_root, **col.extra_arguments
                        )
                        widget_instance.bind(
                            "<<TreeviewSelect>>",
                            lambda e, key=col.key: self._handle_event(key),
                        )
                    else:
                        widget_instance = ttk.Label(parent_root, text="Unknown Widget")
                    widget_instance.grid(column=_cols_no, row=row_no)
                    gv.TABLE_WIDGETS[col.widget_uid]["self_root"] = widget_instance
                    gv.TABLE_WIDGETS[col.widget_uid]["row"] = row_no
                    gv.TABLE_WIDGETS[col.widget_uid]["column"] = _cols_no
                _cols_no += 1
            row_no += 1

    def _handle_event(self, key):
        """
        Internal handler to capture widget events.
        Every interactive widget calls this on user interaction.
        """
        self.last_event = key

    def _on_configure(self, event):
        """
        Handle window-level events such as resize, minimize, maximize/restore.
        This method is bound to the <Configure> event of the window.
        """
        # Check for size changes.
        current_size = (event.width, event.height)
        if current_size != self._last_size:
            self._last_size = current_size
            self.last_event = "--Resize--"

        # Check for state changes (minimized, maximized, normal).
        new_state = self.root.state()
        if new_state != self._last_window_state:
            self._last_window_state = new_state
            if new_state == "iconic":
                self.last_event = "--Minimize--"
            elif new_state == "zoomed":
                self.last_event = "--Maximize--"
            elif new_state == "normal":
                # When restoring from minimized/maximized state.
                self.last_event = "--Restore--"

    def _on_exit(self):
        """
        Handle window exit (clicking the close button).
        """
        self.last_event = "--Exit--"
        self.root.destroy()

    def read_events(self, seconds=0):
        try:
            self.root.update_idletasks()
            self.root.update()
        except tk.TclError:
            return None, {}

        event = self.last_event
        self.last_event = None

        values = {}
        for widget_uid, widget_data in gv.TABLE_WIDGETS.items():
            key = widget_data.get("key")
            widget_instance = widget_data.get("self_root")
            if widget_instance is None:
                continue

            try:
                wtype = widget_data.get("widget_type")
                if wtype == widget_types["TextField"]:
                    values[key] = widget_instance.get()
                elif wtype == widget_types["TextArea"]:
                    values[key] = widget_instance.get("1.0", tk.END).strip()
                elif wtype == widget_types["ComboBox"]:
                    current = widget_instance.get()
                    options = widget_instance.cget("values")
                    try:
                        values[key] = options.index(current)
                    except ValueError:
                        values[key] = None
                elif wtype == widget_types["Slider"]:
                    values[key] = widget_instance.get()
                elif wtype == widget_types["ListBox"]:
                    selection = widget_instance.curselection()
                    values[key] = selection
                elif wtype in (widget_types["CheckBox"], widget_types["Radio"]):
                    values[key] = None  # Extend as needed.
                elif wtype == widget_types["TreeView"]:
                    values[key] = widget_instance.selection()
                else:
                    values[key] = ""
            except tk.TclError:
                # Widget has likely been destroyed; handle gracefully.
                values[key] = None

        return event, values

    def Update(self, key, value):
        """
        Update the widget identified by 'key' with the given 'value'.
        Currently supports TextField and TextArea.
        """
        for widget_uid, widget_data in gv.TABLE_WIDGETS.items():
            if widget_data.get("key") == key:
                widget_instance = widget_data.get("self_root")
                if widget_instance is None:
                    break
                if widget_data.get("widget_type") == widget_types["TextField"]:
                    widget_instance.delete(0, tk.END)
                    widget_instance.insert(0, value)
                elif widget_data.get("widget_type") == widget_types["TextArea"]:
                    widget_instance.delete("1.0", tk.END)
                    widget_instance.insert("1.0", value)
                break

    def set(self, key, value):
        """
        Alias for Update. Allows external code to set widget values.
        """
        self.Update(key, value)

    def get(self, key):
        """
        Retrieve the widget content or configuration based on its type.
        For TextField/TextArea it returns the current text.
        For ComboBox it returns the list of options.
        For Slider it returns its current value.
        """
        for widget_uid, widget_data in gv.TABLE_WIDGETS.items():
            if widget_data.get("key") == key:
                widget_instance = widget_data.get("self_root")
                if widget_instance is None:
                    break
                wtype = widget_data.get("widget_type")
                if wtype == widget_types["TextField"]:
                    return widget_instance.get()
                elif wtype == widget_types["TextArea"]:
                    return widget_instance.get("1.0", tk.END).strip()
                elif wtype == widget_types["ComboBox"]:
                    return widget_instance.cget("values")
                elif wtype == widget_types["Slider"]:
                    return widget_instance.get()
        return None

    def show(self):
        self.root.deiconify()
        self.hidden = False


# Existing widget factory functions.
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
    child_widgets = []
    for widget in kwargs["layout"]:
        widget = widget[0]  # NOTE: nested frames
        widget.in_frame = True
        widget_uid = widget.widget_uid
        gv.TABLE_WIDGETS[widget_uid]["in_frame"] = True
        child_widgets.append(widget_uid)
    if text is not None:
        return Widget("Frame", key=key, text=text, **kwargs)
    else:
        return Widget("Frame", key=key, **kwargs)


def Slider(from_, to, orient="horizontal", key=None, **kwargs):
    """
    Create a slider (scale) widget.
    """
    return Widget("Slider", key=key, from_=from_, to=to, orient=orient, **kwargs)


def ComboBox(values, key=None, **kwargs):
    """
    Create a combo box widget.
    """
    return Widget("ComboBox", key=key, values=values, **kwargs)


def ProgressBar(key=None, **kwargs):
    """
    Create a progress bar widget.
    """
    return Widget("ProgressBar", key=key, **kwargs)


def TreeView(key=None, **kwargs):
    """
    Create a tree view widget.
    """
    return Widget("TreeView", key=key, **kwargs)
