import json
import os
import time
from datetime import datetime
from random import randint
from typing import Optional

from scholarly import scholarly
import pandas as pd

from src.logger import Logger

SEARCH_TERMS = [
    ('"locomotor rehabilitation"', '"non-ambulant"'),
    ('"locomotor rehabilitation"', 'non-ambulant')
]
MAX_LIMIT_PER_SEARCH_TERM =  150

class ScholarScraper:
    def __init__(self):
        self._df: Optional[pd.DataFrame] = None
        self._logger = Logger()

    def get_articles(self):
        for search_term in SEARCH_TERMS:
            final_search_term = f'{search_term[0]} {search_term[1]}'
            self._logger.info(f"searching for: {final_search_term}")
            data = self._search_for_title(final_search_term)
            self._logger.info(f"got data of length: {(len(data))}")
            self._add_to_df(data, final_search_term)
            # save to file
            self._logger.info(f"saving to csv...")
            self._save_to_csv(final_search_term)
            self._logger.info(f"saving to csv completed")
            time.sleep(randint(1, 5))

    def _save_to_csv(self, final_search_term):
        now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        os.mkdir(f"./outputs/{now}")
        name = f"scraped_{final_search_term}_{now}".replace(" ", "_")
        self._df.to_csv(f"../outputs/{name}.csv")

    def _add_to_df(self, data: json, search_term: str) -> None:
        self._df = pd.json_normalize(data)
        self._df["search_term"] = search_term
        self._logger.info(f"created new df")


    def _search_for_title(self, search_term):
        search_query = scholarly.search_pubs(search_term)
        # data = []
        # i = 0
        # while i < MAX_LIMIT_PER_SEARCH_TERM:
        #     time.sleep(1)
        #     try:
        #         out = next(search_query)
        #     except StopIteration:
        #         break
        #     data.append(out)
        #     i += 1

        try:
            out = list(search_query)
        except Exception:
            self._logger.error("failed to get article")
        return out