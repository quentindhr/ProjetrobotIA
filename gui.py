import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Transcription App")
        self.root.configure(bg="white")

        # Logo
        self.logo_label = tk.Label(root, bg="white")
        self.logo_label.pack(pady=20)

        # Text area
        self.text_area = tk.Text(root, height=10, width=50, bg="white")
        self.text_area.pack(pady=20)

        # Button to change logo
        self.change_logo_button = tk.Button(root, text="Changer le logo", command=self.change_logo)
        self.change_logo_button.pack(pady=10)

        # Button to enlarge logo
        self.enlarge_logo_button = tk.Button(root, text="Agrandir le logo", command=self.enlarge_logo)
        self.enlarge_logo_button.pack(pady=10)

        # Default logo
        self.logo_path = None
        self.logo_size = 100  # Default size
        self.update_logo()

    def change_logo(self):
        self.logo_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        self.update_logo()

    def enlarge_logo(self):
        self.logo_size += 50  # Increase size by 50 pixels
        self.update_logo()

    def update_logo(self):
        if self.logo_path:
            img = Image.open(self.logo_path)
            img = img.resize((self.logo_size, self.logo_size), Image.ANTIALIAS)
            self.logo_image = ImageTk.PhotoImage(img)
            self.logo_label.config(image=self.logo_image)
        else:
            self.logo_label.config(image='')

    def update_text_area(self, text):
        self.text_area.insert(tk.END, text + "\n")

def launch_gui():
    root = tk.Tk()
    app = GUI(root)
    return app, root
