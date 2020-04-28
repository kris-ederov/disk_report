import tkinter, os
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from disk_report_functions import ScanFolder, FolderSize, FormatSize

class GenGraph:
    def __init__(self, main_win, folder_path):
        self.main_win = main_win
        self.folder_path = folder_path
        self.fig_init_flg = False

        self.fig = pyplot.figure(figsize=(13, 6), dpi=80, frameon=True)
        self.figaxes = self.fig.add_axes([0.1,0,.8,1])

        self.SetFigAxes(self.folder_path)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_win)
        # self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

    def SetFigAxes(self, folder_path):
        self.folder_path = folder_path

        # self.fig.clf()  --> To completely remove figure
        self.figaxes.clear()  # --> To only clear axis data (i.e. replace with some other data)

        self.list_files, self.list_sizes, self.list_urls = ScanFolder(self.folder_path, True)
        self.list_files_formatted = []
        for index, label in enumerate(self.list_files):
            self.list_files_formatted.append(label + "\n" + FormatSize(self.list_sizes[index]))

        self.figaxes.pie(self.list_sizes, labels = self.list_files_formatted, autopct='%1.1f%%')
        # self.figaxes.axis('equal')
        if self.fig_init_flg: self.canvas.draw()
        self.fig_init_flg = True


if __name__ == "__main__":
    stest = r"D:\Downloads"
    stest2 = r"C:\Users\krissay\Documents"
    
    root = tkinter.Tk()
    MainFig = GenGraph(root, stest)
    root.mainloop()
