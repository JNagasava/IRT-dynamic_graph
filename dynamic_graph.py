import matplotlib.pyplot as plt
from matplotlib.artist import Artist
from matplotlib.widgets import Slider, Button, CheckButtons

from irt import IRT

class Dynamic_Graph:
    
    def __init__(self, model=IRT()):
        
        # Model e XY
        self.model = model
        self.x_icc, self.y_icc = model.icc_xy()
        self.x_iic, self.y_iic = model.iic_xy()

        # Subplot
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.1, bottom=0.42)
        self.fig.canvas.set_window_title('Item Response Theory')
        self.ax.set_ylim([-0.1, 1.1]) 
        self.info_plot()
        plt.grid()

        self.p_icc, = plt.plot(self.x_icc, self.y_icc, linestyle='solid',linewidth=2, color='blue')
        self.p_iic, = plt.plot(self.x_iic, self.y_iic, linestyle='dashed', linewidth=1, color='blue')
        self.p_iic.set_visible(False)

        # Second Model
        self.create_second_model()
        self.update_sliders(second_model=True)

        # Sliders
        self.sliders = {'a': self.add_slider(axes=[0.25, 0.23, 0.59, 0.05], 
                                             label=r'$\mathbb{a}$', 
                                             valmin=0.0, 
                                             valmax=3.0, 
                                             valinit=2.0),
                        'b': self.add_slider(axes=[0.25, 0.13, 0.59, 0.05], 
                                             label=r'$\mathbb{b}$', 
                                             valmin=-3.0, 
                                             valmax=3.0, 
                                             valinit=0.0),
                        'c': self.add_slider(axes=[0.25, 0.03, 0.59, 0.05], 
                                             label=r'$\mathbb{c}$', 
                                             valmin=0.0, 
                                             valmax=1.0, 
                                             valinit=0.0, 
                                             closedmax=False)} 
        self.update_sliders()

        # CheckButtons
        self.checkbtns = CheckButtons(ax=plt.axes([0.1, 0.03, 0.1, 0.15]), labels=[r'$ICC$', r'$IIC$', r'$2nd$'], actives=[True, False, False])
        self.checkbtns.on_clicked(self.check)

        # Button
        self.btn = Button(ax=plt.axes([0.1, 0.21, 0.1, 0.07]), label='Reset')
        self.btn.on_clicked(self.reset)

    def create_second_model(self):

        self.second_model = IRT(a=self.model.a, b=self.model.b, c=self.model.c, theta_min=self.model.theta_min, theta_max=self.model.theta_max)
        self.second_x_icc, self.second_y_icc = self.second_model.icc_xy()
        self.second_x_iic, self.second_y_iic = self.second_model.iic_xy()

        self.second_p_icc, = plt.plot(self.second_x_icc, self.second_y_icc, linestyle='solid',linewidth=2, color='red')
        self.second_p_iic, = plt.plot(self.second_x_iic, self.second_y_iic, linestyle='dashed', linewidth=1, color='red')

        self.second_p_icc.set_visible(False)
        self.second_p_iic.set_visible(False)

        self.second_sliders = {'a': self.add_slider(axes=[0.6, 0.23, 0.25, 0.05], 
                                                    label=r'$\mathbb{a}$', 
                                                    valmin=0.0, 
                                                    valmax=3.0, 
                                                    valinit=2.0, 
                                                    color='#d41526'),
                               'b': self.add_slider(axes=[0.6, 0.13, 0.25, 0.05], 
                                                    label=r'$\mathbb{b}$', 
                                                    valmin=-3.0, 
                                                    valmax=3.0, 
                                                    valinit=0.0, 
                                                    color='#d41526'),
                               'c': self.add_slider(axes=[0.6, 0.03, 0.25, 0.05], 
                                                    label=r'$\mathbb{c}$', 
                                                    valmin=0.0, 
                                                    valmax=1.0, 
                                                    valinit=0.0, 
                                                    closedmax=False, 
                                                    color='#d41526')} 

        self.second_sliders['a'].ax.set_visible(False)
        self.second_sliders['b'].ax.set_visible(False)
        self.second_sliders['c'].ax.set_visible(False)

    def info_plot(self, title=r'$ICC$', xlabel=r'$\theta$', ylabel=r'$P(\theta)$'):
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

    def add_slider(self, axes, label, valmin, valmax, valinit, valfmt="%1.2f", closedmax=True, color=None):
        axSlider = plt.axes(axes)
        slider = Slider(ax=axSlider, 
                        label=label, 
                        valmin=valmin,
                        valmax=valmax,
                        valinit=valinit,
                        valfmt=valfmt,
                        closedmax=closedmax,
                        color=color)

        return slider
    
    def update_sliders(self, second_model=False):

        if not second_model:
            self.sliders['a'].on_changed(self.update_model)
            self.sliders['b'].on_changed(self.update_model)
            self.sliders['c'].on_changed(self.update_model)
        
        else:
            self.second_sliders['a'].on_changed(self.update_second_model)
            self.second_sliders['b'].on_changed(self.update_second_model)
            self.second_sliders['c'].on_changed(self.update_second_model)

    def update_model(self, val=None):

        self.model.a = self.sliders['a'].val
        self.model.b = self.sliders['b'].val
        self.model.c = self.sliders['c'].val
        self.y_icc = self.model.icc_xy()[1]
        self.p_icc.set_ydata(self.y_icc)
        self.y_iic = self.model.iic_xy()[1]
        self.p_iic.set_ydata(self.y_iic)

        if self.p_iic.get_visible() and max([max(self.y_iic), max(self.second_y_iic)]) > 1.0:
            self.ax.set_ylim([-0.1, max([max(self.y_iic), max(self.second_y_iic)]) + 0.1])
        else:
            self.ax.set_ylim([-0.1, 1.1])

        plt.draw()
    
    def update_second_model(self, val=None):

        self.second_model.a = self.second_sliders['a'].val
        self.second_model.b = self.second_sliders['b'].val
        self.second_model.c = self.second_sliders['c'].val
        self.second_y_icc = self.second_model.icc_xy()[1]
        self.second_p_icc.set_ydata(self.second_y_icc)
        self.second_y_iic = self.second_model.iic_xy()[1]
        self.second_p_iic.set_ydata(self.second_y_iic)

        if self.p_iic.get_visible() and max([max(self.y_iic), max(self.second_y_iic)]) > 1.0:
            self.ax.set_ylim([-0.1, max([max(self.y_iic), max(self.second_y_iic)]) + 0.1])
        else:
            self.ax.set_ylim([-0.1, 1.1])

        plt.draw()
    
    def check(self, label):

        if self.checkbtns.get_status()[0] and self.checkbtns.get_status()[1]:
            self.p_icc.set_visible(True)
            self.p_iic.set_visible(True)
            self.info_plot(title=r'$ICC$~$IIC$', xlabel=r'$\theta$', ylabel=r'$P(\theta)$~$I(\theta)$')
        
        elif self.checkbtns.get_status()[0] and not self.checkbtns.get_status()[1]:
            self.p_icc.set_visible(True)
            self.p_iic.set_visible(False)
            self.info_plot(title=r'$ICC$', xlabel=r'$\theta$', ylabel=r'$P(\theta)$')

        elif not self.checkbtns.get_status()[0] and self.checkbtns.get_status()[1]:
            self.p_icc.set_visible(False)
            self.p_iic.set_visible(True)
            self.info_plot(title=r'$IIC$', xlabel=r'$\theta$', ylabel=r'$I(\theta)$')
        
        elif not self.checkbtns.get_status()[0] and not self.checkbtns.get_status()[1]:
            self.p_icc.set_visible(False)
            self.p_iic.set_visible(False)
            self.info_plot(title='', xlabel='', ylabel='')
        
        if self.checkbtns.get_status()[2]:

                self.sliders['a'].ax.set_position([0.25, 0.23, 0.25, 0.05])
                self.sliders['b'].ax.set_position([0.25, 0.13, 0.25, 0.05])
                self.sliders['c'].ax.set_position([0.25, 0.03, 0.25, 0.05])
                
                self.second_p_icc.set_visible(self.checkbtns.get_status()[0])
                self.second_p_iic.set_visible(self.checkbtns.get_status()[1])

                self.second_sliders['a'].ax.set_visible(True)
                self.second_sliders['b'].ax.set_visible(True)
                self.second_sliders['c'].ax.set_visible(True)

        else:
            self.second_p_icc.set_visible(False)
            self.second_p_iic.set_visible(False)

            self.second_sliders['a'].ax.set_visible(False)
            self.second_sliders['b'].ax.set_visible(False)
            self.second_sliders['c'].ax.set_visible(False)

            self.sliders['a'].ax.set_position([0.25, 0.23, 0.59, 0.05])
            self.sliders['b'].ax.set_position([0.25, 0.13, 0.59, 0.05])
            self.sliders['c'].ax.set_position([0.25, 0.03, 0.59, 0.05])

        self.update_model(None)
        self.update_second_model(None)

    def reset(self, val=None):

        self.sliders['a'].reset()
        self.sliders['b'].reset()
        self.sliders['c'].reset()

        self.second_sliders['a'].reset()
        self.second_sliders['b'].reset()
        self.second_sliders['c'].reset()

        self.update_model(None)
        self.update_second_model(None)


    def plot_show(self):
        plt.show()