import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot
import numpy as np

def _draw():
    # fig2 = Figure(figsize=(5, 4), dpi=100)
    # t = np.arange(0, 3, .01)
    # fig2.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

    fig = pyplot.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.axis('equal')
    langs = ['C', 'C++', 'Java', 'Python', 'PHP']
    students = [23,17,35,29,12]
    ax.pie(students, labels = langs,autopct='%1.2f%%')

    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

root = tkinter.Tk()
root.wm_title("Embedding in Tk")

button = tkinter.Button(master=root, text="Draw", command=_draw)
button.pack(side=tkinter.BOTTOM)

tkinter.mainloop()
