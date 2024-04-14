import loguru
import os
import time
from dotenv import load_dotenv

load_dotenv()
old_files = current_files = {}


def get_files_in_current_directory(dir_path):
    exists_files = {}

    for i_file in os.listdir(dir_path):
        path_file = f"{dir_path}/{i_file}"

        if os.path.isfile(path_file):
            exists_files[i_file] = os.stat(path_file).st_mtime
    return exists_files


while True:
    old_files = current_files
    current_files = get_files_in_current_directory(os.getenv("sync_dir"))

    print(f"Старые файлы до сравнения с новыми: {old_files}")
    for key, value in current_files.items():
        if key not in old_files or value != old_files[key]:
            print(f"Пушим {key} на диск")
        else:
            old_files.pop(key)
    print(f"Старые файлы после сравнения с новыми: {old_files}")
    for key in old_files.keys():
        print(f"Удаляем {key} с диска")
    print(f"Старые файлы: {old_files}")

    print(f"Новые файлы: {current_files}")
    print(time.time())

    time.sleep(int(os.getenv("sync_time")))  # Подождем N секунд перед следующей проверкой


# if __name__ == "__main__":
#     func()
