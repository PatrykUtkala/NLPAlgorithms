from Viewers.consoleViewer import Viewer


class ConsoleContact:
    def __init__(self, team):
        self.viewer = None
        self.game_controller = None
        self.team = team

    def setup(self, game_controller, viewer: Viewer):
        self.game_controller = game_controller
        self.viewer = viewer

    def turn(self):
        self.viewer.contact_view(self.team)
        word = input("Wprowadź swoje hasło ")
        number = input("Wprowadź liczbę skojarzeń ")
        return word, number


class ConsoleAgent:
    def __init__(self, team):
        self.viewer = None
        self.game_controller = None
        self.team = team

    def setup(self, game_controller, viewer: Viewer):
        self.game_controller = game_controller
        self.viewer = viewer

    def turn(self, password, number):
        words = None
        go = True
        while go:
            self.viewer.agent_view(password, number, self.team)
            words = input("Wprowadź numer pola lub wpisz !stop ")
            if words == "!stop":
                break
            words_l = words.split()
            for word in words_l:
                code = self.game_controller.check_tile(word)
                if code != "good":
                    go = False
                    break
