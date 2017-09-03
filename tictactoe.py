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

  def GetResult(self, player):
    """
    check if there is a winning game
    """
    def winning_line(elems):
      ll = list(set(elems))
      if len(ll) == 1 and ll[0] != 0:
        return (True, ll[0])
      return (False, None)

    # check the diagonal
    diag_win, winner = winning_line(self.board.diagonal())
    if diag_win:
      if winner == player:
        return 1.0
      else:
        return 0.0

    #check rows
    rows_check = np.apply_along_axis(winning_line, axis=1, arr=self.board)
    row_win = [x[1] for x in rows_check if x[0]]
    # if there is something in row_wine, proceed
    if row_win:
      if row_win[0] == player:
        return 1.0
      else:
        return 0.0

    #check columns
    cols_check = np.apply_along_axis(winning_line, axis=0, arr=self.board)
    col_win = [x[1] for x in cols_check if x[0]]
    # if there is something in col_wine, proceed
    if col_win:
      if col_win[0] == player:
        return 1.0
      else:
        return 0.0

    if self.GetMoves() == []: return 0.5
    assert False # for safety

  def LastPlayer(self):
    """
    Get the ID of the last player
    """
    return 3 - self.playerJustMoved


def play_random_game(game_number, display=False):
  play_number = 0
  board = np.zeros((3,3))
  game = TicTacToe(board)


  # player = np.random.choice([1,2])
  while game.HasRemainingMove():
    play_number += 1
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
  winning_status = game.GetResult(1)
  if winning_status == 1:
    return (True, play_number, 1)
  elif winning_status == 0.0:
    return (True, play_number, 2)
  return (False, play_number, 0)


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
      if result[2] == 1.0:
        player1 += 1
      else:
        player2 += 1
    else:
      neg += 1

  print("Number of positives: %d / %d" % (pos, number_of_games))
  print("Number of negatives: %d / %d" % (neg, number_of_games))
  print("Player1 wins: %2.2f%%" % (float(player1)/pos*100))
  print("Player2 wins: %2.2f%%" % (float(player2)/pos*100))
