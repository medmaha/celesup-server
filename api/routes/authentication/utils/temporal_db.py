import os
import sqlite3
import random
from tokenize import cookie_re
from cryptography.fernet import Fernet

from pathlib import Path

import base64

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent


class Utils:
    __env_key = os.getenv("FERNET_SECRET_KEY")
    __fernet_key = bytes(f"{__env_key}==", "utf-8")
    crypto = Fernet(__fernet_key)

    def get_lookup_fields(self, **kwargs):
        key = kwargs.get("key")
        value = kwargs.get("value")

        return key, value

    def validate_table_name(func):
        """a designed decorator for verifying table_name
        argument in kwargs param and the self.table attribute
        return none if both are none
        """

        def wrapper(self, *args, **kwargs):
            if not self.table and not kwargs.get("table_name"):
                print("\nprovide a table name\n")
                return

            if kwargs.get("table_name"):
                self.table = kwargs["table_name"]
            return func(self, *args, **kwargs)

        return wrapper

    def encrypt_crypto_str(self, value: str):
        "* Encodes a string to byte string"
        value = value.encode("utf-8")
        val = self.crypto.encrypt(value)
        return val.decode()

    def decode_crypto_str(self, value: bytes):
        "* Decodes a bytes to string"
        value = value.encode("utf-8")
        val = self.crypto.decrypt(value)
        return val.decode()

    def create_cookie(self):
        cookie_id = Fernet.generate_key().decode()
        cookie_id = cookie_id.replace("-", "")
        cookie_id = cookie_id.replace("=", "")
        return cookie_id

    def get_dictionary_obj(self, obj):
        dictionary = []

        for key, value in zip(DB_TABLE_ROWS, obj):
            dictionary.append((key, value))

        dictionary = dict(dictionary)

        return dictionary

    def get_raw_data(self, data: dict):
        encrypted_strings = ["email", "phone", "password"]

        for key, value in data.items():
            if not key in encrypted_strings:
                continue

            if value:
                data[key] = self.decode_crypto_str(value)

        return data

    def get_verification_code(self) -> str:
        """Create a random 4 (four) digit numbers\n* Returns the stringified version of it"""

        code = random.randrange(10000, 90000)

        print(code)
        return code


