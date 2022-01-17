#-*- coding: utf-8 -*-
import csv
from random import randint, random
from copy import deepcopy


class Maze:
  def __init__(self, environment, start_x = None, start_y = None, final_x = None, final_y = None):

    self.environment = environment
    self.rows_len = len(environment)
    self.columns_len = len(max(environment,  key = len))
    self.rewards = [] 
    self.set_rewards()
    # if (final_x is None and final_x < self.rows_len) or (final_y is None and final_y < self.columns_len):
    if (final_x is None ) or (final_y is None):
      self.set_final_point()
    else:
      self.final_x = final_x
      self.final_y = final_y

    self.rewards[self.final_x][self.final_y] = 100

    # if (start_x is None and start_x < self.rows_len) or (start_y is None and start_y < self.columns_len):
    if (start_x is None ) or (start_y is None):
      self.set_start_point()
    else:
      self.start_x = start_x
      self.start_y = start_y

    self.environment_with_point = deepcopy(self.environment)
    self.create_maze_with_point()
    self.best_environment = deepcopy(self.environment_with_point)
    self.actual_environment = []


  def set_rewards(self):
    for row in self.environment:
      reward_column=[]
      for item in row:
        if item == 1:
          reward_column.append(-1000)
        elif item == 0:
          reward_column.append(-1)

      self.rewards.append(reward_column)

  def check_free_space(self, r_inx, c_inx):

    # print(r_inx, c_inx)
    if self.rewards[r_inx][c_inx] == -1:
      return True
    else:
      return False

  def check_free_space_and_final(self, r_inx, c_inx):

    # print(r_inx, c_inx)
    if self.rewards[r_inx][c_inx] == -1 and not self.rewards[r_inx][c_inx] == 100:
      return True
    else:
      return False

  def set_start_point(self):
    r_inx = randint(0, self.rows_len-1)
    c_inx = randint(0, self.columns_len-1)
    while not self.check_free_space_and_final(r_inx, c_inx):
      r_inx = randint(0, self.rows_len-1)
      c_inx = randint(0, self.columns_len-1)

    self.start_x = r_inx
    self.start_y = c_inx
    
  def set_final_point(self):
    r_inx = randint(0, self.rows_len-1)
    c_inx = randint(0, self.columns_len-1)
    while not self.check_free_space_and_final(r_inx, c_inx):
      r_inx = randint(0, self.rows_len-1)
      c_inx = randint(0, self.columns_len-1)

    self.final_x = r_inx
    self.final_y = c_inx

  def print_loaded_maze(self):
    for row in self.environment:
      print(row)

  def create_maze_with_point(self):
    self.environment_with_point[self.final_x][self.final_y] = 5
    self.environment_with_point[self.start_x][self.start_y] = 4

  def create_actual_environment(self):
    self.actual_environment = deepcopy(self.environment_with_point)


  def print_maze_with_point(self):
    for row in self.environment_with_point:
      row[:] = ["#" if x==1 else x for x in row]
      row[:] = [" " if x==0 else x for x in row]
      row[:] = ["S" if x==4 else x for x in row]
      row[:] = ["F" if x==5 else x for x in row]
      print(''.join(row))
      # print(row)

  def print_best_maze(self):
    for row in self.best_environment:
      row[:] = ["#" if x==1 else x for x in row]
      row[:] = [" " if x==0 else x for x in row]
      row[:] = ["S" if x==4 else x for x in row]
      row[:] = ["F" if x==5 else x for x in row]
      row[:] = ["-" if x==7 else x for x in row]
      print(''.join(row))