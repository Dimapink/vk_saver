from src.saver import Saver
from src.vk import VK
from src.drive_loader import Ya


def main():
    target_id = input("Введите id пользователя для сохранения фотографий: ")
    if not target_id.isdigit():
        raise ValueError("id должен быть только цифрами")
    disc_key = input("Введите ключ от Yandex Диска: ")
    print("Фотографии будут загружены в папку photos/{id_пользователя}")
    me = VK()
    photos = me.get_photos(target=target_id)
    photos = Saver.parse_photo_data(photos)
    print(f"Сохранение фотографий в папку photos/{target_id}")
    Saver.save_local(photos, target_id)
    print("Отправка фотографий на Яндекс Диск")
    disc = Ya(disc_key)
    disc.recursive_upload(f"photos/{target_id}", f"photos/{target_id}")


if __name__ == "__main__":
    main()
