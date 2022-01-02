import os.path
import PySimpleGUI as sg
import requests
import json
from googleapiclient.http import MediaFileUpload
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os


gauth = GoogleAuth()
gauth.LocalWebserverAuth()       
drive = GoogleDrive(gauth)

path = "data.txt"
googlePath = ""
fileList = []
if not os.path.isfile(path):
    f = open("data.txt","w+")
    f.close()
else:
    f = open("data.txt", "r")
    data = f.read()
    dataSplit = data.split("\n")
    print(dataSplit)
    if len(dataSplit) > 0:
        googlePath = dataSplit[0]
        del dataSplit[0]
        fileList = dataSplit
    f.close()
    print(fileList)



layout =    [
                [
                    sg.In(enable_events=True, key='_BROWSE_'),
                    sg.FileBrowse(file_types=(("Any", "*"),)),

                ],
                [
                    sg.Listbox(values=[], select_mode='extended', enable_events=True, key='_LISTBOX_', size=(60, 10))
                ],
                [
                    sg.Text('Google drive folder ID'),
                    sg.Input('', key='_INPUT_')
                ],
                [
                    sg.Button("Backup" , key='_BACKUP_'),
                    sg.Button("Save" , key='_SAVE_'),
                    sg.Button("Delete" , key='_DELETE_'),
                ]

            ]


# Create the window
window = sg.Window("Google drive automated backup", layout)
window.finalize()
window["_LISTBOX_"].update(fileList)
window["_INPUT_"].update(googlePath)
# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    print(event)


    if event == "_BROWSE_":
        print("browse")
        listbox = window["_LISTBOX_"].get_list_values()
        print(listbox)
        listbox.append(values['_BROWSE_'])
        window["_LISTBOX_"].update(listbox)
    if event == "_BACKUP_":
        print("")
    if event == "_DELETE_":
        selected = window["_LISTBOX_"].get()
        listbox = window["_LISTBOX_"].get_list_values()
        if len(selected) != 0:
            for item in listbox:
                # print(item)
                # print(selected)
                # print("---------")
                if item == selected[0]:
                    listbox.remove(item)
                    # print("removed")
                    break
            print(listbox)
            window["_LISTBOX_"].update(listbox)
    if event == "_SAVE_":
        googlePath = window["_INPUT_"].get()
        print(googlePath)
        f = open("data.txt", "w")
        datatowrite = googlePath + "\n"
        listbox = window["_LISTBOX_"].get_list_values()
        for item in listbox:
            datatowrite += (item + "\n")
        f.write(datatowrite)
        f.close()
        sg.Popup('Saved', keep_on_top=True)

    if event == "_BACKUP_":

        
        folder_id = googlePath

        upload_file_list = window["_LISTBOX_"].get_list_values()
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': folder_id}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload() # Upload the file.
        sg.Popup('Back up complete!', keep_on_top=True)
    if event == "OK" or event == sg.WIN_CLOSED:
        print(event)
        break

window.close()