# config.py
import math

# Number of possible cells in the grid
N = 1024  

# Grid size
grid_size = math.floor(math.sqrt(N))

# Initial tumor size
tumor_size = 1

# Selection pressure
w = 0.5  

# Mutation probability
m = 0.1  

# Number of time steps
T = 40000  

# Payoff matrix for Prisoner's Dilemma
a, b, c, d = 3, 0, 5, 1
