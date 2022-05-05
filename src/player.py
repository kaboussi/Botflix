import contextlib
from typing import Callable
from pathlib import Path
import os

from rich.console import Console
console = Console()

# supported video player
PLAYERS_LIST = ["mpv", "vlc", "mplayer"]
THE_PATH = "config/player.txt"


def is_valid(player_name: str) -> bool:
    '''return True if player exist otherwise False'''

    # the second argument is to check if the file is empty
    return player_name in PLAYERS_LIST and os.stat(THE_PATH).st_size != 0


def keep_asking(player: str) -> str:
    '''Keep asking for the right answer'''
    
    player_is_valid = True
    while player_is_valid:
        if is_valid(player) is False:
            player = console.input(
                "What is your default media player? [bold yellow](mpv, vlc, mplayer)[/ bold yellow] :").lower()
            with open(THE_PATH, mode="w", encoding='utf-8') as file:
                file.write(player)
        else:
            player_is_valid = False
    return player


def check_player() -> Callable[[str], str]:
    """return name of the player in config/player.txt"""
    
    
    path = Path(THE_PATH)
    if path.exists():
        player = path.read_text(encoding='utf-8').lower()
    else:
        player = console.input(
            "What is your default media player? [bold yellow](mpv, vlc, mplayer)[/ bold yellow] :").lower()

        # create a folder then create the player.txt to write in it
        with contextlib.suppress(FileExistsError):
            os.mkdir(path='config')
        with open("config/player.txt", 'w', encoding='utf-8') as file:
            file.write(player)


    return keep_asking(player)

