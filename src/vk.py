"""
Модуль, отвечающий за работу с api vk
"""
import requests


class VK:

    def __init__(self, version='5.131'):
        self.token = "626a2ff1626a2ff1626a2ff13b617db03e6626a626a2ff107932c300ed1070afc206121"
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def parse_target_id(self, target: str) -> str:
        """
        Метод для определения введенного id пользователя
        :param target: строка, id, который вводит пользователь
        :return: определенный id пользователя
        """
        if not target:
            raise ValueError("Введите пользователя")
        if target.startswith("id"):
            target = target.lstrip("id")
            if target.isnumeric():
                return target
        elif target.isnumeric():
            return target
        else:
            user_id = self.get_id_by_screen_name(target)
            return user_id

    def get_id_by_screen_name(self, target):
        """
        Метод для определения id пользователя по его Screen Name
        :param target: имя, которое необходимо найти
        :return: id пользователя по его Screen Name, если id был определен
        """
        url = "https://api.vk.com/method/utils.resolveScreenName"
        params = {"access_token": self.token, "v": self.version, "screen_name": target}
        try:
            response = requests.get(url, params={**self.params, **params})
        except ConnectionError:
            print("Проблема с подключением к api VK")
        else:
            if isinstance(response.json().get("response"), list):
                raise ValueError("Пользователь с таким именем не найден")
            else:
                resolved_id = response.json().get("response").get("object_id")
                return resolved_id

    def get_photos(self, target: str):
        """
        Метод для получения данных о фотографиях профиля пользователя
        :param target: id/Screen name пользователя
        :return: данные по фотографиям пользователя
        """
        url = 'https://api.vk.com/method/photos.get'
        params = {"owner_id": self.parse_target_id(target),
                  "album_id": "profile",
                  "extended": 1,
                  "photo_sizes": 1}
        response = requests.get(url, params={**self.params, **params})
        if response.json().get("error"):
            raise ValueError(f"Возникла ошибка при получении фотографий: "
                             f"{response.json().get("error").get("error_msg")}")

        return response.json()
