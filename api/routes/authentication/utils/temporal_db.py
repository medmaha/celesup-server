import os
import sqlite3
import random
from cryptography.fernet import Fernet

from pathlib import Path

import base64

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent


class Utils:
    __env_key = os.getenv("FERNET_SECRET_KEY")
    __fernet_key = bytes(f"{__env_key}==", "utf-8")
    crypto = Fernet(__fernet_key)

    def valid_lookup_field(self, **kwargs):
        if "code" in kwargs:
            return "code", kwargs["code"]
        elif "cookie_id" in kwargs:
            return "cookie_id", kwargs["cookie_id"]
        else:
            return

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

    def encrypt_crypto_str(self, value):
        value = value.encode("utf-8")
        val = self.crypto.encrypt(value)
        return val.decode()

    def decode_crypto_str(self, value):
        value = value.encode("utf-8")
        val = self.crypto.decrypt(value)
        return val.decode()

    def create_cookie_id(self):
        return Fernet.generate_key().decode()


class DB(Utils):
    """
    A utility class for storing user data for validation process to take place,
    before finally storing the user data into the USER model.
    """

    connection = sqlite3.connect(
        os.path.join(BASE_DIR, "api/routes/authentication/utils/DUMMY_USERS.db"),
        check_same_thread=False,
    )

    db_query = connection.cursor()

    def __init__(self, table_name=None):
        self.table = table_name.lower()

        if table_name:
            self.get_or_create_table()

    def get_or_create_table(self):
        try:
            with self.connection:
                self.db_query.execute(f""" Select * FROM {self.table}""")
            return True
        except:
            created = self.create_table()
            if created:
                return True

    def create_table(self):
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
                        username VARCHAR(50),
                        password TEXT,
                        user_type TEXT,
                        code TEXT,
                        cookie_id TEXT NULL,
                        mailed BOOLEAN DEFAULT(FALSE),
                        is_logged_in BOOLEAN DEFAULT(FALSE)

                    ) """
                )
            return True
        except:
            return

    def alter_table(self, **kwargs):
        pass

    def drop_table(self, **kwargs):
        """Drops database table if table_name is valid"""
        try:
            with self.connection:
                self.db_query.execute(f"DROP TABLE {self.table}")
            self.table = None
            return True
        except:
            return

    def add(self, **kwargs):
        """Adds a temporally record to the database for validation process, password and email are encrypted"""

        # encrypting client password
        password = kwargs["password"]
        kwargs["password"] = self.encrypt_crypto_str(password)

        # encrypting client email
        email = kwargs["email"]
        kwargs["email"] = self.encrypt_crypto_str(email)

        code = self.get_email_code()

        with self.connection:
            self.db_query.execute(
                f""" INSERT INTO {self.table} (code) values("{code}") """
            )

        for column in kwargs:
            self.update(column, kwargs[column], ("code", code))

        kwargs["code"] = code
        return kwargs

    def get(self, **kwargs):
        """Gets a single record from the given database table_name with the password and email is encrypted"""

        lookup = self.valid_lookup_field(**kwargs)
        if not lookup:
            return
        with self.connection:
            data = self.db_query.execute(
                f""" SELECT email, username, code, cookie_id, mailed FROM {self.table} WHERE {lookup[0]}=:lookup """,
                {"lookup": lookup[1]},
            )
            data = data.fetchone()
            if data:
                data = [*data]
                return {
                    "email": self.decode_crypto_str(data[0]),
                    "username": data[1],
                    "code": data[2],
                    "cookie_id": data[3],
                    "mailed": bool(data[4]),
                    "state": "unverified",
                }

    def delete(self, **kwargs):
        "Deletes a single record from the giving db table \n Expecting a (email and code) arguments"
        lookup = self.valid_lookup_field(**kwargs)
        if not lookup:
            return

        with self.connection:
            cursor = self.db_query.execute(
                f""" DELETE FROM {self.table} WHERE  code=:code""",
                {lookup[0]: lookup[1]},
            )
            return True

    def update(self, column, value, lookup):
        with self.connection:
            self.db_query.execute(
                f""" UPDATE {self.table} SET {column}=:value WHERE {lookup[0]}=:lookup """,
                {"value": value, "lookup": lookup[1]},
            )

    def exists(self, **kwargs):
        lookup = self.valid_lookup_field(**kwargs)
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

    def get_email_code(self) -> str:
        """Create a random 7 (seven) digit numbers\n * Returns the stringified version"""

        c_num = random.randrange(100000, 900000)

        code = f"C-{c_num}"

        print(code)

        return code

    def get_auth_response_json(map, state="unverified"):
        if map:
            data = {
                "email": map.get("email"),
                "username": map.get("username"),
                "mailed": map.get("username"),
                "state": state,
            }
        return data


class Database(DB):
    def __init__(self, table_name=None):
        super().__init__(table_name)
        self.object = DB(table_name)

    def __login(self, email, password):
        code = None
        with self.connection:
            items = self.db_query.execute(
                "SELECT email, password, code from {}".format(self.table)
            )
            for item in items.fetchall():
                _email = self.decode_crypto_str(item[0])
                _password = self.decode_crypto_str(item[1])
                if email == _email and password == _password:
                    code = item[2]
                    break
                else:
                    continue
        return code

    def authenticate(self, email, password):
        auth_code = self.__login(email, password)
        acid = self.create_cookie_id()
        if auth_code:
            lookup = (
                "code",
                auth_code,
            )
            self.update("is_logged_in", int(True), lookup)
            self.update("cookie_id", acid, lookup)
            return acid

    def is_authenticated(self, cookie_id):
        auth = False
        with self.connection:
            query = self.db_query.execute(
                f"SELECT * FROM {self.table} WHERE is_logged_in=:status AND cookie_id=:cookie",
                {"status": True, "cookie": cookie_id},
            )
            if query.fetchone():
                auth = True

        return auth

    def un_authenticate(self, cookie_id):
        if self.exists(cookie_id=cookie_id):
            lookup = ("cookie_id", cookie_id)
            self.update("is_logged_in", int(False), lookup)
            self.update("cookie_id", None, lookup)
            return True
        return False

    def update_code(self, **kwargs):
        lookup = self.valid_lookup_field(**kwargs)

        if self.exists(**kwargs):
            code = self.get_email_code()
            self.update("code", code, lookup)
            return code

    def get_raw_data(self, **kwargs):
        """GET raw for data submitted by the user. To create a new user model"""

        lookup = self.valid_lookup_field(**kwargs)

        with self.connection:
            data = self.db_query.execute(
                f""" SELECT email, username, password, user_type FROM {self.table} WHERE {lookup[0]}=:lookup """,
                {"lookup": lookup[1]},
            )
            user = data.fetchone()

            data = {
                "email": user[0],
                "username": user[1],
                "password": user[2],
                "user_type": user[3],
            }

            # decrypting client password
            password = data["password"]
            decrypted_password = self.crypto.decrypt(password).decode()
            data["password"] = decrypted_password

            # decrypting client address
            email = data["email"]
            decrypted_email = self.crypto.decrypt(email).decode()
            data["email"] = decrypted_email

            return data
