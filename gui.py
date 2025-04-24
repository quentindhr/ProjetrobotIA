from tkinter import *


def launch_loading_gui():
    root = Tk()
    root.title("Chargement en cours")
    root.geometry("400x200")

    # Chargement et réduction de l'image
    photo = PhotoImage(file="Image/logo.png")
    photo_reduite = photo.subsample(8, 8)  # Réduit la taille de moitié (facteur 2)

    # Création du Label avec l'image réduite
    lbl_image = Label(root, image=photo_reduite)
    lbl_image.pack(pady=20)

    # Création du Label avec le texte "Chargement en cours..."
    lbl_text = Label(root, text="Chargement en cours...", font=("Helvetica", 16))
    lbl_text.pack(pady=10)

    return root

def close_loading_gui(root):
    root.destroy()
