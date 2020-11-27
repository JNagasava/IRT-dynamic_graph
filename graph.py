from math import exp
from numpy import linspace
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def irt(a=float, b=float, c=float, theta=float) -> float :
    return c + ( 1.0 - c ) / ( 1.0 + exp( -1.0 * a * ( theta - b ) ) )

a = 2.0
b = 0.0
c = 0.0

x = linspace(-3, 3, 1001)
y = [irt(a, b, c, i) for i in x]

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.35)
plt.grid()
plt.title('ICC')
plt.xlabel('theta')
plt.ylabel('P')
p, = plt.plot(x, y, linewidth=2, color='blue')

axSlider1 = plt.axes([0.1, 0.04, 0.8, 0.05])
slder1 = Slider(ax=axSlider1,
                label='a',
                valmin=0.0,
                valmax=3.0,
                valinit=2.0,
                valfmt="%1.2f",
                closedmax=True)

axSlider2 = plt.axes([0.1, 0.14, 0.8, 0.05])
slder2 = Slider(ax=axSlider2,
                label='b',
                valmin=-3.0,
                valmax=3.0,
                valinit=0.0,
                valfmt="%1.2f",
                closedmax=True)

axSlider3 = plt.axes([0.1, 0.24, 0.8, 0.05])
slder3 = Slider(ax=axSlider3,
                label='c',
                valmin=0.0,
                valmax=1.0,
                valinit=0.0,
                valfmt="%1.2f",
                closedmax=True)

def update_a(val):
    p.set_ydata([irt(slder1.val, slder2.val, slder3.val, i) for i in x])
    plt.draw()

def update_b(val):
    p.set_ydata([irt(slder1.val, slder2.val, slder3.val, i) for i in x])
    plt.draw()

def update_c(val):
    p.set_ydata([irt(slder1.val, slder2.val, slder3.val, i) for i in x])
    plt.draw()

slder1.on_changed(update_a)

slder2.on_changed(update_b)

slder3.on_changed(update_c)

plt.show()