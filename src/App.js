import React, { Component } from "react";
import logo from "./logo.svg";
import "./App.css";

import Games from "./elf-game/components/Games";

class App extends Component {
  render() {
    const games = [
      {
        player_name: "Steve",
        current_day: 5,
        elves_remaining: 4,
        money_made: "150.00"
      }
    ];
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to the Great Elf Game!</h1>
        </header>
        <p className="App-intro">
          For rules, see the
          <a href="https://github.com/pythonnortheast/xmas-elves.git">
            online documentation.
          </a>
        </p>

        <Games games={games} />
      </div>
    );
  }
}

export default App;
