import random

class EasyBot:
    def get_action(self, env):
        valid_moves = env.available_actions()
        if random.random() < 0.7:
            return random.choice(valid_moves)
        preferred = [(1,1), (0,0), (0,2), (2,0), (2,2)]
        smart_moves = [move for move in preferred if move in valid_moves]
        if smart_moves:
            return random.choice(smart_moves)
        return random.choice(valid_moves)

