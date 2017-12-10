"""Websocket consumers.
"""
from channels import Group


def ws_connect(message):
    # Add to reader group
    Group("session").add(message.reply_channel)
    # Accept the connection request
    message.reply_channel.send({"accept": True})


def ws_disconnect(message):
    # Remove from reader group on clean disconnect
    Group("session").discard(message.reply_channel)
