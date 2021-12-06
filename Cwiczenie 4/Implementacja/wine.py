#-*- coding: utf-8 -*-
import random

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


        

    def __str__(self):
      """
      Returns string
      """
      return f"Atrybuty: {self._train_data}"

    def get_quality(self):
      """
      Returns wine's quality
      """
      # return self._quality
      return self._train_data[-1]

    def create_train_data(self):
      return self._train_data[0:-1]

    def get_no_attr(self):
      """
      Returns number of atribute
      """
      # return self._quality
      return self.no_attr


if __name__ == "__main__":
    pass
