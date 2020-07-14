import datetime
import os
from pathlib import Path

import paramiko
import pytz
import schedule
from termcolor import colored

# Database server
DB_HOSTNAME = os.getenv("DB_HOSTNAME", "localhost")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Other server
HOSTNAME = os.getenv("HOSTNAME")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

BACKUP_KEY_PUB_FILE = os.getenv("BACKUP_KEY_PUB_FILE")
TIME_ZONE = os.getenv("TIME_ZONE", "Europe/Moscow")

DB_FILENAME = "/tmp/backup_db.sql.gz.enc"


def say_hello():
    print(colored("Hi! This tool will dump PostgreSQL database, compress \n"
                  "and encode it, and then send to other server.\n", "cyan"))


def get_now_datetime_str():
    now = datetime.datetime.now(pytz.timezone(TIME_ZONE))
    return now.strftime('%Y-%m-%d__%H-%M-%S')


def check_key_file_exists():
    if not Path(BACKUP_KEY_PUB_FILE).is_file():
        exit(
            f"\U00002757 Public encrypt key ({BACKUP_KEY_PUB_FILE}) "
            f"not found. If you have no key – you need to generate it. "
            f"You can find help here: "
            f"https://www.imagescape.com/blog/2015/12/18/encrypted-postgres-backups/"
        )


def dump_database():
    print("\U0001F4E6 Preparing database backup started")
    dump_db_operation_status = os.WEXITSTATUS(os.system(
        f"pg_dump -h {DB_HOSTNAME} -U {DB_USER} {DB_NAME} -P {DB_PASSWORD} | gzip -c --best | \
        openssl smime -encrypt -aes256 -binary -outform DEM \
        -out {DB_FILENAME} {BACKUP_KEY_PUB_FILE}"
    ))
    if dump_db_operation_status != 0:
        exit(f"\U00002757 Dump database command exits with status "
             f"{dump_db_operation_status}.")
    print("\U0001F510 DB dumped, archieved and encoded")


def upload_dump_to_server():
    print("\U0001F4C2 Starting upload to Object Storage")
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOSTNAME, username=USERNAME, password=PASSWORD)

    ftp_client = ssh.open_sftp()
    ftp_client.put(DB_FILENAME, f'/share/privobdump/db-{get_now_datetime_str()}.sql.gz.enc')
    ftp_client.close()

    ssh.close()

    print("\U0001f680 Uploaded")


def remove_temp_files():
    os.remove(DB_FILENAME)
    print(colored("\U0001F44D That's all!", "green"))


def create_backup():
    say_hello()
    check_key_file_exists()
    dump_database()
    upload_dump_to_server()
    remove_temp_files()


schedule.every().day.at("10:30").do(create_backup)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
