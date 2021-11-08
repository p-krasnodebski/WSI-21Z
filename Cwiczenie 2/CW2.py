import copy
import matplotlib.pyplot as plt
import random
import numpy as np
import time



def q(x): 
  """Funckja obliczająca wartość funckji celu.
  Argumentem jest lista zmiennych."""
  # return x**2
  # return x[0]**4 - 5*(x[0]**2) - 3*x[0]
  # return 2*x[0]**2 + 2*(x[1]**2) - 4
  # return np.sin(x[0])*(np.exp(1-np.cos(x[1]))**2)+np.cos(x[1])*(np.exp(1-np.sin(x[0]))**2)+(x[0]-x[1])**2

  sum1=0
  sum2=0
  for i in range(1,6):
      sum1 = sum1 + (i* np.cos(((i+1)*x[0]) +i))
      sum2 = sum2 + (i* np.cos(((i+1)*x[1]) +i))

  return sum1 * sum2

def column(matrix, i):
  """Zwrócenie kolumny macierzy"""

  return [row[i] for row in matrix]


def initialize_population(u, x_min, x_max, n):
  """Inicjalizacja populacji losowymi osobnikami"""
  P = []
  for i in range (0,u):
    p = []
    for j in range(0, n):
      p.append(random.uniform(x_min, x_max))
    P.append(p)

  return P


def initialize_one_population(u, x_min, x_max, n):
  """Inicjalizacja populacji klonami"""
  x = random.uniform(x_min, x_max)
  P = []
  for i in range (0,u):
    p = []
    for j in range(0, n):
      p.append(x)
    P.append(p)

  return P

  
def test_population(Po):
  """Ocena populacji"""
  o = []
  for i in Po:
    o.append(q(i))

  return o


def tournament_selection(P, r, o):
  """Selekcja turniejowa"""
  idxs = []
  tournament_population = {} 

  for i in range (0, r):
    idxs.append(random.randrange(0, len(P) - 1))

  for idx in idxs:
    tournament_population[o[idx]] = idx

  best = P[sorted(tournament_population.items())[0][1]]

  return best


def reproduction(P, r, o):
  """Reprodukcja populacji"""
  R = []
  
  for i in range (0, len(P)):
    best = tournament_selection(P, r, o)
    R.append(best)

  return R


def crossover(P, n, alfa, pc):
  """Krzyżowanie populacji"""
  C = []

  for i in range (0, len(P), 2):
    child_1 = []
    child_2 = []
    if random.random() < pc:

      for j in range(0, n):
        parent_1 = P[i][j]
        parent_2 = P[i+1][j]
        child_1.append(alfa * parent_1 + (1 - alfa) * parent_2)
        child_2.append(alfa * parent_2 + (1 - alfa) * parent_1)
    else:
      child_1 = P[i]
      child_2 = P[i+1]

    C.append(child_1)
    C.append(child_2)

  # for i in range (0, int(len(P)/2)):
  #   p_i_1 = random.randrange(0, len(P) - 1)
  #   p_i_2 = random.randrange(0, len(P) - 1)
  #   child_1 = []
  #   child_2 = []

  #   for j in range(0, n):
  #     parent_1 = P[p_i_1][j]
  #     parent_2 = P[p_i_2][j]
  #     child_1.append(alfa * parent_1 + (1 - alfa) * parent_2)
  #     child_2.append(alfa * parent_2 + (1 - alfa) * parent_1)

  #   C.append(child_1)
  #   C.append(child_2)

  return C


def mutation(P, pm, sigma, n):
  """Mutacja"""
  N = np.random.normal
  M = []

  for i in range (0, len(P)):
    x = []

    if random.random() < pm:

      for j in range(0, n):
        x.append(P[i][j] + sigma * N(0, 1))
    else:
      x = P[i]

    M.append(x)

  return M



def genetic_operations(P, pm, sigma, n, alfa, pc):
  """Operacje genetyczne"""
  C = crossover(P, n, alfa, pc) # krzyżowanie osobników
  M = mutation(C, pm, sigma, n) # mutacja osobników

  return M


def succesion(P, M, o, o_m, k):
  """Sukcesja"""
  S = []
  o_s = []

  #d odaj najlepsze osobniki
  for i in range(0, k):
    best_x, best_score, idx = find_min(P, o)
    S.append(best_x)
    o_s.append(best_score)
    del P[idx]
    del o[idx]

  for i in range (0, len(M)):
    S.append(M[i])
    o_s.append(o_m[i])

  # usuń najsłabsze 
  for i in range(0, k):
    worst_x, worst_score, idx = find_max(S, o_s)
    del S[idx]
    del o_s[idx]

  return S, o_s


