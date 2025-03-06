import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
import easyPyGui.easyPyGui as es

# Set GUI parameters: currently supports 'python' as language and 'tkinter' as gui_library.
print('language,library', es.setgui('python', 'tkinter'))

# Define layout as a list of widget definitions.
layout = [
    {'name': 'LabelWidget', 'code': 'tk.Label(root, text="Hello World!")'},
    {'name': 'ButtonWidget', 'code': 'tk.Button(root, text="Click Me!")'}
]

# Create a window with the given layout.
window1 = es.create_window(name='First Window', layout=layout)
print(window1)
window1.show()
