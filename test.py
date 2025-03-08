from src import easyPyGui as es
import tkinter as tk
import config as gv

import csv
import config as gv

# Example usage (if needed)
if __name__ == "__main__":
    # Create a window layout with a mix of widgets
    layout = [
        [
            es.Label("This is a label", key="lbl1"),
            es.Button("Click me", key="btn1"),
            es.Slider(0, 100, key="slider1"),
        ],
        [
            es.TextField("Default text", key="txt1"),
            es.ComboBox(["Option 1", "Option 2"], key="cmb1"),
            es.ProgressBar(key="pbar1", mode="determinate", maximum=100),
        ],
        [
            es.Frame(
                "Frame Title", key="frm1", layout=[[es.Label("Inside frame", key="lbl2")]]
            )
        ],
    ]
    win = es.Window("My App", layout=layout, size=(400, 300), hidden=False)
    # win.show()
    for row in (gv.TABLE_WIDGETS):
        print(row,gv.TABLE_WIDGETS[row],'\n\n')
    tk.mainloop()
