import numpy as np

class TicTacToeEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1
        self.done = False
        self.winner = None
        return self._get_state()

    def step(self, action):
        if self.done or self.board[action] != 0:
            return self._get_state(), -1, True, {}

        self.board[action] = self.current_player
        if self._check_winner(self.current_player):
            self.done = True
            self.winner = self.current_player
            return self._get_state(), 1, True, {}

        if not self.available_actions():
            self.done = True
            self.winner = 0
            return self._get_state(), 0.5, True, {}

        self.current_player *= -1
        return self._get_state(), 0, False, {}

    def available_actions(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == 0]

    def _check_winner(self, player):
        for i in range(3):
            if all(self.board[i, :] == player) or all(self.board[:, i] == player):
                return True
        if all(np.diag(self.board) == player) or all(np.diag(np.fliplr(self.board)) == player):
            return True
        return False

    def _get_state(self):
        return self.board.flatten() * self.current_player

@staticmethod
def _check_winner_static(board, player):
    for i in range(3):
        if all(board[i, :] == player) or all(board[:, i] == player):
            return True
    if all(np.diag(board) == player) or all(np.diag(np.fliplr(board)) == player):
        return True
    return False

TicTacToeEnv._check_winner_static = _check_winner_static

