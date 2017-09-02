import numpy as np

class TicTacToe:
  def __init__(self, board):
    self.playerJustMoved = 2
    self.board = board

  def Clone(self):
      """ Create a deep clone of this game state.
      """
      st = TicTacToe()
      st.playerJustMoved = self.playerJustMoved
      return st

  # display the current game state on screen
  def DisplayGame(self, board, play_number):
    assert(board.shape[0] == board.shape[1])

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

  # get a list of legal moves
  def GetMoves(self, board):
    return list(np.where(board.ravel() == 0)[0])

  # do we have remaining moves
  def HasRemainingMove(self, board):
    return len(self.GetMoves(board))

  # proceed to a move move
  def DoMove(self, move, value, board):
    # is the move a legal move
    def is_legal_move(move, board):
      legal_moves = self.GetMoves(board)
      return True if move in legal_moves else False

    if not is_legal_move(move, board):
      return False
    coords = (np.floor_divide(move, board.shape[0]),
              np.mod(move, board.shape[0]))
    board[coords[0], coords[1]] = value

    # alternate player
    self.playerJustMoved = 3 - self.playerJustMoved

    return True

  # check if there is a winning game
  def GetResult(self, board):
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


def play_random_game(game_number, display=False):
  play_number = 1
  board = np.zeros((3,3))
  game = TicTacToe(board)


  player = np.random.choice([1,2])
  while game.HasRemainingMove(board):
    # get a list of possible moves
    possible_moves = game.GetMoves(board)

    # select a move at random
    move = np.random.choice(possible_moves)

    # play a move
    game.DoMove(move,player,board)

    # show the board
    if display:
      game.DisplayGame(board,play_number)

    # do we have a winner ?
    winning_status = game.GetResult(board)
    if winning_status:
      break

    # switch players
    if game.HasRemainingMove(board):
      player = 1 if player == 2 else 2
      play_number += 1

  return (winning_status, play_number, player)


if __name__ == "__main__":
  from multiprocessing import Pool
  import itertools
  from tqdm import tqdm


  number_of_games = 100000

  results_list = []

  # processing
  pool = Pool()
  for result in tqdm(pool.imap_unordered(play_random_game, range(number_of_games)), total=number_of_games):
    results_list.append(result)

  # compiling results
  pos = 0
  neg = 0
  player1 = 0
  player2 = 0
  for result in results_list:
    if result[0]:
      pos += 1
      if result[2] == 1:
        player1 += 1
      elif result[2]:
        player2 += 1
    else:
      neg += 1

  print("Number of positives: %d / %d" % (pos, number_of_games))
  print("Number of negatives: %d / %d" % (neg, number_of_games))
  print("Player1 wins: %2.2f%%" % (float(player1)/pos*100))
  print("Player2 wins: %2.2f%%" % (float(player2)/pos*100))
