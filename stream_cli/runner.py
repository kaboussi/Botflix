from stream_cli.stream import stream, get_magnet
from stream_cli.interface import print_table_of_movies
from helper.utils import CONFIG_PATH
from helper import utils

from scrapy.crawler import CrawlerProcess
from rich import print

from typing import Callable, Generator, List
from pathlib import Path
import requests


def start_scrawling(spider_class: Callable[[], Generator]) -> List[dict]:
    """takes a spider class as an argument ( TopMoviesSpider or SearchedMoviesSpider )
    return a list of movies inside a dictionnary
    """

    process = CrawlerProcess(
        settings={
            "LOG_LEVEL": "ERROR",
            "USER_AGENT": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        }
    )
    process.crawl(spider_class)
    process.start()

    # exit if result is null
    utils.clear_screen()
    if spider_class.output == []:
        response = requests.get("https://www.torrentgalaxy.to/").status_code
        if response != 200:
            print(
                "[bold red]Unable to connect to torrent provider. Please use vpn. Exiting[/bold red]"
            )
        else:
            print("[bold red]Movie Not Found Error[/bold red]")
        exit(1)

    return spider_class.output


def apprun(scraping_class, is_top_movies_choice: bool) -> None:
    movies = start_scrawling(scraping_class)

    utils.clear_screen()
    if is_top_movies_choice:
        print_table_of_movies(movies, is_top_movies_choice=True)
    else:
        print_table_of_movies(movies, is_top_movies_choice=False)
    magnets = [movie["link"] for movie in movies]
    magnet = get_magnet(magnets)

    player = Path(CONFIG_PATH).read_text()
    stream(magnet, default_player=player)