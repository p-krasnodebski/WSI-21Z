#-*- coding: utf-8 -*-
import csv
from random import randint, random
import numpy as np
import matplotlib.pyplot as plt



class QLearning:

  def __init__(self, Maze, epsilon, beta, gamma):
    self.Maze = Maze
    self.epsilon = epsilon
    self.beta = beta
    self.gamma = gamma
    self.rows = self.Maze.rows_len
    self.columns = self.Maze.columns_len

    self.actions = ['up', 'right', 'down', 'left']
    self.q = []
    self.create_q_table()

    self.iter = []
    self.iter_reward = []
    self.best_path = []
    self.best_reward = -1*10**99


  def create_q_table(self):
    for i in range(self.rows):
      q_column=[]
      for j in range(self.columns):
        q_action = []
        for k in range(len(self.actions)):
          q_action.append(0)
        q_column.append(q_action)
      self.q.append(q_column)

  def check_final_point(self, r_inx, c_inx):
    if self.Maze.rewards[r_inx][c_inx] == 100:
      return True
    else:
      return False

  def next_action(self, r_inx, c_inx, epsilon):
    #if a randomly chosen value between 0 and 1 is less than epsilon, 
    #then choose the most promising value from the Q-table for this state.
    if random() < epsilon:
      return np.argmax(self.q[r_inx][c_inx])
    else: #choose a random action
      return randint(0, 4-1)

  def next_location(self, r_inx, c_inx, action):
    new_row_index = r_inx
    new_column_index = c_inx
    if self.actions[action] == 'up' and r_inx > 0:
      new_row_index -= 1
    elif self.actions[action] == 'right' and c_inx < self.columns - 1:
      new_column_index += 1
    elif self.actions[action] == 'down' and r_inx < self.rows - 1:
      new_row_index += 1
    elif self.actions[action] == 'left' and c_inx > 0:
      new_column_index -= 1
    return new_row_index, new_column_index


  def get_path(self, epochs):

    iter = []
    iter_reward = []
    iter_no = []

    best_path = []
    best_reward = -1*10**99
    

    for episode in range(epochs):
      self.Maze.create_actual_environment()
      actual_path = []
      iter.append(episode)
      actual_reward = 0
      no = 0

      x, y = self.Maze.start_x, self.Maze.start_y
      actual_path.append((self.Maze.start_x, self.Maze.start_y))
      
      while not self.check_final_point(x, y):
        no = no+1
        #choose an action 
        action = self.next_action(x, y, self.epsilon)

        #go to next location
        prev_x, prev_y = x, y
        x, y = self.next_location(x, y, action)

        if(not self.check_final_point(x, y)):
          self.Maze.actual_environment[x][y] = 7
        actual_path.append((x, y))
      
        #reward
        prev_q = self.q[prev_x][prev_y][action]
        reward = self.Maze.rewards[x][y]
        actual_reward = actual_reward + reward

        temporal_difference = reward + (self.gamma * np.max(self.q[x][y])) - prev_q
        new_q = prev_q + (self.beta * temporal_difference)
        self.q[prev_x][prev_y][action] = new_q

      if actual_reward> best_reward:
        best_path = actual_path
        best_reward = actual_reward
        self.Maze.best_environment = self.Maze.actual_environment
      iter_no.append(no)
        
      iter_reward.append(actual_reward)
    print("Najlepsza kara/nagroda: ", best_reward)
    print("Najlepsza ścieżka: ", best_path)

    plt.title(f'Kara/nagroda w kolejnych iteracjach \n Najlepsza nagroda:{round(best_reward, 5)}')
    plt.xlabel('k')
    plt.ylabel('Kara/nagroda')
    plt.scatter(iter, iter_reward, color = 'red', edgecolors='red', s=1)
    # plt.show()

    plt.title(f'Liczba wykonanych kroków')
    plt.xlabel('k')
    plt.ylabel('Liczba kroków')
    plt.scatter(iter, iter_no, color = 'green', edgecolors='green', s=1)
    # plt.show()
