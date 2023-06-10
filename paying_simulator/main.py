import socket
import psycopg2


def main():
    conn = psycopg2.connect(
        database="srs_db",
        user="srs_user",
        password="srs_user",
        host="192.168.1.102",
        port="5432"
    )

    hostname = socket.gethostname()
    ipv4 = socket.gethostbyname(hostname)

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


if __name__ == "__main__":
    main()
