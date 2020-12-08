from matplotlib.pyplot import subplots, subplots_adjust, grid, plot, axes, draw, show, close
from matplotlib.widgets import Slider, Button, CheckButtons

from irt import IRT

class Dynamic_Graph:
    '''
    Classe responsavel pelo grafico dinamica da TRI
    Neste grafico sera possivel realizar comparacoes 2 modelos
    e comparacoes entre a Curva caracteristica do item 
    pela Curva de Informacao do Item
    '''
    
    def __init__(self, model=IRT()):
        '''
        Funcao construtora da classe
        Nela sera feito a inicializacao do plot bem como
        as configuracoes iniciais do modelo de TRI

        Parametros
        ----------
        model : irt.IRT
            modelo de 3 parametros
        '''

        # Model e XY
        self.model = model
        self.x_icc, self.y_icc = model.icc()
        self.x_iic, self.y_iic = model.iic()

        # Subplot
        self.fig, self.ax = subplots()
        subplots_adjust(left=0.1, bottom=0.42)
        self.fig.canvas.set_window_title('Item Response Theory')
        self.ax.set_ylim([-0.1, 1.1]) 
        self.info_plot()
        grid()

        # Curvas do Model
        self.p_icc, = plot(self.x_icc, self.y_icc, linestyle='solid',linewidth=2, color='blue')
        self.p_iic, = plot(self.x_iic, self.y_iic, linestyle='dashed', linewidth=1, color='blue')
        self.p_iic.set_visible(False)

        # Second Model
        self.create_second_model()
        self.update_sliders(second_model=True)

        # Sliders
        self.sliders = {'a': self.add_slider(axes_values=[0.25, 0.23, 0.59, 0.05], 
                                             label=r'$\mathbb{a}$', 
                                             valmin=0.0, 
                                             valmax=5.0, 
                                             valinit=2.0),
                        'b': self.add_slider(axes_values=[0.25, 0.13, 0.59, 0.05], 
                                             label=r'$\mathbb{b}$', 
                                             valmin=-4.0, 
                                             valmax=4.0, 
                                             valinit=0.0),
                        'c': self.add_slider(axes_values=[0.25, 0.03, 0.59, 0.05], 
                                             label=r'$\mathbb{c}$', 
                                             valmin=0.0, 
                                             valmax=1.0, 
                                             valinit=0.0, 
                                             closedmax=False)} 
        self.update_sliders()

        # CheckButtons
        self.checkbtns = CheckButtons(ax=axes([0.1, 0.03, 0.1, 0.15]), labels=[r'$ICC$', r'$IIC$', r'$2nd$'], actives=[True, False, False])
        self.checkbtns.on_clicked(self.check)

        # Button
        self.btn = Button(ax=axes([0.1, 0.21, 0.1, 0.07]), label='Reset')
        self.btn.on_clicked(self.reset)

    def create_second_model(self):
        '''
        Cria um segundo modelo para usar, como comparacao,
        no plot e realiza as configuracoes necessarias
        '''

        # 2nd Model e XY
        self.second_model = IRT(a=self.model.a, b=self.model.b, c=self.model.c, theta_min=self.model.theta_min, theta_max=self.model.theta_max)
        self.second_x_icc, self.second_y_icc = self.second_model.icc()
        self.second_x_iic, self.second_y_iic = self.second_model.iic()

        # Curvas do 2nd Model
        self.second_p_icc, = plot(self.second_x_icc, self.second_y_icc, linestyle='solid',linewidth=2, color='red')
        self.second_p_iic, = plot(self.second_x_iic, self.second_y_iic, linestyle='dashed', linewidth=1, color='red')
        self.second_p_icc.set_visible(False)
        self.second_p_iic.set_visible(False)

        # Sliders do 2nd Model 
        self.second_sliders = {'a': self.add_slider(axes_values=[0.6, 0.23, 0.25, 0.05], 
                                                    label=r'$\mathbb{a}$', 
                                                    valmin=0.0, 
                                                    valmax=5.0, 
                                                    valinit=2.0, 
                                                    color='#d41526'),
                               'b': self.add_slider(axes_values=[0.6, 0.13, 0.25, 0.05], 
                                                    label=r'$\mathbb{b}$', 
                                                    valmin=-4.0, 
                                                    valmax=4.0, 
                                                    valinit=0.0, 
                                                    color='#d41526'),
                               'c': self.add_slider(axes_values=[0.6, 0.03, 0.25, 0.05], 
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
        '''
        Atribui o titulo do grafico e o significado
        dos eixos x e y

        Parametros
        ----------
            title : str
                titulo do grafico
            xlabel : str
                nome do eixo x
            ylabel : str
                nome do eixo y
        '''
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

    def add_slider(self, axes_values, label, valmin, valmax, valinit, valfmt="%1.2f", closedmax=True, color=None):
        '''
        Cria um novo slider a partir de determinadas configuracoes

        Parametros
        ----------
            axes_values : list(float, float, float, float)
                lista com a posicao do slider -> list(left, up, right, bottom)
            label : str
                nome do parametro do slider
            valmin : float
                valor minimo do parametro
            valmax : float
                valor maximo do parametro
            valinit : float
                valor inicial do parametro
            valfmt : str
                formatacao do valor corrente do parametro
            closedmax : bool
                indica se eh permitido usar o valor maximo do parametro
            color : str
                cor da barra do slider
        
        Retorno
        -------
            matplotlib.widgets.Slider
                retorna o slider criado
        '''
        axSlider = axes(axes_values)
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
        '''
        Atualiza os sliders

        Parametros
        ----------
            second_model : bool
                indica qual slider esta atualizando. Se second_model for False entao 
                atualiza o slider do model padrao, caso contrario atualiza o slider
                do second_model
         '''

        if not second_model:
            self.sliders['a'].on_changed(self.update_model)
            self.sliders['b'].on_changed(self.update_model)
            self.sliders['c'].on_changed(self.update_model)
        
        else:
            self.second_sliders['a'].on_changed(self.update_second_model)
            self.second_sliders['b'].on_changed(self.update_second_model)
            self.second_sliders['c'].on_changed(self.update_second_model)

    def update_model(self, val=None):
        '''
        Atualiza os valores do model e dependedo da situacao
        aumenta o limite de visualizacao do eixo y no grafico

        Parametros
        ----------
            val : float
                valor corrente do parametro (nao eh utilizado nesta funcao)
        '''

        # Atualiza os valores do model
        self.model.a = self.sliders['a'].val
        self.model.b = self.sliders['b'].val
        self.model.c = self.sliders['c'].val
        self.y_icc = self.model.icc()[1]
        self.p_icc.set_ydata(self.y_icc)
        self.y_iic = self.model.iic()[1]
        self.p_iic.set_ydata(self.y_iic)

        # Verifica o limite do eixo y
        if self.p_iic.get_visible():
            if self.second_p_iic.get_visible():
                self.ax.set_ylim([-0.1, max([1.0, max(self.y_iic), max(self.second_y_iic)]) + 0.1])
            else:
                self.ax.set_ylim([-0.1, max([1.0, max(self.y_iic)]) + 0.1])
        else:
            self.ax.set_ylim([-0.1, 1.1])

        draw()
    
    def update_second_model(self, val=None):
        '''
        Atualiza os valores do second_model e dependedo da situacao
        aumenta o limite de visualizacao do eixo y no grafico

        Parametros
        ----------
            val : float
                valor corrente do parametro (nao eh utilizado nesta funcao)
        '''
        
        # Atualiza os valores do second_model
        self.second_model.a = self.second_sliders['a'].val
        self.second_model.b = self.second_sliders['b'].val
        self.second_model.c = self.second_sliders['c'].val
        self.second_y_icc = self.second_model.icc()[1]
        self.second_p_icc.set_ydata(self.second_y_icc)
        self.second_y_iic = self.second_model.iic()[1]
        self.second_p_iic.set_ydata(self.second_y_iic)

        # Verifica o limite do eixo y
        if self.p_iic.get_visible():
            if self.second_p_iic.get_visible():
                self.ax.set_ylim([-0.1, max([1.0, max(self.y_iic), max(self.second_y_iic)]) + 0.1])
            else:
                self.ax.set_ylim([-0.1, max([1.0, max(self.y_iic)]) + 0.1])
        else:
            self.ax.set_ylim([-0.1, 1.1])

        draw()
    
    def check(self, label=None):
        '''
        Verifica o status dos checkbuttons para gerenciar o grafico.
        Dependendo da situacao, o grafico podera ter a Curva de Informacao
        do Item, a Curva Caracteristica do Item e um Segundo Modelo para servir
        de comparacao

        Parametros
        ----------
            label : str
                nome do checkbutton que mudou de estado (nao eh utilizado nesta funcao)
        '''

        # ICC e IIC
        if self.checkbtns.get_status()[0] and self.checkbtns.get_status()[1]:
            self.p_icc.set_visible(True)
            self.p_iic.set_visible(True)
            self.info_plot(title=r'$ICC$~$IIC$', xlabel=r'$\theta$', ylabel=r'$P(\theta)$~$I(\theta)$')
        
        # ICC
        elif self.checkbtns.get_status()[0] and not self.checkbtns.get_status()[1]:
            self.p_icc.set_visible(True)
            self.p_iic.set_visible(False)
            self.info_plot(title=r'$ICC$', xlabel=r'$\theta$', ylabel=r'$P(\theta)$')

        # IIC
        elif not self.checkbtns.get_status()[0] and self.checkbtns.get_status()[1]:
            self.p_icc.set_visible(False)
            self.p_iic.set_visible(True)
            self.info_plot(title=r'$IIC$', xlabel=r'$\theta$', ylabel=r'$I(\theta)$')
        
        # Nothing
        elif not self.checkbtns.get_status()[0] and not self.checkbtns.get_status()[1]:
            self.p_icc.set_visible(False)
            self.p_iic.set_visible(False)
            self.info_plot(title='', xlabel='', ylabel='')
        
        # 2nd Model - on
        if self.checkbtns.get_status()[2]:

                self.sliders['a'].ax.set_position([0.25, 0.23, 0.25, 0.05])
                self.sliders['b'].ax.set_position([0.25, 0.13, 0.25, 0.05])
                self.sliders['c'].ax.set_position([0.25, 0.03, 0.25, 0.05])
                
                self.second_p_icc.set_visible(self.checkbtns.get_status()[0])
                self.second_p_iic.set_visible(self.checkbtns.get_status()[1])

                self.second_sliders['a'].ax.set_visible(True)
                self.second_sliders['b'].ax.set_visible(True)
                self.second_sliders['c'].ax.set_visible(True)

        # 2nd Model - off
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
        '''
        Funcao de reset do plot, que quando eh acionado, volta-se
        para os valores iniciais do modelo
        '''
        
        self.sliders['a'].reset()
        self.sliders['b'].reset()
        self.sliders['c'].reset()

        self.second_sliders['a'].reset()
        self.second_sliders['b'].reset()
        self.second_sliders['c'].reset()

        self.update_model(None)
        self.update_second_model(None)


    def plot_show(self):
        '''
        Inicia a exibicao do plot
        '''
        show()
    
    def plot_close(self):
        '''
        Fecha a exibicao do plot
        '''
        close()