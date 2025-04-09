# population.py

import numpy as np
from config import N, tumor_size, grid_size, a, b, c, d, m, immunotherapy_interval, immunotherapy_kill_fraction
from fitness import fitness

def initialize_population():
    population = np.zeros((grid_size, grid_size), dtype=int)
    # Introduce a small tumor at a random location
    random_xs = np.random.choice(range(grid_size - tumor_size + 1), size=1, replace=False)
    random_ys = np.random.choice(range(grid_size - tumor_size + 1), size=1, replace=False)

    print(random_xs)
    for random_x, random_y in zip(random_xs, random_ys):
        population[random_x:random_x + tumor_size, random_y:random_y + tumor_size] = 16

    return population

def mutate(cell):
    flip_idx = np.random.randint(4)
    return cell ^ (1 << flip_idx)

def update_population(pop, frame):
    i = (pop > 11).sum()  # Count of cancer cells
    
    if i == 0:
        return pop  # If no cancer cells, return early
    
    pi_H = ((a * (N - i - 1)) + (b * i)) / (N - 1)
    pi_C = ((c * (N - i)) + (d * (i - 1))) / (N - 1)
    
    f_H = fitness(pi_H)
    f_C = fitness(pi_C)
    
    P_birth_C = ( (i * f_C) / (i * f_C + (N - i) * f_H) ) * ( (N - i) / N)
    P_death_C = ( ( (N - i) * f_H) / (i * f_C + (N-i) * f_H) ) * (i / N)

    # Mutation
    if np.random.rand() < m:
        healthy_indices = np.argwhere(pop < 12)
        if healthy_indices.size > 0:
            x, y = healthy_indices[np.random.choice(len(healthy_indices))]
            pop[x, y] = mutate(pop[x, y])  

    random_number = np.random.rand()

    # Immunotherapy: Kill cancer cells at regular intervals
    if frame % immunotherapy_interval == 0 and frame > 0:
        cancer_indices = np.argwhere(pop > 11)
        if cancer_indices.size > 0:
            num_to_kill = int(len(cancer_indices) * immunotherapy_kill_fraction)
            indices_to_kill = np.random.choice(len(cancer_indices), num_to_kill, replace=False)
            for idx in indices_to_kill:
                x, y = cancer_indices[idx]
                pop[x, y] = 0  # Kill cancer cell

    # Cancer cell stay the same
    if random_number > P_birth_C + P_death_C:
        return pop

    # Cancer cell either dies or gives birth
    else:
        # Get all cancer indices
        cancer_indices = np.argwhere(pop > 11)
        if cancer_indices.size > 0:

            #Get the cancer cell
            cancer_cell = cancer_indices[np.random.choice(len(cancer_indices))]
            x, y = cancer_cell

            # Cancer cell births
            if random_number <= P_birth_C: 
                healthy_indices = np.argwhere(pop < 12)   

                if len(healthy_indices) > 0:
                    new_cell = np.random.choice(len(healthy_indices))
                    x,y = healthy_indices[new_cell].tolist()
                    pop[x,y] = np.random.randint(12,16) 
                else:
                    return pop
             
            # Cancer cell dies
            else:
                pop[x, y] = 0

    return pop
