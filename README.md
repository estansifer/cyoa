# Choose Your Own Adventure Engine

This is a simple engine for playing a choose-your-own-adventure game. The
games, of which I have written only one, are in the `games` subdirectory.
Type

    python cyoa.py

to play. Type `h` for help, `q` to quit, and `b` to go back.

The provided logic cyoa game has a "win" state that is difficult to reach.
If you play through the game in the direct way you should gather sufficient
information to find the "win" state but backtracking or a second play-through
is required. (I mention this here as some people find that unfair.)

The program `chocolate.py` plays a game, and `reflow.py` reflows text to
fit it within a width (both of which I used to write the logic cyoa game).

Tested in python 3.5.1.
