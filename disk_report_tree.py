import tkinter, os
from tkinter import ttk
from disk_report_functions import ScanFolder, FolderSize, FormatSize
from disk_report_graph import GenGraph

class GenTreeview():
    def __init__(self, main_win, folder_path, graph_object):
        self.main_win = main_win
        self.folder_path = folder_path
        self.item_count = 0
        self.dict_folder_urls = {}
        self.graph_object = graph_object

        # self.main_win.title("Treeview")
        # self.main_win.geometry("450x600")

        self.scrollbar = tkinter.Scrollbar(self.main_win)
        self.scrollbar.pack(side = tkinter.RIGHT, fill = tkinter.Y)

        self.tree = tkinter.ttk.Treeview(self.main_win)
        self.tree["yscrollcommand"] = self.scrollbar.set
        
        self.tree.pack(side = tkinter.LEFT)
        self.scrollbar.config(command = self.tree.yview)

        self.tree["columns"] = "size"
        self.tree["height"] = "24"
        self.tree.column("#0", width=360, minwidth=270, stretch=tkinter.NO)
        self.tree.column("size", width=80, minwidth=80, stretch=tkinter.NO)

        self.tree.heading("#0", text="File Name", anchor=tkinter.W)
        self.tree.heading("size", text="Size", anchor=tkinter.W)
        self.tree.bind('<Double-1>', self.on_click)

        self.GenLevel(self.folder_path, "")
    
    # Generate main level of tree
    def GenLevel(self, folder_path, folder_item):

        list_files, list_sizes, list_urls = ScanFolder(folder_path, False)

        for index, filename in enumerate(list_files):
            filesize = FormatSize(list_sizes[index])
            self.sub_folder_item = self.tree.insert(folder_item, "end", "", text = filename, values = (filesize,), open = False)
            if os.path.isdir(list_urls[index]):
                # Save tree item to a dictionary
                self.dict_folder_urls[self.sub_folder_item] = list_urls[index]
                # Generate folder sub-level
                self.GenLevel(list_urls[index], self.sub_folder_item)
            
    def on_click(self, event):
        item = self.tree.selection()[0]
        if item in self.dict_folder_urls: self.graph_object.SetFigAxes(self.dict_folder_urls[item])


if __name__ == "__main__":
    stest = r"D:\Downloads"
    stest2 = r"C:\Users\krissay\Documents"

    root = tkinter.Tk()

    List_treeview = GenTreeview(root, stest)

    root.mainloop()
