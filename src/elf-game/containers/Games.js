import { connect } from "react-redux";

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
  return { games: state.games.uuids };
}

export default connect(mapGameListToProps)(Games);
