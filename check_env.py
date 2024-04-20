import os
from typing import Tuple
from dotenv import load_dotenv
from yandex_disk_handler import YandexDisk


def check_local_path(key: str) -> str:
    value: str = os.environ.get(key)

    if value is None:
        raise FileNotFoundError(f"Отсутствует переменная {key} в файле '.env'")
    elif not os.path.exists(value):
        raise FileNotFoundError(
            f"Искомой папки {value}, указанной в переменной {key} не существует."
            f"Проверьте правильность указываемого пути."
        )
    return value


def check_local_paths() -> Tuple[str, str]:
    path_sync_dir: str = check_local_path("path_sync_dir")
    log_path: str = check_local_path("log_path")
    return path_sync_dir, log_path


def check_sync_time() -> str:
    sync_time: str = os.getenv("sync_time")

    if sync_time is None:
        raise FileNotFoundError("Отсутствует переменная 'sync_time' в файле '.env'")
    elif not sync_time.isdigit():
        raise TypeError("Переменная 'sync_time' должна содержать только цифры")

    return sync_time


def check_remote_data() -> YandexDisk:
    cloud_dir: str = os.getenv("cloud_dir")
    cloud_token: str = os.getenv("cloud_token")

    if cloud_dir is None:
        raise FileNotFoundError("Отсутствует переменная 'cloud_dir' в файле '.env'")
    if cloud_token is None:
        raise FileNotFoundError("Отсутствует переменная 'cloud_token' в файле '.env'")

    remote_disk: YandexDisk = YandexDisk(token=cloud_token, remote_folder=cloud_dir)
    remote_disk.get_info()
    return remote_disk


def check_env() -> Tuple[Tuple[str, str], YandexDisk, str]:
    return check_local_paths(), check_remote_data(), check_sync_time()


load_dotenv()
