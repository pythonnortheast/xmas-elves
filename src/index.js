import React from "react";
import ReactDOM from "react-dom";

import { createStore } from "redux";
import { Provider } from "react-redux";
import thunkMiddleware from "redux-thunk";

import "./index.css";
import App from "./App";
import registerServiceWorker from "./registerServiceWorker";

import elfGame from "./elf-game/reducers";
import { applyMiddleware } from "redux";
import { fetchGames } from "./elf-game/actions";
import { createWebsocketMiddleware } from "./elf-game/middleware";

const store = createStore(
  elfGame,
  { games: { gameMap: {}, uuids: [] } },
  applyMiddleware(
    thunkMiddleware,
    createWebsocketMiddleware("ws://localhost:8000/session/")
  )
);
store.dispatch(fetchGames("http://localhost:8000/game/"));
store.dispatch({ type: "CONNECT_WEBSOCKET" });

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("root")
);
registerServiceWorker();
