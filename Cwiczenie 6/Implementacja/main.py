from file_read import MazeReader
from maze import Maze
from qlearning import QLearning


if __name__ == "__main__":

  path = 'Cwiczenie 6/maze.txt'

  epsilon = 0.7
  beta = 0.9 # learning rate
  gamma = 0.8
  iterations = 50

  environment = MazeReader(path).load_maze()

  #set start point
  #delete a parameter: start_x, start_y, final_x, final_y,  to choose random start and final point
  # maze = Maze(environment)
  maze = Maze(environment, start_x=5, start_y=3, final_x=8, final_y=14)


  # maze.print_loaded_maze()
  # maze.print_maze_with_point()

  q = QLearning(maze, epsilon, beta, gamma)
  q.get_path(iterations)
  maze.print_best_maze()








