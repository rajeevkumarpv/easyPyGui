from src import easyPyGui as es
import tkinter as tk


def btn():
    print("Button Clicked")


layout1 = [
    es.Label("l1", anchor=tk.CENTER),  # check no two labels are same
    es.TextField("text1", font=("calibre", 10, "bold")),
    es.Button("Click Me", key="btn1", command=btn),
    es.RadioButton(
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
    es.TextArea("text box 1"),
]
layout2 = [
    es.Label("l2", anchor=tk.CENTER),  # check no two labels are same
    es.TextField("text2"),
    # es.TextArea("text box 2"),
    es.CheckBox("Accept Terms", checked=True, key="chk1"),
    es.ListBox(["Item 1", "Item 2", "Item 3"], key="list1", selectmode=tk.SINGLE),
]
mainwindow = es.Window(title="SimpleCalculator", layout=layout1)
anotherwindow = es.Window(title="ScientificCalculator", layout=layout2)
mainwindow.show()
anotherwindow.show()
tk.mainloop()
