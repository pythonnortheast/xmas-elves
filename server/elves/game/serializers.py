"""Serializers for Sessions and Days.
"""
from rest_framework import serializers

from .models import Day, Session


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
            'weather': {
                'read_only': True,
            }
        }
        model = Day
