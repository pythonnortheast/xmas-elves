export function createWebsocketMiddleware(url) {
  const socket = new WebSocket(url);

  return store => next => action => {
    switch (action.type) {
      case "CONNECT_WEBSOCKET":
        socket.onmessage = event => {
          store.dispatch({ type: "UPDATE_GAME", game: JSON.parse(event.data) });
        };
        break;
      default:
        break;
    }
    return next(action);
  };
}
