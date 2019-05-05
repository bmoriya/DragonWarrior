#!/usr/bin/env python
from game import Game

def main():
    window_w = 256
    window_h = 240
    multiplier = 3

    fps = 60
    title = "RPG Tutorial"
    
    game = Game(window_w, window_h, fps, title, multiplier)
    game.run()

if __name__ == "__main__":
    main()
