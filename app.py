import customtkinter as ctk
from datetime import date
import rarfile
import os
import shutil
import re
from CustomTkinterMessagebox import CTkMessagebox

app = ctk.CTk()
# app.iconbitmap('logo.ico')
app.title("demo_extractor")
app.geometry("700x400")
app.resizable(False, False)

demo_files = {}
color_theme = '#232F3E'
current_date = date.today()

file_path = ''
rarfile.UNRAR_TOOL = r"C:\Program Files\WinRAR\UnRAR.exe"
target_directory = os.getenv('CSGO_PATH')


def sanitize_filename(filename):
    # Replace invalid characters with an underscore and then remove consecutive underscores
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Replace consecutive underscores with a single one
    sanitized = re.sub(r'_+', '_', sanitized)
    return sanitized.strip('_')  # Optional: Remove leading/trailing underscores if needed

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

    test_btn.configure(state=ctk.DISABLED)
    




def load_file():

    file = ctk.filedialog.askopenfile()
    load_display_demo_files(file)


def load_display_demo_files(file):

    global file_path
    file_path = file.name

    
    main_frame = ctk.CTkFrame(app)
    main_frame.place(x=10, y=50, relwidth = 0.5, relheight=0.2)

    main_frame.grid_columnconfigure(0, weight=0)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_columnconfigure(2, weight=0)

    main_frame.rowconfigure((0,1,2,3,4,6), weight=1)

    #ctk.CTkLabel(main_frame, bg_color="red").pack(expand=True, fill='both')


    type_file = file.name.split('/')[-1].split('.')

    if type_file[-1] == 'rar':
    
        with rarfile.RarFile(file_path) as rf:

            for i, obj in enumerate(rf.infolist()):

                file = obj.filename.split('.')

                file_name = file[0]
                file_type = file[-1]

                print(obj)

                var = ctk.BooleanVar(value=True)
                checkbox = ctk.CTkCheckBox(main_frame, width=0, text='', variable=var, checkbox_height=20, checkbox_width=20, fg_color=color_theme)
                # checkbox.pack(padx=20, pady=10, anchor="w")
                checkbox.grid(row=i, column=0, padx=0)

                file_name_entry = ctk.CTkEntry(main_frame)
                file_name_entry.insert(0, "{}_{}".format(current_date, file_name))
                file_name_entry.grid(row = i, column=1, sticky='ew')
                
                file_type_label = ctk.CTkLabel(main_frame, text=" .{}".format(file_type))
                file_type_label.grid(row = i, column = 2)

                demo_files[obj] = {"checkbox": checkbox, "name": file_name_entry, "main_object": obj, 'rar_path': file_path}

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








button = ctk.CTkButton(app, text="Browse", fg_color=color_theme, command=load_file)
button.pack(side=ctk.TOP, anchor=ctk.NW, padx=10, pady=10)

test_btn = ctk.CTkButton(app, text='TestSavePrint', command=test)
test_btn.pack(side=ctk.LEFT, padx=10, pady=10)

textLabel = ctk.CTkLabel(app, text=f'csgo absolute path: {target_directory}')
textLabel.place(x=10, y=375)

# name_field = ctk.CTkTextbox(app, width=400, height=200)
# name_field.pack(pady=10)

# text = ctk.CTkLabel(app, text="")
# text.pack(padx=20, pady=40)




app.mainloop()