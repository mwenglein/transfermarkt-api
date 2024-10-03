from dataclasses import dataclass
from datetime import datetime

from app.services.base import TransfermarktBase
from app.utils.utils import extract_from_url
from app.utils.xpath import Competitions

@dataclass
class TransfermarktCompetitionSearch(TransfermarktBase):
    """
    A class for searching football competitions on Transfermarkt and retrieving search results.

    Args:
        query (str): The search query for finding football clubs.
        URL (str): The URL template for the search query.
        page_number (int): The page number of search results (default is 1).
    """

    query: str = None
    URL: str = (
        "https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={query}&Wettbewerb_page={page_number}"
    )
    page_number: int = 1

    def __post_init__(self) -> None:
        """Initialize the TransfermarktCompetitionSearch class."""
        self.URL = self.URL.format(query=self.query, page_number=self.page_number)
        self.page = self.request_url_page()

    def __parse_search_results(self) -> list:
        """
        Parse and retrieve the search results for football competitions from Transfermarkt.

        Returns:
            list: A list of dictionaries, each containing details of a football competition,
                including its unique identifier, name, country, associated clubs, number of players,
                total market value, mean market value, and continent.
        """
        idx = [extract_from_url(url) for url in self.get_list_by_xpath(Competitions.Search.URLS)]
        name = self.get_list_by_xpath(Competitions.Search.NAMES)
        country = self.get_list_by_xpath(Competitions.Search.COUNTRIES)
        clubs = self.get_list_by_xpath(Competitions.Search.CLUBS)
        players = self.get_list_by_xpath(Competitions.Search.PLAYERS)
        total_market_value = self.get_list_by_xpath(Competitions.Search.TOTAL_MARKET_VALUES)
        mean_market_value = self.get_list_by_xpath(Competitions.Search.MEAN_MARKET_VALUES)
        continent = self.get_list_by_xpath(Competitions.Search.CONTINENTS)

        return [
            {
                "id": idx,
                "name": name,
                "country": country,
                "clubs": clubs,
                "players": players,
                "totalMarketValue": total_market_value,
                "meanMarketValue": mean_market_value,
                "continent": continent,
            }
            for idx, name, country, clubs, players, total_market_value, mean_market_value, continent in zip(
                idx,
                name,
                country,
                clubs,
                players,
                total_market_value,
                mean_market_value,
                continent,
            )
        ]

    def search_competitions(self) -> dict:
        """
        Perform a search for football competitions and retrieve the search results.

        Returns:
            dict: A dictionary containing search results, including competition details.
        """
        self.response["query"] = self.query
        self.response["pageNumber"] = self.page_number
        self.response["lastPageNumber"] = self.get_last_page_number(Competitions.Search.BASE)
        self.response["results"] = self.__parse_search_results()
        self.response["updatedAt"] = datetime.now()

        return self.response


    def __parse_all_competitions_results(self, page) -> dict:
        """
        Returns a dictionary of competitions.
        """
        competitions_dict = {}

        tables = page.find_all("table", {"class": "items"})
        items_table = tables[0]
        content = items_table.select("tbody > tr")[1:]

        tier = "First Tier"
        for row in content:
            columns = row.select("td")

            if len(columns) == 1:
                tier = columns[0].text.strip()
            else:
                id = columns[0].select("a")[1]["href"].split("/")[-1]
                name = columns[0].text.strip()
                country = columns[3].select("img")[0]["title"]
                total_clubs = int(columns[4].text.strip())
                total_players = int(columns[5].text.strip())
                avg_age = float(columns[6].text.strip())
                foreigners_percent = float(columns[7].text.strip().replace("%", ""))
                total_value = columns[9].text.strip()
                tier = tier
                competition = {
                    "id": id,
                    "name": name,
                    "country": country,
                    "total_clubs": total_clubs,
                    "total_players": total_players,
                    "avg_age": avg_age,
                    "foreigners_percent": foreigners_percent,
                    "total_value": total_value,
                    "tier": tier
                }
                competitions_dict[id] = competition

        print("\n\n************************************************************\n\n")
        print(competitions_dict)
        return competitions_dict

    def get_all_competitions(self) -> dict:
        """
        Returns all competitions.
        """
        self.URL = "https://www.transfermarkt.com/wettbewerbe/europa/wettbewerbe"
        self.page = self.request_url_bsoup()
        self.response = self.__parse_all_competitions_results(self.page)

        return self.response