#-*- coding: utf-8 -*-
import csv

class MazeReader:
  def __init__(self, stream):
    self.stream = stream
    self.maze = self.load_maze()


  def load_maze(self):

    environment = []
    with open(self.stream) as f:
        lines = f.readlines()
        rows = len(lines)
        for line in lines:
          row = []
          for letter in line:
            if letter == ".":
              row.append(0)
            elif letter =="#":
              row.append(1)
          environment.append(row)

    return environment


