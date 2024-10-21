# Impact Isolation - Zenith Coding

Hello! A couple of years ago, I took an Intro to AI course ([CS 3600](https://gt-student-wiki.org/mediawiki/index.php/CS_3600)) at Georgia Tech. I thought one of the problems we did for homework was super fascinating: a game called "Impact Isolation". This repository is my attempt to push the problem as far as I can take it myself, because I feel like I did not challenge myself hard enough back when this was a course assignment.

# Overview

To talk about Impact Isolation, let's first talk about what the base game of Isolation is. It is actually very simple! The board is a grid of empty cells, and there are two agents (players) who follow these rules:

1. You move to any empty cell by a [Queen's move](https://en.wikipedia.org/wiki/Queen_(chess)) that is not blocked by a filled cell (any amount horizontally, vertically, or diagonally).
2. Every cell that has been/is currently occupied by an agent is filled cell, and it cannot be traversed to or past.
3. You must be the last person to be able to move in order to win the game.

Now, to turn this into *Impact* Isolation, you just have to add one more rule.

4. If you move more than 1 cell, then a 1 cell "crater" forms around you, blocking you in the horizontal/vertical directions.

The rules are very similar to the [Angel Problem](https://en.wikipedia.org/wiki/Angel_problem), except the two agents are pitted against another in containing the opponent. At a very high level, the strategy is to block your opponent into a smaller area than yourself so that you have the most available moves left yourself. But to be honest, I am writing this introduction before I have even written my first bot, so I don't know the depth (pun intended) of how far this idea goes!

# Installation

TODO: write this :)