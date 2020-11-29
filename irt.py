from numpy import linspace
from math import exp

class IRT:
    '''
    Classe com as informacoes do modelo de 3 parametros
    da TRI (Teoria de Resposta ao Item)
    Esta classe tambem tem a funcao de realizar os calculos da probabilidade
    de acerto de um item e da informacao do item 
    '''

    def __init__(self, a=2.0, b=0.0, c=0.0, theta_min=-3.0, theta_max=3.0):
        '''
        Funcao construtora da classe a qual atribui os valores dos parametros
        do modelo

        Parametros
        ----------
            a : float
                discriminate do item
            b : float
                dificuldade do item
            c : float
                chance de acerto ao acaso
            theta_min : float
                habilidade minima do individuo. Eh usado para a Curva Caracteristica
                do Item e para a Curva de Informacao do Item
            theta_max : float
                habilidade maxima do individuo. Eh usado para a Curva Caracteristica
                do Item e para a Curva de Informacao do Item
        '''
        self.a = a
        self.b = b
        self.c = c
        self.theta_min = theta_min
        self.theta_max = theta_max

    def probability(self, theta=float) -> float:
        '''
        Calcula a probabilidade de acertar o item partir da habilidade
        do individuo

        Parametros
        ----------
            theta : float
                habilidade do individuo
            
        Retorno
        -------
            float
                retorna a probabilidade de acertar o item
        '''
        return self.c + ( 1.0 - self.c ) / ( 1.0 + exp( -1.0 * self.a * ( theta - self.b ) ) )
    
    def icc(self, dots=1001):
        '''
        Gera os valores x e y da Curva Caracteristica do Item

        Parametros
        ----------
            dots : int
                quantidade de pontos na curva
        
        Retorno
        -------
            list(float...), list(float...)
                retorna os valores de x e y da Curva
        '''
        x = linspace(self.theta_min, self.theta_max, dots)
        y = [self.probability(k) for k in x]
        return x, y
    
    def infomation(self, theta=float) -> float:
        '''
        Calcula a informacao do item a partir da habilidade theta
        do individuo

        Parametros
        ----------
            theta : float
                habilidade do individuo
        
        Retorno
        -------
            float
                retorna a informacao do item
        '''
        p = self.probability(theta)
        q = 1 - p
        return self.a**2 * ( ( p - self.c )**2 / ( 1 - self.c )**2 ) * ( q / p )
    
    def iic(self, dots=1001):
        '''
        Gera os valores x e y da Curva de Informacao do Item

        Parametros
        ----------
            dots : int
                quantidade de pontos na curva
        
        Retorno
        -------
            list(float...), list(float...)
                retorna os valores de x e y da Curva
        '''
        x = linspace(self.theta_min, self.theta_max, dots)
        y = [self.infomation(k) for k in x]
        return x, y