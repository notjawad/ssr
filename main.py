import tkinter as tk
import ttkbootstrap as boot
import threading
import time
import os
import json
import re
import webbrowser

from tkinter import messagebox
from samsung.auth import connect as samsung_connect
from PIL import Image, ImageTk


def split_upper(s):
    up = filter(None, re.split("([A-Z][^A-Z]*)", s))
    return " ".join(up).title()


def open_url(url):
    webbrowser.open(url)


def load_theme():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            config = json.load(f)
            return config["theme"]


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Samsung TV Remote")
        self.geometry("315x515")
        self.resizable(False, False)

        self.tv = None

        self.create_remote_layout()
        self.create_menu()

    def create_remote_layout(self):

        self.remote_frame = boot.Frame(self)
        self.remote_frame.pack(fill=tk.BOTH, expand=True)

        self.ip_label = boot.Label(self.remote_frame, text="IP Address:")
        self.ip_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

        self.ip_entry = boot.Entry(self.remote_frame)
        self.ip_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config = json.load(f)
                self.ip_entry.insert(0, config["ip"])

        self.connect_text = tk.StringVar()
        self.connect_text.set("Connect")
        self.connect_button = boot.Button(
            self.remote_frame,
            textvariable=self.connect_text,
            command=threading.Thread(target=self.connect, daemon=True).start,
        )
        self.connect_button.grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)

        self.power_frame = boot.Frame(self.remote_frame)
        self.power_frame.grid(
            row=1, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5
        )

        self.power_button = boot.Button(
            self.power_frame,
            text="Power",
            bootstyle="danger",
            command=threading.Thread(target=self.power, daemon=True).start,
        )
        self.power_button.grid(row=0, column=0, padx=4)

        self.volume_up_button = boot.Button(
            self.power_frame,
            text="Volume +",
            command=self.volume_up,
        )
        self.volume_up_button.grid(row=0, column=1, padx=5)

        self.volume_down_button = boot.Button(
            self.power_frame,
            text="Volume -",
            command=self.volume_down,
        )
        self.volume_down_button.grid(row=0, column=2, padx=5)

        self.mute_button = boot.Button(
            self.power_frame,
            text="Mute",
            command=self.mute,
        )
        self.mute_button.grid(row=0, column=3, padx=5)

        self.number_frame = boot.Frame(self.remote_frame)
        self.number_frame.grid(
            row=2, column=0, columnspan=3, sticky=tk.W, padx=60, pady=5
        )

        self.numbers = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "0",
            "Back",
            "Enter",
        ]

        for i, number in enumerate(self.numbers):
            button = boot.Button(
                self.number_frame,
                text=number,
                width=5,
            )
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)

        for button in self.number_frame.winfo_children():
            if button["text"] == "Back":
                button["command"] = self.back
            elif button["text"] == "Enter":
                button["command"] = self.enter
            elif button["text"] == "0":
                button["command"] = self.zero
            elif button["text"] == "1":
                button["command"] = self.one
            elif button["text"] == "2":
                button["command"] = self.two
            elif button["text"] == "3":
                button["command"] = self.three
            elif button["text"] == "4":
                button["command"] = self.four
            elif button["text"] == "5":
                button["command"] = self.five
            elif button["text"] == "6":
                button["command"] = self.six
            elif button["text"] == "7":
                button["command"] = self.seven
            elif button["text"] == "8":
                button["command"] = self.eight
            elif button["text"] == "9":
                button["command"] = self.nine

        self.arrow_frame = boot.Frame(self.remote_frame)
        self.arrow_frame.grid(
            row=4, column=0, columnspan=3, sticky=tk.W, padx=60, pady=5
        )

        self.up_button = boot.Button(
            self.arrow_frame,
            text="Up",
            width=5,
        )
        self.up_button.grid(row=0, column=1, pady=5, padx=5)

        self.down_button = boot.Button(
            self.arrow_frame,
            text="Down",
            width=5,
            command=self.down,
        )
        self.down_button.grid(row=2, column=1, pady=5, padx=5)

        self.left_button = boot.Button(
            self.arrow_frame,
            text="Left",
            width=5,
            command=self.left,
        )
        self.left_button.grid(row=1, column=0, pady=5, padx=5)

        self.right_button = boot.Button(
            self.arrow_frame,
            text="Right",
            width=5,
            command=self.right,
        )
        self.right_button.grid(row=1, column=2, pady=5, padx=5)

        self.ok_button = boot.Button(
            self.arrow_frame,
            text="OK",
            width=5,
            command=self.ok,
        )
        self.ok_button.grid(row=1, column=1, pady=5, padx=5)

        self.rest_frame = boot.Frame(self.remote_frame)
        self.rest_frame.grid(
            row=5, column=0, columnspan=3, sticky=tk.W, padx=40, pady=5
        )

        bts = ["Home", "Menu", "Info"]

        for i, bt in enumerate(bts):
            button = boot.Button(
                self.rest_frame,
                text=bt,
                width=7,
            )
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)

        for button in self.rest_frame.winfo_children():
            if button["text"] == "Home":
                button["command"] = self.home
            elif button["text"] == "Menu":
                button["command"] = self.menu
            elif button["text"] == "Info":
                button["command"] = self.info

        self.color_frame = boot.Frame(self.remote_frame)
        self.color_frame.grid(
            row=6, column=0, columnspan=3, sticky=tk.W, padx=40, pady=5
        )

        self.color_buttons = [
            "Green",
            "Yellow",
            "Cyan",
            "Red",
        ]

        for i, color in enumerate(self.color_buttons):
            button = boot.Button(
                self.color_frame,
                text=color,
                width=4,
            )
            button.grid(row=i // 4, column=i % 4, padx=5, pady=5)

        for button in self.color_frame.winfo_children():

            if button["text"] == "Red":
                button["command"] = self.red
                button["bootstyle"] = "danger"
                button["text"] = ""

            elif button["text"] == "Green":
                button["command"] = self.green
                button["bootstyle"] = "success"
                button["text"] = ""

            elif button["text"] == "Yellow":
                button["command"] = self.yellow
                button["bootstyle"] = "warning"
                button["text"] = ""

            elif button["text"] == "Cyan":
                button["command"] = self.cyan
                button["bootstyle"] = "info"
                button["text"] = ""

        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config = json.load(f)
                if config["theme"] in [
                    "darkly",
                    "solar",
                    "superhero",
                    "cyborg",
                    "vapor",
                ]:
                    self.image = ImageTk.PhotoImage(
                        Image.open("assets/light_logo.png").resize((25, 25))
                    )

                else:
                    self.image = ImageTk.PhotoImage(
                        Image.open("assets/dark_logo.png").resize((25, 25))
                    )
        else:
            self.image = ImageTk.PhotoImage(
                Image.open("assets/light_logo.png").resize((25, 25))
            )

        self.image_label = boot.Label(
            self.remote_frame, image=self.image, cursor="hand2"
        )
        self.image_label.grid(row=7, column=2, sticky=tk.E, padx=10, pady=10)

        self.image_label.bind(
            "<Button-1>", lambda e: open_url("https://github.com/notjawad")
        )

    def create_menu(self):

        self.menu = boot.Menu(self)
        self.config(menu=self.menu)

        self.themes_menu = boot.Menu(self.menu, tearoff=0)
        self.themes_menu.add_command(
            label="Darkly", command=lambda: self.change_theme("darkly")
        )
        self.themes_menu.add_command(
            label="Flatly", command=lambda: self.change_theme("flatly")
        )
        self.themes_menu.add_command(
            label="Lumen", command=lambda: self.change_theme("lumen")
        )
        self.themes_menu.add_command(
            label="Minty", command=lambda: self.change_theme("minty")
        )
        self.themes_menu.add_command(
            label="Pulse", command=lambda: self.change_theme("pulse")
        )
        self.themes_menu.add_command(
            label="Sandstone", command=lambda: self.change_theme("sandstone")
        )
        self.themes_menu.add_command(
            label="Simplex", command=lambda: self.change_theme("simplex")
        )

        self.themes_menu.add_command(
            label="Solar", command=lambda: self.change_theme("solar")
        )

        self.themes_menu.add_command(
            label="Superhero", command=lambda: self.change_theme("superhero")
        )
        self.themes_menu.add_command(
            label="United", command=lambda: self.change_theme("united")
        )
        self.themes_menu.add_command(
            label="Yeti", command=lambda: self.change_theme("yeti")
        )

        self.themes_menu.add_command(
            label="Cyborg", command=lambda: self.change_theme("cyborg")
        )

        self.themes_menu.add_command(
            label="Vapor", command=lambda: self.change_theme("vapor")
        )

        self.menu.add_cascade(label="Themes", menu=self.themes_menu)

    def connect(self):
        if self.ip_entry.get() == "":
            messagebox.showerror("Error", "Please enter an IP address.")
            return

        ip = self.ip_entry.get()
        if ip:
            if not os.path.exists("config.json"):
                with open("config.json", "w") as f:
                    json.dump({"ip": ip}, f, indent=4)

            self.tv = samsung_connect(ip)
            self.connect_button["bootstyle"] = "success"
            self.update()

            self.ip_entry["state"] = "disabled"
            self.connect_button["state"] = "disabled"

            self.apps = self.tv.app_list()

            self.launch_menu = boot.Menu(self.menu, tearoff=False)
            self.menu.add_cascade(label="Launch App", menu=self.launch_menu)

            self.device_menu = boot.Menu(self.menu, tearoff=False)
            self.menu.add_cascade(label="Device", menu=self.device_menu)
            self.device_menu.add_command(
                label="Device Info",
                command=threading.Thread(target=self.device_info).start,
            )

            for app in self.apps:
                self.launch_menu.add_command(
                    label=app["name"],
                    command=threading.Thread(
                        target=self.launch_app, args=(app["appId"],)
                    ).start,
                )
            messagebox.showinfo("Success", "Connected successfully.")

    def launch_app(self, app_id):
        self.tv.run_app(app_id)
        time.sleep(1)

        status = self.tv.rest_app_status(app_id)
        if status["running"]:
            messagebox.showinfo("Success", "App launched successfully.")

    def device_info(self):
        info = self.tv.rest_device_info()

        features = []
        for key, value in info["device"].items():
            if key in (
                "FrameTVSupport",
                "GamePadSupport",
                "ImeSyncedSupport",
                "TokenAuthSupport",
                "VoiceSupport",
            ):
                features.append(f"{split_upper(key)}: {value}")
        features = "\n".join(features)

        other_info = []
        for key, value in info["device"].items():
            if key not in (
                "FrameTVSupport",
                "GamePadSupport",
                "ImeSyncedSupport",
                "TokenAuthSupport",
                "VoiceSupport",
            ):
                other_info.append(f"{split_upper(key)}: {value}")

        other_info = "\n".join(other_info)
        messagebox.showinfo(
            "Device Info", f"Features:\n\n{features} \n\nOther Info:\n\n{other_info}"
        )

    def change_theme(self, theme):
        boot.Style(theme)
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                data = json.load(f)
                data["theme"] = theme
            with open("config.json", "w") as f:
                json.dump(data, f, indent=4)

            if theme in [
                "darkly",
                "solar",
                "superhero",
                "cyborg",
                "vapor",
            ]:
                self.image = ImageTk.PhotoImage(
                    Image.open("assets/light_logo.png").resize((25, 25))
                )

            else:
                self.image = ImageTk.PhotoImage(
                    Image.open("assets/dark_logo.png").resize((25, 25))
                )

            self.image_label["image"] = self.image

    def send_key(self, key):
        self.tv.send_key(key)

    def volume_up(self):
        try:
            self.tv.send_key("KEY_VOLUP")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def volume_down(self):
        try:
            self.tv.send_key("KEY_VOLDOWN")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def mute(self):
        try:
            self.tv.send_key("KEY_MUTE")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def power(self):
        try:
            self.tv.send_key("KEY_POWER")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def back(self):
        try:
            self.tv.send_key("KEY_RETURN")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def enter(self):
        try:
            self.tv.send_key("KEY_ENTER")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def zero(self):
        try:
            self.tv.send_key("KEY_0")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def one(self):
        try:
            self.tv.send_key("KEY_1")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def two(self):
        try:
            self.tv.send_key("KEY_2")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def three(self):
        try:
            self.tv.send_key("KEY_3")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def four(self):
        try:
            self.tv.send_key("KEY_4")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def five(self):
        try:
            self.tv.send_key("KEY_5")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def six(self):
        try:
            self.tv.send_key("KEY_6")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def seven(self):
        try:
            self.tv.send_key("KEY_7")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def eight(self):
        try:
            self.tv.send_key("KEY_8")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def nine(self):
        try:
            self.tv.send_key("KEY_9")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def up(self):
        try:
            self.tv.send_key("KEY_UP")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def down(self):
        try:
            self.tv.send_key("KEY_DOWN")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def left(self):
        try:
            self.tv.send_key("KEY_LEFT")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def right(self):
        try:
            self.tv.send_key("KEY_RIGHT")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def ok(self):
        try:
            self.tv.send_key("KEY_OK")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def home(self):
        try:
            self.tv.send_key("KEY_HOME")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def menu(self):
        try:
            self.tv.send_key("KEY_MENU")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def info(self):
        try:
            self.tv.send_key("KEY_INFO")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def red(self):
        try:
            self.tv.send_key("KEY_RED")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def green(self):
        try:
            self.tv.send_key("KEY_GREEN")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def cyan(self):
        try:
            self.tv.send_key("KEY_CYAN")
        except:
            messagebox.showerror("Error", "Not connected to TV")

    def yellow(self):
        try:
            self.tv.send_key("KEY_YELLOW")
        except:
            messagebox.showerror("Error", "Not connected to TV")


if __name__ == "__main__":
    app = App()
    app.mainloop()
