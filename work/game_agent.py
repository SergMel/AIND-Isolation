"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

class UF:
 
 def __init__(self, n):
  if n < 1:
   raise ValueError("Number if items should be greter then 0")
  self.groupIds = list(range(n)) 
  self.groupCount = n
  self.sz = [1] * n
  
 def root(self, i):
  while i != self.groupIds[i]:  
   self.groupIds[i] = self.groupIds[self.groupIds[i]]
   i = self.groupIds[i]
  return i
 
 def connected(self,i, j):
  if i >= len(self.groupIds) or j >= len(self.groupIds):
    raise ValueError("Item index is out of range")
  return self.root(i) == self.root(j)
 
 
 def union(self, i, j):
  if self.connected(i, j):
   return
  ri = self.root(i)
  rj = self.root(j)
  if (self.sz[ri] < self.sz[rj]):
   self.groupIds[rj] =ri
   self.sz[ri] +=self.sz[rj]
  else:
   self.groupIds[ri] = rj
   self.sz[rj] += self.sz[ri]
  self.groupCount -=1   
  
 def count(self):
  return self.groupCount


def calculate_position_score(mv, height, width):
        
    if (mv[0] < 1 or mv[0] > height - 2) and (mv[1] < 1 or mv[1] > width - 2):
        return 1
    if (mv[0] < 1 or mv[0] > height - 2) and (mv[1] < 2 or mv[1] > width - 3) or \
        (mv[0] < 2 or mv[0] > height - 3) and (mv[1] < 1 or mv[1] > width - 2):
        return 2
    if (mv[0] < 2 or mv[0] > height - 3) and (mv[1] < 2 or mv[1] > width - 3):
        return 3
    if (mv[0] < 2 or mv[0] > height - 3) or (mv[1] < 2 or mv[1] > width - 3):
        return 5    
    
    return 7

def get_index(game, loc):
    return loc[0] * game.height + loc[1]

def get_location(game, i):
    return (i % game.height, i // game.height)

def get_moves(game, loc):
    if loc == Board.NOT_MOVED:
        return self.get_blank_spaces()

    r, c = loc
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]
    valid_moves = [(r + dr, c + dc) for dr, dc in directions
                   if game.move_is_legal((r + dr, c + dc))]        
    return valid_moves


def get_accessible_count(game, blanks, player ):    
    dic = dict((get_index(game, blanks[i]), i) for i in range(blanks) )
    uf = UF(len(blanks))
    
    
    
    
def custom_score_t(game, player, k):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    opponent = game.get_opponent(player)           
    
    op_mvs = game.get_legal_moves(opponent)
    mvs = game.get_legal_moves(player)
    
    if not op_mvs:
        return float("inf")
    
    if not mvs:
        return float("-inf")
    
    res = float(len(mvs)) - 0.001 * len(op_mvs) 

    return res

def custom_score(game, player):
    return custom_score_t(game, player, 0.04)

def custom_score_0(game, player):
    return custom_score_t(game, player, 0.08)

def custom_score_1(game, player):
    return custom_score_t(game, player, 0.12)

def custom_score_2(game, player):
    return custom_score_t(game, player, 0.16)

def custom_score_3(game, player):
    return custom_score_t(game, player, 0.20)

def custom_score_4(game, player):
    return custom_score_t(game, player, 0.24)

def custom_score_5(game, player):
    return custom_score_t(game, player, 0.28)

def custom_score_6(game, player):
    return custom_score_t(game, player, 0.32)

def custom_score_7(game, player):
    return custom_score_t(game, player, 0.36)

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=25.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)            
        
        _, move = max([(self.getMin(game.forecast_move(m), depth-1), m) for m in legal_moves])
        # TODO: finish this function!
        return move

    def getMax(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        if depth == 0:
            return self.score(game, self)
            
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return float("-inf")            
        
        return max([self.getMin(game.forecast_move(m), depth-1) for m in legal_moves])
         
    def getMin(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        if depth == 0:
            return self.score(game, self)
            
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return float("inf")            
        
        return min([self.getMax(game.forecast_move(m), depth-1) for m in legal_moves])


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()                    
        
        res = None
        try:
            depth = 1
            while True:            
                next_res = self.alphabeta(game, depth)
                res = next_res
                depth+=1
        except SearchTimeout:
            return res   
             

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()            
        
        return self.alphabeta_pair(game, depth, alpha, beta)[0]
    
    def alphabeta_pair(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return ((-1, -1), float("-inf"))            
        max_val = float("-inf")
        move = (-1, -1)
        for m in legal_moves:
            val = self.getMin(game.forecast_move(m), depth-1,  alpha, beta)
            if val > max_val or max_val==float("-inf"):
                max_val = val
                move = m
            alpha = max(max_val, alpha)        
        
        return (move, max_val)

    def getMax(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        if depth == 0:
            return self.score(game, self)
        
        legal_moves = game.get_legal_moves()
        
        if not legal_moves:
            return float("-inf")      
        
              
        max_val = float("-inf")
        for m in legal_moves:
            max_val = max(max_val, self.getMin(game.forecast_move(m), depth-1, alpha, beta))
            if max_val >= beta:
                return max_val
            alpha = max(max_val, alpha)              
        
        return max_val
         
    def getMin(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self)
        
        legal_moves = game.get_legal_moves()
        
        if not legal_moves:
            return float("inf")      
                       
        min_val = float("inf")
        for m in legal_moves:
            min_val = min(min_val, self.getMax(game.forecast_move(m), depth-1, alpha, beta))
            if min_val <= alpha:
                return min_val
            beta = min(min_val, beta)              
        
        return min_val
