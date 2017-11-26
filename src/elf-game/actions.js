/**
 * Extract the game from the state object and inject it into props.
 * @param {Object} state The state object from redux.
 * @param {Object} state.gameMap The mapping of Game UUID -> Game objects.
 * @param {Object} props The props injected onto the component.
 * @param {string} props.uuid The uuid that will be looked up in the gameMap.
 * @return {Object} The props for the component.
 */
export function mapGameToProps(state, props) {
  return state.gameMap[props.uuid];
}

/**
 * Map a list of games, sorted by money_made, into the props.
 * @param {Object} state The state object from redux.
 * @param {object} state.gameMap The mapping of Game UUID -> Game objects.
 * @param {string} state.gameMap.money_made The value of money made.
 * @param {string[]} state.uuids The uuids of objects in the list.
 * @return {Object[]} The sorted list of games.
 */
export function mapGameListToProps(state) {
  return { games: state.games.uuids };
}
