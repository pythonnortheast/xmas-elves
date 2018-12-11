# Christmas Elves

The annual Christmas Elves game server and client

Python North East December brings you the Christmas Elf Challenge. Your task,
should you choose to accept it, is to manage the Christmas Tree selling
business.

## Running your Game

This part of the guide will give you the instructions to set up the game so you
can start trying to set a high score!

### Installation

Make sure you have Python installed - if you have Windows, check out the
[Beginner's Guide of the Xmas Elves document][xmas-elves-doc].

Once you're ready, you can get the client code running:

```bash
pyvenv venv
. venv/bin/activate
pip install pyne-xmas-elves
```

### Building your Bot

Create your game file, called `game.py`:

```python
from pyne_xmas_elves.client import BaseGame


class Game(BaseGame):
    PLAYER_NAME = 'Father Christmas'

    def turn(self, elves):
        woods = elves // 2
        forest = (elves - woods) // 2
        mountain = elves - woods - forest
        return woods, forest, mountains

```

#### Helper Attributes

While taking a turn, you can access the following attributes on `self`:

* `amount_raised` - total money raised
* `current_turn` - the current turn number
* `last_turn` - the last turn number
* `previous_weather` - the weather on the previous day

### Run the game

After creating your bot, you can run the game:

```bash
elves game
```

## Running the Server (optional)

### Installing Dependencies

The server is self-contained with an SQLite database, so just install the
requirements:

```bash
pip install -r requirements.txt
```

### Running

We're using Django Channels, so running the server is as easy as:

```bash
python server/manage.py runserver
```

## The API

To interact with the server session, we use a simple REST API to send new data
into the server. The full API docs can be found by running a server and
navigating to `/docs/`.

### Starting a New Session

To start a new session, send a `POST` request with a `name` variable
form-encoded to `https://<host>/sessions/`:

```bash
curl https://example.com/sessions/ -X POST -d player_name="Scott"
```

and you'll get a simple JSON object back with a `session` URL that you post your
turns against.

### Taking a Turn

To take a turn, make a `POST` request against the `day` endpoint of a session.

## Instructions and Rules

See the [attached Google Doc][xmas-elves-doc] for the rules and any of the
latest tips and tricks.

[xmas-elves-doc]: https://docs.google.com/document/d/1p3upVEv7zDcT_0ZQKbJqo_nudHUwIoLAo1TkxzBb7ZA/edit?usp=sharing
