import hashlib
import os

from typing import Dict, Any, Union

from loguru import logger


def get_files_local_dir(dir_path: str) -> Dict[str, str]:
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
    if cloud_folder:
        cloud_files: Dict[str, str] = {item["name"]: item["sha256"] for item in cloud_folder["_embedded"]["items"]}
    else:
        cloud_files: Dict[str, str] = {}

    return cloud_files
