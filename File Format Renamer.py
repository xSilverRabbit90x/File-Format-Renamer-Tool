import os
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox, Frame, Listbox, StringVar
from tkinter import ttk  # Import the ttk library for the Combobox

class FileFormatRenamer:
    def __init__(self, master):
        self.master = master
        master.title("File Format Renamer")  # Updated title
        master.geometry("620x400")
        master.config(bg="#f0f0f0")

        # Font for the text
        font = ("Arial", 12)

        # Main frame
        self.frame = Frame(master, bg="#f0f0f0")
        self.frame.pack(pady=20)

        # Label for folder selection
        self.label = Label(self.frame, text="Select a folder:", font=font, bg="#f0f0f0")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        # Entry field for the folder
        self.path_entry = Entry(self.frame, width=40, font=font, bg="#f0ffff")
        self.path_entry.grid(row=0, column=1, padx=10, pady=10)

        # Button to select the folder
        self.select_button = Button(self.frame, text="Browse", command=self.select_folder, font=font, bg="#87CEEB", fg="white")
        self.select_button.grid(row=0, column=2, padx=10, pady=10)

        # Label for renaming method selection
        self.method_label = Label(master, text="Renaming method:", font=font, bg="#f0f0f0")
        self.method_label.pack(pady=10)

        # Variable for the Combobox
        self.rename_method = StringVar(master)
        self.rename_method.set("jpg")  # Default value

        # Combobox for renaming method
        self.methods = [
            'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg', 'tiff', 
            'txt', 'pdf', 'doc', 'rtf', 'csv', 'md', 'htm', 'html', 'py', 'json', 'config', 'spec', 'toc', 'pkg', 'pyz', 'pyc', 'exe', 'bat',
            'mp3', 'wav', 'ogg', 'aac',
            'mp4', 'avi', 'mkv', 'mov', 'flv',
            'zip', 'rar', '7z', 'tar', 'gz', 'bz2'
        ]
        self.method_menu = ttk.Combobox(master, textvariable=self.rename_method, values=self.methods, state='readonly', font=font)
        self.method_menu.pack(pady=5)

        # Button to rename files
        self.rename_button = Button(master, text="Rename Files", command=self.rename_files, state='disabled', font=font, bg="#87CEEB", fg="white")
        self.rename_button.pack(pady=10)

        # Listbox to display files to rename
        self.file_list = Listbox(master, width=50, height=10, font=font)
        self.file_list.pack(pady=10)

        self.folder_path = ""

        # Bind the event to check manual path
        self.path_entry.bind("<KeyRelease>", self.check_path)

        # Status label
        self.status_label = Label(master, text="", font=font, bg="#f0f0f0")
        self.status_label.pack(pady=10)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.path_entry.delete(0, 'end')
            self.path_entry.insert(0, self.folder_path)
            self.list_files()  # Update file list

    def check_path(self, event=None):
        self.folder_path = self.path_entry.get().strip()
        if os.path.isdir(self.folder_path):
            self.list_files()  # Update file list
        else:
            self.file_list.delete(0, 'end')  # Clear the list if the path is not valid

        self.rename_button.config(state='normal' if self.file_list.size() > 0 else 'disabled')
        if self.file_list.size() > 0:
            self.status_label.config(text="Choose a renaming method")
        else:
            self.status_label.config(text="")

    def list_files(self):
        self.file_list.delete(0, 'end')  # Clear the list
        if os.path.isdir(self.folder_path):
            for filename in os.listdir(self.folder_path):
                if filename.lower().endswith(tuple(self.methods)):
                    self.file_list.insert('end', filename)
            self.rename_button.config(state='normal' if self.file_list.size() > 0 else 'disabled')
            if self.file_list.size() > 0:
                self.status_label.config(text="Choose a renaming method")
            else:
                self.status_label.config(text="")

    def rename_files(self):
        if not self.folder_path or not os.path.isdir(self.folder_path):
            messagebox.showwarning("Warning", "No valid folder selected.")
            return

        selected_method = self.rename_method.get()
        new_extension = f'.{selected_method}'

        try:
            for i in range(self.file_list.size()):
                filename = self.file_list.get(i)
                file_path = os.path.join(self.folder_path, filename)

                # Create the new file name with the selected extension
                base_name = os.path.splitext(file_path)[0]
                new_file_path = base_name + new_extension

                # Handle conflicts by adding a numeric suffix if needed
                counter = 1
                while os.path.exists(new_file_path):
                    new_file_path = f"{base_name}_{counter}{new_extension}"
                    counter += 1

                # Rename the file
                os.rename(file_path, new_file_path)

            messagebox.showinfo("Success", f"All files have been renamed to {selected_method}.")
            self.list_files()  # Update the file list after renaming
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = Tk()
    renamer = FileFormatRenamer(root)  # Updated class name instantiation
    root.mainloop()
