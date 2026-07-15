from enum import Enum

from yt_dlp.utils.networking import normalize_url

from src.database.bootstrap import get_database
from src.database.entities.record import Record


class FileType(Enum):
    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"


class DownloadsRepository:
    def __init__(self):
        self._collection = get_database().downloads

    @classmethod
    def create_record(
        cls, file_ids: list[str], user_id: str, url: str, file_type: FileType
    ):
        normalized_url = normalize_url(url)
        return Record(
            file_ids=file_ids, user_id=user_id, url=normalized_url, file_type=file_type
        )

    def get(self, url: str) -> Record | None:
        normalized_url = normalize_url(url)
        if db_record := self._collection.find_one({"url": normalized_url}):
            return Record(**db_record)
        return None

    def delete(self, url: str) -> None:
        normalized_url = normalize_url(url)
        self._collection.delete_one({"url": normalized_url})

    def add(
        self, file_ids: list[str], user_id: str, url: str, file_type: FileType
    ) -> str:
        if record := self.get(url):
            self.delete(record.url)

        record = Record(
            user_id=user_id, file_ids=file_ids, url=url, file_type=file_type
        )

        print(record)

        result = self._collection.insert_one(
            record.model_dump(by_alias=True, mode="json")
        )
        print(result, record)
        return str(result.inserted_id)
