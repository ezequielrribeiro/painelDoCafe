
class TmpCache:

    def __init__(self, file_path: str = "tmp_cache.json", default_expiration_time: int = 24) -> None:
        self.set_file_path(file_path)
        self.set_default_expiration_time(default_expiration_time)

    def load(self) -> None:
        pass

    def flush(self) -> None:
        pass

    def add_item(self, item, key: str) -> None:
        pass

    def get_item(self, key: str):
        pass

    def get_all_items(self):
        pass

    def set_default_expiration_time(self, default_expiration_time: int = 24) -> None:
        self.__default_expiration_time = default_expiration_time

    def set_file_path(self, file_path: str) -> None:
        self.__file_path = file_path