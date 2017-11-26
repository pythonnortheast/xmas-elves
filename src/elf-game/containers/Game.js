import { connect } from "react-redux";
import Game from "../components/Game";

/**
 * Extract the game from the state object and inject it into props.
 * @param {Object} state The state object from redux.
 * @param {Object} state.gameMap The mapping of Game UUID -> Game objects.
 * @param {Object} props The props injected onto the component.
 * @param {string} props.uuid The uuid that will be looked up in the gameMap.
 * @return {Object} The props for the component.
 */
function mapGameToProps(state, props) {
  const game = state.games.gameMap[props.uuid];
  game.key = game.uuid;
  return game;
}
export default connect(mapGameToProps)(Game);
