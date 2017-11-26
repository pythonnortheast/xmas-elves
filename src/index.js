import React from "react";
import ReactDOM from "react-dom";
import thunkMiddleware from "redux-thunk";
import { createStore } from "redux";
import { Provider } from "react-redux";
import "./index.css";
import App from "./App";
import registerServiceWorker from "./registerServiceWorker";

import elfGame from "./elf-game/reducers";
import { applyMiddleware } from "redux";
import { fetchGames } from "./elf-game/actions";

const store = createStore(
  elfGame,
  { games: { gameMap: {}, uuids: [] } },
  applyMiddleware(thunkMiddleware)
);
store.dispatch(fetchGames("http://localhost:8000/game/"));

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("root")
);
registerServiceWorker();
