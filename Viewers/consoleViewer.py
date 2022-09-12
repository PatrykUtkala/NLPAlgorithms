import numpy as np


class Viewer:
    def __init__(self):
        self.my_map = None
        self.colors = {0: '\033[94m', 1: '\033[91m', 2: '\033[95m', 3: '\033[30m', 4: '\033[90m'}
        self.colors_agent = {0: '\033[95m', 1: '\033[95m', 2: '\033[95m', 3: '\033[95m', 4: '\033[90m'}

    def setup(self, my_map):
        self.my_map = my_map

    def contact_view(self, current_team):
        current_map = np.copy(self.my_map.current_game_map)
        current_words = list(self.my_map.word_list)
        print(current_map)
        print(current_words)
        print("\033[94mTeam Blue" if current_team == 'b' else "\033[91mTeam Red")
        for i, number in enumerate(current_map):
            current_words[i] = self.colors.get(number, '\033[90m') + current_words[i]

        for i in range(5):
            print(" ".join(current_words[i*5:(i+1)*5]))
        print("\033[97m")

    def agent_view(self, word, word_number, current_team):
        current_map = np.copy(self.my_map.current_game_map)
        current_words = list(self.my_map.word_list)
        print("\033[94mTeam Blue" if current_team == 'b' else "\033[91mTeam Red")
        print("hasło:", word)
        print("liczba skojarzeń:", word_number)
        print("słowa:")
        for i, number in enumerate(current_map):
            current_words[i] = self.colors_agent.get(number, '\033[90m') + current_words[i]

        for i in range(5):
            print(" ".join(current_words[i*5:(i+1)*5]))
        print("\033[97m")
