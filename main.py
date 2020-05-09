import tkinter, os, shutil
from pathlib import Path
from disk_report_functions import FormatSize, FilesData
from disk_report_tree import GenTreeview
from disk_report_graph import GenGraph

def CreateFrame(frame_parent, frame_height, frame_width, frame_side):
    frame = tkinter.Frame(frame_parent)
    if frame_height != 0: frame.configure(height = frame_height)
    if frame_width != 0: frame.configure(width = frame_width)
    frame.pack(side = frame_side)
    if frame_height != 0: frame.pack_propagate(0)
    return frame

def SetPathLabelText(Label_text, text):
    Label_text.set("  Contents of folder:  " + str(text))
    
def SetDiskLabels(LabelDrive_text, LabelSpaceUsed_text, used_percent, disk_path):
    drive_letter, temp = os.path.splitdrive(disk_path)
    total, used, free = shutil.disk_usage(disk_path)
    used_percent.set(used / total * 100)
    
    LabelDrive_text.set("Drive " + drive_letter)
    LabelSpaceUsed_text.set(FormatSize(free) + " free of " + FormatSize(total))

def SaveScan(RootFolder):
    save_path = tkinter.filedialog.asksaveasfilename(title = "Save scan to file", filetypes = (("Text files", ".txt"),("all files","*.*")), defaultextension = ".txt")
    RootFolder.SaveTo(save_path)

def OpenFolder(RootFolder, Treeview, Graph, LabelPath_text, LabelDrive_text, LabelSpaceUsed_text, used_percent, file_flg):
    """ file_flg indicates whether this is a new folder scan or retrieve saved scan from a file """
    if file_flg:
        scan_path = tkinter.filedialog.askopenfilename(title = "Open scan from file", filetypes = (("Text files", ".txt"),("all files","*.*")))
        RootFolder.init(scan_path)
        folder_path = RootFolder.MainFolderPath()
    else: 
        folder_path = tkinter.filedialog.askdirectory()
        RootFolder.init(folder_path)

    list_files, list_sizes, list_urls = RootFolder.FolderContents(folder_path, True, True)

    Treeview.NewTree(RootFolder)
    Graph.SetFigAxes(list_files, list_sizes)

    SetPathLabelText(LabelPath_text, folder_path)
    SetDiskLabels(LabelDrive_text, LabelSpaceUsed_text, used_percent, folder_path)

def GenDiskReport(main_win, disk_path):
    LabelPath_text = tkinter.StringVar()
    LabelDrive_text = tkinter.StringVar()
    LabelSpaceUsed_text = tkinter.StringVar()
    used_percent = tkinter.DoubleVar()

    main_win.title("Disk Reporter v0.1")
    frametop    = CreateFrame(main_win, 40, 1460, tkinter.TOP)
    framebot    = CreateFrame(main_win, 80, 1460, tkinter.BOTTOM)
    framemid    = CreateFrame(main_win,  0,    0, tkinter.BOTTOM)
    framemid1   = CreateFrame(framemid,  0,    0, tkinter.LEFT)
    framemid2   = CreateFrame(framemid,  0,    0, tkinter.RIGHT)
    framebot1   = CreateFrame(framebot, 80,  360, tkinter.LEFT)
    framebot2   = CreateFrame(framebot, 80,  600, tkinter.LEFT)
    framebot1_1 = CreateFrame(framebot1, 0,    0, tkinter.TOP)
    framebot1_2 = CreateFrame(framebot1, 0,    0, tkinter.TOP)

    # Table d'hôte
    RootFolder = FilesData(disk_path)
    list_files, list_sizes, list_urls = RootFolder.FolderContents(disk_path, True, True)

    Graph = GenGraph(framemid2, list_files, list_sizes)
    Treeview = GenTreeview(framemid1, RootFolder, Graph)

    # Top frame widgets
    # icon_folder = Path(os.path.dirname(__file__))
    # global open_icon
    # open_icon = tkinter.PhotoImage(file = icon_folder / "icons" / "open.png")
    
    NewScan_button = tkinter.Button(frametop, text = " Select folder to scan ", compound = tkinter.LEFT, #image = open_icon,
        command = lambda: OpenFolder(RootFolder, Treeview, Graph, LabelPath_text, LabelDrive_text, LabelSpaceUsed_text, used_percent, False))
    NewScan_button.pack(side = tkinter.LEFT)

    SetPathLabelText(LabelPath_text, disk_path)
    LabelPath = tkinter.Label(frametop, textvariable = LabelPath_text)
    LabelPath.pack(side = tkinter.LEFT)

    # Bottom frame widgets
    LabelDesc = tkinter.Label(framebot1_1, text = "Click on folder for preview in chart; Double click to open in explorer")
    LabelDesc.pack(side = tkinter.TOP)

    OpenScan_button = tkinter.Button(framebot1_2, text = " Open scan from file ", compound = tkinter.LEFT, #image = open_icon,
        command = lambda: OpenFolder(RootFolder, Treeview, Graph, LabelPath_text, LabelDrive_text, LabelSpaceUsed_text, used_percent, True))
    OpenScan_button.pack(side = tkinter.LEFT)

    SaveScan_button = tkinter.Button(framebot1_2, text = " Save scan to file ", 
        command = lambda: SaveScan(RootFolder))
    SaveScan_button.pack(side = tkinter.RIGHT)

    # Drive Information section
    SetDiskLabels(LabelDrive_text, LabelSpaceUsed_text, used_percent, disk_path)

    LabelDrive = tkinter.Label(framebot2, textvariable = LabelDrive_text)
    LabelDrive.pack(side = tkinter.TOP)

    DriveBar = tkinter.ttk.Progressbar(framebot2, orient = "horizontal", length = 400, variable = used_percent, mode = "determinate")
    DriveBar.pack(side = tkinter.TOP)

    LabelSpaceUsed = tkinter.Label(framebot2, textvariable = LabelSpaceUsed_text)
    LabelSpaceUsed.pack(side = tkinter.TOP)

    # Needed to close window properly when 'X' is pressed
    main_win.protocol("WM_DELETE_WINDOW", lambda item1 = Graph, item2 = main_win: CloseWin(item1, item2))

def CloseWin(item1, item2):
    item1.CloseFigure()
    item2.destroy()

stest = r"D:\Downloads"
stest2 = r"C:\Users\krissay\Documents"
stest3 = r"E:"
stest4 = "C:\\"
stest5 = os.getcwd()

window = tkinter.Tk()

GenDiskReport(window, stest5)

window.mainloop()
