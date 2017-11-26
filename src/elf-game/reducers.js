import { combineReducers } from "redux";

/**
 * Reduce the state and action based on retrieving games from the server.
 * @param {Object} state The existing state object.
 * @param {Object} action The action to perform.
 * @param {string} action.type The action to perform.
 * @param {string} action.status Either 'success' or 'error'.
 * @param {Object[]} [action.games] The list of games.
 * @return {Object} The new state object.
 */
function games(state = {}, action) {
  switch (action.type) {
    case "RESET_GAME_LIST":
      return getGameList(action.games);
    default:
      return state;
  }
}

/**
 *
 * @param {Object[]} [games] The array of games from the server.
 * @param {string} games.uuid The UUID for each game.
 */
function getGameList(games = []) {
  const gameMap = {};
  games.forEach(game => (gameMap[game.uuid] = game));
  const uuids = games.map(game => game.uuid);
  return { gameMap, uuids };
}

export default combineReducers({ games });
