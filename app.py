import customtkinter as ctk
from datetime import date
import rarfile
import os
import shutil
import re
import fnmatch
from dotenv import load_dotenv

load_dotenv()

# app config
app = ctk.CTk()
app.title("demo_exporter")
app._set_appearance_mode("light")
app.configure(bg="white")
app.geometry("700x400")
app.resizable(False, False)


# variables
demo_files = {}
csgo_folder_files = {}
dynamic_buttons = []
color_theme = '#232F3E'
danger_theme = '#990011'
current_date = date.today()
file_path = ''
target_directory = os.getenv('CSGO_PATH')
rarfile.UNRAR_TOOL =  os.getenv('UNRAR_PATH') # "C:\Program Files\WinRAR\UnRAR.exe"



# Partials
def sanitize_filename(filename):
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    sanitized = re.sub(r'_+', '_', sanitized)
    return sanitized.strip('_')  




def select_all_partial():
    
    # iterate over each file and set the checkbox status to true
    for file in csgo_folder_files:
        base = csgo_folder_files[file]
        base['checkbox'].select(True)


def delete_all_partial():

    global csgo_folder_files

    # iterate over each file, check if the checkbox is checked and delete it.
    for file in csgo_folder_files:
        base = csgo_folder_files[file]
        if base['checkbox'].get():
            os.remove(base['file_path'])
            dynamic_buttons[0].destroy()
            dynamic_buttons[1].destroy()

    csgo_folder_files = {} # csgo_files_files.clear() instead of setting variable to global
    refresh_partial()



def export_files_partial():

    try:

        temp = file_path.split('/')[-1].split('.')
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
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        refresh_partial()

    

def refresh_partial():

    if dynamic_buttons:
        for btn in dynamic_buttons:
            btn.destroy()

    scrollable_frame = ctk.CTkScrollableFrame(
        app,
        orientation="vertical",
        width=350,
        height=300,
        fg_color='white'
    )

    scrollable_frame.place(x=360, relwidth = 0.485, relheight=0.9)
    scrollable_frame.grid_columnconfigure(0, weight=0)
    scrollable_frame.grid_columnconfigure(1, weight=1)
    
    i = 0


    for filename in os.listdir(target_directory):
        file_path = os.path.join(target_directory, filename)
        if os.path.isfile(os.path.join(target_directory, filename)):
            if fnmatch.fnmatch(filename, '*dem'):

                scrollable_frame.grid_rowconfigure(i, weight=0)

                var = ctk.BooleanVar(value=False) 
                checkbox = ctk.CTkCheckBox(scrollable_frame, width=0, text='', variable=var, checkbox_height=20, checkbox_width=20, border_width=2, fg_color=color_theme) # Create a checkbox object
                checkbox.grid(row=i, column=0)

                file_name_entry = ctk.CTkLabel(scrollable_frame, text=filename, width=0, anchor='w') 
                file_name_entry.grid(row = i, column=1, sticky='ew')

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

    


def load_nd_display_demo_files_partial(file):

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
                checkbox = ctk.CTkCheckBox(main_frame, width=0, text='', variable=var, checkbox_height=20, checkbox_width=20, border_width=2, fg_color=color_theme) # Create a checkbox object
                checkbox.grid(row=i, column=0, pady=(2, 2)) # Set the field to be in row = i and column 0

                file_name_entry = ctk.CTkEntry(main_frame, corner_radius=1) # Create file_name object field
                file_name_entry.insert(0, "{}_{}".format(current_date, file_name)) # Set the name as current_date + file_name
                file_name_entry.grid(row = i, column=1, sticky='ew', pady=(2, 2)) # Set the field to be in row = i and column 1
                
                file_type_label = ctk.CTkLabel(main_frame, text=" .{}".format(file_type)) # Create file_type object label
                file_type_label.grid(row = i, column = 2, pady=(2, 2)) # Set the field to be in row = i and columnm 2

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



def load_file():

    file = ctk.filedialog.askopenfile()
    export_btn = ctk.CTkButton(main_button_frame, text="Export", fg_color=color_theme, command=export_files_partial)
    export_btn.pack(side=ctk.LEFT)
    load_nd_display_demo_files_partial(file)



base_frame = ctk.CTkFrame(app, fg_color='white')
base_frame.place(x=0, y=0, relwidth = 1, relheight = 1)


main_frame = ctk.CTkFrame(base_frame, fg_color='white')
main_frame.place(x=10, y=50, relwidth = 0.47, relheight=0.8)

main_frame.grid_columnconfigure(0, weight=0)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_columnconfigure(2, weight=0)


main_button_frame = ctk.CTkFrame(app, fg_color='white')
main_button_frame.pack(anchor=ctk.NW, padx=10, pady=10)

browse_btn = ctk.CTkButton(main_button_frame, text="Browse", fg_color=color_theme, command=load_file)
browse_btn.pack(side=ctk.LEFT, padx=10)

refresh_btn = ctk.CTkButton(app, text='Refresh', fg_color=color_theme, command=refresh_partial)
refresh_btn.pack(side=ctk.RIGHT, anchor=ctk.S, padx=(0, 10), pady=10)
refresh_partial()




app.mainloop()