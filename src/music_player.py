import pygame
import os
import customtkinter


def get_songs_from_dir():
    songs = { }
    supported_extenions = (".wav", ".mp3", ".ogg")
    try:
        ask_directory = customtkinter.filedialog.askdirectory()
        for file in os.listdir(ask_directory):
            if file.lower().endswith(supported_extenions):
                # songs[0].append(file)
                file_path = os.path.join(ask_directory, file)
                # songs[1].append(file_path)
                songs[file] = file_path
        return songs
    except FileNotFoundError:
        return songs


def play_music(music):
    pygame.mixer.music.load(music)
    pygame.mixer.music.play()


def initialize(root, main_window):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)
    root.after(0, check_music_done, root, main_window)


def play(song):
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(0)


def stop():
    pygame.mixer.music.stop()


def pause():
    pygame.mixer.music.pause()


def resume():
    pygame.mixer.music.unpause()


def set_volume(value):
    pygame.mixer.music.set_volume(value)


def check_music_done(root, main_window):
    if not pygame.mixer.music.get_busy() and main_window.play_button_state != "None" and main_window.play_button_state != "Paused":
        main_window.play_next_song()
    root.after(1000, check_music_done, root, main_window)