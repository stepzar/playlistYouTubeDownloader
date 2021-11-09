import shutil
import time
import requests
import json

from pytube import YouTube, Playlist
import subprocess
import os
import threading

def download_playlist(url):
    playlist = Playlist(url)

    cont = 1
    if os.path.isdir(playlist.title):
        print("Cartella Playlist già esistente: " + playlist.title)
        return

    os.mkdir(playlist.title)
    threads = []
    for song in playlist.videos:
        t = threading.Thread(target=download_song_tomp3, args=(song, playlist.title,))
        t.start()
        threads.append(t)

    map(lambda t: t.join(), threads)
    while threads[-1].is_alive():
        #wait
        time.sleep(0.5)



def download_song_tomp3(song, playlist_title):
    print(song.title)

    # download
    try:
        song.streams.filter(only_audio=True)[4].download(output_path=playlist_title, filename=song.title + ".mp3")
    except:
        song.streams.filter(only_audio=True)[2].download(output_path=playlist_title, filename=song.title + ".mp3")

    # convert
    #subprocess.run(["ffmpeg", "-i", "temp/" + song.title, playlist_title + "/" + song.title + ".mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    print("Downloaded: " + song.title)

def activate(license):
    url = "https://api.keygen.sh/v1/accounts/kitemmuort01/licenses/actions/validate-key"

    payload = json.dumps({
        "meta": {
            "key": license,
            "scope": {
                "product": "cb718770-4c17-4ccc-b1ef-35ed772b866c",
                "policy": "79c0f3cd-033e-4aaa-bfef-30f0de5d95cb",
                "fingerprint": "39:57:94:94:48:98:01:83"
            }
        }
    })

    headers = {
        'Content-Type': 'application/vnd.api+json',
        'Accept': 'application/vnd.api+json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.json()["data"] == None:
        return False
    else:
        return True

if __name__ == '__main__':
    print("Software created by stepzar, check my github: github.com/stepzar")
    print("\n\n")

    license = input("Inserisci la chiave di licenza: ")

    if activate(license):
        link = input("Inserisci il link della playlist youtube: ")

        while not(link.startswith("https://www.youtube.com") or link.startswith("https://youtube.com")):
            link = input("Inserisci un link corretto: ")

        print("Downloading...\n\n")
        if "playlist" in link:
            download_playlist(link)

        print("\n\nDownload Completato! Grazie per avermi scelto, stepzar <3")

        #shutil.rmtree("temp")
    else:
        print("Devi attivare la tua copia di Playlist Downloader")
