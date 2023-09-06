# Simple Chat

Simple Chat is a basic client-server chat application built in Python. It allows one client to connect to a server for real-time, text-based communication.

## Features

- Text-based chat functionality between one client and one server.
- Chat participants can play games of rock-paper-scissors.
- Simple and straightforward communication between the client and server using socket library

## Requirements
* Python 3
* socket library

## Getting Started
SimpleChat uses a client-server model. You must have one instance of the server running first, then start a client to connect to that server.  
You will need to configure the HOSTNAME and PORT on both server and client to the same hostname:port so they can connect via socket.  

You can run the server with...
```bash
python server.py
```

And the client with...
```bash
python client.py
```

## Usage

1. Start the server first.
2. Start the client (server must be up and running before client can connect).
3. Each participant can now take turns entering chat messages. Special commands can be used to enter/exit both game mode and chat.
4. To play rock-paper-scissors, type "rock," "paper," or "scissors" when prompted during a chat session.

## Special Commands
These commands must be entered alone in a message
### Basic Commands (in normal chat)
* /q.....(q)uit Chat
* /p.....(p)lay 'Rock, Paper, Scissors' with chat partner

### Game Commands (in game mode)
* /e.....(e)exit the game and return to regular chat
* /q.....(q)uit the game and exit chat as well
* Game will prompt players to play (r)ock, (p)aper, or (s)cissors

## License
[MIT License](LICENSE)
