import numpy as np
from tqdm import tqdm

def display_board(board, play_number):
  assert(board.shape == (3, 3))

  def print_empty():
    print("|-|-|-|")

  def print_row(row):
    print("|%d|%d|%d|" % (row[0], row[1], row[2]))

  print("|Game:%d|" % play_number)
  print_empty()
  print_row(board[0])
  print_empty()
  print_row(board[1])
  print_empty()
  print_row(board[2])
  print_empty()


def list_legal_moves(board):
  return list(np.where(board.ravel() == 0)[0])

def has_remaining_move(board):
  return len(list_legal_moves(board))

def is_legal_move(move, board):
  legal_moves = list_legal_moves(board)
  return True if move in legal_moves else False

def make_move(move, value, board):
  if not is_legal_move(move, board):
    return False
  coords = (np.floor_divide(move, board.shape[0]),
            np.mod(move, board.shape[0]))
  board[coords[0], coords[1]] = value
  return True


def is_game_won(board):

  def winning_line(elems):
    ll = list(set(elems))
    if len(ll) == 1 and ll[0] != 0:
      return True
    return False

  # check the diagonal
  if winning_line(board.diagonal()):
    return True

  #check rows
  if True in np.apply_along_axis(winning_line, axis=1, arr=board):
    return True

  #check columns
  if True in np.apply_along_axis(winning_line, axis=0, arr=board):
    return True

  # nothing was found
  return False


def play_random_game(display=True):
  play_number = 1
  board = np.zeros((3,3))

  player = np.random.choice([1,2])
  while has_remaining_move(board):
    # get a list of possible moves
    possible_moves = list_legal_moves(board)

    # select a move at random
    move = np.random.choice(possible_moves)

    # play a move
    make_move(move,player,board)

    # show the board
    if display:
      display_board(board,play_number)

    # do we have a winner ?
    winning_status = is_game_won(board)
    if winning_status:
      break

    # switch players
    if has_remaining_move(board):
      player = 1 if player == 2 else 2
      play_number += 1

  return (winning_status, play_number, player)


if __name__ == "__main__":
  pos = 0
  neg = 0
  player1 = 0
  player2 = 0
  results_list = []
  for i in tqdm(range(10000)):
    result = play_random_game(display=False)
    results_list.append(result)

    if result[0]:
      pos += 1
      if result[2] == 1:
        player1 += 1
      else:
        player2 += 1
    else:
      neg += 1



  print("Number of positives: %d" % pos)
  print("Number of negatives: %d" % neg)
  print("Player1 wins: %d" % player1)
  print("Player2 wins: %d" % player2)

# result, play_number = play_random_game()
# if result:
#   print("We have a winner !")
# else:
#   print("Nobody wins")
