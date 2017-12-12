import React, { Component } from "react";
import "./App.css";

import Games from "./elf-game/containers/Games";

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Welcome to the Great Elf Game!</h1>
        </header>
        <div class="App-overlay">
          <p className="App-intro">
            For rules, see the
            <a href="https://github.com/pythonnortheast/xmas-elves.git">
              online documentation.
            </a>
          </p>

          <div className="App-content">
            <Games />
          </div>
        </div>
      </div>
    );
  }
}

export default App;
