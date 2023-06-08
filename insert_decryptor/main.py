import psycopg2


def main():
    conn = psycopg2.connect(
        database="srs_db",
        user="srs_user",
        password="srs_user",
        host="192.168.1.102",
        port="5432"
    )

    file_path = "../dist/Decryptor.exe"
    with open(file_path, "rb") as file:
        file_data = file.read()

    cur = conn.cursor()


    insert_query = "INSERT INTO Decryptors (name, data) VALUES (%s, %s)"
    file_name = "Decryptor.exe"
    cur.execute(insert_query, (file_name, file_data))

    conn.commit()

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()