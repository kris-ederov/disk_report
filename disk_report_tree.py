import tkinter, os
from tkinter import ttk
from disk_report_functions import FormatSize, FilesData
from PIL import Image, ImageTk

class GenTreeview():
    def NewTree(self, RootFolder):
        self.RootFolder = RootFolder
        self.root_path = RootFolder.MainFolderPath()

        self.tree.delete(self.tree.get_children())
        self.GenLevel(self.root_path, "")

    def __init__(self, main_win, RootFolder, graph_object):
        self.main_win = main_win
        self.RootFolder = RootFolder
        self.root_path = self.RootFolder.MainFolderPath()
        self.graph_object = graph_object

        self.scrollbar = tkinter.Scrollbar(self.main_win)
        self.scrollbar.pack(side = tkinter.RIGHT, fill = tkinter.Y)

        self.tree = ttk.Treeview(self.main_win)
        self.tree["yscrollcommand"] = self.scrollbar.set
        
        self.tree.pack(side = tkinter.LEFT)
        self.scrollbar.config(command = self.tree.yview)

        self.tree["columns"] = ["size", "empty"]
        self.tree["height"] = "23"
        self.tree["selectmode"] = "browse"
        
        self.tree.column("#0", width=360, minwidth=270, stretch=tkinter.NO)
        self.tree.column("size", width=70, minwidth=70, stretch=tkinter.NO, anchor = tkinter.E)
        self.tree.column("empty", width=10, minwidth=15)

        self.tree.heading("#0", text="File Name", anchor=tkinter.W)
        self.tree.heading("size", text="Size", anchor=tkinter.W)

        self.folder_icon = ImageTk.PhotoImage(Image.open("icons\\folder.png"))
        self.file_icon = ImageTk.PhotoImage(Image.open("icons\\file.png"))
        
        self.GenLevel(self.root_path, "")

    # Generate main level of tree
    def GenLevel(self, folder_path, parent_item):
        if parent_item == "":
            filesize = FormatSize(self.RootFolder.MainFolderSize())
            root_name = os.path.basename(folder_path)
            if not root_name: root_name = folder_path
            filename = str(root_name) + " (Root)"

            # Generate main level
            parent_item = self.tree_insert(parent_item, filename, filesize, True, folder_path)

        # Generate folder sub-levels
        list_files, list_sizes, list_urls = self.RootFolder.FolderContents(folder_path, False, False)

        for index, filename in enumerate(list_files):
            filesize = FormatSize(list_sizes[index])
            self.sub_item = self.tree_insert(parent_item, filename, filesize, False, list_urls[index])

            if os.path.isdir(list_urls[index]):
                # Generate folder sub-level
                self.GenLevel(list_urls[index], self.sub_item)
            else:
                # Set file icon
                self.tree.item(self.sub_item, image = self.file_icon)

            if index > 20:
                self.tree.insert(parent_item, "end", "", text = "...")
                break

    def tree_insert(self, parent_item, filename, filesize, open_flg, tags_arg):
        item = self.tree.insert(parent_item, "end", "", text = filename, values = (filesize,),
            open = open_flg, image = self.folder_icon, tags = (tags_arg,))

        # Bind clicks to item based on tag
        if os.path.isdir(tags_arg): self.item_bind(tags_arg)

        return item

    def item_bind(self, url):
        if self.graph_object is not "":
            self.tree.tag_bind(url, sequence = '<ButtonPress-1>',
                callback = lambda event, arg=url: self.on_1click(event, arg))

        self.tree.tag_bind(url, sequence = '<Double-1>',
            callback = lambda event, arg=url: self.on_2click(event, arg))

    def on_1click(self, event, path):
        list_files, list_sizes, list_urls = self.RootFolder.FolderContents(path, True, False)
        self.graph_object.SetFigAxes(list_files, list_sizes)
    
    def on_2click(self, event, path):
        os.startfile(path)


if __name__ == "__main__":
    stest = r"D:\Downloads"
    stest2 = r"C:\Users\krissay\Documents"

    root = tkinter.Tk()

    RootFolder = FilesData(stest)

    List_treeview = GenTreeview(root, RootFolder, "")

    root.mainloop()
