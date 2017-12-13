from rest_framework import serializers


def positive_number(value):
    """Validate the given number is positive.
    """
    if value < 0:
        raise serializers.ValidationError('This field must be >= 0')
