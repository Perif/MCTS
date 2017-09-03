import numpy as np

class TicTacToe:
  def __init__(self, board, random_player=True):
    self.playerJustMoved = np.random.choice([1,2]) if random_player else 2
    self.board = board

  def Clone(self):
      """ Create a deep clone of this game state.
      """
      st = TicTacToe(self.board.copy())
      st.playerJustMoved = self.playerJustMoved
      return st

  def __repr__(self,):
    """
    Return a string representation of the board
    """
    assert(self.board.shape[0] == self.board.shape[1])

    def print_row(row):
      return "|%d|%d|%d|" % (row[0], row[1], row[2])

    representation = "|-|-|-|\n"
    representation += print_row(self.board[0])
    representation += "\n|-|-|-|\n"
    representation += print_row(self.board[1])
    representation += "\n|-|-|-|\n"
    representation += print_row(self.board[2])
    representation += "\n|-|-|-|\n"

    return representation

  def GetMoves(self):
    """
    Return a list of possible legal moves
    """
    return list(np.where(self.board.ravel() == 0)[0])

  def HasRemainingMove(self):
    """
    Check if moves are still possible
    """
    return len(self.GetMoves())

  def DoMove(self, move):
    """
    Do a game move
    """
    # is the move a legal move
    def is_legal_move(move):
      legal_moves = self.GetMoves()
      return True if move in legal_moves else False

    if not is_legal_move(move):
      return False
    coords = (np.floor_divide(move, self.board.shape[0]),
              np.mod(move, self.board.shape[0]))
    self.board[coords[0], coords[1]] = self.playerJustMoved

    # alternate player
    self.playerJustMoved = 3 - self.playerJustMoved

    return True

  def GetResult(self):
    """
    check if there is a winning game
    """
    def winning_line(elems):
      ll = list(set(elems))
      if len(ll) == 1 and ll[0] != 0:
        return True
      return False

    # check the diagonal
    if winning_line(self.board.diagonal()):
      return True

    #check rows
    if True in np.apply_along_axis(winning_line, axis=1, arr=self.board):
      return True

    #check columns
    if True in np.apply_along_axis(winning_line, axis=0, arr=self.board):
      return True

    # nothing was found
    return False

  def LastPlayer(self):
    """
    Get the ID of the last player
    """
    return 3 - self.playerJustMoved


def play_random_game(game_number, display=False):
  play_number = 1
  board = np.zeros((3,3))
  game = TicTacToe(board)


  # player = np.random.choice([1,2])
  while game.HasRemainingMove():
    # get a list of possible moves
    possible_moves = game.GetMoves()

    # select a move at random
    move = np.random.choice(possible_moves)

    # play a move
    game.DoMove(move)

    # show the board
    if display:
      print(str(game))

    # do we have a winner ?
    winning_status = game.GetResult()
    if winning_status:
      break

    # switch players
    if game.HasRemainingMove():
      # player = 1 if player == 2 else 2
      play_number += 1

  return (winning_status, play_number, game.LastPlayer())


if __name__ == "__main__":
  from multiprocessing import Pool
  import itertools
  from tqdm import tqdm


  number_of_games = 5000

  results_list = []

  # processing
  pool = Pool()
  for result in tqdm(pool.imap_unordered(play_random_game, range(number_of_games)),
                     total=number_of_games):
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
