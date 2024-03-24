import requests
import os
from datetime import datetime
from alive_progress import alive_it


class Saver:
    @staticmethod
    def get_largest_photo(photos: list[dict]):
        print(photos)
        largest_size = (0, "a")
        largest_image = {}
        for metadata in photos:
            size = (metadata.get("height") * metadata.get("width"), metadata.get("type"))
            if size > largest_size:
                largest_size = size
                largest_image = metadata
        print(largest_image)
        return largest_image

    @staticmethod
    def parse_photo_data(data: dict) -> list[dict]:
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
    def parse_name(photos: list[dict]):
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
        directory_name = "photos"
        # f"{directory_name}/{user_id}"
        if not os.path.exists(os.path.join(directory_name, user_id)):
            os.makedirs(os.path.join(directory_name, user_id))
        for name, photo_data in alive_it(data_to_save.items()):
            photo = requests.get(photo_data.get("size").get("url")).content
            with open(f"{directory_name}/{user_id}/{name}.png", "wb") as file:
                file.write(photo)
