"""Tests for the Elf Game Session Logic.
"""
from unittest.mock import patch

from django.test import TestCase

from .models import Session, Day


class SessionTestCase(TestCase):
    """Test the Session models.
    """

    fixtures = [
        'game/sessions',
    ]

    def test_get_current_day(self):
        """Get the current day for the session.
        """
        session = self._get_session()
        self.assertEqual(session.current_day, 2)

    def test_create_day(self):
        """Creating a day adds one to the day count.
        """
        day = Day.objects.create(session=self._get_session(),
                                 elves_woods=4,
                                 elves_forest=4,
                                 elves_mountains=4)
        self.assertEqual(day.day, 3)

    @patch('elves.game.models.random')
    def test_random_weather(self, random):
        """Creating a day sets the weather at random.
        """
        random.choice.return_value = 'good'
        day = Day.objects.create(session=self._get_session(),
                                 elves_woods=4,
                                 elves_forest=4,
                                 elves_mountains=4)

        self.assertEqual(day.weather, 'good')
        self.assertEqual(random.choice.call_count, 1)

    @patch('elves.game.models.random')
    def test_usually_good_weather(self, random):
        """The random generator should have a 2:1 chance for good weather.
        """
        random.choice.return_value = 'snow'
        Day.objects.create(session=self._get_session(),
                           elves_woods=4,
                           elves_forest=4,
                           elves_mountains=4)

        self.assertListEqual(random.choice.call_args[0][0],
                             ['good', 'good', 'snow'])

    def _get_session(self):
        return Session.objects.get(pk='fd5b2d8e-78f9-40b3-9d6a-3c39a17ba106')
