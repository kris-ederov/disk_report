import tkinter, os
from tkinter import ttk
from disk_report_functions import ScanFolder, FolderSize, FormatSize
from disk_report_tree import GenTreeview
from disk_report_graph import GenGraph

def GenDiskReport(main_win, disk_path):
    main_win.title("Disk Reporter v0.1")

    frametop = tkinter.Frame(main_win, height = "40", width = "1470")
    frametop.pack(side = tkinter.TOP)
    frametop.pack_propagate(0)

    quit_button = tkinter.Button(frametop, text="Quit", command=quit)
    quit_button.pack(side = tkinter.RIGHT)
    
    framebot = tkinter.Frame(main_win)
    framebot.pack(side = tkinter.BOTTOM)

    framebot1 = tkinter.Frame(framebot)
    framebot1.pack(side = tkinter.LEFT)
    
    framebot2 = tkinter.Frame(framebot)
    framebot2.pack(side = tkinter.RIGHT)

    Graph = GenGraph(framebot2, disk_path)
    Treeview = GenTreeview(framebot1, disk_path, Graph)

stest = r"D:\Downloads"
stest2 = r"C:\Users\krissay\Documents"
stest3 = r"E:"

window = tkinter.Tk()

GenDiskReport(window, stest2)

window.mainloop()
