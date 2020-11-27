import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

from irt import IRT

class Dynamic_Graph:
    
    def __init__(self, model=IRT()):
        
        # Model e XY
        self.model = model
        self.x, self.y = model.icc_xy()

        # Subplot
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.1, bottom=0.35)
        self.info_plot()
        plt.grid()
        self.p, = plt.plot(self.x, self.y, linewidth=2, color='blue')

        # Sliders
        self.sliders = {'a': self.add_slider(axes=[0.1, 0.04, 0.8, 0.05], label='a', valmin=0.0, valmax=3.0, valinit=2.0),
                        'b': self.add_slider(axes=[0.1, 0.14, 0.8, 0.05], label='b', valmin=-3.0, valmax=3.0, valinit=0.0),
                        'c': self.add_slider(axes=[0.1, 0.24, 0.8, 0.05], label='c', valmin=0.0, valmax=1.0, valinit=0.0)} 
        self.update_sliders()
        
        
    def info_plot(self, title='ICC', xlabel='theta', ylabel='P'):
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

    def add_slider(self, axes, label, valmin, valmax, valinit, valfmt="%1.2f", closedmax=True):
        axSlider = plt.axes(axes)
        slider = Slider(ax=axSlider, 
                        label=label, 
                        valmin=valmin,
                        valmax=valmax,
                        valinit=valinit,
                        valfmt=valfmt,
                        closedmax=closedmax)
        return slider
    
    def update_sliders(self):
        self.sliders['a'].on_changed(self.update_model)
        self.sliders['b'].on_changed(self.update_model)
        self.sliders['c'].on_changed(self.update_model)

    def update_model(self, val):
        self.model.a = self.sliders['a'].val
        self.model.b = self.sliders['b'].val
        self.model.c = self.sliders['c'].val
        self.p.set_ydata(self.model.icc_xy()[1])
        plt.draw()

    def plot_show(self):
        plt.show()