# population.py

import numpy as np
from config import N, tumor_size, grid_size, a, b, c, d, m
from fitness import fitness

def initialize_population():
    population = np.zeros((100, 100), dtype=int)

    # Introduce a small tumor at a random location
    random_x = np.random.randint(0, grid_size - tumor_size + 1)
    random_y = np.random.randint(0, grid_size - tumor_size + 1)
    population[random_x:random_x + tumor_size, random_y:random_y + tumor_size] = np.random.randint(11,16)
    
    return population

def mutate(cell):
    flip_idx = np.random.randint(4)
    return cell ^ (1 << flip_idx)

def update_population(pop):
    i = (pop >= 11).sum()  # Count of cancer cells
    
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
        healthy_indices = np.argwhere(pop < 11)
        if healthy_indices.size > 0:
            x, y = healthy_indices[np.random.choice(len(healthy_indices))]
            pop[x, y] = mutate(pop[x, y])  

    random_number = np.random.rand()

    # Cancer cell stay the same
    if random_number > P_birth_C + P_death_C:
        return pop

    # Cancer cell either dies or gives birth
    else:
        # Get all cancer indices
        cancer_indices = np.argwhere(pop == 1)
        if cancer_indices.size > 0:

            #Get the cancer cell
            cancer_cell = cancer_indices[np.random.choice(len(cancer_indices))]
            x, y = cancer_cell

            # Cancer cell births
            if random_number <= P_birth_C: 
            #Get all 8 neighbours of the cancer cell
                neighbours = [(x-1%grid_size, y), (x-1%grid_size, y+1%grid_size), (x,y+1%grid_size), (x+1%grid_size,y+1%grid_size), (x+1%grid_size,y), 
                            (x+1%grid_size,y-1%grid_size), (x,y-1%grid_size), (x-1%grid_size,y-1%N)]

                new_cell = np.random.choice(len(neighbours))
                print('cancer cell indices', x, y)
                print('New cell: ', neighbours[new_cell])
                pop[neighbours[new_cell]] = 1
            
            # Cancer cell dies
            else:
                pop[x, y] = 0

    return pop
