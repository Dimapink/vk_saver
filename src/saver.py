"""
Модуль, отвечающий за обработку данных фотографий и их загрузку
"""
import json
import requests
import os
from datetime import datetime
from alive_progress import alive_it


class Saver:
    @staticmethod
    def get_largest_photo(photos: list[dict]):
        """
        Метод для определения наибольшей фотографии из списка
        :param photos: структура данных, информация о доступных размерах одного фото
        :return: структура данных, информация о фото с наибольшим размером
        """
        largest_size = (0, "a")
        largest_image = {}
        for metadata in photos:
            size = (metadata.get("height") * metadata.get("width"), metadata.get("type"))
            if size > largest_size:
                largest_size = size
                largest_image = metadata
        return largest_image

    @staticmethod
    def parse_photo_data(data: dict):

        photo_data = (data.get("response").get("items"))
        payload = []
        for photo in photo_data:
            size = Saver.get_largest_photo(photo.get("sizes"))
            payload.append({"likes": sum(photo.get("likes").values()),
                            "size": size,
                            "date": photo.get("date"),
                            "id": photo.get("id")})
        payload = Saver.parse_name(payload)
        return payload

    @staticmethod
    def parse_name(photos: list[dict]) -> dict:
        """
        Метод определения имени фото при сохранении
        :param photos: список фотографий
        :return: словарь: {имя фотографии: данные о фото}
        """
        result = {}
        for name, data in enumerate(photos, 1):
            if result.get(data.get("likes")):
                name = f"{data.get('likes')}_{datetime.fromtimestamp(data.get('date')).strftime("%d-%m-%Y--%H-%M")}"
            else:
                name = data.get("likes")
            result.update({name: data})
        return result

    @staticmethod
    def save_local(data_to_save, user_id):
        """
        Метод сохранения фотографий
        :param data_to_save: данные о фото для сохранения
        :param user_id: id пользователя (имя папки)
        :return:
        """
        directory_name = "photos"
        if not os.path.exists(os.path.join(directory_name, user_id)):
            os.makedirs(os.path.join(directory_name, user_id))
        for name, photo_data in alive_it(data_to_save.items()):
            photo = requests.get(photo_data.get("size").get("url")).content
            with open(f"{os.path.join(directory_name, user_id, str(name))}.png", "wb") as file:
                file.write(photo)

    @staticmethod
    def create_report(data_to_save, user_id):
        """
        Метод генерации отчета о фотографиях
        :param data_to_save:
        :param user_id:
        :return:
        """
        directory_name = "photos"
        if not os.path.exists(os.path.join(directory_name, user_id)):
            os.makedirs(os.path.join(directory_name, user_id))
        payload = []
        for name, photo_data in data_to_save.items():
            payload.append(
                {"file_name": name,
                 "size": photo_data.get("size").get("type")})
        report = {"report": payload}
        with open(f"{os.path.join(directory_name, user_id, 'report')}.json", "w") as file:
            json.dump(report, file, indent=4)
