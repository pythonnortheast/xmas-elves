import React, { Component } from "react";
import PropTypes from "prop-types";

import "./Games.css";

import Game from "./Game";

class Table extends Component {
  static propTypes = {
    games: PropTypes.arrayOf(PropTypes.objectOf(PropTypes.any))
  };

  render() {
    const games = this.props.games.map(game => (
      <Game
        current_day={game.current_day}
        player_name={game.player_name}
        elves_remaining={game.elves_remaining}
        money_made={game.money_made}
      />
    ));
    return (
      <table class="Games">
        <thead>
          <tr>
            <th>Player Name</th>
            <th>Turns Played</th>
            <th>Elves Remaining</th>
            <th>Money Made</th>
          </tr>
        </thead>
        <tbody>{games}</tbody>
      </table>
    );
  }
}

export default Table;
