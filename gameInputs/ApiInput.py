import requests

from Viewers.consoleViewer import Viewer
from GameCodes import num_to_code, code_to_num


class ApiContact:
    def __init__(self, team):
        self.viewer = None
        self.game_controller = None
        self.team = team
        self.address = None

    def setup(self, game_controller, viewer: Viewer):
        self.game_controller = game_controller
        self.viewer = viewer

    def set_address(self, address):
        self.address = address + '/words'
        return self

    def turn(self):
        # self.viewer.contact_view(self.team)
        my_map = self.game_controller.game_map
        response = requests.post(self.address, json={"team": code_to_num[self.team], "current_game_map": my_map.current_game_map.tolist(),
                                                     "current_word_list": my_map.current_word_list})
        answer = response.json()
        return answer["word"], answer["number"]


class ApiAgent:
    def __init__(self, team):
        self.viewer = None
        self.game_controller = None
        self.team = team
        self.address = None

    def setup(self, game_controller, viewer: Viewer):
        self.game_controller = game_controller
        self.viewer = viewer

    def set_address(self, address):
        self.address = address + '/find'
        return self

    def turn(self, password, number):
        go = True
        tries = 0
        while go:
            self.viewer.agent_view(password, number, self.team)
            my_map = self.game_controller.game_map
            response = requests.post(self.address, json={"current_word_list": my_map.current_word_list,
                                                         "password": password})
            tries += 1
            answer = response.json()
            words = answer["word"]
            print("AI guess:", words)
            if words == "!stop":
                break
            words_l = words.split()
            for word in words_l:
                code = self.game_controller.check_tile(word)
                if code != "good":
                    go = False
                    break
            if tries >= int(number):
                go = False
