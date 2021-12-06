import numpy as np 
from math import sqrt, pi, exp
import matplotlib.pyplot as plt
from NBC import NBC

path = 'winequality-white.csv'

no_test = 5

# for the training and test set, a value from range (0, 1)
# for validation, an integral value in the range (1, infinity)
# other values ​​raise an error
factor = 5
mean_error = 0

for x in range(no_test):

  nbc = NBC(path, factor)

  data = nbc.data

  err =nbc.mean_error
  print(err)

  mean_error += err/no_test

print("Średnia strata próby:", round(mean_error, 4))


