"""Tests for the Elf Game Session Logic.
"""
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
        self.assertEqual(session.current_day, 1)

    def test_create_day(self):
        """Creating a day adds one to the day count.
        """
        day = Day.objects.create(session=self._get_session(),
                                 elves_woods=4,
                                 elves_forest=4,
                                 elves_mountains=4)
        self.assertEqual(day.day, 2)

    def _get_session(self):
        return Session.objects.get(pk='fd5b2d8e-78f9-40b3-9d6a-3c39a17ba106')
