import shutil
import time

from pytube import YouTube, Playlist
import subprocess
import os
import threading

def download_playlist(url):
    playlist = Playlist(url)

    if not os.path.isdir("temp"):
        os.mkdir("temp")

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
    # download
    try:
        song.streams.filter(only_audio=True)[4].download(output_path="temp", filename=song.title)
    except:
        song.streams.filter(only_audio=True)[2].download(output_path="temp", filename=song.title)

    # convert
    subprocess.run(["ffmpeg", "-i", "temp/" + song.title, playlist_title + "/" + song.title + ".mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    print("Downloaded: " + song.title)


if __name__ == '__main__':
    print("Software created by stepzar, check my github: github.com/stepzar")
    print("\n\n")
    link = input("Enter your video/playlist URL: ")

    while not(link.startswith("https://www.youtube.com") or link.startswith("https://youtube.com")):
        link = input("Enter a correct youtube URL: ")

    print("Downloading...\n\n")
    if "playlist" in link:
        download_playlist(link)

    print("\n\nDownload Complete! Thansk for using this product, by stepzar <3")

    shutil.rmtree("temp")
