# main.py

from population import initialize_population
from animation import create_animation

def main():
    """Main function to run the tumor growth simulation."""
    population = initialize_population()
    create_animation(population)

if __name__ == "__main__":
    main()