from math import exp
from file_read  import WineCsvReader
import numpy as np
import random
import csv

def activation_der(x):
    return exp(x)/((exp(x)+1)**2)

def vector_product(vect_a, vect_b):
    return sum([a_ * b_ for (a_, b_) in zip(vect_a, vect_b)])

output_data = []

class Classifier:
  def __init__(self, layers_sizes, beta, factor, epochs, stream):
        self.stream = stream
        self.factor = factor
        self.attr = []
        self.data = self.read_data()
        self.input_size = self.data[0].no_attr
        random.shuffle(self.data)
        self.validation_data = []
        self.train_data = []
        self.test_data = []

        self.n = 0
        self.mean_error_train = 0
        self.mean_error_test = 0

        if self.factor < 1 and self.factor > 0:
            print("Podział na zbiór treningowy i testowy")
            self.train_data, self.test_data = self.two_sets()
            self.n = 1
        elif self.factor > 1 and type(self.factor) == int:
            self.validation_data = self.split_data()
            print("Walidacja danych")
            self.n = self.factor
        else:
            print("Błąd")
            return


        for i in range(self.n):
          if self.n > 1:
              self.train_data = []
              self.test_data = self.validation_data[i]
              
              for j in range(self.n):
                  if j !=i:
                      self.train_data = self.train_data + self.validation_data[j]

          E = Network(layers_sizes, self.input_size, beta)
          print(len(self.train_data))
          erroe, out = E.train(self.train_data, epochs)
          self.mean_error_train += erroe/self.n
          output_data.append(out)

          self.mean_error_test += E.test(self.test_data)/self.n
        print("Średni błąd dla zbioru treningowego:", 1 - self.mean_error_train) 
        print("Średni błąd dla zbioru testowego:", 1 - self.mean_error_test) 


        # Opcjonalny zapis danych do pliku
        # with open('GFG', 'w') as f:
        #   write = csv.writer(f)
          
        #   # write.writerow(fields)
        #   write.writerows(output_data)

  def read_data(self):

      with open(self.stream, newline='', encoding="utf-8") as file:
      
          raw_data = WineCsvReader(file, self.attr).read_file()

      return raw_data

  def two_sets(self):
      """
      Devide data into two group
      """
      no = int(self.factor*len(self.data))
      train_data = self.data[:no]
      test_data = self.data[no+1:]
      return train_data, test_data

  def split_data(self):
      """
      Devide data for validation
      """
      table = []
      k, m = divmod(len(self.data), self.factor)
      for i in range(self.factor):
          table.append(self.data[i*k+min(i, m):(i+1)*k+min(i+1, m)])
      return table


class Neuron:
    def __init__(self, input_size):
        self.weights = []
        self.output = 0
        self.der = []
        for i in range(input_size):
            self.weights.append(random.uniform(-1/np.sqrt(11), 1/np.sqrt(11)))

    def activation(self, input):
        z = vector_product(input, self.weights)

        self.output = exp(z)/(exp(z)+1)

        return self.output

    def end_output(self, input):
        z = vector_product(input, self.weights)
        # self.output = exp(z)/(exp(z)+1)
        self.output = z
        return self.output

class Layer:
    def __init__(self, size, input_size):
        self.neurons = []
        for i in range(size):
            self.neurons.append(Neuron(input_size))

    def calculate_output(self, input):
        output = []
        for neuron in self.neurons:
            output.append(neuron.activation(input))
        return output
        
    def calculate_end_output(self, input):
        output = []
        for neuron in self.neurons:
            output.append(neuron.end_output(input))
        return output

class Network:
    def __init__(self, layers_sizes, input_size, beta):
        self.layers = []
        self.beta = beta
        for i, size in enumerate(layers_sizes):
            if i == 0:
                self.layers.append(Layer(size, input_size))
            else:
                self.layers.append(Layer(size, layers_sizes[i-1]))
        
    def calculate_output(self, input):
        local_output = input
        for layer in self.layers[:-1]:
            local_output = layer.calculate_output(local_output)
        local_output = self.layers[-1].calculate_end_output(local_output)
        return local_output

    def train(self, data, epochs):
      out = []
      for a in range(epochs):
        correct = 0
        random.shuffle(data)
        for b, wine in enumerate(data):
          x=wine.get_train_data()
          y=wine.get_y_vector()
          local_output = self.calculate_output(x)

          for i in range(len((self.layers))-1, -1, -1): # odwrócenie kolejności warstw - propagacja wsteczna
            if i == (len(self.layers) - 1):# pochodna warstwy wyjściowej
              for  j, neuron in enumerate(self.layers[i].neurons):
                neuron.der = []
                for  k, back_neuron in enumerate(self.layers[i-1].neurons):
                  neuron.der.append(2 * (-(y[j]) + neuron.output) * back_neuron.output)
            else: # pochodne warstw ukrytych
              if i == 0: # pierwsza warstwa ukryta
                dq__dy_x = []
                for  j, neuron in enumerate(self.layers[i].neurons):
                  der_sum = 0 
                  for  k, out_neuron in enumerate(self.layers[len((self.layers))-1].neurons):
                    der_sum += 2 * (-(y[k]) + out_neuron.output) * out_neuron.weights[j]
                  dq__dy_x.append(der_sum)
                for  j, neuron in enumerate(self.layers[i].neurons):
                  neuron.der = []
                  for  k, input in enumerate(x):
                    neuron.der.append(dq__dy_x[j] * activation_der(neuron.output) * input)
              else: # pozostałe warstwy ukryte
                dq__dy_x = []
                for  j, neuron in enumerate(self.layers[i].neurons):
                  der_sum = 0 
                  for  k, out_neuron in enumerate(self.layers[len((self.layers))-1].neurons):
                    der_sum += 2 * (-(y[k]) + out_neuron.output) * out_neuron.weights[j] 
                  dq__dy_x.append(der_sum)
                for  j, neuron in enumerate(self.layers[i].neurons):
                  neuron.der = []
                  for  k, back_neuron in enumerate(self.layers[i-1].neurons):
                    neuron.der.append(dq__dy_x[j] * activation_der(neuron.output) * back_neuron.output)

                  
          # Aktualizacja wag
          for layer in self.layers:
              for neuron in layer.neurons:
                # print(neuron.der)
                for i, weight in enumerate(neuron.weights):
                  neuron.weights[i] -= self.beta*neuron.der[i]

          if y[local_output.index(max(local_output))] == 1:
              correct +=  1

        if(a%10 == 0):
          print(a, correct / len(data))  
        out.append(correct / len(data))     
      # self.mean_error_train += correct / len(data)/self.n
      return correct / len(data), out

    def test(self, data):
        correct = 0
        for wine in data:
          x=wine.get_train_data()
          y=wine.get_y_vector()
          local_output = self.calculate_output(x)
          if y[local_output.index(max(local_output))] == 1:
            correct +=  1

        correct / len(data)
        print("Dopasowanie zbioru testowego:", correct / len(data)) 
        # self.mean_error_test += err/self.n
        return correct / len(data)


if __name__ == "__main__":

    # Path to file
    path = 'winequality-red.csv'

    # Learning rate
    beta = 0.1
    # Number of neurons in hidden layers and for the last element in list - number of neurons in output layer
    layers = [8, 6]

    # for the training and test set, a value from range (0, 1)
    # for validation, an integral value in the range (1, infinity)
    # other values ​​raise an error
    factor = 5

    # number of training epochs
    n_epochs = 800

    Classifier(layers, beta, factor, n_epochs, path)

