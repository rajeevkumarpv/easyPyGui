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
            es.Label("This is a label", key="lbl1",sticky='N'),
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
    # tk.mainloop()#use update
    while True:
        events,values=win.read_events(seconds=0.06)#milliseconds to wait
        if events == None:
            continue
        if events=='--Exit--':#do not destroy automatically
            win.hide() #hides window
            win.show() #shows window
            win.unload()#destroy window even if its root level
            break;
        if events=='btn1':
            print(f"text entered{values['txt1']}")#values contain all values for all widgets in dict 
            win.set('txt1','')
        if events=='cmb1':
            selection=values['cmb1']
            print(f'Selected {win.get('cmb1')[selection]}')
        print(events)
