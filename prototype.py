import customtkinter as ctk

# Create the main app window
app = ctk.CTk()
app.geometry("800x600")  # Set the permanent dimensions for the main window

scrollable_frame = ctk.CTkScrollableFrame(master=app, width=200, height=200)
scrollable_frame.pack()


for x in range(20):
	ctk.CTkLabel(scrollable_frame, text='This isa  test').pack()


app.mainloop()
