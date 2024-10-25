import customtkinter as ctk
from datetime import date
import rarfile
import os
import shutil
import re
from CustomTkinterMessagebox import CTkMessagebox
import fnmatch
from time import sleep

# app config
app = ctk.CTk()
app.title("demo_extractor")
app.geometry("700x400")
app.resizable(False, False)


# variables
demo_files = {}
csgo_folder_files = {}
color_theme = '#232F3E'
danger_theme = '#990011'
current_date = date.today()
file_path = ''
target_directory = os.getenv('CSGO_PATH')
rarfile.UNRAR_TOOL = r"C:\Program Files\WinRAR\UnRAR.exe"

dynamic_buttons = []


# Partials
def sanitize_filename(filename):
    # Replace invalid characters with an underscore and then remove consecutive underscores
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Replace consecutive underscores with a single one
    sanitized = re.sub(r'_+', '_', sanitized)
    return sanitized.strip('_')  # Optional: Remove leading/trailing underscores if needed


def main_display_worker_partial():

    scrollable_frame = ctk.CTkScrollableFrame(
        app,
        orientation="vertical",
        width=350,
        height=300,
    )

    scrollable_frame.place(x=350, y=50, relwidth = 0.485, relheight=0.75)
    scrollable_frame.grid_columnconfigure(0, weight=0)
    scrollable_frame.grid_columnconfigure(1, weight=1)

    i = 0

    for filename in os.listdir(target_directory):
        file_path = os.path.join(target_directory, filename)
        if os.path.isfile(os.path.join(target_directory, filename)):
            if fnmatch.fnmatch(filename, '*dem'):

                scrollable_frame.grid_rowconfigure(i, weight=0)

                var = ctk.BooleanVar(value=False) # Create boolean object and set its value to True
                checkbox = ctk.CTkCheckBox(scrollable_frame, width=0, text='', variable=var, checkbox_height=20, checkbox_width=20, fg_color=color_theme) # Create a checkbox object
                checkbox.grid(row=i, column=0) # Set the field to be in row = i and column 0

                file_name_entry = ctk.CTkLabel(scrollable_frame, text=filename, width=0, anchor='w') # Create file_name object field
                file_name_entry.grid(row = i, column=1, sticky='ew') # Set the field to be in row = i and column 1

                i += 1
        
    if not i:
        ctk.CTkLabel(scrollable_frame, text='Found no .dem files').pack()
        

def select_all_partial():
    
    for file in csgo_folder_files:
        base = csgo_folder_files[file]
        base['checkbox'].select(True)
        print(base['checkbox'].get())


def delete_all_partial():

    for file in csgo_folder_files:
        base = csgo_folder_files[file]
        #print(base['checkbox'].get())
        print(base['checkbox'].get())
        if base['checkbox'].get():
            os.remove(base['file_path'])
            
            dynamic_buttons[0].destroy()
            dynamic_buttons[1].destroy()

    main_display_worker_partial()



def test(*args):

    try:

        temp = file_path.split('/')[-1].split('.')

        file_name = temp[0]
        file_type = temp[-1]
    
        if file_type == 'rar':
            with rarfile.RarFile(file_path) as rf:
                for file in demo_files:
                    base = demo_files[file]
                    
                    if base['checkbox'].get():

                        new_file_name = sanitize_filename(base['name'].get())
                        
                        
                        target_file_path = os.path.join(target_directory, new_file_name + '.dem')


                        extracted_path = rf.extract(base['main_object'].filename)
                        
                        shutil.move(extracted_path, target_file_path)
                        print(f"Extracted and renamed: {base['main_object']} → {new_file_name}")
        
        else:
            pass
                    
    except rarfile.BadRarFile:
        print("Error: Invalid or corrupted RAR file")
    except Exception as e:
        print(f"An error occurred: {str(e)}")



    CTkMessagebox.messagebox(title='demo_copier', text=f'Moved selected demos to csgo folder.', sound='on', button_text='OK')

    # export.configure(state=ctk.DISABLED)
    






def load_file():

    file = ctk.filedialog.askopenfile()
    export = ctk.CTkButton(app, text='Export', fg_color=color_theme, command=test)
    export.pack(side=ctk.LEFT, anchor=ctk.S, padx=10, pady=10)
    load_display_demo_files(file)




