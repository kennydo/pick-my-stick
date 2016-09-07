import os
import os.path
from typing import Iterator


class StickerStore:
    "Stores stickers and sticker packs"

    def __init__(self, storage_path: str) -> None:
        # Validate that the storage path is usable
        if not os.path.isdir(storage_path):
            raise ValueError("Storage path '{0}' is not a valid storage direcotory".format(storage_path))

        self.storage_path = storage_path

    def list_pack_ids(self) -> Iterator[str]:
        for entry in os.scandir(self.storage_path):
            if not entry.is_dir():
                continue

            yield entry.name

    def list_sticker_ids(self, pack_id: str) -> Iterator[str]:
        pack_path = os.path.join(self.storage_path, pack_id)

        if not os.path.isdir(pack_path):
            raise ValueError("Pack {0} is not a valid pack".format(pack_id))

        for entry in os.scandir(pack_path):
            if not entry.is_file():
                continue

            yield entry.name

    def get_sticker_path_by_id(self, pack_id: str, sticker_id: str) -> str:
        sticker_path = os.path.join(self.storage_path, pack_id, sticker_id)

        if not os.path.isfile(sticker_path):
            raise ValueError("Sticker {0} for pack {1} is not a valid sticker".format(sticker_id, pack_id))

        return sticker_path
