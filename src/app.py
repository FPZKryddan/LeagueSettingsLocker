import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os
import sys
import stat

WIDTH = 750
HEIGHT = 150

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    root.geometry(f"{width}x{height}+{x}+{y}")

def toggle_write_acess():
    if settings_has_write_access():
        os.chmod("./game.cfg", stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        os.chmod("./PersistedSettings.json", stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

        text_label.config(text="Settings currently locked!", fg="red")
        button.config(text="Unlock league settings!")
        image_label.config(image=lock_image)
    else:
        os.chmod("./game.cfg", stat.S_IWUSR | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        os.chmod("./PersistedSettings.json", stat.S_IWUSR | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

        text_label.config(text="Settings currently unlocked!", fg="green")
        button.config(text="Lock league settings!")
        image_label.config(image=unlock_image)


def found_settings_file() -> bool:
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    targets = ["PersistedSettings.json", "game.cfg"]
    found = 0
    for file in files:
        print(os.stat(file))
        if file in targets:
            found +=1
        if found == len(targets):
            return True
    return False

def settings_has_write_access() -> bool:
    if os.access("./game.cfg", os.W_OK):
        return True
    return False


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")  
    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("LeagueSettingsLocker")
    center_window(root, WIDTH, HEIGHT)

    frame = tk.Frame(root)
    frame.pack(pady=10, padx=10)

    text_label = tk.Label(frame, text="Settings currently locked!", font=("Arial", 14), anchor="center", fg="red")
    text_label.pack(side=tk.TOP, fill=tk.X, pady=5)

    unlock_image_path = resource_path("images/unlock.png")
    unlock_image = Image.open(unlock_image_path)
    unlock_image = unlock_image.resize((75, 75))
    unlock_image = ImageTk.PhotoImage(unlock_image)

    lock_image_path = resource_path("images/lock.png")
    lock_image = Image.open(lock_image_path)
    lock_image = lock_image.resize((75, 75))
    lock_image = ImageTk.PhotoImage(lock_image)

    image_label = tk.Label(frame, image=unlock_image)
    image_label.pack(side=tk.LEFT)


    button = tk.Button(frame, text="Lock league settings!", command=toggle_write_acess, width=45, height=5)
    button.pack(side=tk.RIGHT, padx=10)


    # check for setting files
    if not found_settings_file():
        text_label.config(text="Setting files not found!", fg="red")
        button.config(state="disabled")
    else:
        # check permissions
        if not settings_has_write_access():
            text_label.config(text="Settings currently locked!", fg="red")
            button.config(text="Unlock league settings!")
            image_label.config(image=lock_image)
        else:
            text_label.config(text="Settings currently unlocked!", fg="green")
            button.config(text="Lock league settings!")
            image_label.config(image=unlock_image)



    root.mainloop()