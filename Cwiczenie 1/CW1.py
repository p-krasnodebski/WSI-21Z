
import matplotlib.pyplot as plt
import numpy as np

# Definicja funkcji i pochodnej
df = lambda x: 2*x -1 # Pochodna
yf = lambda x: x**2 + 3 - x # Funkcja

# df = lambda x: np.cos(x) # Pochodna
# yf = lambda x: np.sin(x) # Funkcja

# Wykres funckji
x=np.arange(-10,10,0.1)
y=yf(x)

plt.figure(figsize=(3,3), dpi=10
plt.xlabel('x')
plt.ylabel('y')
plt.axhline(y=0, color="#cccccc")
plt.axvline(x=0, color="#cccccc")

# Tablice punktów wyznaczanych przez algorytm
x_alg = []
y_alg = []

# Definicja zmiennych dla algorytmu
x_k = -9 #
step = 0.6
precision = 0.05 #
previous_step_size = 1 #
i = 0 
max_i = 20

plt.title(f'Wykres funkcji, krok:{step}')
plt.title(f'Wykres funkcji, x_0:{x_k}')

x_alg.append(x_k)
y_alg.append(yf(x_k))

# Pętla algorytmu
while previous_step_size > precision and i < max_i:
    x_nk = x_k - step * df(x_k) #
    previous_step_size = abs(x_nk - x_k)
    x_k=x_nk
    i = i+1
    print("Iteracja",i,"\nx:",x_k) 
    x_alg.append(x_k)
    y_alg.append(yf(x_k))
    
print("Minimum lokalne:", x_k)

# Pokazanie danych
plt.plot(x,y,)
plt.scatter(x_alg, y_alg,color = 'red', edgecolors='black')
plt.show()