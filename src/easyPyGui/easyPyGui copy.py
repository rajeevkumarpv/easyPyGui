import tkinter as tk
import time


class Widget:
    _uid_counter = 1

    def __init__(self, widget_type, key=None, **kwargs):
        self.uid = Widget._uid_counter
        Widget._uid_counter += 1

        self.type = widget_type
        self.args = kwargs
        # If no key is provided and a "text" argument exists, use it as key.
        if key is None and "text" in kwargs:
            self.key = kwargs["text"]
        elif key:
            self.key = key
        else:
            self.key = f"widget_{self.uid}"
        self.child_widgets = []  # For container widgets.
        self.root_widget = None  # The actual tkinter widget.
        self.root_variable = None  # For variable-based widgets.
        self.event_trigger = None  # For event signaling.


class Window:
    _uid_counter = 1
    _root_instance = None

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
        self._initialize_layout(self.root, self.layout)

        # Ensure all widget keys are unique.
        widget_keys = [w.key for w in self.child_widgets]
        if len(widget_keys) != len(set(widget_keys)):
            raise ValueError(
                "Duplicate widget keys detected. Ensure all widget keys are unique."
            )

        self.root.protocol("WM_DELETE_WINDOW", self.hide)

    def _initialize_layout(self, parent, layout):
        """
        Initialize layout in the given parent container.
        If layout is a nested list, treat each inner list as a row.
        """
        # If layout is nested (i.e. rows)
        if layout and isinstance(layout[0], list):
            for row in layout:
                # Create a frame for the row.
                row_frame = tk.Frame(parent)
                row_frame.pack(fill=tk.X, padx=5, pady=5)
                # Decide layout based on the number of widgets in the row.
                if len(row) == 1:
                    # Single widget row: pack to fill horizontally.
                    for wg in row:
                        self._create_widget(wg, row_frame)
                        if wg.type not in ("RadioButton", "ListBox", "TextArea"):
                            wg.root_widget.pack(fill=tk.X, padx=5, pady=5)
                        else:
                            # For scrollable items, grid might be more appropriate.
                            wg.root_widget.grid(row=0, column=0, padx=5, pady=5)
                else:
                    # Multiple widgets in a row: pack side by side.
                    for wg in row:
                        self._create_widget(wg, row_frame)
                        if wg.type not in ("RadioButton", "ListBox", "TextArea"):
                            wg.root_widget.pack(side=tk.LEFT, padx=5, pady=5)
                        else:
                            wg.root_widget.grid(
                                row=0, column=row.index(wg), padx=5, pady=5
                            )
        else:
            # Flat layout: each widget gets its own row.
            for wg in layout:
                self._create_widget(wg, parent)
                if wg.type not in ("RadioButton", "ListBox", "TextArea"):
                    wg.root_widget.pack(fill=tk.X, padx=5, pady=5)
                else:
                    wg.root_widget.grid(row=0, column=0, padx=5, pady=5)

    def _create_widget(self, wg, parent):
        """Helper to create a widget in the given parent container."""
        if wg.type == "Label":
            if "text" not in wg.args:
                raise ValueError("Label widget must have a 'text' argument")
            text_value = wg.args.pop("text")
            wg.root_variable = tk.StringVar(value=text_value)
            wg.root_widget = tk.Label(parent, textvariable=wg.root_variable, **wg.args)
            self.child_widgets.append(wg)

        elif wg.type == "TextField":
            if "text" not in wg.args:
                raise ValueError("TextField widget must have a 'text' argument")
            text_value = wg.args.pop("text")
            wg.root_variable = tk.StringVar(value=text_value)

            def on_text_change(*args, widget=wg):
                widget.event_trigger = "text_changed"

            wg.root_variable.trace("w", on_text_change)
            wg.root_widget = tk.Entry(parent, textvariable=wg.root_variable, **wg.args)
            self.child_widgets.append(wg)

        elif wg.type == "TextArea":
            if "text" not in wg.args:
                raise ValueError("TextArea widget must have a 'text' argument")
            text_value = wg.args.pop("text")
            wg.root_widget = tk.Text(parent, **wg.args)
            wg.root_widget.insert(tk.INSERT, text_value)

            def on_textarea_change(event, widget=wg):
                widget.event_trigger = "text_area_changed"

            wg.root_widget.bind("<KeyRelease>", on_textarea_change)
            self.child_widgets.append(wg)

        elif wg.type == "Button":
            if "text" not in wg.args:
                raise ValueError("Button widget must have a 'text' argument")
            text_value = wg.args.pop("text")
            original_command = wg.args.pop("command", None)

            def wrapped_command(widget=wg, cmd=original_command):
                widget.event_trigger = "button_clicked"
                if cmd:
                    cmd()

            wg.root_widget = tk.Button(
                parent, text=text_value, command=wrapped_command, **wg.args
            )
            self.child_widgets.append(wg)

        elif wg.type == "CheckBox":
            if "text" not in wg.args:
                raise ValueError("CheckBox widget must have a 'text' argument")
            text_value = wg.args.pop("text")
            wg.root_variable = tk.BooleanVar(value=wg.args.pop("checked", False))

            def on_check_change(*args, widget=wg):
                widget.event_trigger = "checkbox_toggled"

            wg.root_variable.trace("w", on_check_change)
            wg.root_widget = tk.Checkbutton(
                parent, text=text_value, variable=wg.root_variable, **wg.args
            )
            self.child_widgets.append(wg)

        elif wg.type == "RadioButton":
            if "options" not in wg.args:
                raise ValueError("RadioButton widget must have an 'options' argument")
            options = wg.args.pop("options")
            wg.root_variable = tk.StringVar()
            first_value = next(iter(options.values()))
            wg.root_variable.set(first_value)

            def on_radio_change(*args, widget=wg):
                widget.event_trigger = "radio_changed"

            wg.root_variable.trace("w", on_radio_change)
            frame = tk.Frame(parent)
            wg.radio_buttons = []
            for label, value in options.items():
                rb = tk.Radiobutton(
                    frame, text=label, variable=wg.root_variable, value=value, **wg.args
                )
                rb.pack(anchor=tk.W)
                wg.radio_buttons.append(rb)
            wg.root_widget = frame
            self.child_widgets.append(wg)

        elif wg.type == "ListBox":
            if "items" not in wg.args:
                raise ValueError("ListBox widget must have an 'items' argument")
            items = wg.args.pop("items")
            wg.root_widget = tk.Listbox(parent, **wg.args)
            for item in items:
                wg.root_widget.insert(tk.END, item)

            def on_listbox_select(event, widget=wg):
                widget.event_trigger = "listbox_selection_changed"

            wg.root_widget.bind("<<ListboxSelect>>", on_listbox_select)
            self.child_widgets.append(wg)

        elif wg.type == "Frame":
            # Remove the nested layout from kwargs so it doesn't get passed to tk.Frame
            nested_layout = wg.args.pop("values", None)
            # Create a LabelFrame if a "text" is provided, else a plain Frame.
            if "text" in wg.args:
                text_value = wg.args.pop("text")
                wg.root_widget = tk.LabelFrame(parent, text=text_value, **wg.args)
            else:
                wg.root_widget = tk.Frame(parent, **wg.args)
            # Add the frame widget to the list of child widgets.
            self.child_widgets.append(wg)
            # Process the nested layout if provided.
            # if nested_layout is not None:
            #     # This call creates a new layout context: widgets in the nested_layout will
            #     # be added as children of this frame (wg.root_widget) rather than the main window.
            #     self._initialize_layout(wg.root_widget, nested_layout)
        print(f"Created {wg.type} with key: {wg.key}")

    def hide(self):
        self.hidden = True
        self.root.withdraw()

    def show(self):
        if self.hidden:
            self.root.deiconify()
            self.hidden = False

    def poll_events(self):
        events = []
        for widget in self.child_widgets:
            if widget.event_trigger:
                event_info = {"widget_key": widget.key, "event": widget.event_trigger}
                if widget.root_variable:
                    event_info["value"] = widget.root_variable.get()
                events.append(event_info)
                widget.event_trigger = None
        return events

    def update_window(self):
        try:
            self.root.update_idletasks()
            self.root.update()
        except tk.TclError:
            pass

    def read_window(self, seconds=0.01):
        time.sleep(seconds)
        self.update_window()
        events = self.poll_events()
        event = events[0]["widget_key"] if events else None
        values = {}
        for widget in self.child_widgets:
            if widget.root_variable is not None:
                values[widget.key] = widget.root_variable.get()
            elif widget.type == "TextArea":
                values[widget.key] = widget.root_widget.get("1.0", tk.END).strip()
        return event, values

    def get(self, key):
        for widget in self.child_widgets:
            if widget.key == key:
                if widget.root_variable is not None:
                    return widget.root_variable.get()
                elif widget.type == "TextArea":
                    return widget.root_widget.get("1.0", tk.END).strip()
                else:
                    return None
        return None

    def set(self, key, value):
        for widget in self.child_widgets:
            if widget.key == key:
                if widget.root_variable is not None:
                    widget.root_variable.set(value)
                elif widget.type == "TextArea":
                    widget.root_widget.delete("1.0", tk.END)
                    widget.root_widget.insert(tk.INSERT, value)
                break
        self.update_window()


# Factory functions remain similar.
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


def Frame(text=None, key=None, **kwargs):
    # Use "layout" or "values" to define nested layouts.
    if text is not None:
        return Widget("Frame", key=key, text=text, **kwargs)
    else:
        return Widget("Frame", key=key, **kwargs)
