"""The routing rules for the Elf Game.
"""
from rest_framework import routers

from .views import SessionViewSet


router = routers.SimpleRouter()

router.register(r'game', SessionViewSet)
urlpatterns = router.urls
