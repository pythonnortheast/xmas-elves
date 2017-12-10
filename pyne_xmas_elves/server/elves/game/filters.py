"""Filters for running games.
"""
from django.db.models import Count, functions as f
import django_filters as filters

from .models import Session


class SessionFilterSet(filters.FilterSet):
    """Filters for sessions.
    """

    ACTIVE_CHOICES = (
        ('only', 'Active'),
        ('complete', 'Complete'),
    )
    active = filters.ChoiceFilter(choices=ACTIVE_CHOICES,
                                  method='filter_active',
                                  name='day_count')

    class Meta:
        model = Session
        exclude = 'uuid', 'elves_start'

    def filter_active(self, queryset, name, value):
        """Filter the active/complete sessions.
        """
        queryset = queryset.annotate(**{name: Count('days')})

        if value == 'only':
            lookup = '__'.join([name, 'lt'])
        elif value == 'complete':
            lookup = '__'.join([name, 'gte'])

        # Ignore below from coverage reports django-filters will never execute
        # this method if value is not in CHOICES
        return queryset.filter(**{lookup: 10})  # pragma: no cover
