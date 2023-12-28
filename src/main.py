import customtkinter
from main_window import MainWindow
import music_player


if __name__ == "__main__":
    root = customtkinter.CTk()
    main_window = MainWindow(root)
    music_player.initialize(root, main_window)
    root.mainloop()