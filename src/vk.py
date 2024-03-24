import requests


class VK:

    def __init__(self, version='5.131'):
        self.token = "626a2ff1626a2ff1626a2ff13b617db03e6626a626a2ff107932c300ed1070afc206121"
        self.id = 298866132
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_photos(self, target):
        url = 'https://api.vk.com/method/photos.get'
        params = {"owner_id": target,
                  "album_id": "profile",
                  "extended": 1,
                  "photo_sizes": 1}
        response = requests.get(url, params={**self.params, **params})
        if response.json().get("error"):
            raise ValueError(f"Возникла ошибка при получении фотографий: {response.json().get("error")}")
        return response.json()
