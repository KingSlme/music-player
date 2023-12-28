import customtkinter
import tkinter
import music_player


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.songs = { }
        self.song_names = []
        self.current_song_name = "None"
        self.current_song_path = "None"
        self.play_button_state = "None"
        self.song_listbox = None
        self.play_button = None
        self.previous_button = None
        self.next_button = None
        self.volume_slider = None
        self.create_main_window()

    @staticmethod
    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}") 

    def toggle_buttons(self, state):
        self.play_button.configure(state=state)
        self.previous_button.configure(state=state)
        self.next_button.configure(state=state)

    def play_button_callback(self):
        if self.play_button_state == "None":
            self.play_song()
        elif self.play_button_state == "Playing":
            self.play_button_state = "Paused"
            self.play_button.configure(text="Resume")
            music_player.pause()
        elif self.play_button_state == "Paused":
            self.play_button_state = "Playing"
            self.play_button.configure(text="Pause")
            music_player.resume()

    def clear_song_listbox(self):
        self.song_listbox.delete(0, "end")

    def select_song(self, index):
        self.song_listbox.selection_clear(0, "end")
        self.song_listbox.selection_set(index)
        self.song_listbox.see(index)

    def choose_songs_button_callback(self):
        self.play_button_state = "None"
        self.play_button.configure(text="Play")
        music_player.stop()
        self.songs = music_player.get_songs_from_dir()
        self.song_names = list(self.songs.keys())
        self.clear_song_listbox()
        for i, song_name in enumerate(self.song_names):
            self.song_listbox.insert(i, song_name)
        if len(self.song_names) > 0:
            self.select_song(0)
            self.current_song_name = self.song_names[0]
            self.current_song_path = self.songs[self.current_song_name]
            self.toggle_buttons("normal")
        else:
            self.toggle_buttons("disabled")

    def song_listbox_selection_callback(self, event):
        self.current_song_name = self.song_listbox.get(self.song_listbox.curselection())
        self.current_song_path = self.songs[self.current_song_name]
        self.play_song()
    
    def play_previous_song(self):
        if self.song_names.index(self.current_song_name) == 0:
            # Start from end index
            self.select_song(len(self.song_names) - 1)
            self.current_song_name = self.song_names[len(self.song_names) - 1]
        else:
            self.select_song(self.song_names.index(self.current_song_name) - 1)
            self.current_song_name = self.song_names[self.song_names.index(self.current_song_name) - 1]
        self.current_song_path = self.songs[self.current_song_name]
        self.play_song()

    def play_next_song(self):
        if self.song_names.index(self.current_song_name) == len(self.song_names) - 1:
            # Start from beginning index
            self.select_song(0)
            self.current_song_name = self.song_names[0]
        else:
            self.select_song(self.song_names.index(self.current_song_name) + 1)
            self.current_song_name = self.song_names[self.song_names.index(self.current_song_name) + 1]
        self.current_song_path = self.songs[self.current_song_name]
        self.play_song()

    def play_song(self):
        self.play_button_state = "Playing"
        self.play_button.configure(text="Pause")
        music_player.play(self.current_song_path)

    def volume_slider_callback(self, *_):
        music_player.set_volume(self.volume_slider.get() / 100)

    def create_main_window(self):
        # Main Window
        self.root.title("Music Player")
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        MainWindow.center_window(self.root, 250, 370)
        self.root.resizable(width=False, height=False)
        # Frames
        frame = customtkinter.CTkFrame(master=self.root)
        frame.pack(pady=10, padx=10, fill="both", expand=True)
        button_frame = customtkinter.CTkFrame(master=frame, bg_color=['gray92', 'gray14'], fg_color=['gray90', 'gray13'], corner_radius=0)
        button_frame.grid(row=1, column=0, pady=(0, 10))
        # Listbox
        self.song_listbox = tkinter.Listbox(master=frame,font="Inter 12 bold", fg="#a6a5a4", width=23, height=10 ,bg="#3c3c3c" ,selectmode=tkinter.SINGLE, bd=0, highlightthickness=0, activestyle="none")
        self.song_listbox.grid(row=0, column=0, padx=10, pady=10)
        self.song_listbox.bind("<<ListboxSelect>>", self.song_listbox_selection_callback)
        # Buttons
        self.play_button = customtkinter.CTkButton(master=button_frame, width=90, height=40, text="Play", font=customtkinter.CTkFont("Inter", 20, weight="bold"), command=self.play_button_callback)
        self.play_button.grid(row=0, column=1, padx=10)
        self.previous_button = customtkinter.CTkButton(master=button_frame, width=50, height=40, text="<-", font=customtkinter.CTkFont("Inter", 20, weight="bold"), command=self.play_previous_song)
        self.previous_button.grid(row=0, column=0, padx=(10, 0))
        self.next_button = customtkinter.CTkButton(master=button_frame, width=50, height=40, text="->", font=customtkinter.CTkFont("Inter", 20, weight="bold"), command=self.play_next_song)
        self.next_button.grid(row=0, column=2, padx=(0, 10))
        choose_songs_button = customtkinter.CTkButton(master=frame, width=100, height=40, text="Choose Songs", font=customtkinter.CTkFont("Inter", 20, weight="bold"), command=self.choose_songs_button_callback)
        choose_songs_button.grid(row=4, column=0, pady=(0, 10))
        self.toggle_buttons("disabled")
        # Progress Bars
        self.volume_slider = customtkinter.CTkSlider(master=frame, width=210, height=20, progress_color="#0288f5", from_=0, to=100, hover=False, command=self.volume_slider_callback)
        self.volume_slider.grid(row=3, column=0, pady=(0, 10))