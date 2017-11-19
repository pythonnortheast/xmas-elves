"""Tests for the Elf Game Session Logic.
"""
from decimal import Decimal
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

    def test_elves_remaining_session(self):
        """Each session knows how many elves are left-over.
        """
        session = self._get_session()
        self.assertEqual(session.elves_remaining, 11)

    def test_total_profit(self):
        """Each session tracks its total profit.
        """
        session = self._get_session()

        wood_profit = self._get_woods_profit(8 + 6)  # Day 1 & 2
        forest_profit = self._get_forest_profit(3)  # Day 1
        mountain_profit = self._get_mountain_profit(1)  # Day 1

        self.assertEqual(session.money_made,
                         wood_profit + forest_profit + mountain_profit)

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

    def test_elves_sent(self):
        """Elves sent is the total sent to forest, woods + mountains.
        """
        day = self._get_snowy_day()
        self.assertEqual(day.elves_sent, 12)

    def test_elves_returned_good(self):
        """When weather is good, all elves come home.
        """
        day = self._get_good_day()
        self.assertEqual(day.elves_returned, 12)

    def test_elves_returned_snow(self):
        """When weather is snowy, mountain elves are lost.
        """
        day = self._get_snowy_day()
        self.assertEqual(day.elves_returned, 11)

    def test_total_money_good(self):
        """The total calculated on good weather accounts all money.
        """
        day = self._get_good_day()
        woods = self._get_woods_profit(8)
        forest = self._get_forest_profit(3)
        mountains = self._get_mountain_profit(1)

        self.assertEqual(day.money_made, woods + forest + mountains)

    def test_total_money_snow(self):
        """The total calculated on snowy weather only counts money from woods.
        """
        day = self._get_snowy_day()
        woods = self._get_woods_profit(6)

        self.assertEqual(day.money_made, woods)

    def _get_session(self):
        """Get the active session.
        """
        return Session.objects.get(pk='fd5b2d8e-78f9-40b3-9d6a-3c39a17ba106')

    def _get_good_day(self):
        """Return the day of good weather.
        """
        return Day.objects.get(pk=1)

    def _get_snowy_day(self):
        """Return the day of snowy weather.
        """
        return Day.objects.get(pk=2)

    def _get_woods_profit(self, elves):
        """Woods give £10 per elf.
        """
        return Decimal('10.00') * elves

    def _get_forest_profit(self, elves):
        """Forest gives £20 per elf.
        """
        return Decimal('20.00') * elves

    def _get_mountain_profit(self, elves):
        """Mountains give £50 per elf.
        """
        return Decimal('50.00') * elves
