import os
import getpass as gt

def main():
    username = gt.getuser()
    directories = [f'C:\\Users\\{username}\\Desktop', f'C:\\Users\\{username}\\Documents']

    for directory in directories:
        print(directory)

if __name__ == "__main__":
    main()