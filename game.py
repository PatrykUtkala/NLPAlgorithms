"""
0 - b, 1 - r, 2 - c, 3 - k
"""
import random
import numpy as np
import os


class MapReader:
    def __init__(self):
        with open('maps.txt') as f:
            maps = f.readlines()
        self.maps = maps
        self.targets = [['b', 0], ['r', 1], ['c', 2], ['k', 3]]

    def get_map(self):
        my_map = random.choice(self.maps).replace("\n", "")
        start_team, my_map = my_map.split(':')
        for set in self.targets:
            my_map = my_map.replace(set[0], str(set[1]))

        my_map = list(my_map.replace("/", ""))
        my_map = list(map(int, my_map))
        my_map = np.array(my_map)
        return my_map


class WordsReader:
    def __init__(self):
        with open('Words.txt', 'r', encoding="utf-8") as f:
            lines = f.readlines()
        self.words_pairs = lines

    def get_words_for_game(self):
        chosen_words = set()
        word_list = list()
        while len(word_list) < 25:
            word_pair = random.choice(self.words_pairs)
            word_pair = word_pair.replace('\n', '')
            if word_pair in chosen_words:
                continue
            chosen_words.add(word_pair)
            word_pair = word_pair.split('/')

            word = random.choice(word_pair)
            word_list.append(word)
        return word_list


class Game:
    def __init__(self, words_reader: WordsReader, maps_reader: MapReader, inputs):
        """

        Args:
            words_reader: WordsReader
            maps_reader: MapReader
            inputs: list of input objects in order: blue word, blue find, red word, red find
        """
        self.inputs = {'bw': inputs[0], 'bf': inputs[1], 'rw': inputs[2], 'rf': inputs[3]}
        self.maps_reader = maps_reader
        self.words_reader = words_reader
        self.current_game = None
        self.current_game_state = None
        self.current_map = None
        self.current_starting_team = None

    def init_new_game(self):
        self.current_starting_team, self.current_map = self.maps_reader.get_map()
        self.current_game = self.words_reader.get_words_for_game()
        self.current_game_state = np.zeros(25)

    def turn(self, current_team):
        number, word = self.inputs[current_team + 'w'].read_word(self.current_game, self.current_map,
                                                                 self.current_game_state)
        find_state = 0
        while find_state == 0:
            word = self.inputs[current_team + 'f'].read_find(self.current_game, self.current_game_state, number, word)
            if word not in self.current_game:
                self.inputs[current_team + 'f'].mistake_notice()
                continue
            number -= 1
            if number < 1:
                find_state = 1
                continue

        return 'finished'

    def connection_word_phase(self, input_object):
        pass

    def find_phase(self, input_object):
        pass


if __name__ == '__main__':
    MR = MapReader()
    game_map = MR.get_map()

    WR = WordsReader()
    words = WR.get_words_for_game()

    with open('Words.txt') as f:
        lines = f.readlines()
