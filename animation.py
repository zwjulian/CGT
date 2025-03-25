import sys
from config import N, tumor_size, a, b, c, d, m
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from population import update_population

def create_animation(population):
    # Create two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))  # 1 row, 2 columns

    # Create initial images for the first plot (population grid)
    im1 = ax1.imshow(population, cmap='viridis', interpolation='nearest')

    # Setup for the second plot (number of cancer cells over time)
    ax2.set_xlabel('Frames')
    ax2.set_ylabel('Number of Cancer Cells')
    ax2.set_xlim(0, 1000)
    ax2.set_ylim(0, 1000)

    cancer_counts = []  # List to store number of cancer cells at each frame
    line, = ax2.plot([], [], label="Cancer Cells Count", color='red')
    ax2.legend()

    # Initialize function to set the first frame of both plots
    def init():
        im1.set_array(population)
        line.set_data([], [])
        return im1, line

    # Update function to modify both plots
    def update(frame):
        nonlocal population
        population[:] = update_population(population)  # Update the population

        # Update the first plot (population grid)
        im1.set_array(population)

        # Count the number of cancer cells (number of 1s in population)
        num_cancer_cells = np.sum(population == 1)
        cancer_counts.append(num_cancer_cells)  # Append the count of cancer cells

        line.set_data(range(len(cancer_counts)), cancer_counts)  # Update the line data

        return im1, line 

    # Create the animation with a maximum of 1000 frames
    ani = FuncAnimation(fig, update, frames=1000, init_func=init, repeat=False)

    # Show the plot
    plt.show()
