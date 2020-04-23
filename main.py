import tkinter, os
from tkinter import ttk
from disk_report_functions import ScanFolder, FolderSize, FormatSize
from disk_report_tree import GenTreeview
from disk_report_graph import GenGraph

main_win = tkinter.Tk()
main_win.title("Disk Reporter v0.1")

frame1 = tkinter.Frame(main_win, bg = "green")
frame1.pack(side = tkinter.LEFT, fill = tkinter.Y)
 
frame2 = tkinter.Frame(main_win, bg = "blue")
frame2.pack(side = tkinter.RIGHT)

# frame3 = tkinter.Frame(main_win, width=200, height=100, bg = "yellow")
# frame3.pack(side = tkinter.BOTTOM)

# quit_button3 = tkinter.Button(frame3, text="Quit", command=quit)
# quit_button3.pack()

stest = r"D:\Downloads"
stest2 = r"C:\Users\krissay\Documents"
stest3 = r"E:"

Graph = GenGraph(frame2, stest)
Treeview = GenTreeview(frame1, stest, Graph)

main_win.mainloop()
