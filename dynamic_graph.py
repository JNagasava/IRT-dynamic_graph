import matplotlib.pyplot as plt
from matplotlib.artist import Artist
from matplotlib.widgets import Slider, Button, CheckButtons

from irt import IRT

class Dynamic_Graph:
    
    def __init__(self, model=IRT(), model2=IRT()):
        
        # Model e XY
        self.model = model
        self.x_icc, self.y_icc = model.icc_xy()
        self.x_iic, self.y_iic = model.iic_xy()

        # self.model2 = model2
        # self.x_icc2, self.y_icc2 = model2.icc_xy()
        # self.x_iic2, self.y_iic2 = model2.iic_xy()

        # Subplot
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.1, bottom=0.38)
        self.ax.set_ylim([-0.1, 1.1]) 
        self.info_plot()
        plt.grid()

        self.p1_icc, = plt.plot(self.x_icc, self.y_icc, linestyle='solid',linewidth=2, color='blue')
        self.p1_iic, = plt.plot(self.x_iic, self.y_iic, linestyle='dashed', linewidth=1, color='blue')
        self.p1_iic.set_visible(False)

        # self.p2_icc, = plt.plot(self.x_icc2, self.y_icc2, linestyle='solid',linewidth=2, color='red')
        # self.p2_iic, = plt.plot(self.x_iic2, self.y_iic2, linestyle='dashed', linewidth=1, color='red')
        # self.p2_icc.set_visible(False)
        # self.p2_iic.set_visible(False)

        # Sliders
        self.sliders = {'a': self.add_slider(axes=[0.24, 0.03, 0.6, 0.05], label=r'$\mathbb{a}$', valmin=0.0, valmax=3.0, valinit=2.0),
                        'b': self.add_slider(axes=[0.24, 0.13, 0.6, 0.05], label=r'$\mathbb{b}$', valmin=-3.0, valmax=3.0, valinit=0.0),
                        'c': self.add_slider(axes=[0.24, 0.23, 0.6, 0.05], label=r'$\mathbb{c}$', valmin=0.0, valmax=1.0, valinit=0.0, closedmax=False)} 

        # self.sliders2 = {'a': self.add_slider(axes=[0.5, 0.03, 0.25, 0.05], label='a', valmin=0.0, valmax=3.0, valinit=2.0),
        #                  'b': self.add_slider(axes=[0.5, 0.13, 0.25, 0.05], label='b', valmin=-3.0, valmax=3.0, valinit=0.0),
        #                  'c': self.add_slider(axes=[0.5, 0.23, 0.25, 0.05], label='c', valmin=0.0, valmax=1.0, valinit=0.0, closedmax=False)} 
        # self.sliders2['a'].ax.set_visible(False)
        # self.sliders2['b'].ax.set_visible(False)
        # self.sliders2['c'].ax.set_visible(False)

        self.update_sliders()

        # CheckButtons
        # self.checkbtns = CheckButtons(ax=plt.axes([0.1, 0.08, 0.1, 0.15]), labels=['ICC', 'IIC', '2 models'], actives=[True, False, False])
        self.checkbtns = CheckButtons(ax=plt.axes([0.1, 0.03, 0.1, 0.15]), labels=[r'$ICC$', r'$IIC$'], actives=[True, False])
        self.checkbtns.on_clicked(self.check)

        # Button
        self.btn = Button(ax=plt.axes([0.1, 0.21, 0.1, 0.07]), label='Reset')
        self.btn.on_clicked(self.reset)

    def info_plot(self, title=r'$ICC$', xlabel=r'$\theta$', ylabel=r'$P(\theta)$'):
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

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

        # self.sliders2['a'].on_changed(self.update_model)
        # self.sliders2['b'].on_changed(self.update_model)
        # self.sliders2['c'].on_changed(self.update_model)

    def update_model(self, val=None):

        self.model.a = self.sliders['a'].val
        self.model.b = self.sliders['b'].val
        self.model.c = self.sliders['c'].val
        self.y_icc = self.model.icc_xy()[1]
        self.p1_icc.set_ydata(self.y_icc)
        self.y_iic = self.model.iic_xy()[1]
        self.p1_iic.set_ydata(self.y_iic)

        # self.model2.a = self.sliders2['a'].val
        # self.model2.b = self.sliders2['b'].val
        # self.model2.c = self.sliders2['c'].val
        # self.y_icc2 = self.model2.icc_xy()[1]
        # self.p2_icc.set_ydata(self.y_icc2)
        # self.y_iic2 = self.model2.iic_xy()[1]
        # self.p2_iic.set_ydata(self.y_iic2)

        if self.p1_iic.get_visible() and max(self.y_iic) > 1.0:
            self.ax.set_ylim([-0.1, max(self.y_iic) + 0.1])
        else:
            self.ax.set_ylim([-0.1, 1.1])

        # if self.p2_iic.get_visible() and max(self.y_iic2) > 1.0:
        #     self.ax.set_ylim([-0.1, max(self.y_iic2) + 0.1])
        # else:
        #     self.ax.set_ylim([-0.1, 1.1])

        plt.draw()
    
    def check(self, label):

        if self.checkbtns.get_status()[0] and self.checkbtns.get_status()[1]:
            self.p1_icc.set_visible(True)
            self.p1_iic.set_visible(True)
            self.info_plot(title=r'$ICC$~$IIC$', xlabel=r'$\theta$', ylabel=r'$P(\theta)$~$I(\theta)$')
        
        elif self.checkbtns.get_status()[0] and not self.checkbtns.get_status()[1]:
            self.p1_icc.set_visible(True)
            self.p1_iic.set_visible(False)
            self.info_plot(title=r'$ICC$', xlabel=r'$\theta$', ylabel=r'$P$')

        elif not self.checkbtns.get_status()[0] and self.checkbtns.get_status()[1]:
            self.p1_icc.set_visible(False)
            self.p1_iic.set_visible(True)
            self.info_plot(title=r'$IIC$', xlabel=r'$\theta$', ylabel=r'$I$')
        
        elif not self.checkbtns.get_status()[0] and not self.checkbtns.get_status()[1]:
            self.p1_icc.set_visible(False)
            self.p1_iic.set_visible(False)
            self.info_plot(title='', xlabel='', ylabel='')
        
        # if self.checkbtns.get_status()[2]:
        #     self.p2_icc.set_visible(self.p1_icc.get_visible())
        #     self.p2_iic.set_visible(self.p1_iic.get_visible())
        #     self.sliders2['a'].ax.set_visible(True)
        #     self.sliders2['b'].ax.set_visible(True)
        #     self.sliders2['c'].ax.set_visible(True)

        #     self.sliders['a'].canvas = [0.3, 0.03, 0.2, 0.05]
        #     self.sliders['b'].canvas = [0.3, 0.13, 0.2, 0.05]
        #     self.sliders['c'].canvas = [0.3, 0.23, 0.2, 0.05]

        #     plt.draw()

        #     # self.sliders['a'].ax.set_axes([0.6, 0.03, 0.25, 0.05])
        #     # self.sliders['b'].ax.set_axes([0.6, 0.13, 0.25, 0.05])
        #     # self.sliders['c'].ax.set_axes([0.6, 0.23, 0.25, 0.05])

        #     # self.sliders['a'].set_ax = plt.axes([0.6, 0.03, 0.25, 0.05])
        #     # self.sliders['b'].set_ax = plt.axes([0.6, 0.13, 0.25, 0.05])
        #     # self.sliders['c'].set_ax = plt.axes([0.6, 0.23, 0.25, 0.05])
        
        # else:
        #     self.p2_icc.set_visible(False)
        #     self.p2_iic.set_visible(False)
        #     self.sliders2['a'].ax.set_visible(False)
        #     self.sliders2['b'].ax.set_visible(False)
        #     self.sliders2['c'].ax.set_visible(False)

        #     # self.sliders['a'].ax.set_ax([0.24, 0.03, 0.25, 0.05])
        #     # self.sliders['b'].ax.set_ax([0.24, 0.13, 0.25, 0.05])
        #     # self.sliders['c'].ax.set_ax([0.24, 0.23, 0.25, 0.05])

            
        #     # self.sliders['b'].set_ax = plt.axes([0.24, 0.13, 0.25, 0.05])
        #     # self.sliders['c'].set_ax = plt.axes([0.24, 0.23, 0.25, 0.05])


        self.update_model(None)

    def reset(self, val=None):

        self.sliders['a'].reset()
        self.sliders['b'].reset()
        self.sliders['c'].reset()

        self.update_model()


    def plot_show(self):
        plt.show()