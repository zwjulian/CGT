import sys
from config import N, tumor_size, grid_size, T, a, b, c, d, m
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from population import update_population

def create_animation(population):
    # Create two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))  # 1 row, 2 columns

    # Create initial images for the first plot (population grid)
    im1 = ax1.imshow(population, cmap='viridis', interpolation='nearest', vmin=0, vmax=15)

    # Setup for the second plot (number of cancer cells over time)
    ax2.set_xlabel('Frames')
    ax2.set_ylabel('Number of Cancer Cells')
    ax2.set_xlim(0, T)
    ax2.set_ylim(0, N)
    ax2.set_xticks(np.arange(0, T+1, 5000))  # or choose another interval if needed
    ax2.set_xticklabels([f"{x/10000:.1f}" for x in np.arange(0, T+1, 5000)])
    ax2.set_xlabel(r'Frames($\times 10^4$)')

    cancer_counts = []  # List to store number of cancer cells at each frame
    line, = ax2.plot([], [], label="Cancer Cells Count", color='red')
    ax2.legend()


    # Colorbar to represent different cell states
    cbar = fig.colorbar(im1, ax=ax1, orientation='vertical', location='left', fraction=0.02, pad=0.1)
    cbar.set_label('Cell State')
    
    # You can customize the ticks and labels on the colorbar if needed
    cbar.set_ticks([0, 5, 10, 15])
    cbar.set_ticklabels(['Healthy', 'Mutated', 'Tumor', 'Tumor'])
    plt.savefig('initial_population.png')

    # Initialize function to set the first frame of both plots
    def init():
        im1.set_array(population)
        line.set_data([], [])
        return im1, line

    # Update function to modify both plots
    def update(frame):
        nonlocal population
        population[:] = update_population(population, frame)  # Update the population

        im1.set_array(population)

        # Count the number of cancer cells (number of 1s in population)
        num_cancer_cells = np.sum(population >= 11)
        cancer_counts.append(num_cancer_cells) 

        line.set_data(range(len(cancer_counts)), cancer_counts) 

        if frame % 5000 == 0: 
            plt.savefig(f'population_frame_{frame}.png')

        return im1, line 

    # Create the animation with a maximum of 1000 frames
    ani = FuncAnimation(fig, update, frames=T, init_func=init, repeat=False)

    # Show the plot
    plt.show()
