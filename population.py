# population.py

import numpy as np
from config import N, tumor_size, a, b, c, d, m
from fitness import fitness

def initialize_population():
    population = np.zeros((N, N), dtype=int)  # 0 = healthy, 1 = cancerous

    # Introduce a small tumor at a random location
    random_x = np.random.randint(0, N - tumor_size + 1)
    random_y = np.random.randint(0, N - tumor_size + 1)
    population[random_x:random_x + tumor_size, random_y:random_y + tumor_size] = 1
    
    return population

def update_population(pop):
    i = np.sum(pop)  # Count of cancer cells
    
    if i == 0:
        return pop  # If no cancer cells, return early
    
    pi_H = ((a * (N - i - 1)) + (b * i)) / (N - 1)
    pi_C = ((c * (N - i)) + (d * (i - 1))) / (N - 1)
    
    f_H = fitness(pi_H)
    f_C = fitness(pi_C)
    
    P_birth_C = (f_C * i) / (f_C * i + f_H * (N - i))
    P_birth_H = 1 - P_birth_C
    
    P_death_C = i / N
    P_death_H = (N - i) / N

    # Mutation
    if np.random.rand() < m:
        healthy_indices = np.argwhere(pop == 0)
        if healthy_indices.size > 0:
            x, y = healthy_indices[np.random.choice(len(healthy_indices))]
            pop[x, y] = 1  

    # Death
    if np.random.rand() < P_death_C:
        cancer_indices = np.argwhere(pop == 1)
        if cancer_indices.size > 0:
            x, y = cancer_indices[np.random.choice(len(cancer_indices))]
            pop[x, y] = 0  
    else:
        healthy_indices = np.argwhere(pop == 0)
        if healthy_indices.size > 0:
            x, y = healthy_indices[np.random.choice(len(healthy_indices))]
            pop[x, y] = 1  

    # Birth
    if np.random.rand() < P_birth_C:
        healthy_indices = np.argwhere(pop == 0)
        if healthy_indices.size > 0:
            x, y = healthy_indices[np.random.choice(len(healthy_indices))]
            pop[x, y] = 1  
    else:
        cancer_indices = np.argwhere(pop == 1)
        if cancer_indices.size > 0:
            x, y = cancer_indices[np.random.choice(len(cancer_indices))]
            pop[x, y] = 0  

    return pop
