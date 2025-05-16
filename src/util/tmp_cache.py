import json
import os
from datetime import datetime, timedelta


class TmpCache:
    __cache_items: dict[str, dict]

    def __init__(self, file_path: str = "tmp_cache.json", default_expiration_time: int = 24) -> None:
        self.set_file_path(file_path)
        self.set_default_expiration_time(default_expiration_time)
        self.__cache_items = {}

    def load(self) -> None:
        """Load products data from cache file if it exists."""
        if os.path.exists(self.__file_path):
            try:
                with open(self.__file_path, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                    keep_cache_info = {}
                    now = datetime.now()

                    # Iterate through items in cache
                    for key, information in cache_data.items():
                        timestamp = datetime.fromisoformat(information['timestamp'])
                        if now - timestamp > timedelta(hours=information['expiration_time']):
                            continue
                        keep_cache_info[key] = information

                    self.__cache_items = keep_cache_info

            except (json.JSONDecodeError, KeyError):
                self.__cache_items = {}

    def flush(self) -> None:
        """Save products data to cache file with timestamp."""
        # update items at cache_info
        actual_timestamp = datetime.now().isoformat()
        for key, information in self.__cache_items.items():
            if information['timestamp'] == None:
                self.__cache_items[key]['timestamp'] = actual_timestamp

        with open(self.__file_path, 'w', encoding='utf-8') as f:
            json.dump(self.__cache_items, f, ensure_ascii=False, indent=2)

    def add_item(self, key: str, data, expiration_time: int = None) -> None:
        if key in self.__cache_items:
            self.upd_item(key, data, expiration_time)
            return

        if expiration_time == None:
            expiration_time = self.__default_expiration_time

        cache_item = {'data' : data, 'expiration_time' : expiration_time, 'timestamp' : None}
        self.__cache_items[key] = cache_item

    def upd_item(self, key: str, data, expiration_time: int = None) -> None:
        if key not in self.__cache_items:
            self.add_item(key, data, expiration_time)
            return

        if expiration_time == None:
            expiration_time = self.__default_expiration_time

        self.__cache_items[key]['data'] = data
        self.__cache_items[key]['expiration_time'] = expiration_time
        self.__cache_items[key]['timestamp'] = None

    def get_item(self, key: str):
        return self.__cache_items[key]['data']

    def get_all_items(self):
        return {key: item['data'] for key, item in self.__cache_items.items()}

    def set_default_expiration_time(self, default_expiration_time: int = 24) -> None:
        self.__default_expiration_time = default_expiration_time

    def set_file_path(self, file_path: str) -> None:
        self.__file_path = file_path