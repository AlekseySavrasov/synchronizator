"""
Скрипт для работы с удаленным хранилищем на Яндекс.Диске.

"""

import requests
from loguru import logger
from requests import Response


class YandexDisk:
    """
    Класс для работы с удаленным хранилищем на Яндекс.Диске.

    Attributes:
        token (str): Токен для доступа к API Яндекс.Диска.
        folder_path (str): Путь к удаленной папке на Яндекс.Диске.
        base_url (str): Базовый URL для API Яндекс.Диска.
    """

    def __init__(self, token: str, remote_folder: str):
        self.token: str = token
        self.folder_path: str = remote_folder
        self.base_url: str = "https://cloud-api.yandex.net/v1/disk/resources"

    def load(self, local_folder: str, file_name: str, overwrite: bool = False) -> bool:
        """
        Загружает файл на удаленное хранилище.

        Args:
            local_folder (str): Путь к локальной директории с файлом.
            file_name (str): Имя файла.
            overwrite (bool, optional): Флаг перезаписи файла на удаленном хранилище. По умолчанию False.

        Returns:
            bool: Результат выполнения операции загрузки файла.
        """
        url: str = f"{self.base_url}/upload?path={self.folder_path}/{file_name}&overwrite=true"
        headers: dict[str, str] = {"Authorization": f"OAuth {self.token}"}

        try:
            response: Response = requests.get(url, headers=headers)
            response.raise_for_status()

            upload_url = response.json()["href"]

            with open(f"{local_folder}{file_name}", "rb") as file:
                response: Response = requests.put(upload_url, data=file)

                if overwrite:
                    logger.info(f"Файл {file_name} успешно перезаписан.")
                else:
                    logger.info(f"Файл {file_name} успешно записан.")

            return response.status_code == 201

        except requests.exceptions.RequestException:
            error_msg: str = f"Файл {file_name} {'не перезаписан' if overwrite else 'не записан'}. Ошибка соединения"
            logger.error(error_msg)
            return False

    def reload(self, local_file_path: str, file_name: str) -> bool:
        """
        Перезагружает файл на удаленное хранилище (перезаписывает).

        Args:
            local_file_path (str): Путь к локальному файлу.
            file_name (str): Имя файла.

        Returns:
            bool: Результат выполнения операции перезагрузки файла.
        """
        return self.load(local_file_path, file_name, overwrite=True)

    def delete(self, filename: str) -> bool:
        """
        Удаляет файл с удаленного хранилища.

        Args:
            filename (str): Имя файла для удаления.

        Returns:
            bool: Результат выполнения операции удаления файла.
        """
        url: str = f"{self.base_url}?path={self.folder_path}/{filename}"
        headers: dict[str, str] = {"Authorization": f"OAuth {self.token}"}

        try:
            response: Response = requests.delete(url, headers=headers)
            logger.info(f"Файл {filename} успешно удален.")

            return response.status_code == 204

        except requests.exceptions.ConnectionError:
            logger.error(f"Файл {filename} не удален. Ошибка соединения")
            return False

    def get_info(self) -> dict:
        """
        Получает информацию о содержимом удаленного хранилища.

        Returns:
            dict: Информация о содержимом удаленного хранилища в формате JSON.
        """
        url: str = f"{self.base_url}/?path={self.folder_path}"
        headers: dict[str, str] = {"Authorization": f"OAuth {self.token}"}

        try:
            response: Response = requests.get(url, headers=headers)

            if response.status_code == 401:
                raise requests.exceptions.HTTPError(
                    "Ошибка авторизации пользователя. Проверьте корректность токена 'cloud_token'"
                )
            elif response.status_code == 404:
                raise requests.exceptions.HTTPError(
                    "Ошибка поиска удаленного ресурса. Проверьте корректность названия удаленной папки 'cloud_dir'"
                )

            return response.json()

        except requests.exceptions.ConnectionError:
            logger.error(f"Ошибка подключения к удаленному диску. Ошибка соединения")

        return {}
