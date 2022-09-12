import numpy as np
import random
from GameCodes import num_to_code, code_to_num


class MapReaderBase:
    def __init__(self):
        self.targets = [['b', 0], ['r', 1], ['c', 2], ['k', 3]]
        pass

    def get_map(self):
        with open('Words.txt', 'r', encoding="utf-8") as f:
            lines = f.readlines()
        words_pairs = lines
        chosen_words = set()
        word_list = list()
        while len(word_list) < 25:
            word_pair = random.choice(words_pairs)
            word_pair = word_pair.replace('\n', '')
            if word_pair in chosen_words:
                continue
            chosen_words.add(word_pair)
            word_pair = word_pair.split('/')

            word = random.choice(word_pair)
            word_list.append(word)

        with open('maps.txt') as f:
            maps = f.readlines()
        my_map = random.choice(maps).replace("\n", "")
        start_team, my_map = my_map.split(':')
        for target_set in self.targets:
            my_map = my_map.replace(target_set[0], str(target_set[1]))

        my_map = list(my_map.replace("/", ""))
        my_map = list(map(int, my_map))
        my_map = np.array(my_map)

        return word_list, my_map


class Map:
    def __init__(self, map_reader: MapReaderBase):
        self.map_reader = map_reader
        self.word_list = None
        self.current_word_list = None
        self.game_map = None
        self.current_game_map = None

    def generate(self):
        self.word_list, self.game_map = self.map_reader.get_map()
        self.current_word_list, self.current_game_map = list(self.word_list), np.copy(self.game_map)

    def starting_team(self):
        if np.count_nonzero(self.game_map == 0) > np.count_nonzero(self.game_map == 1):
            return "b"
        else:
            return "r"

    def check_win(self, current_team):
        if 10 in self.current_game_map or 11 in self.current_game_map\
                or np.count_nonzero(self.current_game_map == 0) == 0 or np.count_nonzero(self.current_game_map == 1) == 0:
            return True
        return False

    def check_word(self, word, current_team):
        if word not in self.current_word_list:
            return "f"
        index = self.current_word_list.index(word)
        code_to_return = num_to_code[self.current_game_map[index]]
        self.current_word_list[index] = ""
        if code_to_return == "k":
            self.current_game_map[index] = 10 if current_team == "b" else 11
        else:
            self.current_game_map[index] = 4
        return code_to_return

    def victory(self):
        if 10 in self.current_game_map or np.count_nonzero(self.current_game_map == 1) == 0:
            return 'r'
        elif 11 in self.current_game_map or np.count_nonzero(self.current_game_map == 0) == 0:
            return 'b'
        else:
            raise Exception("Wrong victory status")




if __name__ == "__main__":
    mrb = MapReaderBase()
    new_map = Map(mrb)
    new_map.generate()
    print(new_map.game_map)
    print(new_map.word_list)

    print(new_map.game_map.reshape((5, 5)))
    for i in range(5):
        print(new_map.word_list[i*5:(i+1)*5])
