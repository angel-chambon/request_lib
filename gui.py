from tkinter import *
from tkinter.ttk import *
import main
import ast


class Data:
    def write(key, value):
        open(f'data/gui/{str(key)}.data', 'w').writelines(str(value))
        return True
    

    def read(key):
        value = open(f'data/gui/{str(key)}.data', 'r').readline()
        return value


def ListRequests():
    return main.Request_index.get_list()


def Worker(event):
    # Get the selected item from the listbox
    selected_index = list_box.curselection()
    selected_item = list_box.get(selected_index)
    url, method, headers, datajson = main.Save.load(selected_item)

    Data.write('actual_selection', selected_item)
    
    # Update the Entry widgets with new values
    entry_name.delete(0, END)
    entry_name.insert(0, selected_item)

    entry_url.delete(0, END)
    entry_url.insert(0, url)
    
    entry_method.delete(0, END)
    entry_method.insert(0, method)
    
    entry_headers.delete(0, END)
    entry_headers.insert(0, headers)
    
    entry_datajson.delete(0, END)
    entry_datajson.insert(0, datajson)


def UpdateRequest():
    main.Save.update(
        name=Data.read('actual_selection'),
        url=entry_url.get(),
        method=entry_method.get(),
        headers=entry_headers.get(),
        datajson=ast.literal_eval(entry_datajson.get()))
    

def NewRequest():
    main.Save.new(
        name=entry_name.get(),
        url=entry_url.get(),
        method=entry_method.get(),
        headers=entry_headers.get(),
        datajson=ast.literal_eval(entry_datajson.get()))
    UpdateListBox()
    

def UpdateListBox():
    list_box.delete(0, END)
    for item in ListRequests():
        list_box.insert(END, item)


def SendRequest():
    result = main.Requests.make(
        name=entry_name.get()
    )
    print(result)


window = Tk()
window.title('REQUEST LIB')

label_title = Label(window, text='REQUEST LIB', font='Arial')
label_name = Label(window, text='name')
label_url = Label(window, text='url')
label_method = Label(window, text='method')
label_headers = Label(window, text='headers')
label_datajson = Label(window, text='datajson')
list_box = Listbox(window, height=10, selectmode=EXTENDED)
entry_name = Entry(window)
entry_url = Entry(window)
entry_method = Entry(window)
entry_headers = Entry(window)
entry_datajson = Entry(window)
update_button = Button(window, text="UPDATE", command=lambda: UpdateRequest())
new_button = Button(window, text="NEW", command=lambda: NewRequest())
refresh_button = Button(window, text="REFRESH", command=lambda: UpdateListBox())
send_button = Button(window, text="SEND", command=lambda: SendRequest())

label_title.grid(row=0, column=1, pady=(10, 5))
label_name.grid(row=2, column=0, padx=(10, 5), pady=5, sticky="e")
label_url.grid(row=3, column=0, padx=(10, 5), pady=5, sticky="e")
label_method.grid(row=4, column=0, padx=(10, 5), pady=5, sticky="e")
label_headers.grid(row=5, column=0, padx=(10, 5), pady=5, sticky="e")
label_datajson.grid(row=6, column=0, padx=(10, 5), pady=5, sticky="e")
list_box.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
entry_name.grid(row=2, column=1, padx=(0, 10), pady=5, sticky="we")
entry_url.grid(row=3, column=1, padx=(0, 10), pady=5, sticky="we")
entry_method.grid(row=4, column=1, padx=(0, 10), pady=5, sticky="we")
entry_headers.grid(row=5, column=1, padx=(0, 10), pady=5, sticky="we")
entry_datajson.grid(row=6, column=1, padx=(0, 10), pady=5, sticky="we")
update_button.grid(row=7, column=1, padx=(450, 10), pady=(0, 10))
new_button.grid(row=7, column=1, padx=(600, 10), pady=(0, 10))
refresh_button.grid(row=7, column=1, padx=(300, 10), pady=(0, 10))
send_button.grid(row=7, column=1, padx=(150, 10), pady=(0, 10))

window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(1, weight=1)

list_box.bind('<<ListboxSelect>>', Worker)

scrollbar = Scrollbar(window, orient="vertical", command=list_box.yview)
scrollbar.grid(row=1, column=2, sticky='ns')
list_box.config(yscrollcommand=scrollbar.set)

UpdateListBox()

window.mainloop()