def find_min(P, o):
    """Wyszukiwanie indeksu elementu najmniejszego."""
    k = 0
    i = 1
    right = len(P) - 1
    while i <= right:
        if o[i] < o[k]:
            k = i
        i += 1
    return P[k], o[k], k

def find_max(P, o):
    """Wyszukiwanie indeksu elementu największego."""
    k = 0
    i = 1
    right = len(P) - 1
    while i <= right:
        if o[i] > o[k]:
            k = i
        i += 1
    return P[k], o[k], k


def evolution_algoritm(u, sigma, k, type, t_max):
  n = 2 # liczba zmiennych w funkcji
  Po = [] # lista populacji początkowej
  P = [] # lista całej populacji
  O = [] # lista oceny 
  O_best = [] # najlepsza ocena danej populacji
  x_min = -10 # najmniejsza wartośc osobnika 
  x_max = 10 # największa wartośc osobnika 
  t = 0 # iteracje
  pm = 0.4 # prawdopodobuieństwo muatcji
  pc = 0.4 # prawdopodobuieństwo krzyżowania
  r = 2 #rozmiar turnieju
  alfa = 0.1

  start = time.time()

# inicjalizacja populacji
  if type:
    Po = initialize_population(u, x_min, x_max, n)
  else:
    Po = initialize_one_population(u, x_min, x_max, n)

  P.append(Po)
  o = test_population(Po)
  O.append(copy.copy(o))

  iter = []
  iter.append(t)
  best_x, best_score, b = find_min(P[0], o)
  O_best.append(best_score)

  while t < t_max:
    # reprodukcja
    R = [] 
    R = reproduction(P[t], r, o)

    # operacje genetyczne
    M = genetic_operations(R, pm, sigma, n, alfa, pc)

    # ocena
    o_m = test_population(M)
    best_x_m, best_score_m, b = find_min(M, o_m)

    if best_score_m <= best_score:
      best_score = best_score_m
      best_x = best_x_m

    O_best.append(best_score)

    # sukcesja elitarna
    P_now = copy.copy(P[t])
    P_t, o = succesion(P_now , M, o, o_m, k)



    P.append(copy.copy(P_t))
    O.append(copy.copy(o))
    t = t+1
    iter.append(t)

  end = time.time()

  total_time = end - start


  print("{0:02f}s".format(total_time))
  print(best_score)
  print(best_x)

  # # 3D
  # fig = plt.figure(figsize=(4.5,4.5), dpi=100)
  # ax = fig.add_subplot( projection='3d')
  # ax.set_title(f'Populacja')
  # fig.text(0.5, 0.04, f'Najlepszy osobnik: \n {round(best_x[0], 5)}, {round(best_x[1], 5)}', ha='center', va='center')
  # ax.set_xlabel('x1')
  # ax.set_ylabel('x2')
  # ax.set_zlabel('y')
  # ax.scatter(column(P[t_max], 0), column(P[t_max], 1), O[t_max], color = 'red', edgecolors='red', s = 1)
  # plt.show()

  # # 2D

  # plt.title(f'Najlepsze wartości funkcji celu \n Wartość osiągnięta:{round(best_score, 5)}')
  # plt.xlabel('t')
  # plt.ylabel('y_min')
  # plt.scatter(iter, O_best, color = 'red', edgecolors='red', s=1)
  # plt.show()

  return P, O, O_best, total_time,


if __name__ == "__main__":
  t_max = 500 # liczba iteracji

  type = 1 # 0 - populacja identyczna, 1 - populacja w pełni losowa
  u = 1000 # liczba osobników
  sigma = 0.1 #siła mutacji
  k = 1 # rozmiar elity


  P, O, O_best, time = evolution_algoritm(u, sigma, k, type, t_max)


  with open(f'{t_max}_P_{type}_{u}_{sigma}_{k}.txt', 'w') as filehandle:
      for listitem in P[t_max]:
          filehandle.write('%s\n' % listitem)

  with open(f'{t_max}_O_{type}_{u}_{sigma}_{k}.txt', 'w') as filehandle:
      for listitem in O_best:
          filehandle.write('%s\n' % listitem)
