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

const local = window.location.host.startsWith("localhost");

const host = local ? "localhost:8000" : "elves.pythonnortheast.com";
const secure = local ? "" : "s";

const store = createStore(
  elfGame,
  { games: { gameMap: {}, uuids: [] } },
  applyMiddleware(
    thunkMiddleware,
    createWebsocketMiddleware(`ws${secure}://${host}/session/`)
  )
);
store.dispatch(fetchGames(`http${secure}://${host}/game/`));
store.dispatch({ type: "CONNECT_WEBSOCKET" });

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("root")
);
registerServiceWorker();
