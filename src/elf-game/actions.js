import fetch from "cross-fetch";

export function requestGames() {
  return {
    type: "REQUEST_GAMES"
  };
}

export function resetGameList(json) {
  return {
    type: "RESET_GAME_LIST",
    games: json,
    receivedAt: Date.now()
  };
}

export function fetchGames(url) {
  return function(dispatch) {
    dispatch(requestGames(url));

    return fetch(url)
      .then(
        response => response.json(),
        error => console.error("Error occurred", error)
      )
      .then(json => dispatch(resetGameList(json)));
  };
}
