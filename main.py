"""
Скрипт для синхронизации файлов между локальной директорией и удаленным хранилищем на Яндекс.Диске.
Файл содержит основную логику программы синхронизации.

"""

import time

from loguru import logger
from typing import Dict, Tuple

from check_env import check_env
from file_utils import create_cloud_files, get_files_local_dir
from yandex_disk_handler import YandexDisk

local_paths: Tuple[str, str, int]
yandex_disk: YandexDisk
sync_time: int

local_paths, yandex_disk, sync_time = check_env()

logger.add(
    f"{local_paths[1]}logfile.log",
    format="synchronizer {time:YYYY-MM-DD HH:mm:ss.SSS} {level} {message}",
    level="INFO"
)
logger.info(f"Программа синхронизации файлов начинает работу с директорией\n{local_paths[0]}")


def start_sync() -> None:
    """
        Функция для запуска синхронизации файлов между локальной директорией и удаленным хранилищем.

        Returns:
            None
    """
    first_sync: bool = False

    while True:
        local_folder: Dict[str, str] = get_files_local_dir(local_paths[0])
        cloud_files: Dict[str, str] = create_cloud_files(yandex_disk.get_info())

        if not first_sync:
            for item_name in local_folder:
                if item_name not in cloud_files:
                    yandex_disk.load(local_paths[0], item_name)
            first_sync = True
            continue

        for item_name in local_folder.keys() - cloud_files.keys():
            yandex_disk.load(local_paths[0], item_name)

        for item_name, item_sha256 in cloud_files.items():
            if item_name in local_folder and local_folder[item_name] != item_sha256:
                yandex_disk.reload(local_paths[0], item_name)

        for item_name in cloud_files.keys() - local_folder.keys():
            yandex_disk.delete(item_name)

        time.sleep(int(sync_time))


if __name__ == "__main__":
    start_sync()
