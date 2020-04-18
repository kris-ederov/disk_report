import tkinter, os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot
from disk_report_functions import ScanFolder, FolderSize, FormatSize

class GenWin:
    def __init__(self, folder_path):
        self.folder_path = folder_path

        self.main_win = tkinter.Tk()
        self.main_win.title("Disk Reporter")
        self.main_win.geometry("1200x600")

        self.button2 = tkinter.Button(master=self.main_win, text="Quit", command=quit)
        self.button2.pack(side=tkinter.BOTTOM)

        self.fig = pyplot.figure(figsize=(6, 6), dpi=85, frameon=True)
        self.ax = self.fig.add_axes([0.1,0,.8,1])
        self.list_files, self.list_sizes = ScanFolder(self.folder_path, True)
        self.list_files_formatted = []
        for index, label in enumerate(self.list_files):
            self.list_files_formatted.append(label + "\n" + FormatSize(self.list_sizes[index]))
        self.ax.pie(self.list_sizes, labels = self.list_files_formatted, autopct='%1.1f%%')
        # ax.axis('equal')

        self.button3 = tkinter.Button(master=self.main_win, text="Test", command=lambda: self.TestFig())
        self.button3.pack(side=tkinter.BOTTOM)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_win)
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH)
        self.canvas.draw()

        tkinter.mainloop()
    
    def TestFig(self):
        # self.fig.clf()  --> To completely remove figure
        self.ax.clear()  # --> To only clear axis data (i.e. replace with some other data)
        testlist1 = ["aa", "bb", "cc"]
        testlist2 = [1, 2, 3]
        self.ax.pie(testlist2, labels = testlist1, autopct='%1.1f%%')
        self.canvas.draw()

if __name__ == "__main__":
    stest = r"D:\Downloads"
    stest2 = r"C:\Users\krissay\Documents"
    
    MainFig = GenWin(stest2)
