"""
Функции для создания словарей с именами файлов и их хеш-суммы для локальной и удаленной директорией.

"""

import hashlib
import os
from typing import Dict, Any, Union

from loguru import logger


def get_files_local_dir(dir_path: str) -> Dict[str, str]:
    """
    Получает хэш-суммы файлов в указанной локальной директории.

    Args:
        dir_path (str): Путь к локальной директории.

    Returns:
        Dict[str, str]: Словарь, в котором ключи - имена файлов, а значения - их хэш-суммы.
    """
    exists_files: Dict[str, str] = {}

    for file_name in os.listdir(dir_path):
        path_file: str = os.path.join(dir_path, file_name)

        if os.path.isfile(path_file):
            try:
                with open(path_file, 'rb') as file:
                    file_hash = hashlib.sha256()
                    for chunk in iter(lambda: file.read(4096), b''):
                        file_hash.update(chunk)
                exists_files[file_name] = file_hash.hexdigest()
            except PermissionError:
                logger.error(f"Нет доступа к файлу {file_name}.")

    return exists_files


def create_cloud_files(cloud_folder: Union[Dict[str, Any], None]) -> Dict[str, str]:
    """
    Создает словарь с именами файлов и их хэш-суммами из удаленной папки.

    Args:
        cloud_folder (Union[Dict[str, Any], None]): Информация о содержимом удаленной папки.

    Returns:
        Dict[str, str]: Словарь, в котором ключи - имена файлов, а значения - их хэш-суммы.
    """
    if cloud_folder:
        cloud_files: Dict[str, str] = {item["name"]: item["sha256"] for item in cloud_folder["_embedded"]["items"]}
    else:
        cloud_files: Dict[str, str] = {}

    return cloud_files
