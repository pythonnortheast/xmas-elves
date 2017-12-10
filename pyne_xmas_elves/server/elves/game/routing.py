from channels.routing import route
from .consumers import ws_connect, ws_disconnect


CHANNEL_ROUTING = [
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect)
]
