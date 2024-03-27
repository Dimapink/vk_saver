"""
Модуль, отвечающий за соединение и загрузку фотографий на Яндекс Диск
"""
import posixpath
import os
import requests
import yadisk
from alive_progress import alive_it


class Ya:
    def __init__(self, key):
        self.disc = yadisk.YaDisk(token=key)
        try:
            self.disc.get_disk_info()
        except yadisk.exceptions.UnauthorizedError as e:
            print(f"Проблема взаимодействия с диском, проверьте ключ, {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"Проблема взаимодействия с диском, проверьте интернет соединение, {e}")

    def recursive_upload(self, from_dir: str, to_dir: str):
        """
        Метод загрузки фотографий на Яндекс Диск
        :param from_dir: папка, откуда будут браться фотографии
        :param to_dir: папка на диске куда будет сохранены фото
        :return: None
        """
        if not self.disc.is_dir("photos"):
            self.disc.mkdir("photos")
        for root, dirs, files in os.walk(from_dir):
            p = root.split(from_dir)[1].strip(os.path.sep)
            dir_path = posixpath.join(to_dir, p)

            try:
                self.disc.mkdir(dir_path)
            except yadisk.exceptions.PathExistsError:
                pass

            for file in alive_it(files):
                file_path = posixpath.join(dir_path, file)
                p_sys = p.replace("/", os.path.sep)
                in_path = os.path.join(from_dir, p_sys, file)

                try:
                    self.disc.upload(in_path, file_path)
                except yadisk.exceptions.PathExistsError:
                    pass
        print(f"Диск пользователя {self.disc.get_disk_info().user.display_name} был обновлен\n")
