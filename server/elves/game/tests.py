"""Tests for the Elf Game Session Logic.
"""
from decimal import Decimal
from unittest.mock import patch

from django.core.urlresolvers import reverse
from django.test import TestCase

from rest_framework import status, test

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

    def test_create_with_day(self):
        """Can pass the day in manually.
        """
        day = Day.objects.create(session=self._get_session(),
                                 elves_woods=4,
                                 elves_forest=4,
                                 elves_mountains=4,
                                 day=4)
        self.assertEqual(day.day, 4)

    @patch('elves.game.models.random')
    def test_create_with_weather(self, random):
        """Can pass weather in manually.
        """
        day = Day.objects.create(session=self._get_session(),
                                 elves_woods=4,
                                 elves_forest=4,
                                 elves_mountains=4,
                                 weather='good')
        self.assertEqual(day.weather, 'good')
        self.assertFalse(random.choice.called)

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


class GameTestCase(test.APITestCase):
    """Test the Elf Game logic.
    """

    fixtures = [
        'game/sessions',
    ]

    SESSION_ID = 'fd5b2d8e-78f9-40b3-9d6a-3c39a17ba106'

    def test_list_response_code(self):
        """The session-list returns HTTP 200.
        """
        response = self.client.get(reverse('session-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_sessions(self):
        """List the sessions with the player data.
        """
        response = self.client.get(reverse('session-list'))

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['player_name'], 'Steve Jones')

    def test_new_session_201(self):
        """New player session returns 201.
        """
        response = self.client.post(reverse('session-list'),
                                    {'player_name': 'James Smith'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_new_session_data(self):
        """New player session returns information for querying + adding days.
        """
        response = self.client.post(reverse('session-list'),
                                    {'player_name': 'James Smith'})

        self.assertEqual(response.data['player_name'], 'James Smith')
        self.assertTrue(response.data['uuid'])
        self.assertEqual(response.data['elves_remaining'], 12)
        self.assertEqual(response.data['money_made'], '0.00')

    def test_list_days_200(self):
        """The list of days returns HTTP 200.
        """
        response = self.client.get(reverse('session-day',
                                           kwargs={'pk': self.SESSION_ID}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_day_list(self):
        """The list of days returns each day's info for a session.
        """
        response = self.client.get(reverse('session-day',
                                           kwargs={'pk': self.SESSION_ID}))

        self.assertEqual(len(response.data), 2)

    def test_day_order(self):
        """Days are ordered by day #
        """
        response = self.client.get(reverse('session-day',
                                           kwargs={'pk': self.SESSION_ID}))

        for i, day in enumerate(response.data, start=1):
            self.assertEqual(day['day'], i)

    def test_get_day_1(self):
        """Day 1 maps to the first day.
        """
        response = self.client.get(reverse('session-day',
                                           kwargs={'pk': self.SESSION_ID}))

        day = response.data[0]
        self.assertEqual(day['elves_sent'], 12)
        self.assertEqual(day['elves_returned'], 12)
        self.assertEqual(day['money_made'], '190.00')

    def test_get_day_2(self):
        """Day 2 maps to the second day.
        """
        response = self.client.get(reverse('session-day',
                                           kwargs={'pk': self.SESSION_ID}))

        day = response.data[1]
        self.assertEqual(day['elves_sent'], 12)
        self.assertEqual(day['elves_returned'], 11)
        self.assertEqual(day['money_made'], '60.00')

    def test_create_day_201(self):
        """Add a day returns 201.
        """
        response = self.client.post(
            reverse('session-day', kwargs={'pk': self.SESSION_ID}),
            {
                'elves_woods': 5,
                'elves_forest': 5,
                'elves_mountains': 1,
            })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         msg=response.data)

    @patch('elves.game.models.random')
    def test_create_day_data(self, random):
        """Creating a day with the number of elves to send.
        """
        random.choice.return_value = 'good'

        response = self.client.post(
            reverse('session-day', kwargs={'pk': self.SESSION_ID}),
            {
                'elves_woods': 5,
                'elves_forest': 5,
                'elves_mountains': 1,
            })

        self.assertDictEqual(
            response.data,
            {
                'day': 3,
                'elves_woods': 5,
                'elves_forest': 5,
                'elves_mountains': 1,
                'money_made': '200.00',
                'elves_sent': 11,
                'elves_returned': 11,
                'weather': 'good',
            })

    @patch('elves.game.models.random')
    def test_create_send_all_elves(self, random):
        """Creating a day requires all elves to be sent.
        """
        random.choice.return_value = 'good'

        response = self.client.post(
            reverse('session-day', kwargs={'pk': self.SESSION_ID}),
            {
                'elves_woods': 5,
                'elves_forest': 5,
                'elves_mountains': 0,
            })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertListEqual(response.data['elves_woods'],
                             ['You must send exactly 11 elves'])
        self.assertListEqual(response.data['elves_forest'],
                             ['You must send exactly 11 elves'])
        self.assertListEqual(response.data['elves_mountains'],
                             ['You must send exactly 11 elves'])
        self.assertFalse(random.choice.called)

    @patch('elves.game.models.random')
    def test_create_too_many_elves(self, random):
        """Can only send available elves.
        """
        random.choice.return_value = 'good'

        response = self.client.post(
            reverse('session-day', kwargs={'pk': self.SESSION_ID}),
            {
                'elves_woods': 5,
                'elves_forest': 5,
                'elves_mountains': 2,
            })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertListEqual(response.data['elves_woods'],
                             ['You must send exactly 11 elves'])
        self.assertListEqual(response.data['elves_forest'],
                             ['You must send exactly 11 elves'])
        self.assertListEqual(response.data['elves_mountains'],
                             ['You must send exactly 11 elves'])
        self.assertFalse(random.choice.called)

    @patch('elves.game.models.random')
    def test_max_turns(self, random):
        """Can only run the game for 10 rounds.
        """
        random.choice.return_value = 'good'
        for x in range(3, 11):
            Day.objects.create(
                elves_woods=11,
                elves_forest=0,
                elves_mountains=0,
                session=self._get_session(),
                day=x)

        response = self.client.post(
            reverse('session-day', kwargs={'pk': self.SESSION_ID}),
            {
                'elves_woods': 5,
                'elves_forest': 5,
                'elves_mountains': 1,
            })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         msg=response.data['day'])

        self.assertListEqual(response.data['day'],
                             ['Your elf game has completed at 10 turns!'])

    def _get_session(self):
        """Get the active session.
        """
        return Session.objects.get(pk='fd5b2d8e-78f9-40b3-9d6a-3c39a17ba106')
