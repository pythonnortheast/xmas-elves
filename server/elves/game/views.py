"""Views for Managing a Session.
"""
from rest_framework import decorators, response, viewsets

from .models import Day, Session
from .serializers import DaySerializer, SessionSerializer


class SessionViewSet(viewsets.ModelViewSet):
    """Manage a Session and its Days.
    """

    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    @decorators.detail_route(methods=['get'], url_path='day')
    def day_list(self, request, pk):
        """Get the list of days for a given session.
        """
        serialized = DaySerializer(self.get_object().days.all(), many=True)
        return response.Response(serialized.data)

    # @decorators.detail_route(methods=['post'], url_path='day')
    # def create_day(self, request, pk):
    #     """Create a new day for a session.
    #     """
