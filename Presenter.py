import repository


class Presenter:
    def __init__(self, players=set()):
        self._players = list(players)
        self._history = list()
        self._repository = repository
        self._current_player = 0

    def get_current_player(self):
        """TODO: Doc..."""
        return self._players[self._current_player]

    def turn(self, option):
        """TODO: Doc..."""
        if self.check_history(option):
            self._log(option, False)

            return False

        word = self.search(option)
        if word:
            status = (word == option)
            self._log(option, status)

            if status:
                self._next_player()

            return status

        self._log(option, False)

        return False

    def check_history(self, option):
        """TODO: Doc..."""
        for turn in self._history:
            if turn.get('word') == option:
                return True

        return False

    def search(self, option):
        """TODO: Doc..."""
        words = self._repository.search(option)
        if len(words) == 0:
            return None

        return words[0].get('word')

    def _log(self, option, status, note=''):
        """TODO: Doc..."""
        self._history.append({
            'player': self.get_current_player(),
            'word': option,
            'status': status,
            'note': note
        })

        return self

    def _next_player(self):
        """TODO: Doc..."""
        if self._current_player + 1 >= len(self._players):
            self._current_player = 0
        else:
            self._current_player += 1

        return self
