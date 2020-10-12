import os
import socket
from pathlib import Path

import psycopg2
from termcolor import colored

DB_HOSTNAME = os.getenv("DB_HOSTNAME", "localhost")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

BACKUP_KEY_PRIVATE_FILE = os.getenv("BACKUP_KEY_PRIVATE_FILE")
DB_FILENAME = os.getenv("DB_FILENAME")

connection = psycopg2.connect(
    f"dbname={DB_NAME} user={DB_USER} host='{DB_HOSTNAME}' password={DB_PASSWORD}")
cursor = connection.cursor()


def say_hello():
    print(colored(
        "This tool will get last database backup, \n"
        "decompress and unzip it, and then load to local database \n",
        "cyan"))


def check_hostname():
    hostname = socket.gethostname()
    if not hostname.startswith('loader-') and not hostname.endswith('.local'):
        exit(f"\U00002757 It seems this is not loader server "
             f"({colored(hostname, 'red')}), exit.")
    print(colored("We are on some loader or local server, ok\n", "green"))


def check_key_file_exists():
    if not Path(BACKUP_KEY_PRIVATE_FILE).is_file():
        exit(
            f"""\U00002757 Private encrypt key ({BACKUP_KEY_PRIVATE_FILE}) "
            "not found. You can find help here: "
            "https://www.imagescape.com/blog/2015/12/18/encrypted-postgres-backups/"""
        )


def unencrypt_database():
    operation_status = os.WEXITSTATUS(os.system(
        f"""openssl smime -decrypt -in {DB_FILENAME} -binary \
            -inform DEM -inkey {BACKUP_KEY_PRIVATE_FILE} \
            -out /tmp/db.sql.gz"""
    ))
    if operation_status != 0:
        exit(f"\U00002757 Can not unecrypt db file, status "
             f"{operation_status}.")
    print(f"\U0001F511 Database unecnrypted")


def unzip_database():
    _silent_remove_file("/tmp/db.sql")
    operation_status = os.WEXITSTATUS(os.system(
        f"""gzip -d /tmp/db.sql.gz"""
    ))
    if operation_status != 0:
        exit(f"\U00002757 Can not unecrypt db file, status "
             f"{operation_status}.")
    print(f"\U0001F4E4 Database unzipped")


def clear_database():
    tables = _get_all_db_tables()
    if not tables:
        return
    with connection:
        with connection.cursor() as local_cursor:
            local_cursor.execute("\n".join([
                f'drop table if exists "{table}" cascade;'
                for table in tables]))
    print(f"\U0001F633 Database cleared")


def load_database():
    print(f"\U0001F4A4 Database load started")
    operation_status = os.WEXITSTATUS(os.system(
        f"""psql -h {DB_HOSTNAME} -U {DB_USER} {DB_NAME} < /tmp/db.sql"""
    ))
    if operation_status != 0:
        exit(f"\U00002757 Can not load database, status {operation_status}.")
    print(f"\U0001F916 Database loaded")


def remove_temp_files():
    _silent_remove_file(DB_FILENAME)
    print(colored("\U0001F44D That's all!", "green"))


def _get_all_db_tables():
    cursor.execute("""SELECT table_name FROM information_schema.tables
                      WHERE table_schema = 'public' order by table_name;""")
    results = cursor.fetchall()
    tables = []
    for row in results:
        tables.append(row[0])
    return tables


def _silent_remove_file(filename: str):
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    say_hello()
    check_hostname()
    check_key_file_exists()
    unencrypt_database()
    unzip_database()
    clear_database()
    load_database()
    remove_temp_files()
