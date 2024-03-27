import os
from src.saver import Saver
from src.vk import VK
from src.drive_loader import Ya


def start(target_id, disc_key):
    print("Фотографии будут загружены в папку photos/{id_пользователя}")
    try:
        vk = VK()
        photos = vk.get_photos(target=target_id)
        photos = Saver.parse_photo_data(photos)
    except Exception as e:
        print(e)
    else:
        print(f"Сохранение фотографий в папку photos/{target_id}")
        try:
            Saver.save_local(photos, target_id)
        except Exception as e:
            print(e)
        else:
            print("Отправка фотографий на Яндекс Диск")
            try:
                disc = Ya(disc_key)
                disc.recursive_upload(os.path.join("photos", target_id), f"photos/{target_id}")
            except Exception as e:
                print(e)
            finally:
                print(f"Отчет о фотографиях сформирован в папке {target_id}")
                Saver.create_report(photos, target_id)


if __name__ == "__main__":
    user_id = input("Введите id пользователя для сохранения фотографий: ")
    key = input("Введите ключ от Yandex Диска: ")
    start(user_id, key)
