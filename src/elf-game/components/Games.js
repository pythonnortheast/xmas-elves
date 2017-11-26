import React, { Component } from "react";
import PropTypes from "prop-types";

import "./Games.css";

import Game from "../containers/Game";

class GameTable extends Component {
  static propTypes = {
    games: PropTypes.arrayOf(PropTypes.string)
  };

  render() {
    return (
      <table className="Games">
        <thead>
          <tr>
            <th>Player Name</th>
            <th>Turns Played</th>
            <th>Elves Remaining</th>
            <th>Money Made</th>
          </tr>
        </thead>
        <tbody>
          {this.props.games.map(uuid => <Game key={uuid} uuid={uuid} />)}
        </tbody>
      </table>
    );
  }
}

export default GameTable;
