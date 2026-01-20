import matplotlib as mpl
import matplotlib.pyplot as plt
from random import randint
from time import sleep

class plots:
    def __init__(self, rows, cols, x, y):
        mpl.rcParams["axes.spines.right"] = False
        mpl.rcParams["axes.spines.top"] = False
        #fig is the entire screen and ax is the individual plots
        self.fig, self.ax = plt.subplots(rows, cols, figsize = (5, 6.5))
        self.intial_pos(x, y)
        self.fig.tight_layout()
        self.fig.subplots_adjust(hspace=0.6, left=.15, top=.95, right=.9, bottom=.1)
        #self.ax.spines['right'].set_visible(False)
        #self.ax.spines['top'].set_visible(False)
        plt.ion()
        self.fig.canvas.draw_idle()
        self.fig.show()
        self.titles = ['' for i in range(rows*cols)]
        self.xlabels = ['' for i in range(rows*cols)]
        self.ylabels = ['' for i in range(rows*cols)]
    
    #The coordinate is 
    def plot_data(self, coor, Xdata, Ydata, Ymin):
        ax = self.ax[coor]
        fig = self.fig
        #clears old data
        ax.cla()
        #adds data
        if isinstance(Xdata, list):
            ax.plot(Xdata, Ydata)
        elif isinstance(Xdata, dict):
            for key, lists in Xdata:
                ax.plot(Xdata, lists)

        #resets labels
        ax.set_title(self.titles[coor])
        ax.set_xlabel(self.xlabels[coor])
        ax.set_ylabel(self.ylabels[coor])
        #ylimit
        self.set_ymin(coor, Ymin)
        #redraw the whole figure
        fig.canvas.flush_events()
        fig.canvas.draw_idle()

    def intial_pos(self, x, y):
        self.fig.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    
    def label(self, coor, Xtitle, Ytitle, PlotTitle):
        ax = self.ax[coor]
        self.titles[coor] = PlotTitle
        self.xlabels[coor] = Xtitle
        self.ylabels[coor] = Ytitle
        ax.set_title(PlotTitle)
        ax.set_xlabel(Xtitle)
        ax.set_ylabel(Ytitle)
    
    def add_point(self, coor, Xdata, Ydata):
        ax = self.ax[coor]
        ax.scatter(Xdata, Ydata, c='blue')
        self.fig.canvas.draw_idle()

    def set_ymin(self, coor, ymin):
        ax = self.ax[coor]
        ax.set_ylim(bottom=ymin)
        self.fig.canvas.draw_idle()
