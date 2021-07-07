#
#  DataPlot Utils for using on Ubuntu linux with Tk and QT problems to show graphics
#
#  Cristiano S Oliveira (out0)

from tkinter import ttk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter.constants import W
from typing import Callable
import matplotlib
from numpy import void
from threading import Thread
matplotlib.use("TkAgg")


class PlotWindow(tk.Tk):
    def __init__(self, title: str, w: int, h: int, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, title)
        self.geometry('{0}x{1}'.format(w, h))
        self.figure = Figure()

    # def NewPage(self, title: str, f):
    def new_plot(self, title: str, line: int, col_num: int, col_pos: int) -> matplotlib.axes.Axes:
        subplot = self.figure.add_subplot(line, col_num, col_pos)
        if title:
            subplot.set_title(title)
        return subplot

    def show(self):
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.after(1000, self.__upd)
        self.mainloop()

    def __upd(self):
        self.canvas.draw()
        self.after(250, self.__upd)

    def close(self):
        self.quit();
        


class BackgroundTask(Thread):
    def __init__(self, window: PlotWindow, task: Callable[[PlotWindow], void]):
        Thread.__init__(self)
        self.window = window
        self.task = task
        self.start()

    def run(self):
        self.task(self.window)

class PlotApp:
    def __init__(self, title: str, width: int, height: int):
         self.window = PlotWindow(title, width, height)

    def PlotContext(self, window: PlotWindow) -> void:
        pass

    def show(self) -> void:
        BackgroundTask(self.window, self.PlotContext)
        self.window.show()


class MyPlotApp(PlotApp):
    def PlotContext(self, window: PlotWindow):
        input('press enter to plot first results');

        plot = window.new_plot("aaa", 1, 2, 1)
        X = [1, 2, 3, 4, 5, 6, 7]
        Y = [1, 2, 3, 4, 5, 6, 7]
        plot.plot(X, Y, 'ro', ms=10, mec='k')
        plot.set_ylabel('Profit in $10,000')
        plot.set_xlabel('Population of City in 10,000s')

        input('press enter to plot next results');

        plot2 = window.new_plot(None, 1, 2, 2)
        X = [1, 2, 3, 4, 5, 6, 7]
        Y = [1, 2, 3, 4, 5, 6, 7]
        plot2.plot(X, Y, 'ro', ms=10, mec='k')
        plot2.set_ylabel('Profit2 in $10,000')
        plot2.set_xlabel('Population2 of City in 10,000s')

        input('press enter to close');
        window.close()



def main():
    app = MyPlotApp("teste", 1600, 700)
    app.show()
    print("done")

if __name__ == '__main__':
    main()
