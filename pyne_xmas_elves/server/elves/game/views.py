"""Views for Managing a Session.
"""
from json import dumps

from django.http.request import HttpRequest
from channels import Group
from rest_framework import decorators, response, status, viewsets

from .filters import SessionFilterSet
from .models import Day, Session
from .serializers import DaySerializer, SessionSerializer


class SessionViewSet(viewsets.ModelViewSet):
    """Manage a Session and its Days.
    """

    filter_class = SessionFilterSet
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    @decorators.detail_route(methods=['get', 'post'], url_path='day',
                             serializer_class=DaySerializer)
    def day_list(self, request: HttpRequest, pk: int):
        """Dispatch the day_list handling.

        When we have a GET, return the list.
        When we have a POST, create a new day.
        """
        method = request.method.lower()
        return self._day_list() if method == 'get' else self._create_day()

    def perform_create(self, serializer: SessionSerializer):
        """Create the new session and send to the websocket.
        """
        instance = serializer.save()
        self._send_to_websocket(instance)

    def _day_list(self):
        """Return the day list.
        """
        serialized = self.get_serializer(
            self.get_object().days.all(), many=True)
        return response.Response(serialized.data)

    def _create_day(self):
        """Create a new day for a session.

        Sends the created day to the websocket.
        """
        serialized = DaySerializer(data=self.request.data,
                                   context={'session': self.get_object()})
        serialized.is_valid(raise_exception=True)
        instance = serialized.save()
        self._send_day_to_websocket(instance)
        return response.Response(serialized.data,
                                 status=status.HTTP_201_CREATED)

    def _send_day_to_websocket(self, instance: Day):
        """Send the passed-in day to the websocket.
        """
        self._send_to_websocket(instance.session)

    def _send_to_websocket(self, instance: Session):
        """Send the updated game session information.
        """
        serializer = SessionSerializer(instance)

        output = dumps(serializer.data)
        Group('session').send({
            'text': output
        })
