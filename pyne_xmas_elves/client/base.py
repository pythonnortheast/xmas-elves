"""The Base Game code.
"""
from decimal import Decimal
from urllib.parse import urljoin

import requests

from .exceptions import (ConnectToServerException, NotSetupException,
                         ServerResponseException, WrongElvesException)

_BASE_SERVER_URL = 'https://elves.pythonnortheast.com'


class BaseGame:
    """The Base Game that we extend from.
    """

    MAX_TURNS = 10
    PLAYER_NAME = None
    SERVER_URL = _BASE_SERVER_URL

    def __init__(self):
        if not self.PLAYER_NAME:
            raise NotSetupException(
                'You must set PLAYER_NAME on {}'.format(
                    self.__class__.__name__))

        uuid, elves, money = self.start_session()
        self._session_id = uuid
        self._elves = elves
        self._money = money
        self._weather = None
        self._current_turn = None

    @property
    def amount_raised(self):
        return self._money

    @property
    def current_turn(self):
        return self._current_turn

    @property
    def last_turn(self):
        return self.MAX_TURNS

    @property
    def previous_weather(self):
        return self._weather

    def turn(self, elves):
        """Implement this method to run the game.
        """
        raise NotImplementedError('The "turn" method must be implemented. It '
                                  'takes the number of elves argument (int).')

    def run(self):
        """Execute the game engine.
        """
        for turn in range(1, self.MAX_TURNS + 1):
            print('Playing turn: {}'.format(turn))
            self._current_turn = turn

            woods, forest, mountain = self.turn(self._elves)

            if not self._is_enough_elves(woods, forest, mountain, self._elves):
                raise WrongElvesException(woods, forest, mountain, self._elves)

            print('Sending elves: {0} (woods), {1} (forest), '
                '{2} (mountain)...'.format(woods, forest, mountain))

            data = self._send_elves(woods, forest, mountain)
            self._money += Decimal(data['money_made'])
            self._elves = data['elves_returned']
            self._weather = data['weather']

            print('* elves returned: {returned}\n'
                  '* money made: {money}\n'
                  '* weather was: {weather}\n'.format(
                      money=self._money,
                      weather=self._weather,
                      returned=self._elves))

    def start_session(self):
        """Generate a Session ID and return it.
        """
        url = urljoin(self.SERVER_URL, "game/")
        response = requests.post(url, {'player_name': self.PLAYER_NAME})
        data = response.json()
        return (data['uuid'],
                data['elves_remaining'],
                Decimal(data['money_made']))

    def _send_elves(self, woods, forest, mountain):
        """Send decision on elves distribution to the server.

        Does not check if game rules were followed.

        """
        path = 'game/{s._session_id}/day/'.format(s=self)
        url = urljoin(self.SERVER_URL, path)
        data = {
            'elves_woods': woods,
            'elves_forest': forest,
            'elves_mountains': mountain
        }
        response = requests.post(url, json=data)

        if response.status_code != 201:
            if response.status_code == 400:
                raise ServerResponseException(response)
            else:
                raise ConnectToServerException(response)

        return response.json()

    def _is_enough_elves(self, woods, forest, mountain, total):
        """Check (client-side) if we have enough elves to send.
        """
        return (woods + forest + mountain) == total
