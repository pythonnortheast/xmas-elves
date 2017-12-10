"""Model the basic game systems.
"""
import random

from decimal import Decimal
from uuid import uuid4

from django.core import exceptions
from django.db import models


class DayQuerySet(models.QuerySet):
    """QuerySet managing the state of individual days.
    """

    def create(self, *args, **kwargs):
        """Set a default day based on the previous days.

        The front-end user shouldn't be able to determine the day.
        """
        if 'day' not in kwargs:
            kwargs['day'] = self.filter(
                session=kwargs['session']).aggregate(
                    latest=models.functions.Coalesce(models.Max('day'), 0)
            )['latest'] + 1

        if 'weather' not in kwargs:
            kwargs['weather'] = random.choice(['good', 'good', 'snow'])

        return super().create(*args, **kwargs)

    def get_current_day(self):
        """Return the highest day.
        """
        return self.latest().day


class Session(models.Model):
    """Model an individual game session.

    A session consists of 10 turns and tracks the total number of elves
    available to the player in each session.
    """

    MAX_DAYS = 10

    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid4)

    elves_start = models.PositiveIntegerField(default=12)
    player_name = models.CharField(max_length=200)

    def __str__(self):
        """Return a str representation.
        """
        return 'Day {s.current_day} - with {s.current_elves} remaining'.format(
            s=self)

    @property
    def current_day(self):
        """Return the current day.

        This runs an extra query.
        """
        return self.days.get_current_day()

    @property
    def elves_remaining(self):
        """Return the current remaining elves.

        This runs an extra query.
        """
        try:
            last_day = self.days.latest()
        except exceptions.ObjectDoesNotExist:
            return self.elves_start
        return last_day.elves_returned

    @property
    def money_made(self):
        """Return the total money made for a session.
        """
        return sum(d.money_made for d in self.days.all())


class Day(models.Model):
    """A day for which elves were sent to the forest or mountain.
    """

    objects = DayQuerySet.as_manager()

    WEATHER_CHOICES = (
        ('good', 'Good'),
        ('snow', 'Snow'),
    )

    WOODS_VALUE = Decimal('10.00')
    FOREST_VALUE = Decimal('20.00')
    MOUNTAINS_VALUE = Decimal('50.00')

    session = models.ForeignKey(Session, related_name='days',
                                help_text='The session for the day.')

    day = models.PositiveIntegerField(help_text='The current day.')
    weather = models.CharField(
        choices=WEATHER_CHOICES, max_length=10,
        help_text='The autocalculated weather for the day. If the weather is '
        'good, all elves will return. If it snowed, all elves sent to the '
        'mountains will die and any elves sent to the forest return '
        'empty-handed.')

    elves_woods = models.PositiveIntegerField(
        help_text='Elves sent to the woods by the player. These elves acquire '
        '£10 worth of wood for this day.')
    elves_forest = models.PositiveIntegerField(
        help_text='Elves sent to the forest by the player. These elves acquire '
        '£20 worth of wood for this day if the weather was good. If not, they '
        'will return empty-handed.')
    elves_mountains = models.PositiveIntegerField(
        help_text='Elves sent to the mountains by the player. These elves '
        'acquire £50 worth of wood for this day if the weather was good. If '
        'not, they will all die.')

    class Meta:
        get_latest_by = 'day'
        unique_together = 'session', 'day'

    def __str__(self):
        """The string representation.
        """
        return 'Day {s.day} for Session {session} with {elves} elves'.format(
            s=self, session=self.session.uuid, elves=self.elves_sent)

    @property
    def elves_sent(self):
        """Return the total elves sent.
        """
        return self.elves_forest + self.elves_mountains + self.elves_woods

    @property
    def elves_returned(self):
        """Return the total elves that returned safely.

        In good weather, all elves return.
        In snowy weather, only elves sent to the forest and woods return.
        """
        if self.weather == 'good':
            return self.elves_sent

        return self.elves_forest + self.elves_woods

    @property
    def money_made(self):
        """Return the total money made by the elves.

        Woods are £10 per elf.
        Forests are £20 per elf.
        Mountains are £50 per elf.

        In good weather, all elves return. In snowy weather, only elves sent to
        the woods return with money.
        """
        elves_woods = self.elves_woods * self.WOODS_VALUE

        if self.weather == 'snow':
            return elves_woods

        elves_forest = self.elves_forest * self.FOREST_VALUE
        elves_mountains = self.elves_mountains * self.MOUNTAINS_VALUE

        return elves_woods + elves_forest + elves_mountains
