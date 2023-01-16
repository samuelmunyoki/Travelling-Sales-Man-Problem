
from IPython.utils.path import random
import math

MUTATION_PROBALITY = 0.5
MAX_POPULATION = 30
MAX_ITERATIONS = 70

# Cities Data
CITIES = {"Codes": ["A", "B", "C", "D", "E"], "Distances": [[0, 100, 37, 50, 98],[99, 0, 87, 75, 170], [30, 69, 0, 83, 74], [58, 11, 96, 0,288], [249, 90, 90, 232, 0]]}

class Gene:
  Code = None
  def __init__(self, code):
    self.Code = code

class Chromosome: 
  Genes = []
  Fitness = 0

  def __init__(self, genes):
      self.Genes = genes

  def get_fitness(self):
    _fitness = 0
    for i in range(1, len(self.Genes)):
      current_gene = self.Genes[i-1].Code
      next_gene = self.Genes[i].Code
      current_gene_index = CITIES["Codes"].index(current_gene)
      next_gene_index = CITIES["Codes"].index(next_gene)
      _fitness += CITIES["Distances"][current_gene_index][next_gene_index]
      self.Fitness = _fitness
    return  self.Fitness


  def mutate(self, mutation_probabilty):
    number_of_genes = len(self.Genes)
    number_of_changes = math.floor(number_of_genes*mutation_probabilty)
    for _ in range(0, number_of_changes):
      random_index_1 = random.randrange(0, len(self.Genes))
      random_index_2 = random.randrange(0, len(self.Genes))
      self.Genes[random_index_1], self.Genes[random_index_2]  = self.Genes[random_index_2] , self.Genes[random_index_1] 
      new_chromosome = Chromosome(self.Genes)
    return new_chromosome
  

  def __str__(self):
    return f"Chromosome: {str(self.Genes)}"

def print_chromosome(chromosome):
  r = []
  for g in chromosome.Genes:
    r.append(g.Code)
  print("  -->  ".join(r))

def elitism(population):
  population_data = []
  for i in range(0, len(population)):
    c_fitness = population[i].get_fitness()
    population_data.append({"Fitness":c_fitness , "Chromosome": population[i]})
  population_data = sorted(population_data, key=lambda k: k['Fitness'], reverse=True)
  return population_data[0]["Chromosome"], population_data[1]["Chromosome"]

def crossover(chromosomeA, chromosomeB):
  ca_codes = []
  cb_codes = []
  adjacents = []
  clean_adjacents = []
  city_entries = []
  crossover_genes= []
  for i in range(0, len(chromosomeA.Genes)):
    ca_codes.append(chromosomeA.Genes[i].Code)
    cb_codes.append(chromosomeB.Genes[i].Code)
  for i in range(0, len(chromosomeA.Genes)):
    gene_code = ca_codes[i]
    l1 = None
    l2 = None
    r1 = None
    r2 = None
    if ca_codes.index(ca_codes[i])-1 >= 0:
      l1 = ca_codes[ca_codes.index(ca_codes[i])-1]
    if cb_codes.index(ca_codes[i])-1 >= 0:
      l2 = cb_codes[cb_codes.index(ca_codes[i])-1]
    if ca_codes.index(ca_codes[i]) < len(chromosomeA.Genes)-1:
      r1 = ca_codes[ca_codes.index(ca_codes[i])+1]
    if cb_codes.index(ca_codes[i]) < len(chromosomeA.Genes)-1:
      r2 = cb_codes[cb_codes.index(ca_codes[i])+1]
    adjacents.append({gene_code: [l1, l2, r1, r2]})
  for i in range(0, len(adjacents)):
    for key, value in adjacents[i].items():
      k = key
      v = list(filter(lambda x : x != None, value))
      v= set(v)
      clean_adjacents.append({k: list(v)})
  current_city = random.choice(CITIES["Codes"])
  random_parent = random.choice([chromosomeA, chromosomeA])
  current_city = random_parent.Genes[0].Code
  crossover_genes.append(current_city)
  city_arr = [list(t.values())[0] for i, t in enumerate(clean_adjacents) ]
  for node in CITIES["Codes"]:
      city_entries.append({node: sum(x.count(node) for x in city_arr)})
  city_entries = sorted(city_entries, key=lambda k: list(k.values())[0])
  for node in city_entries:
    if list(node.keys())[0] not in crossover_genes:
      crossover_genes.append(list(node.keys())[0])
  child = []
  
  for gene_code in crossover_genes:
    child.append(Gene(gene_code))
  child_chromosome  = Chromosome(child)
  return child_chromosome

def initialize_population( population_size):
  initial_population = []
  for i in range(0, population_size):
    arr = random.sample(CITIES["Codes"], k = len(CITIES["Codes"]))
    child = []
    for gene_code in arr:
      child.append(Gene(gene_code))
    c = Chromosome(child)
    initial_population.append(c)
  return initial_population

def generate_solution(population_size):
  population = initialize_population(population_size)
  c1, c2 = elitism(population)
  best_fitness = 0
  bestChromosome = population[0]
  c1_fitness = c1.get_fitness()
  c2_fitness = c2.get_fitness()
    # Check Fitness
  best_fitness = c1_fitness
  if c2_fitness <= best_fitness:
    best_fitness <= c2_fitness
    
  for i in range(1, MAX_ITERATIONS):
    # CrossOver
    ca = crossover(c1,c2)
    # Mutate
    c1 = ca.mutate(MUTATION_PROBALITY)
    c1_fitness = c1.get_fitness()
    if c1_fitness <= best_fitness:
      best_fitness = c1_fitness
      bestChromosome = c1
    if i == MAX_ITERATIONS-1:
      print("-------------------------------------------\nShortest Distance : {}\n-------------------------------------------".format(best_fitness))
      print_chromosome(c1)
      print("-------------------------------------------\n") 



generate_solution(population_size = MAX_POPULATION)