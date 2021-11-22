import time
import random
AI_X = "X"
AI_O = "O"

# Sprawdzenie czy gra zakończyłą się wygraną
def game_win(board):
  if (board[0][0] == board[0][1] and board[0][0] == board[0][2] and board[0][0] != ' '):
      return True
  elif (board[1][0] == board[1][1] and board[1][0] == board[1][2] and board[1][0] != ' '):
      return True
  elif (board[2][0] == board[2][1] and board[2][0] == board[2][2] and board[2][0] != ' '):
      return True
  elif (board[0][0] == board[1][0] and board[0][0] == board[2][0] and board[0][0] != ' '):
      return True
  elif (board[0][1] == board[1][1] and board[0][1] == board[2][1] and board[0][1] != ' '):
      return True
  elif (board[0][2] == board[1][2] and board[0][2] == board[2][2] and board[0][2] != ' '):
      return True
  elif (board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[0][0] != ' '):
      return True
  elif (board[2][0] == board[1][1] and board[2][0] == board[0][2] and board[2][0] != ' '):
      return True
  else:
      return False

# Sprawdzenie czy gra zakończyłą się wygraną konkretnego gracza
def game_sign_win(sign, board):
  if (board[0][0] == board[0][1] and board[0][0] == board[0][2] and board[0][0] == sign):
      return True
  elif (board[1][0] == board[1][1] and board[1][0] == board[1][2] and board[1][0] == sign):
      return True
  elif (board[2][0] == board[2][1] and board[2][0] == board[2][2] and board[2][0] == sign):
      return True
  elif (board[0][0] == board[1][0] and board[0][0] == board[2][0] and board[0][0] == sign):
      return True
  elif (board[0][1] == board[1][1] and board[0][1] == board[2][1] and board[0][1] == sign):
      return True
  elif (board[0][2] == board[1][2] and board[0][2] == board[2][2] and board[0][2] == sign):
      return True
  elif (board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[0][0] == sign):
      return True
  elif (board[2][0] == board[1][1] and board[2][0] == board[0][2] and board[2][0] == sign):
    return True
  else:
    return False

# Sprawdzenie czy gra zakończyła się remisem
def game_draw(board):
  for i in board:
    for j in i:
      if j == ' ':
        return False
  return True

# Wyświetlenie planszy
def print_board(board):
  for i in board:
    print(i)
    print()

# Sprawdzenie czy pole jest puste
def empty_field(x, y, board):
  if(board[x][y]) == ' ':
    return True
  else:
    return False

# Sprawdzenie stanu gry
def check_state(letter, board, scores):
  global count_x
  global count_o

  if(game_win(board)):
    if letter == AI_X:
      print("AI_X wins")
      print_board(board)
      print("Liczba przeszukanych stanów gracza X: ", count_x)
      print("Liczba przeszukanych stanów gracza O: ", count_o)
      scores[0] += 1
      return 3
    if letter == AI_O:
      print("AI_O wins")
      print_board(board)
      print("Liczba przeszukanych stanów gracza X: ", count_x)
      print("Liczba przeszukanych stanów gracza O: ", count_o)
      scores[1] += 1
      return 2

  if(game_draw(board)):
    print("Draw")
    print_board(board)
    print("Liczba przeszukanych stanów gracza X: ", count_x)
    print("Liczba przeszukanych stanów gracza O: ", count_o)
    scores[2] += 1 
    return 1   

