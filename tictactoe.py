import numpy as np

def DisplayGame(state, play_number):
  assert(state.shape[0] == state.shape[1])

  def print_empty():
    print("|-|-|-|")

  def print_row(row):
    print("|%d|%d|%d|" % (row[0], row[1], row[2]))

  print("|Game:%d|" % play_number)
  print_empty()
  print_row(state[0])
  print_empty()
  print_row(state[1])
  print_empty()
  print_row(state[2])
  print_empty()


def GetMoves(state):
  return list(np.where(state.ravel() == 0)[0])

def HasRemainingMove(state):
  return len(GetMoves(state))

def is_legal_move(move, state):
  legal_moves = GetMoves(state)
  return True if move in legal_moves else False

def DoMove(move, value, state):
  if not is_legal_move(move, state):
    return False
  coords = (np.floor_divide(move, state.shape[0]),
            np.mod(move, state.shape[0]))
  state[coords[0], coords[1]] = value
  return True


def GetResult(state):

  def winning_line(elems):
    ll = list(set(elems))
    if len(ll) == 1 and ll[0] != 0:
      return True
    return False

  # check the diagonal
  if winning_line(state.diagonal()):
    return True

  #check rows
  if True in np.apply_along_axis(winning_line, axis=1, arr=state):
    return True

  #check columns
  if True in np.apply_along_axis(winning_line, axis=0, arr=state):
    return True

  # nothing was found
  return False


def play_random_game(game_number, display=False):
  play_number = 1
  state = np.zeros((3,3))

  player = np.random.choice([1,2])
  while HasRemainingMove(state):
    # get a list of possible moves
    possible_moves = GetMoves(state)

    # select a move at random
    move = np.random.choice(possible_moves)

    # play a move
    DoMove(move,player,state)

    # show the state
    if display:
      DisplayGame(state,play_number)

    # do we have a winner ?
    winning_status = GetResult(state)
    if winning_status:
      break

    # switch players
    if HasRemainingMove(state):
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
