from concurrent.futures import ThreadPoolExecutor
import requests


class HackerNewsClient:
    __base_url = "https://hacker-news.firebaseio.com/v0/"

    def __init__(self, endpoint) -> None:
        self.endpoint = endpoint
        self.__previous_items = set()

    def __fetch_item_ids(self, count: int|None)-> list[int]:
        url = self.__base_url + self.endpoint
        response = requests.get(url)
        item_ids = response.json()

        # Optional limit on the number of returned items
        if count is not None:
            item_ids = item_ids[:count]

        return item_ids

    def __fetch_item_by_id(self, item_id: int)-> dict:
        url = self.__base_url + f"item/{item_id}.json"
        item_data = requests.get(url)
        return item_data.json()
    
    def fetch_items(self, count: int|None)-> list[dict]:
        item_ids = self.__fetch_item_ids(count)

        # Prevent fetching the same items twice in a row
        new_item_ids = list(set(item_ids) - self.__previous_items)
        self.__previous_items.update(new_item_ids)

        # Use threadpool to fetch items concurrently
        with ThreadPoolExecutor() as executor:
            item_iterator = executor.map(self.__fetch_item_by_id, new_item_ids)
            new_items = list(item_iterator)

        return new_items