class DB(Utils):
    """
    A utility class for storing user data for validation process to take place,
    before finally storing the user data into the USER model.
    """

    connection = sqlite3.connect(
        os.path.join(BASE_DIR, "api/routes/authentication/UNVERIFIED_ACCOUNTS.db"),
        check_same_thread=False,
    )

    db_query = connection.cursor()

    def __init__(self, table_name=None):
        table_name = table_name or "verification_db"
        self.table = "verification_db"

        self.init()

    def init(self):
        try:
            with self.connection:
                self.db_query.execute(f""" Select * FROM {self.table}""")
            return True
        except:
            created = self.initialize_table()
            if created:
                return True

    def initialize_table(self):
        """Specifically design to create a database table.
        For a temporal record storage of signing up clients,
        with the intention to delete record after validation process.
        """
        try:
            with self.connection:
                self.db_query.execute(
                    f""" Create Table {self.table} (
                        id INTEGER NOT NULL PRIMARY KEY,
                        email TEXT,
                        username VARCHAR(50) NULL,
                        password TEXT NULL,
                        account_type TEXT,
                        code TEXT,
                        cookie_id TEXT NULL,
                        phone TEXT NULL,
                        mailed BOOLEAN DEFAULT(FALSE),
                        is_logged_in BOOLEAN DEFAULT(FALSE)
                    ) """
                )
            return True
        except:
            return

    def retrieve(self, lookup: dict, **kwargs):
        """Gets a single record from the given database table_name with the password and email is encrypted"""
        lookup = self.get_lookup_fields(**lookup)
        if lookup:
            with self.connection:
                data = self.db_query.execute(
                    f""" SELECT * FROM {self.table} WHERE {lookup[0]}=:lookup """,
                    {"lookup": lookup[1]},
                )
                data = data.fetchone()
                data = self.get_dictionary_obj(data)

                RAW_DATA = kwargs.get("raw") is not None

                if len(data) == len(DB_TABLE_ROWS) and not RAW_DATA:
                    return data

                if RAW_DATA and len(data) == len(DB_TABLE_ROWS):
                    return self.get_raw_data(data)

    def delete(self, lookup: dict):
        "Deletes a single record from the giving db table \n Expecting a (email and code) arguments"
        lookup = self.get_lookup_fields(**lookup)
        if not lookup:
            return

        with self.connection:
            self.db_query.execute(
                f""" DELETE FROM {self.table} WHERE  {lookup[0]}=:lookup""",
                {"lookup": lookup[1]},
            )
            return True

    def update(self, column: str, value: str, lookup: dict):
        lookup = self.get_lookup_fields(**lookup)
        if not lookup:
            raise ValueError("Invalid lookup parameter provided")

        with self.connection:
            self.db_query.execute(
                f""" UPDATE {self.table} SET {column}=:value WHERE {lookup[0]}=:lookup """,
                {"value": value, "lookup": lookup[1]},
            )

    def exists(self, lookup: dict):
        lookup = self.get_lookup_fields(**lookup)
        if not lookup:
            return
        self.db_query.execute(
            f""" 
                SELECT * FROM {self.table} WHERE {lookup[0]}=:lookup
            """,
            {"lookup": lookup[1]},
        )
        data = self.db_query.fetchall()
        return bool(len(data))

    def insert(self, field: str, value: str, lookup: dict | None = None):

        if lookup and self.exists(lookup):
            client = self.retrieve(lookup)

            return client.get("cookie_id")

        if field in ["email", "password", "phone"]:
            value = self.encrypt_crypto_str(value)

        with self.connection:
            cookie_id = self.create_cookie()
            self.db_query.execute(
                f""" INSERT INTO {self.table} ({field}, cookie_id) values("{value}", "{cookie_id}")"""
            )
            return cookie_id


class Database(DB):
    def __init__(self, table_name=None):
        super().__init__(table_name)
        self.object = DB(table_name)

    def __login(self, email: str, password: str):
        cookie_id: str | None = None
        with self.connection:
            items = self.db_query.execute(
                "SELECT email, password, cookie_id from {}".format(self.table)
            )
            for item in items.fetchall():
                if item[0] and item[1]:
                    _email = self.decode_crypto_str(item[0])
                    _password = self.decode_crypto_str(item[1])
                    if email == _email and password == _password:
                        cookie_id = item[2]
                        break
                    continue

        return cookie_id

    def authenticate(self, email: str, password: str):
        cookie_id = self.__login(email, password)
        if cookie_id:
            lookup = {"key": "cookie_id", "value": cookie_id}
            user = self.retrieve(lookup, raw=True)
            data = {"username": user["username"], "name": "", "cookie_id": cookie_id}
            self.update("is_logged_in", int(True), lookup)
            return data

    def is_authenticated(self, cookie_id: str):
        auth = False
        with self.connection:
            query = self.db_query.execute(
                f"SELECT * FROM {self.table} WHERE is_logged_in=:status AND cookie_id=:cookie",
                {"status": True, "cookie": cookie_id},
            )
            if query.fetchone():
                auth = True

        return auth

    def un_authenticate(self, cookie_id: str):
        if self.exists({"key": "cookie_is", "value": cookie_id}):
            lookup = {"key": "cookie_id", "value": cookie_id}
            self.update("is_logged_in", int(False), lookup)
            self.update("cookie_id", None, lookup)
            return True
        return False

    def update_code(self, lookup: dict):
        lookup = self.get_lookup_fields(**lookup)

        if self.exists(lookup):
            code = self.get_verification_code()
            self.update("code", code, lookup)
            return code


DB_TABLE_ROWS = (
    "id",
    "email",
    "username",
    "password",
    "account_type",
    "code",
    "cookie_id",
    "phone",
    "mailed",
    "is_logged_in",
)
