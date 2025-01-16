import psycopg2
import configparser
config = configparser.ConfigParser()
config.read('settings.ini')
password = config["password"]['password']

conn = psycopg2.connect(database = 'clientData', user = 'postgres', password = password)
with conn.cursor() as cur:
    cur.execute("""
        DROP TABLE IF EXISTS Numbers;
        DROP TABLE IF EXISTS Client;
            """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS Client(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(60) NOT NULL,
                last_name VARCHAR(60) NOT NULL,
                email VARCHAR(60) NOT NULL
                );           
        """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS Numbers(
                numbersid SERIAL PRIMARY KEY,
                number VARCHAR(15),
                id int not null,
                FOREIGN KEY (id) REFERENCES Client(id)
                );
        """)
    conn.commit()

conn.close()