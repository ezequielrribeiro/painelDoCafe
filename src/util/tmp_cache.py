class TmpCache:
    __cache_items: dict[str, dict]

    def __init__(self, file_path: str = "tmp_cache.json", default_expiration_time: int = 24) -> None:
        self.set_file_path(file_path)
        self.set_default_expiration_time(default_expiration_time)
        self.__cache_items = {}

    def load(self) -> None:
        pass

    def flush(self) -> None:
        pass

    def add_item(self, item, key: str, expiration_time: int = None) -> None:
        if expiration_time == None:
            expiration_time = self.__default_expiration_time

        cache_item = {'data' : item, 'expiration_time' : expiration_time}
        self.__cache_items[key] = cache_item

    def get_item(self, key: str):
        return self.__cache_items[key]['data']

    def get_all_items(self):
        return {key: item['data'] for key, item in self.__cache_items.items()}

    def set_default_expiration_time(self, default_expiration_time: int = 24) -> None:
        self.__default_expiration_time = default_expiration_time

    def set_file_path(self, file_path: str) -> None:
        self.__file_path = file_path