import json
from pprint import pprint
import requests
from tqdm import tqdm


class VK:
    def __init__(self, token, version="5.131"):
        self.params = {"access_token": token, "v": version}
        self.base = "https://api.vk.com/method"

    def get_friends(self, user_id, count=5):
        url = f"{self.base}/friends.get"
        params = {"user_id": user_id, "fields": ["city"], "count": count}
        params.update(self.params)
        response = requests.get(url, params=params)
        return response.json()

    def get_photos(self, user_id, count=5, album_id="profile"):
        url = f"{self.base}/photos.get"
        params = {
            "owner_id": user_id,
            "count": count,
            "album_id": album_id,
            "extended": 1,
        }
        params.update(self.params)
        response = requests.get(url, params=params)
        return response.json()


class YD:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://cloud-api.yandex.net/v1/disk/resources"
        self.headers = {"Authorization": f"OAuth {self.token}"}

    def create_folder(self, folder_name):
        url = self.base_url
        params = {"path": folder_name}
        response = requests.put(url, headers=self.headers, params=params)
        if response.status_code == 201:
            print(f'Папка "{folder_name}" успешно создана на Яндекс.Диске.')
        else:
            print(f'Папка "{folder_name}" уже существует на Яндекс.Диске.')

    def upload_file(self, path, url):
        upload_url = f"{self.base_url}/upload"
        params = {"path": path, "url": url}
        response = requests.post(upload_url, headers=self.headers, params=params)
        if response.status_code == 202:
            print(f'Файл "{path}" успешно загружен на Яндекс.Диск.')
        else:
            print(f"Ошибка при загрузке файла: {response.status_code}")


if __name__ == "__main__":
    vk_token = input("Введите ваш токен ВКонтакте: ")
    yd_token = input("Введите ваш токен Яндекс.Диска: ")
    user_id = input("Введите ID пользователя ВКонтакте: ")

    vk = VK(vk_token)
    photos = vk.get_photos(user_id, 5, "profile")
    pprint(photos)
    
    disk = YD(yd_token)
    disk.create_folder("Photos")

    photos_info = []

    for photo in tqdm(
        photos["response"]["items"], desc="Загрузка фотографий", unit="фото"
    ):
        photo_url = photo["sizes"][-1]["url"]
        photo_size = photo["sizes"][-1]["type"]
        photo_name = f"Photos/photo_{photo['id']}.jpg"
        disk.upload_file(photo_name, photo_url)

        photos_info.append(
            {"file_name": f"photo_{photo['id']}.jpg", "size": photo_size}
        )

with open("photos_info.json", "w", encoding="utf-8") as file:
    json.dump(photos_info, file, ensure_ascii=False, indent=4)

print("Информация о фотографиях сохранена в файл 'photos_info.json'.")
