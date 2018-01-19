import repository


class Presenter:
    def __init__(self, players=set(), penalty=0.3):
        p = list()
        for player in players:
            p.append({
                'name': player,
                'score': 0.0
            })
        self._players = p
        self._history = list()
        self._repository = repository
        self._current_player = 0
        self.PENALTY = penalty

    def get_current_player(self):
        """TODO: Doc..."""
        return self._players[self._current_player]

    def get_last_turn(self, success):
        """TODO: Doc..."""
        if not len(self._history):
            return None

        if not success:
            return self._history[-1]

        for i in range(1, len(self._history)):
            if self._history[-i].get('status'):
                return self._history[-i]

        return None

    def turn(self, option):
        """TODO: Doc..."""
        option = option.lower()
        o_len = len(option)

        if self.check_history(option):
            self._log(option, False)
            self._add_score(-o_len)

            return False

        if self.get_last_turn(True) and option[0] != self.get_last_turn(True).get('option')[-1]:
            self._log(option, False)
            self._add_score(-o_len)

            return False

        word = self.search(option)
        # print """\n\nFOUND: %s\n\n""" % word
        if word:
            status = (word == option)
            self._log(option, status)
            self._add_score(o_len if status else -o_len)

            if status:
                self._next_player()

            return status

        self._log(option, False)
        self._add_score(-o_len)

        return False

    def check_history(self, option):
        """TODO: Doc..."""
        for turn in self._history:
            if turn.get('option') == option and turn.get('status') == True:
                return True

        return False

    def search(self, option):
        """TODO: Doc..."""
        words = self._repository.search(option)
        if len(words) == 0:
            return None

        return words[0].get('_word')

    def _log(self, option, status, note=''):
        """TODO: Doc..."""
        self._history.append({
            'player': self.get_current_player().get('name'),
            'option': option,
            'score': len(option) if status else -len(option),
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

    def _add_score(self, score):
        cp = self.get_current_player()
        score = score if score >= 0 else score * self.PENALTY
        cp['score'] += score

        if cp['score'] < 0.0:
            cp['score'] = 0.0

        return self
