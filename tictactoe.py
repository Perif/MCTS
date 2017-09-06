import random

class TicTacToe:
  def __init__(self):
    self.playerJustMoved = random.choice([1,2])
    # self.board = np.zeros((3,3))
    self.board = [0,0,0,0,0,0,0,0,0] # 0 = empty, 1 = player 1, 2 = player 2

  def Clone(self):
      """ Create a deep clone of this game state.
      """
      st = TicTacToe()
      st.playerJustMoved = self.playerJustMoved
      st.board = self.board[:]
      return st

  def __repr__(self,):
    """
    Return a string representation of the board
    """
    s= ""
    for i in range(9):
        s += ".XO"[self.board[i]]
        if i % 3 == 2: s += "\n"
    return s

  def GetMoves(self):
    """
    Return a list of possible legal moves
    """
    return [i for i in range(9) if self.board[i] == 0]

  def HasRemainingMove(self):
    """
    Check if moves are still possible
    """
    return len(self.GetMoves())

  def DoMove(self, move):
    """
    Do a game move
    """
    assert move >= 0 and move <= 8 and move == int(move) and self.board[move] == 0
    self.playerJustMoved = 3 - self.playerJustMoved
    self.board[move] = self.playerJustMoved

  def HasWinning(self):
    """
    check if there is a winning game
    """
    for (x,y,z) in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
            if self.board[x] == self.board[y] == self.board[z]:
              if self.board[x] == 1 or self.board[x] == 2:
                return True
    return False

  def GetResult(self, player):
    """
    check if there is a winning game
    """
    for (x,y,z) in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
            if self.board[x] == self.board[y] == self.board[z]:
                if self.board[x] == player:
                    return 1
                else:
                    return -1
    return 0 # draw
    assert False # for debugging

  def LastPlayer(self):
    """
    Get the ID of the last player
    """
    return 3 - self.playerJustMoved


def play_random_game(game_number, display=False):
  play_number = 0
  game = TicTacToe()

  # player = np.random.choice([1,2])
  while game.HasRemainingMove():
    play_number += 1
    # get a list of possible moves
    possible_moves = game.GetMoves()

    # select a move at random
    move = random.choice(possible_moves)

    # play a move
    game.DoMove(move)

    # show the board
    if display:
      print(str(game))

    # do we have a winner ?
    winning_status = game.HasWinning()
    if winning_status:
      break

    # switch players
    if game.HasRemainingMove():
      # player = 1 if player == 2 else 2
      play_number += 1

  return (winning_status, game.LastPlayer())

if __name__ == "__main__":
  from multiprocessing import Pool
  import itertools
  from tqdm import tqdm

  number_of_games = 100000

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
      if result[1] == 1:
        player1 += 1
      elif result[1]:
        player2 += 1
    else:
      neg += 1

  print("Number of positives: %d / %d" % (pos, number_of_games))
  print("Number of negatives: %d / %d" % (neg, number_of_games))
  print("Player1 wins: %2.2f%%" % (float(player1)/pos*100))
  print("Player2 wins: %2.2f%%" % (float(player2)/pos*100))
