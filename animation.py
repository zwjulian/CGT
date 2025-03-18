# animation.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from population import update_population

def create_animation(population):
    fig, ax = plt.subplots()
    im = ax.imshow(population, cmap='viridis', interpolation='nearest')

    def init():
        im.set_array(population)
        return im,

    def update(frame):
        nonlocal population
        population[:] = update_population(population)
        im.set_array(population)
        return im,

    ani = FuncAnimation(fig, update, frames=200, init_func=init, blit=True)
    plt.show()
