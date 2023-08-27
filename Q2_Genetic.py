import random

class Facility:
    def __init__(self, id, capacity, fixed_cost, operating_cost):
        self.id = id
        self.capacity = capacity
        self.fixed_cost = fixed_cost
        self.operating_cost = operating_cost
        self.customers = []

    def add_customer(self, customer):
        self.customers.append(customer)

    def remove_customer(self, customer):
        self.customers.remove(customer)

class Customer:
    def __init__(self, id, demand):
        self.id = id
        self.demand = demand

class GeneticAlgorithm:
    def __init__(self, population_size, num_generations, crossover_rate, mutation_rate):
        self.population_size = population_size
        self.num_generations = num_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.population = []

    def initialize_population(self, facilities, customers):
        for _ in range(self.population_size):
            chromosome = []
            for customer in customers:
                facility = random.choice(facilities)
                chromosome.append((customer.id, facility.id))
            self.population.append(chromosome)

    def evaluate_fitness(self, chromosome):
        total_cost = 0
        for customer_id, facility_id in chromosome:
            facility = facilities[facility_id]
            customer = customers[customer_id]
            total_cost += facility.fixed_cost + facility.operating_cost * customer.demand
        return -total_cost  # Minimize cost, so negate the value

    def select_parents(self):
        # Tournament selection
        tournament_size = 2
        parents = []
        for _ in range(2):
            tournament = random.sample(self.population, tournament_size)
            parent = max(tournament, key=lambda x: self.evaluate_fitness(x))
            parents.append(parent)
        return parents

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            crossover_point = random.randint(1, len(parent1) - 1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            return child1, child2
        else:
            return parent1, parent2

    def mutate(self, chromosome):
        mutated_chromosome = []
        for gene in chromosome:
            if random.random() < self.mutation_rate:
                customer_id, _ = gene
                facility_id = random.randint(0, len(facilities) - 1)
                mutated_gene = (customer_id, facility_id)
                mutated_chromosome.append(mutated_gene)
            else:
                mutated_chromosome.append(gene)
        return mutated_chromosome

    def evolve(self):
        for _ in range(self.num_generations):
            new_population = []

            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents()
                child1, child2 = self.crossover(parent1, parent2)
                mutated_child1 = self.mutate(child1)
                mutated_child2 = self.mutate(child2)
                new_population.extend([mutated_child1, mutated_child2])

            self.population = new_population

        best_chromosome = max(self.population, key=lambda x: self.evaluate_fitness(x))
        best_fitness = self.evaluate_fitness(best_chromosome)
        return best_chromosome, -best_fitness  # Return the positive fitness value

# Example usage
facilities = [
    Facility(id=0, capacity=100, fixed_cost=10, operating_cost=1),
    Facility(id=1, capacity=200, fixed_cost=20, operating_cost=2),
    Facility(id=2, capacity=150, fixed_cost=15, operating_cost=1.5)
]

customers = [
    Customer(id=0, demand=50),
    Customer(id=1, demand=80),
    Customer(id=2, demand=120)
]

ga = GeneticAlgorithm(population_size=10, num_generations=100, crossover_rate=0.8, mutation_rate=0.2)
ga.initialize_population(facilities, customers)
best_chromosome, best_fitness = ga.evolve()

print("Best Solution:", best_chromosome)
print("Best Cost:", best_fitness)
