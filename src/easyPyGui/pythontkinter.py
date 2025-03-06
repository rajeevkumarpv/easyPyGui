import tkinter as tk


def init_window(name: str):
    """
    Initialize a tkinter window for Python.
    (python, tkinter)
    :param name: Window title.
    :return: tk.Tk instance.
    """
    root = tk.Tk()
    root.title(name)
    return root


def display_window(root):
    """
    Display the tkinter window.
    (python, tkinter)
    :param root: The tkinter root instance.
    """
    root.mainloop()


def create_widget(widget_def: dict, root):
    """
    Create a tkinter widget.
    (python, tkinter)
    widget_def should be a dictionary with keys 'name' and 'code'.
    'code' is expected to be a valid tkinter widget constructor string.
    :param widget_def: Dictionary containing widget definition.
    :param root: The tkinter root instance.
    :return: A tkinter widget instance.
    """
    try:
        # Warning: using eval can be dangerous; in production, consider a safer parser.
        widget = eval(widget_def["code"], {"tk": tk, "root": root})
        return widget
    except Exception as e:
        print("Error creating widget:", e)
        return None
