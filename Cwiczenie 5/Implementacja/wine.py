#-*- coding: utf-8 -*-
import numpy as np

class Wine:

    def __init__(self, row, attr = []):

        """
        Constructs a wine object from csv file.
        """
        self._train_data = []



        if len(attr) == 0:

          self.no_attr = len(row.values()) -1

          for i in row.values():
            self._train_data.append(i)

        else:
          self.no_attr = len(attr) -1
          for count, item in enumerate(row.values()):
            if count in attr:
              self._train_data.append(item)


        self.y_vector= self.create_y_vector()
        self.normalized_train_data = self.create_train_data()

    def __str__(self):
      """
      Returns string
      """
      return f"Atrybuty: {self._train_data}"

    def get_quality(self):
      """
      Returns wine's quality
      """
      return int(self._train_data[-1])

    def create_train_data(self):
      """
      Create attributes
      """
      train_data = []
      for x in self._train_data[0:-1]:
        train_data.append(float(x))

      X = np.array(train_data)
      X = (X - X.mean(axis=0)) / X.std(axis=0)

      return X

    def get_train_data(self):
      """
      Returns attributes
      """
      return self.normalized_train_data

    def create_y_vector(self):
      """
      Create class of wine vector
      """
      output = [0, 0, 0, 0, 0, 0]
      quality =  self.get_quality()
      output[quality - 3] = 1
      return output

    def get_y_vector(self):
      """
      Returns class of wine vector
      """
      return self.y_vector

    def get_no_attr(self):
      """
      Returns number of atribute
      """
      # return self._quality
      return self.no_attr


if __name__ == "__main__":
    pass
