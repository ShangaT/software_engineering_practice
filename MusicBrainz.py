import requests
import statistics
import matplotlib.pyplot as plt

def get_album_average_track_length(album_id):
    url = f"https://musicbrainz.org/ws/2/release/{album_id}?fmt=json&inc=recordings"
    response = requests.get(url)
    data = response.json()    
    media = [] #список списков     
    for medium in data.get("media", []):
        track_lengths = []
        for track in medium.get("tracks", []):
            track_lengths.append(int(track["length"]))
        media.append(track_lengths)
    return media
    
def get_average_lengths(list_media):
    values = []
    media = [] #список средних длин треков на каждом носителе
    for track_lengths in list_media:
        average_on_medium = statistics.mean(track_lengths)
        media.append(average_on_medium)
    values = {
        "media": media,
        "all": statistics.mean(media)
    }
    return values

def get_data_artist(artist_id):
    url = f"https://musicbrainz.org/ws/2/artist/{artist_id}?fmt=json&inc=release-groups"
    response = requests.get(url)
    data = response.json()
    return data

def get_sort_albums(data):
    albums = []
    for release_group in data.get("release-groups", []):
        album_type = release_group.get("primary-type")
        if album_type and album_type != "Compilation":
            album = {
                "title": release_group.get("title"),
                "date": release_group.get("first-release-date")
            }
            albums.append(album)    

    sorted_albums = sorted(albums, key=lambda album: album["date"])
    return sorted_albums

def visualize_average_track_lengths(albums, average_lengths):
    plt.figure(figsize=(10, 5))
    plt.barh(albums, average_lengths)
    plt.xticks(rotation=90)
    plt.xlabel("Средняя длинна треков")
    plt.ylabel("ID релиза")
    plt.title("СРЕДНЯЯ ДЛИННА ТРЕКОВ В РЕЛИЗЕ")
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    #Вывести среднюю длину треков в релизе и на каждом отдельном диске
    releases = ["c96d6546-25e4-4717-b514-62684245675f",
                "ed118c5f-d940-4b52-a37b-b1a205374abe",
                "a4864e94-6d75-4ade-bc93-0dabf3521453",
                "e6e4ae10-4241-43a5-a9ae-911277348c59", 
                "51031f3d-033a-4ab1-9739-a33b4e3eef02",
                "594687cc-bdc1-4fff-858f-25bb5ec0d87d"
                ]

    medium_lengths_all = []
    for i in releases:
        lengths = get_album_average_track_length(i)
        medium_lengths = get_average_lengths(lengths)
        medium_lengths_media = ", ".join(str(value) for value in medium_lengths["media"])
        print(f'Средняя длинна треков релизе: {medium_lengths["all"]}\nНа каждом отдельном диске: {medium_lengths_media}\n')
        medium_lengths_all.append(medium_lengths["all"])

    visualize_average_track_lengths(releases, medium_lengths_all)

    #Вывести список названий альбомов с датой выхода. Альбомы не могут быть типа «компиляция». Список должен быть отсортирован по дате выхода альбома
    artist_name = lambda data: data.get("name")
    artist_ids = ["cc197bad-dc9c-440d-a5b5-d52ba2e14234",
                "f90e8b26-9e52-4669-a5c9-e28529c47894",
                "53b106e7-0cc6-42cc-ac95-ed8d30a3a98e",
                "83d91898-7763-47d7-b03b-b92132375c47",
                "0b51c328-1f2b-464c-9e2c-0c2a8cce20ae",
                "86437518-fca1-4117-b698-b371b72d76a5",
                "d620cf32-e240-46a4-a078-db87acb5ffa0",
                "e4b06dc9-c196-49e1-a20a-554e72d95268",
                "0783b768-6719-450b-a7e1-7e891da17af3",
                "5ca35ace-4006-4d4a-af04-5cd91dafab14",
                "f7456b5b-e5a5-454e-b5db-047308210c8e",
                "247efe0f-80f1-477c-a4a0-b5cb1b8c832e",
                "0944e98f-0b9f-4574-babc-7badf4cd0f74",
                "064db6e8-fdfb-4acb-a327-fc2de75b37de",
                "ae97ba5f-e7ed-4ed5-9a53-eba415fc49d4"]

    for i in artist_ids:
        data = get_data_artist(i)
        name = artist_name(data)
        albums = get_sort_albums(data)
        print(f'ИСПОЛНИТЕЛЬ: {name}\n')
        for album in albums:
            print(f'НАИМЕНОВАНИЕ: {album["title"]}\nДАТА ВЫХОДА: {album["date"]}\n')

   



