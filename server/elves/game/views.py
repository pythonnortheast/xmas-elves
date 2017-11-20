"""Views for Managing a Session.
"""
from rest_framework import decorators, response, status, viewsets

from .models import Day, Session
from .serializers import DaySerializer, SessionSerializer


class SessionViewSet(viewsets.ModelViewSet):
    """Manage a Session and its Days.
    """

    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    @decorators.detail_route(methods=['get', 'post'], url_path='day',
                             serializer_class=DaySerializer)
    def day_list(self, request, pk):
        """Dispatch the day_list handling.

        When we have a GET, return the list.
        When we have a POST, create a new day.
        """
        method = request.method.lower()
        return self._day_list() if method == 'get' else self._create_day()

    def _day_list(self):
        """Return the day list.
        """
        serialized = self.get_serializer(
            self.get_object().days.all(), many=True)
        return response.Response(serialized.data)

    def _create_day(self):
        """Create a new day for a session.
        """
        serialized = DaySerializer(data=self.request.data,
                                   context={'session': self.get_object()})
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return response.Response(serialized.data,
                                 status=status.HTTP_201_CREATED)
