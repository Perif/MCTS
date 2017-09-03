import random
import tictactoe
import numpy as np
from math import sqrt, log

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """

    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # the move that got us to this node - "None" for the root node
        self.parentNode = parent  # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves()  # future child nodes
        # the only part of the state that the Node needs later
        self.playerJustMoved = state.playerJustMoved

    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key=lambda c: c.wins /
                   c.visits + sqrt(2 * log(self.visits) / c.visits))[-1]
        return s

    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move=m, parent=self, state=s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
            s += c.TreeToString(indent + 1)
        return s

    def IndentString(self, indent):
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
            s += str(c) + "\n"
        return s


def UCT(rootstate, itermax, verbose=False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state=rootstate)

    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()

        # Select
        while node.untriedMoves == [] and node.childNodes != []:  # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)

        # Expand
        # if we can expand (i.e. state/node is non-terminal)
        if node.untriedMoves != []:
            m = random.choice(node.untriedMoves)
            state.DoMove(m)
            node = node.AddChild(m, state)  # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetMoves() != []:  # while state is non-terminal
            state.DoMove(random.choice(state.GetMoves()))

        # Backpropagate
        while node != None:  # backpropagate from the expanded node and work back to the root node
            # state is terminal. Update node with result from POV of node.playerJustMoved
            node.Update(state.GetResult(node.playerJustMoved))
            node = node.parentNode

    # Output some information about the tree - can be omitted
    if (verbose):
        print rootnode.TreeToString(0)
    else:
        print rootnode.ChildrenToString()

    # return the move that was most visited
    return sorted(rootnode.childNodes, key=lambda c: c.visits)[-1].move


def UCTPlayGame():
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    state = tictactoe.TicTacToe()
    while (state.GetMoves() != []):
        print str(state)
        if state.LastPlayer() == 1:
            # play with values for itermax and verbose = True
            m = UCT(rootstate=state, itermax=1000, verbose=False)
        else:
            m = np.random.choice(state.GetMoves())
            #m = UCT(rootstate=state, itermax=100, verbose=False)
        print "Best Move: " + str(m) + "\n"
        state.DoMove(m)
    if state.GetResult(state.LastPlayer()) == 1.0:
        print "Player " + str(state.LastPlayer()) + " wins!"
    elif state.GetResult(state.LastPlayer()) == 0.0:
        print "Player " + str(3 - state.LastPlayer()) + " wins!"
    else:
        print "Nobody wins!"
    print str(state)


if __name__ == "__main__":
    """ Play a single game to the end using UCT for both players.
    """
    UCTPlayGame()
