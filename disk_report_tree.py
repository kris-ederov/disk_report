import tkinter, os
from tkinter import ttk
from disk_report_functions import ScanFolder, FolderSize, FormatSize
from disk_report_graph import GenGraph
from PIL import Image, ImageTk

class GenTreeview():
    def __init__(self, main_win, folder_path, graph_object):
        self.main_win = main_win
        self.folder_path = folder_path
        self.item_count = 0
        self.dict_folder_urls = {}
        self.graph_object = graph_object

        self.scrollbar = tkinter.Scrollbar(self.main_win)
        self.scrollbar.pack(side = tkinter.RIGHT, fill = tkinter.Y)

        self.tree = tkinter.ttk.Treeview(self.main_win)
        self.tree["yscrollcommand"] = self.scrollbar.set
        
        self.tree.pack(side = tkinter.LEFT)
        self.scrollbar.config(command = self.tree.yview)

        self.tree["columns"] = "size", "empty"
        self.tree["height"] = "23"
        self.tree["selectmode"] = "browse"
        
        self.tree.column("#0", width=360, minwidth=270, stretch=tkinter.NO)
        self.tree.column("size", width=70, minwidth=70, stretch=tkinter.NO, anchor = tkinter.E)
        self.tree.column("empty", width=10, minwidth=15)

        self.tree.heading("#0", text="File Name", anchor=tkinter.W)
        self.tree.heading("size", text="Size", anchor=tkinter.W)

        self.folder_icon = ImageTk.PhotoImage(Image.open("icons\\folder.png"))
        self.file_icon = ImageTk.PhotoImage(Image.open("icons\\file.png"))
        self.GenLevel(self.folder_path, "")

    # Generate main level of tree
    def GenLevel(self, folder_path, parent_item):
        if parent_item == "":
            filesize = FormatSize(FolderSize(folder_path))
            root_path, root_name = os.path.split(folder_path)
            filename = root_name + " (Root)"

            # Generate main level
            self.sub_folder_item = self.tree.insert(parent_item, "end", "", text = filename, values = (filesize,), 
                open = True, image = self.folder_icon, tags = (folder_path,))

            # Bind clicks to item
            self.item_bind(self.tree, folder_path)

            parent_item = self.sub_folder_item

        # Generate folder sub-levels
        list_files, list_sizes, list_urls = ScanFolder(folder_path, False)

        for index, filename in enumerate(list_files):
            filesize = FormatSize(list_sizes[index])
            self.sub_folder_item = self.tree.insert(parent_item, "end", "", text = filename, values = (filesize,), 
                open = False, tags = (list_urls[index],))

            if os.path.isdir(list_urls[index]):
                # Bind clicks to item
                self.item_bind(self.tree, list_urls[index])

                # Set folder icon
                self.tree.item(self.sub_folder_item, image = self.folder_icon)

                # Generate folder sub-level
                self.GenLevel(list_urls[index], self.sub_folder_item)
            else:
                # Set file icon
                self.tree.item(self.sub_folder_item, image = self.file_icon)

    def item_bind(self, tree, url):
        if self.graph_object is not "":
            self.tree.tag_bind(url, sequence = '<ButtonPress-1>',
                callback = lambda event, arg=url: self.on_1click(event, arg))

        self.tree.tag_bind(url, sequence = '<Double-1>',
            callback = lambda event, arg=url: self.on_2click(event, arg))

    def on_1click(self, event, path):
        self.graph_object.SetFigAxes(path)
    
    def on_2click(self, event, path):
        os.startfile(path)

    def NewLevel(self, folder_path):
        self.folder_path = folder_path

        self.tree.delete(self.tree.get_children())
        self.GenLevel(self.folder_path, "")


if __name__ == "__main__":
    stest = r"D:\Downloads"
    stest2 = r"C:\Users\krissay\Documents"

    root = tkinter.Tk()

    List_treeview = GenTreeview(root, stest, "")

    root.mainloop()
