import tkinter, os, shutil
# from tkinter import ttk, filedialog
from disk_report_functions import ScanFolder, FolderSize, FormatSize
from disk_report_tree import GenTreeview
from disk_report_graph import GenGraph

def SetPathLabelText(Label_text, text):
    Label_text.set("  Contents of folder:  " + str(text))

def OpenFolder(Treeview, Graph, LabelPath_text, LabelDrive_text, LabelSpaceUsed_text, used_percent):
    folder_path = tkinter.filedialog.askdirectory()
    Treeview.NewLevel(folder_path)
    Graph.SetFigAxes(folder_path)
    SetPathLabelText(LabelPath_text, folder_path)
    SetDiskLabels(LabelDrive_text, LabelSpaceUsed_text, used_percent, folder_path)
    
def SetDiskLabels(LabelDrive_text, LabelSpaceUsed_text, used_percent, disk_path):
    drive_letter, temp = os.path.splitdrive(disk_path)
    total, used, free = shutil.disk_usage(disk_path)
    used_percent.set(used / total * 100)
    
    LabelDrive_text.set("Drive " + drive_letter)
    LabelSpaceUsed_text.set(FormatSize(free) + " free of " + FormatSize(total))

def GenDiskReport(main_win, disk_path):
    LabelPath_text = tkinter.StringVar()
    SetPathLabelText(LabelPath_text, disk_path)
    LabelDrive_text = tkinter.StringVar()
    LabelSpaceUsed_text = tkinter.StringVar()
    used_percent = tkinter.DoubleVar()

    main_win.title("Disk Reporter v0.1")

    frametop = tkinter.Frame(main_win, height = "40", width = "1460")
    frametop.pack(side = tkinter.TOP)
    frametop.pack_propagate(0)

    framebot = tkinter.Frame(main_win, height = "80", width = "1460")
    framebot.pack(side = tkinter.BOTTOM)
    framebot.pack_propagate(0)
    
    framemid = tkinter.Frame(main_win)
    framemid.pack(side = tkinter.BOTTOM)

    framemid1 = tkinter.Frame(framemid)
    framemid1.pack(side = tkinter.LEFT)
    
    framemid2 = tkinter.Frame(framemid)
    framemid2.pack(side = tkinter.RIGHT)

    framebot1 = tkinter.Frame(framebot, height = "80", width = "360")
    framebot1.pack(side = tkinter.LEFT)
    framebot1.pack_propagate(0)

    framebot2 = tkinter.Frame(framebot, height = "80", width = "600")
    framebot2.pack(side = tkinter.LEFT)
    framebot2.pack_propagate(0)

    Graph = GenGraph(framemid2, disk_path)
    Treeview = GenTreeview(framemid1, disk_path, Graph)

    LabelPath = tkinter.Label(frametop, textvariable = LabelPath_text)

    global open_icon
    open_icon = tkinter.PhotoImage(file = "icons\\open.png")
    open_button = tkinter.Button(frametop, text = " Select folder ", image = open_icon, compound = tkinter.LEFT, 
        command = lambda: OpenFolder(Treeview, Graph, LabelPath_text, LabelDrive_text, LabelSpaceUsed_text, used_percent))
    open_button.pack(side = tkinter.LEFT)
    LabelPath.pack(side = tkinter.LEFT)

    quit_button = tkinter.Button(frametop, text = "Quit", command = quit)
    quit_button.pack(side = tkinter.RIGHT)

    LabelDesc = tkinter.Label(framebot1, text = "Click on folder for preview in chart; Double click to open in explorer")
    LabelDesc.pack(side = tkinter.TOP)

    # Drive Information section
    SetDiskLabels(LabelDrive_text, LabelSpaceUsed_text, used_percent, disk_path)

    LabelDrive = tkinter.Label(framebot2, textvariable = LabelDrive_text)
    LabelDrive.pack(side = tkinter.TOP)

    DriveBar = tkinter.ttk.Progressbar(framebot2, orient = "horizontal", length = 400, variable = used_percent, mode = "determinate")
    DriveBar.pack(side = tkinter.TOP)

    LabelSpaceUsed = tkinter.Label(framebot2, textvariable = LabelSpaceUsed_text)
    LabelSpaceUsed.pack(side = tkinter.TOP)

stest = r"D:\Downloads"
stest2 = r"C:\Users\krissay\Documents"
stest3 = r"E:"

window = tkinter.Tk()

GenDiskReport(window, stest)

window.mainloop()
