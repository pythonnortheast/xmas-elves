import React, { Component } from "react";
import logo from "./logo.svg";
import "./App.css";

import Games from "./elf-game/components/Games";

class App extends Component {
  render() {
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

        <Games />
      </div>
    );
  }
}

export default App;
