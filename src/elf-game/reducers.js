import { uniq } from "lodash";
import { combineReducers } from "redux";

/**
 * Reduce the state and action based on retrieving games from the server.
 * @param {Object} state The existing state object.
 * @param {Object} action The action to perform.
 * @param {string} action.type The action to perform.
 * @param {string} action.status Either 'success' or 'error'.
 * @param {Object[]} [action.games] The list of games.
 * @param {Object} [action.game] The game to update.
 * @return {Object} The new state object.
 */
function games(state = {}, action) {
  switch (action.type) {
    case "RESET_GAME_LIST":
      return getGameList(action.games);
    case "UPDATE_GAME":
      console.log(action);
      return updateGameList(state, action.game);
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

/**
 * Insert or update the given game list into the state.
 * @param {Object} state The state object
 * @param {string[]} state.uuids The list of uuids
 * @param {Object[]} state.gameMap The map of UUID -> games
 * @param {Object} game The updated game object
 * @return {Object} The gameMap and uuids
 */
function updateGameList(state, game) {
  const gameByUuid = {};
  gameByUuid[game.uuid] = game;
  return {
    gameMap: Object.assign({}, state.gameMap, gameByUuid),
    uuids: uniq([...state.uuids, game.uuid])
  };
}

export default combineReducers({ games });