def load_csgo_demo_files():

    if dynamic_buttons:
        for btn in dynamic_buttons:
            btn.destroy()

    scrollable_frame = ctk.CTkScrollableFrame(
        app,
        orientation="vertical",
        width=350,
        height=300,
    )

    scrollable_frame.place(x=350, y=50, relwidth = 0.485, relheight=0.75)
    scrollable_frame.grid_columnconfigure(0, weight=0)
    scrollable_frame.grid_columnconfigure(1, weight=1)
    
    i = 0

    for filename in os.listdir(target_directory):
        file_path = os.path.join(target_directory, filename)
        if os.path.isfile(os.path.join(target_directory, filename)):
            if fnmatch.fnmatch(filename, '*dem'):

                scrollable_frame.grid_rowconfigure(i, weight=0)

                var = ctk.BooleanVar(value=False) # Create boolean object and set its value to True
                checkbox = ctk.CTkCheckBox(scrollable_frame, width=0, text='', variable=var, checkbox_height=20, checkbox_width=20, fg_color=color_theme) # Create a checkbox object
                checkbox.grid(row=i, column=0) # Set the field to be in row = i and column 0

                file_name_entry = ctk.CTkLabel(scrollable_frame, text=filename, width=0, anchor='w') # Create file_name object field
                file_name_entry.grid(row = i, column=1, sticky='ew') # Set the field to be in row = i and column 1

                i += 1

                csgo_folder_files[filename] = {'checkbox': checkbox, 'file_path': file_path}

    if not i:
        ctk.CTkLabel(scrollable_frame, text='Found no .dem files').pack()
        


    delete = ctk.CTkButton(app, text='Delete', fg_color=danger_theme, command=delete_all_partial)
    delete.pack(side=ctk.RIGHT, anchor=ctk.S, padx=10, pady=10)

    select_all = ctk.CTkButton(app, text='All', fg_color=color_theme, width=10, command=select_all_partial)
    select_all.pack(side=ctk.RIGHT, anchor=ctk.S, pady=10)

    dynamic_buttons.append(delete)
    dynamic_buttons.append(select_all)

    #load_demo_files.configure(state=ctk.DISABLED)


def load_display_demo_files(file):

    global file_path
    file_path = file.name


    type_file = file.name.split('/')[-1].split('.') # Split the file into its name and file type

    if type_file[-1] == 'rar': # Check if the opened file is in rar format
    
        with rarfile.RarFile(file_path) as rf: # Use rarfile.Rarfile(file_path) to temporarily open a file inside its root folder.

            for i, obj in enumerate(rf.infolist()): # Iterate over all files within the rar file.

                main_frame.grid_rowconfigure(i, weight=0) # Create a row for each file in rf

                file = obj.filename.split('.') # Split the file into its and file type
                file_name = file[0] # File name
                file_type = file[-1] # File type

                var = ctk.BooleanVar(value=True) # Create boolean object and set its value to True
                checkbox = ctk.CTkCheckBox(main_frame, width=0, text='', variable=var, checkbox_height=20, checkbox_width=20, fg_color=color_theme) # Create a checkbox object
                checkbox.grid(row=i, column=0) # Set the field to be in row = i and column 0

                file_name_entry = ctk.CTkEntry(main_frame) # Create file_name object field
                file_name_entry.insert(0, "{}_{}".format(current_date, file_name)) # Set the name as current_date + file_name
                file_name_entry.grid(row = i, column=1, sticky='ew') # Set the field to be in row = i and column 1
                
                file_type_label = ctk.CTkLabel(main_frame, text=" .{}".format(file_type)) # Create file_type object label
                file_type_label.grid(row = i, column = 2) # Set the field to be in row = i and columnm 2

                demo_files[obj] = {"checkbox": checkbox, "name": file_name_entry, "main_object": obj, 'rar_path': file_path} # Set obj (file) as a dictionary key and its objects



    elif type_file[-1] == 'dem':

        file_name = type_file[0]
        file_type = type_file[-1]
        
        var = ctk.BooleanVar(value=True)
        checkbox = ctk.CTkCheckBox(main_frame, width=0, text='', variable=var, checkbox_height=20, checkbox_width=20, fg_color=color_theme)
        checkbox.grid(row=0, column=0, padx=0)

        file_name_entry = ctk.CTkEntry(main_frame)
        file_name_entry.insert(0, "{}_{}".format(current_date, file_name))
        file_name_entry.grid(row = 0, column=1, sticky='ew')
                        
        file_type_label = ctk.CTkLabel(main_frame, text=" .{}".format(file_type))
        file_type_label.grid(row = 0, column = 2)

        demo_files[obj] = {"checkbox": checkbox, "name": file_name_entry, "main_object": obj, 'rar_path': file_path}


    else:
        print("Cannot open file ")




main_frame = ctk.CTkFrame(app)
main_frame.place(x=10, y=50, relwidth = 0.47, relheight=0.8)

main_frame.grid_columnconfigure(0, weight=0)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_columnconfigure(2, weight=0)
    


#ctk.CTkLabel(main_frame, bg_color="red").pack(expand=True, fill='both')



button = ctk.CTkButton(app, text="Browse", fg_color=color_theme, command=load_file)
button.pack(side=ctk.TOP, anchor=ctk.NW, padx=10, pady=10)






load_demo_files = ctk.CTkButton(app, text='Load_folder', fg_color=color_theme, command=load_csgo_demo_files)
load_demo_files.pack(side=ctk.RIGHT, anchor=ctk.S, padx=10, pady=10)

# textLabel = ctk.CTkLabel(app, text=f'csgo absolute path: {target_directory}')
# textLabel.place(x=10, y=375)

# name_field = ctk.CTkTextbox(app, width=400, height=200)
# name_field.pack(pady=10)

# text = ctk.CTkLabel(app, text="")
# text.pack(padx=20, pady=40)




app.mainloop()