# fitness.py

from config import w

def fitness(payoff):
    """Calculate fitness based on payoff and selection pressure."""
    return 1 - w + w * payoff  
