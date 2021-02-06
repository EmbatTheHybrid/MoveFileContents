# Move folders in specified folder

# Imports
import PySimpleGUI as sg
import os

# Sets the theme of the GUI
sg.theme('DarkPurple2')

# Variable initilization
prevfold = ""

# Layout of the left side
layout_left = [
    [
        sg.Text("Contents Folder:", text_color="Violet"),
        sg.Input(size=(33, 1), enable_events=True, key="-CONTENTS-", tooltip="The folder to get contents from"),
        sg.FolderBrowse(),
    ],
    [
        sg.Text("Move to:", text_color="Violet"),
        sg.Input(size=(33, 1), enable_events=True, key="-MOVE-", tooltip="The folder to move the contents to"),
        sg.FolderBrowse(),
    ],
    [sg.Button("Move Folder", enable_events=True, key="-MOVEFOLDER-"), sg.Button("Back", enable_events=True, key="-BACK-", tooltip="Move back a folder")],
    [sg.Text("\nHow to use:\n1) Click 'Browse' on the same line as 'Contents Folder' and select a folder with stuff you want to move\n2) Click 'Browse' on the same line as 'Move to' and select a folder you want to move the contents to\n3) Click on files in the right side list to move them to the 'Move to' folder. Double click on a folder to enter it", size=(42,10), text_color="Violet")]
]

# Layout of right side
layout_right = [
    [sg.Listbox(values=[], enable_events=True, size=(40, 20), key="-LIST-", bind_return_key=True)]
]


# Main Layout
layout = [
    [
        sg.Column(layout_left),
        sg.VerticalSeparator(),
        sg.Column(layout_right)
    ]
]

# Window Creation
window = sg.Window("Move Contents by Embat", return_keyboard_events=True, layout=layout)

# Event handler
while True:
    event, values = window.read()
    def updateList(folder : str = values["-CONTENTS-"]):
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
        ]
        window["-LIST-"].update(fnames)
    print(event, values)
    if event == "-LIST-":
        try:
            filename = values["-LIST-"][0] # Get selected list value
            contentsfold = f"{values['-CONTENTS-']}/{filename}"
            if os.path.isdir(contentsfold): # Checks if selected item is a folder/directory
                if prevfold == filename: # Checks if user is pressing a folder that was already pressed
                    window['-CONTENTS-'].update(contentsfold)
                    updateList(contentsfold)
                else:
                    prevfold = filename
            else:
                # Sends file to Move To folder
                os.rename(f"{values['-CONTENTS-']}/{filename}", f"{values['-MOVE-']}/{filename}")
                updateList()
        except:
            pass
    elif event == sg.WIN_CLOSED:
        break
    elif event == "-CONTENTS-":
        updateList()
    elif event == "-BACK-":
        # Moves the content folder back by one directory
        try:
            backval = os.path.split(values["-CONTENTS-"])[0]
            window["-CONTENTS-"].update(backval)
            updateList(backval)
        except:
            pass
    elif event == "-MOVEFOLDER-":
        # Moves the selected folder to the Move to folder
        try:
            filename = values["-LIST-"][0]
            os.rename(f"{values['-CONTENTS-']}/{filename}", f"{values['-MOVE-']}/{filename}")
            updateList()
            prevfold = ""
        except:
            pass
    elif event == "BackSpace:8":
        window["-BACK-"].click()

window.close()
