import tkinter, os
from tkinter import ttk, filedialog
from disk_report_functions import ScanFolder, FolderSize, FormatSize
from disk_report_tree import GenTreeview
from disk_report_graph import GenGraph

def SetLabelText(Label_text, text):
    Label_text.set("  Contents of folder:  " + str(text))

def OpenFolder(Treeview, Graph, LabelPath_text):
    folder_path = tkinter.filedialog.askdirectory()
    Treeview.NewLevel(folder_path)
    Graph.SetFigAxes(folder_path)
    SetLabelText(LabelPath_text, folder_path)

def GenDiskReport(main_win, disk_path):
    main_win.title("Disk Reporter v0.1")

    frametop = tkinter.Frame(main_win, height = "40", width = "1460")
    frametop.pack(side = tkinter.TOP)
    frametop.pack_propagate(0)

    framebot = tkinter.Frame(main_win, height = "40", width = "1460")
    framebot.pack(side = tkinter.BOTTOM)
    framebot.pack_propagate(0)
    
    framemid = tkinter.Frame(main_win)
    framemid.pack(side = tkinter.BOTTOM)

    framemid1 = tkinter.Frame(framemid)
    framemid1.pack(side = tkinter.LEFT)
    
    framemid2 = tkinter.Frame(framemid)
    framemid2.pack(side = tkinter.RIGHT)

    Graph = GenGraph(framemid2, disk_path)
    Treeview = GenTreeview(framemid1, disk_path, Graph)

    LabelPath_text = tkinter.StringVar()
    SetLabelText(LabelPath_text, disk_path)
    LabelPath = tkinter.Label(frametop, textvariable = LabelPath_text)

    global open_icon
    open_icon = tkinter.PhotoImage(file = "icons\\open.png")
    open_button = tkinter.Button(frametop, text = " Select folder ", image = open_icon, compound = tkinter.LEFT, 
        command = lambda: OpenFolder(Treeview, Graph, LabelPath_text))
    open_button.pack(side = tkinter.LEFT)
    LabelPath.pack(side = tkinter.LEFT)

    quit_button = tkinter.Button(frametop, text = "Quit", command = quit)
    quit_button.pack(side = tkinter.RIGHT)

    LabelDesc = tkinter.Label(framebot, text = "Double click on folder for preview in chart")
    LabelDesc.pack(side = tkinter.LEFT)


stest = r"D:\Downloads"
stest2 = r"C:\Users\krissay\Documents"
stest3 = r"E:"

window = tkinter.Tk()

GenDiskReport(window, stest2)

window.mainloop()
