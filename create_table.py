import psycopg2


def db_connection():
    conn = psycopg2.connect(
        host='localhost',
        password=1234,
        user='postgres',
        port=5544,
        dbname='client_data'
    )
    return conn


def create_schema():
    query = """CREATE SCHEMA IF NOT EXISTS public"""

    conn = None
    try:
        conn = db_connection()
        cur = conn.cursor()

        cur.execute(query)

        conn.commit()
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_table():

    queries = (
        """
        DROP TABLE IF EXISTS public.clients
        """,
        """
        CREATE TABLE IF NOT EXISTS public.clients (
            AGE integer,
            GENDER integer,
            EDUCATION VARCHAR(100),
            MARITAL_STATUS VARCHAR(100),
            CHILD_TOTAL smallint,
            DEPENDANTS smallint,
            SOCSTATUS_WORK_FL smallint,
            SOCSTATUS_PENS_FL smallint,
            REG_ADDRESS_PROVINCE VARCHAR(100),
            FACT_ADDRESS_PROVINCE VARCHAR(100),
            POSTAL_ADDRESS_PROVINCE VARCHAR(100),
            FL_PRESENCE_FL smallint,
            OWN_AUTO smallint,
            FAMILY_INCOME VARCHAR(100),
            PERSONAL_INCOME numeric,
            ID_CLIENT serial PRIMARY KEY NOT NULL,
            GEN_INDUSTRY VARCHAR(100),
            GEN_TITLE VARCHAR(100),
            JOB_DIR VARCHAR(100),
            WORK_TIME numeric,
            CREDIT numeric,
            TERM smallint,
            FST_PAYMENT numeric,
            LOAN_COUNT smallint,
            CLOSED_FL smallint,
            AGREEMENT_RK integer,
            TARGET smallint
        )
        """,
        """
        DROP TABLE IF EXISTS public.predictions
        """,
        """
        CREATE TABLE IF NOT EXISTS public.predictions (
            ID_CLIENT serial PRIMARY KEY NOT NULL, 
            AGREEMENT_RK integer,
            PREDICTION smallint
        )
        """)

    conn = None
    try:
        conn = db_connection()
        cur = conn.cursor()

        for query in queries:
            cur.execute(query)

        conn.commit()
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_data():
    conn = db_connection()
    cur = conn.cursor()

    sql = """
        COPY clients 
        FROM '/var/lib/postgresql/data/client_dataset_clean.csv'
        DELIMITER ','
        CSV HEADER;
    """

    cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()
    print("Data ingested successfully")


if __name__ == "__main__":
    create_schema()
    create_table()
    insert_data()



