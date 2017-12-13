"""Serializers for Sessions and Days.
"""
from rest_framework import serializers

from .models import Day, Session
from .validators import positive_number


class SessionSerializer(serializers.ModelSerializer):
    """A single game session.

    Identified using the `uuid` field, POST a new day against this endpoint to
    with your elf allocation.
    """

    current_day = serializers.IntegerField(read_only=True)
    elves_remaining = serializers.IntegerField(read_only=True)
    money_made = serializers.DecimalField(read_only=True, max_digits=10,
                                          decimal_places=2)

    class Meta:
        exclude = 'elves_start',
        model = Session
        extra_kwargs = {
            'uuid': {
                'read_only': True,
            },
        }


class DaySerializer(serializers.ModelSerializer):
    """Manage an individual Day.
    """

    elves_sent = serializers.IntegerField(read_only=True)
    elves_returned = serializers.IntegerField(read_only=True)

    money_made = serializers.DecimalField(read_only=True, max_digits=10,
                                          decimal_places=2)

    class Meta:
        exclude = 'session', 'id'
        extra_kwargs = {
            'day': {
                'read_only': True,
            },
            'weather': {
                'read_only': True,
            },
            'elves_woods': {
                'validators': [positive_number],
            },
            'elves_forest': {
                'validators': [positive_number],
            },
            'elves_mountains': {
                'validators': [positive_number],
            },
        }
        model = Day

    def validate(self, attrs):
        """Validate the whole day.

        Run a number of validation rules including ensuring we don't allow
        more elves than exist to be sent. We also assign any extra information
        we need to create the Day.
        """
        attrs['session'] = self.context['session']

        self._validate_total_elves(attrs)
        self._validate_day()
        return attrs

    def _validate_day(self):
        """Validate we have not run for more than 10 days.
        """
        if self.context['session'].days.count() == Session.MAX_DAYS:
            raise serializers.ValidationError({
                'day': 'Your elf game has completed at {} turns!'.format(
                    Session.MAX_DAYS)
            })

    def _validate_total_elves(self, attrs):
        """Validate elves sent == elves available.

        If this is invalid, raise serializers.ValidationError.
        """
        remaining = self.context['session'].elves_remaining

        elves_sent = (
            attrs['elves_woods'] +
            attrs['elves_forest'] +
            attrs['elves_mountains'])
        if remaining != elves_sent:
            message = 'You must send exactly {} elves'.format(remaining)
            raise serializers.ValidationError({
                'elves_woods': message,
                'elves_forest': message,
                'elves_mountains': message
            })
