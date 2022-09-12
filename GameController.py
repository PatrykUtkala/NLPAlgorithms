"""

"""
from maps import Map
from maps import MapReaderBase
from Viewers.consoleViewer import Viewer
from gameInputs.consoleInput import ConsoleAgent, ConsoleContact
from gameInputs.ApiInput import ApiAgent, ApiContact


class GameController:
    def __init__(self, map_loader, viewer, players1, players2):
        """

        Args:
            map_loader: Class used to get map setup
            viewer: class used by players objects to view current game state
            players1: Blue team [contact, agent]
            players2: Red team [contact, agent]
        """
        self.game_map = Map(map_loader)
        self.viewer = viewer
        self.Players1 = players1
        self.Players2 = players2
        self.setup()
        self.players = {"b": players1, "r": players2}
        self.quick_swap = {"b": "r", "r": "b"}
        self.CurrentPlayers = None
        self.current_team = None
        self.finished = True

    def setup(self):
        """
        Setup class connections
        """
        self.viewer.setup(self.game_map)
        self.Players1[0].setup(self, self.viewer)
        self.Players1[1].setup(self, self.viewer)
        self.Players2[0].setup(self, self.viewer)
        self.Players2[1].setup(self, self.viewer)

    def new_game(self):
        """
        Create new game with present objects
        """
        self.game_map.generate()
        starting_team = self.game_map.starting_team()
        self.CurrentPlayers = self.players[starting_team]
        self.current_team = starting_team

        self.finished = False

    def play(self):
        """
        Play game until it's finished
        """
        while not self.finished:
            word, number = self.CurrentPlayers[0].turn()
            self.CurrentPlayers[1].turn(word, number)
            self.check_if_finished()
            self.swap_teams()

        print("the winner is team:" + self.game_map.victory())

    def check_if_finished(self):
        """
        Checks map to determine if game is finished
        """
        self.finished = self.game_map.check_win(self.current_team)

    def swap_teams(self):
        """
        Swap current team at the end of a turn
        """
        if self.finished:
            return
        self.current_team = self.quick_swap[self.current_team]
        self.CurrentPlayers = self.players[self.current_team]

    def check_tile(self, word):
        """
        Checks if words is on the map and what is under it. The method determinds if guessing shoud continue.

        Args:
            word: word to check

        Returns: code of check
        """
        code = self.game_map.check_word(word, self.current_team)
        if code == self.current_team:
            if self.game_map.check_win(self.current_team):
                return "finished"
            else:
                return "good"
        elif code == "k":
            return "dead"
        else:
            return "stop"
        pass


if __name__ == "__main__":
    map_loader = MapReaderBase()
    viewer = Viewer()
    # players1 = [ConsoleContact('b'), ConsoleAgent('b')]
    # players2 = [ConsoleContact('r'), ConsoleAgent('r')]
    address = "http://0001-35-243-170-205.ngrok.io"
    # players1 = [ApiContact('b').set_address(address), ConsoleAgent('b')]
    # players2 = [ApiContact('r').set_address(address), ConsoleAgent('r')]
    players1 = [ApiContact('b').set_address(address), ApiAgent('b').set_address(address)]
    players2 = [ApiContact('r').set_address(address), ApiAgent('r').set_address(address)]

    game = GameController(map_loader, viewer, players1, players2)
    game.new_game()
    game.viewer.contact_view(game.current_team)
    game.play()
