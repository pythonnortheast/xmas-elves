import { connect } from "react-redux";
import { sortBy } from "lodash";

import Games from "../components/Games";

/**
 * Map a list of games, sorted by money_made, into the props.
 * @param {Object} state The state object from redux.
 * @param {object} state.gameMap The mapping of Game UUID -> Game objects.
 * @param {string} state.gameMap.money_made The value of money made.
 * @param {string[]} state.uuids The uuids of objects in the list.
 * @return {Object[]} The sorted list of games.
 */
function mapGameListToProps(state) {
  const uuids = sortBy(state.games.uuids, uuid => {
    const game = state.games.gameMap[uuid];
    return parseFloat(game.money_made) * -1;
  });
  return { games: uuids };
}

export default connect(mapGameListToProps)(Games);
