import tkinter, os
from tkinter import ttk
from disk_report_functions import ScanFolder, FolderSize, FormatSize

class GenTreeview():
    def __init__(self, main_win, folder_path):
        self.main_win = main_win
        self.folder_path = folder_path

        self.main_win.title("Treeview")
        self.main_win.geometry("450x600")

        self.scrollbar = tkinter.Scrollbar(self.main_win)
        self.scrollbar.pack(side = tkinter.RIGHT, fill = tkinter.Y)

        self.tree = tkinter.ttk.Treeview(self.main_win)
        self.tree["yscrollcommand"] = self.scrollbar.set
        
        self.tree.pack(side = tkinter.LEFT)
        self.scrollbar.config(command = self.tree.yview)

        self.tree["columns"] = "size"
        self.tree["height"] = "20"
        self.tree.column("#0", width=350, minwidth=270, stretch=tkinter.NO)
        self.tree.column("size", width=100, minwidth=100, stretch=tkinter.NO)

        self.tree.heading("#0", text="File Name", anchor=tkinter.W)
        self.tree.heading("size", text="Size", anchor=tkinter.W)

        self.GenLevel(self.folder_path, "")
    
    # Generate main level of tree
    def GenLevel(self, folder_path, folder_item):

        list_files, list_sizes, list_urls = ScanFolder(folder_path, False)

        for index, filename in enumerate(list_files):
            filesize = FormatSize(list_sizes[index])
            sub_folder_item = self.tree.insert(folder_item, "end", "", text = filename, values = (filesize,))
            # Generate folder sub-level
            if os.path.isdir(list_urls[index]):
                self.GenLevel(list_urls[index], sub_folder_item)


if __name__ == "__main__":
    stest = r"D:\Downloads"
    stest2 = r"C:\Users\krissay\Documents"

    root = tkinter.Tk()

    List_treeview = GenTreeview(root, stest)

    root.mainloop()
