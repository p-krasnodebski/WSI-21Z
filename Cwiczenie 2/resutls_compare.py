import copy
import matplotlib.pyplot as plt
import random
import numpy as np
t_max = 500 # liczba iteracji
t = 0
iter = []
iter.append(t)

while t < t_max:
  t = t+1
  iter.append(t)

# PRZED WYWOŁANIEM NALEŻY UTWORZYĆ ODPOWIEDNIE PLIKI POPRZEZ FUNKCJE Z PLIKU CW2.py

type =  [1,   1,  1,    1,   1,   1,   1 ] # 0 - populacja identyczna, 1 - populacja w pełni losowa
u =     [10,  10, 10,   100, 500, 500, 1000] # liczba osobników
sigma = [0.1, 0.5,0.1,   2, 0.1,  2,  0.1] #siła mutacji
k =     [10,  10, 1,     1,   1,    10,  1]  # rozmiar elity

O_best = []

for i in range(0, len(type)):
  table = []
  with open(f'{t_max}_O_{type[i]}_{u[i]}_{sigma[i]}_{k[i]}.txt', 'r') as filehandle:
      for line in filehandle:

          currentPlace = line[:-1]
          table.append(float(currentPlace))
  O_best.append(table)

plt.title(f'Najlepsze wartości funkcji celu')
plt.xlabel('t')
plt.ylabel('y_min')
plt.scatter(iter, O_best[0], s=1)
plt.scatter(iter, O_best[1], s=1)
plt.scatter(iter, O_best[2], s=1)
plt.scatter(iter, O_best[3], s=1)
plt.scatter(iter, O_best[4], s=1)
plt.scatter(iter, O_best[5], s=1)
plt.scatter(iter, O_best[6], s=1)
plt.legend([f"u={u[0]}, sigma={sigma[0]} , k={k[0]}", f"u={u[1]}, sigma={sigma[1]} , k={k[1]}", f"u={u[2]}, sigma={sigma[2]} , k={k[2]}" , f"u={u[3]}, sigma={sigma[3]} , k={k[3]}", f"u={u[4]}, sigma={sigma[4]} , k={k[4]}", f"u={u[5]}, sigma={sigma[5]} , k={k[5]}", f"u={u[6]}, sigma={sigma[6]} , k={k[6]}"  ], markerscale=5, loc='upper right')
plt.show()


