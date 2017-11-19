"""Views for Managing a Session.
"""
from rest_framework import viewsets

from .models import Day, Session
from .serializers import SessionSerializer


class SessionViewSet(viewsets.ModelViewSet):
    """Manage a Session and its Days.
    """

    queryset = Session.objects.all()
    serializer_class = SessionSerializer
