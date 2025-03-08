from src import easyPyGui as es
import tkinter as tk
import config as gv

radio1 = [
    [
        es.RadioButton(
            options={
                "RadioButton 1": "1",
                "RadioButton 2": "2",
                "RadioButton 3": "3",
                "RadioButton 4": "4",
                "RadioButton 5": "5",
            },
            key="radio1",
        ),
    ],
    [
        es.Button("btn", key="btn2"),
        es.Button("btn2", key="btn3"),
    ],
]
layout1 = [
    [
        es.Label("l1", anchor=tk.CENTER),
        es.TextField("text1", font=("calibre", 10, "bold")),
    ],
        [es.Frame("options","options", layout=radio1)],
        [
            es.Button("Click Me", key="btn1"),
        ],
]
mainwindow = es.Window(title="SimpleCalculator", layout=layout1)
# mainwindow.show()
while True:
    #     event, values = mainwindow.read_window(seconds=0.01)
    #     if event is not None:
    #         if event == "btn1":
    #             print(mainwindow.get("radio1"))
    #         if event == "radio1":
    #             print(f"Radio Pressed: {values.get(event)}")
    #         if event == "widget_5":
    #             print(f"Text: {values.get(event)}")
    """"""

# # consider using pack for widgets in single row or column (by len widgets in row may be) and grid to scrollable items such as lsitbox,textarea.
