import React, { Component } from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";

import { mapGameToProps } from "../actions";

import "./Game.css";

class Game extends Component {
  static propTypes = {
    uuid: PropTypes.string,
    current_day: PropTypes.number,
    elves_remaining: PropTypes.number,
    money_made: PropTypes.string,
    player_name: PropTypes.string
  };

  render() {
    return (
      <tr className="Game-row">
        <td>{this.props.player_name}</td>
        <td className="number">{this.props.current_day}</td>
        <td className="number">{this.props.elves_remaining}</td>
        <td className="amount">£{this.props.money_made}</td>
      </tr>
    );
  }
}

export default connect(mapGameToProps)(Game);