# Algorytm Minimax
def minimax(player_1, player_2, board, depth, max, alfa, beta, ab_x, ab_o):

  if player_1 == AI_X:
    global count_x
    count_x += 1
  if player_1 == AI_O:
    global count_o
    count_o += 1

  if depth == 0:
    if game_sign_win(player_1, board):
      return 1
    elif game_sign_win(player_2, board):
      return -1
    else:
      return 0
  if depth != 0:

    if game_sign_win(player_1, board):
      return 1
    elif game_sign_win(player_2, board):
      return -1
    elif game_draw(board):
      return 0

    if max:
        best_score = -1000

        for i, row in enumerate(board):
          for j, col in enumerate(row):
            if col == ' ':
              board[i][j] = player_1
              score =  minimax(player_1, player_2, board, depth-1, False, alfa, beta, ab_x, ab_o)
              board[i][j] =  ' '
              if score > best_score:
                best_score = score

              if score > alfa:
                alfa = score
              if beta <= alfa:
                if player_1 == AI_X and ab_x:
                  break
                if player_1 == AI_O and ab_o:
                  break

        return best_score

    else:
      best_score = 1000

      for i, row in enumerate(board):
        for j, col in enumerate(row):
          if col == ' ':
            board[i][j] = player_2
            score =  minimax(player_1, player_2, board, depth-1, True, alfa, beta, ab_x, ab_o)
            board[i][j] =  ' '
            if score < best_score:
              best_score = score
            if score < beta:
              beta = score
            if alfa >= beta:
              if player_1 == AI_X and ab_x:
                break
              if player_1 == AI_O and ab_o:
                break

      return best_score

# Wykonanie ruchu algorytmem Minimax
def move(player_1, player_2, d, board, scores, ab_x, ab_o):
  alfa = -1000
  beta = 1000
  best_score = -1000
  best_move_x = -1
  best_move_y = -1

  for i, row in enumerate(board):
    for j, col in enumerate(row):
      if col == ' ':
        board[i][j] = player_1
        score =  minimax(player_1, player_2, board, d, False, alfa, beta, ab_x, ab_o)
        board[i][j] =  ' '
        if score > best_score:
          best_score = score
          best_move_x = i
          best_move_y = j

  # Sprawdzenie czy wyznaczona pozycja jest poprawna
  if(empty_field(best_move_x, best_move_y, board)):
    board[best_move_x][best_move_y] = player_1
  else:
    print("Error")
    exit()

  # Sprawdzenie warunku zakończenia gry
  state = check_state(player_1, board, scores)
  return state, board

# Wykonanie losowego ruchu
def random_move(player_1, board, scores):
  best_move_x = -1
  best_move_y = -1
  free_spaces = []

  for i, row in enumerate(board):
    for j, col in enumerate(row):
      if col == ' ':
        free_spaces.append((i, j))

  place = random.choices(free_spaces)      
  best_move_x = place[0][0]
  best_move_y = place[0][1]

  # Sprawdzenie czy wyznaczona pozycja jest poprawna
  if(empty_field(best_move_x, best_move_y, board)):
    board[best_move_x][best_move_y] = player_1
  else:
    print("Error")
    exit()

  # Sprawdzenie warunku zakończenia gry
  state = check_state(player_1, board, scores)


  return state, board

# Funkcja realizująca grę
def game(d_x, d_o, ab_x = False, ab_o = False, n=1, rand = False):
  # Tablica wygranych, przegranych, remisów
  scores = [0, 0, 0]

  for z in range(n):
    board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    # Licznik przeszukań
    global count_x
    count_x = 0
    global count_o
    count_o = 0

    # Ruch do czasu wygrania rozgrywki
    while not game_win(board):
      if rand:
        game, board = random_move(AI_X, board, scores)
      else:
        game, board = move(AI_X, AI_O, d_x, board, scores, ab_x, ab_o)
      if game is not None:
        break
      game, board = move(AI_O, AI_X, d_o, board, scores, ab_x, ab_o)

  print("Wygrane -", scores[0], ", przegrane -", scores[1], ", remisy -", scores[2], " gracza X")

if __name__ == "__main__":

  # Włączenie przyciania
  ab_X = False
  ab_O = False

  # Czy gracz X gra randomowo
  rand_move = True

  # Głębokości przeszukiwań drzewa
  d_X = 9
  d_O = 3

  # Rozgrywka
  game(d_X, d_O, ab_x = ab_X, ab_o = ab_O, n=1, rand = rand_move)










