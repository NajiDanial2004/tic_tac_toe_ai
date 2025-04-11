import torch
from env.tic_tac_toe import TicTacToeEnv

class HybridBot:
    def __init__(self, model, bot_player):
        self.model = model.eval()
        self.bot_player = bot_player
        self.human_player = -bot_player

    def get_action(self, env):
        # Rule 1: Win if possible
        for move in env.available_actions():
            temp_board = env.board.copy()
            temp_board[move] = self.bot_player
            if TicTacToeEnv._check_winner_static(temp_board, self.bot_player):
                return move

        # Rule 2: Block opponent win
        for move in env.available_actions():
            temp_board = env.board.copy()
            temp_board[move] = self.human_player
            if TicTacToeEnv._check_winner_static(temp_board, self.human_player):
                return move

        # Rule 3: Take center
        if env.board[1, 1] == 0:
            return (1, 1)

        # Rule 4: Use DQN policy
        state = torch.FloatTensor(env._get_state()).unsqueeze(0)
        with torch.no_grad():
            q_vals = self.model(state)[0]
        valid = env.available_actions()
        flat = [r * 3 + c for r, c in valid]
        best = max(flat, key=lambda x: q_vals[x])
        return divmod(best, 3)

