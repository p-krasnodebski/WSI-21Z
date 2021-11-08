from CW2 import evolution_algoritm
import matplotlib.pyplot as plt

type = 1 # 0 - populacja identyczna, 1 - populacja w pełni losowa

sigma = 2 #siła mutacji
k = 10 # rozmiar elity
t_max = 500

u = [10, 20, 50, 100, 200, 500, 1000, 2000] # ilości populacji

time_list = []

for i, val in enumerate(u):
  n = 3
  med = 0  
  for j in range(0, n):
    P, O, O_best, time = evolution_algoritm(u[i], sigma, k, type, t_max)
    med += time

  time_list.append(med/n)
  u[i] = str(u[i])


plt.bar(u, time_list)
plt.xlabel('Wielkośc populacji', fontsize=12, color='#323232')
plt.ylabel('Czas działania', fontsize=12, color='#323232')
plt.title('Zależność czasu działania od wielkości populacji', fontsize=16, color='#323232')
plt.show() 