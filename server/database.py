import copy
import sqlite3

from password import hash_password, verify_password
from encryption import encrypt_message


class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
        self.column_cache = {}

    def get_connection(self):
        """Get the database connection."""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def close_connection(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def get_columns(self, table):
        if table not in self.column_cache:
            cursor = self.connection.cursor()
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cursor.fetchall()]
            self.column_cache[table] = columns

        return copy.deepcopy(self.column_cache[table])

    def fetch_one(self, table, where, arguments=None, exclude_columns=None):
        columns = self.get_columns(table)

        # Exclude specified column if needed
        if exclude_columns:
            if isinstance(exclude_columns, str):
                exclude_columns = [exclude_columns]

            for exclude_column in exclude_columns:
                if exclude_column in columns:
                    columns.remove(exclude_column)

        columns_str = ", ".join(columns)
        cursor = self.connection.cursor()

        cursor.execute(f"SELECT {columns_str} FROM {table} WHERE {where}", arguments)
        row = cursor.fetchone()

        return dict(zip(columns, row))

    def fetch_all(self, table, exclude_columns=None):
        columns = self.get_columns(table)

        # Exclude specified column if needed
        if exclude_columns:
            if isinstance(exclude_columns, str):
                exclude_columns = [exclude_columns]

            for exclude_column in exclude_columns:
                if exclude_column in columns:
                    columns.remove(exclude_column)

        columns_str = ", ".join(columns)
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT {columns_str} FROM {table}")
        result = cursor.fetchall()

        return [dict(row) for row in result]

    def get_user_by_login(self, email, password):
        cursor = self.connection.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        if user and verify_password(user['password'], password):
            return user

    def get_projects(self):
        return self.fetch_all('projects')

    def get_providers(self):
        return self.fetch_all('providers', ['apiKey','apiSecret'])

    def get_provider(self, provider_id):
        return self.fetch_one('providers', 'id = ?', (provider_id,))

    def get_users(self):
        return self.fetch_all('users', 'password')

    def add_project(self, name, type, provider, instance, url, version, extra):
        cursor = self.connection.cursor()

        # Insert a new record into the 'users' table
        cursor.execute('''
        INSERT INTO projects (name, type, provider, instance, url, version, extra) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, type, provider, instance, url, version, extra))

        self.connection.commit()

    def add_provider(self, name, type, api_key, api_secret):
        cursor = self.connection.cursor()

        # Insert a new record into the 'users' table
        cursor.execute('''
        INSERT INTO providers (name, type, apiKey, apiSecret) 
        VALUES (?, ?, ?, ?)
        ''', (name, type, encrypt_message(api_key), encrypt_message(api_secret)))

        self.connection.commit()

    def update_provider(self, provider_id, name, type, api_key, api_secret):
        cursor = self.connection.cursor()

        # Insert a new record into the 'users' table
        cursor.execute('''
        UPDATE providers
        SET name = ?, type = ?, apiKey = ?, apiSecret = ?
        WHERE id = ?
        ''', (name, type, encrypt_message(api_key), encrypt_message(api_secret), provider_id))

        self.connection.commit()

    def create_db(self):
        cursor = self.get_connection().cursor()

        # Check if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        table_exists = cursor.fetchone()

        if not table_exists:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                provider TEXT NOT NULL,
                instance TEXT NOT NULL,
                url TEXT NOT NULL,
                version TEXT NOT NULL,
                extra TEXT NOT NULL
            )
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS providers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                apiKey TEXT NOT NULL,
                apiSecret TEXT NOT NULL
            )
            ''')

            cursor.execute('''
            INSERT INTO users (name, email, password) 
            VALUES (?, ?, ?)
            ''', ('admin', 'admin@admin.admin', hash_password('password')))

            self.connection.commit()
            self.close_connection()
