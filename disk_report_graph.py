import tkinter
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from disk_report_functions import FormatSize, FilesData

class GenGraph:
    def __init__(self, main_win, list_files, list_sizes):
        self.main_win = main_win
        self.list_files = list_files
        self.list_sizes = list_sizes

        self.fig_init_flg = False

        self.fig = pyplot.figure(figsize=(13, 6), dpi=80, frameon=True)
        self.figaxes = self.fig.add_axes([0.1,0,.8,1])

        self.SetFigAxes(self.list_files, self.list_sizes)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_win)
        # self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

    # def SetNewPath(self, folder_path):
    #     self.folder_path = folder_path

    #     RootFolder = FilesData(self.folder_path)
    #     self.list_files, self.list_sizes, self.list_urls = RootFolder.FolderContents(self.folder_path, True, True)

    #     self.SetFigAxes(self.list_files, self.list_sizes)

    def SetFigAxes(self, list_files, list_sizes):
        self.list_files = list_files
        self.list_sizes = list_sizes

        # self.fig.clf()  --> To completely remove figure
        self.figaxes.clear()  # --> To only clear axis data (i.e. replace with some other data)

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

    RootFolder = FilesData(stest)
    list_files, list_sizes, list_urls = RootFolder.FolderContents(stest, True, True)

    MainFig = GenGraph(root, list_files, list_sizes)

    root.mainloop()
    