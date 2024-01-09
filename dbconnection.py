import datetime
import json
import sqlite3

class DBconnection:
    def __init__(self, db_name='products.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

def __enter__(self):
    self.conn = sqlite3.connect(self.db_name)
    self.cursor = self.conn.cursor()
    return self

def __exit__(self, exc_type, exc_value, traceback):
    if self.conn:
        self.conn.commit()
        self.conn.close()

def insert_product(self, title, image_url):
        try:
            self.cursor.execute('INSERT INTO products (title, image_url) VALUES (?, ?)', (title, image_url))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error while inserting product:", e)  # Debugging statement
            raise e

def get_all_products(self):
        try:
            self.cursor.execute('SELECT title, image_url FROM products')
            products = [{'title': title, 'image_url': image_url} for title, image_url in self.cursor.fetchall()]
            return products
        except sqlite3.Error as e:
            print("Error while retrieving products:", e)  # Debugging statement
            raise e

def get_cached_result(self, search_key):
        try:
            # Execute a query to retrieve cached results for the given search_key
            self.cursor.execute('SELECT result, timestamp FROM search_cache WHERE search_key = ?', (search_key,))
            cached_result = self.cursor.fetchone()

            if cached_result:
                cached_result_json = cached_result[0]
                timestamp_str = cached_result[1]

                # Convert the timestamp string to a datetime object
                timestamp = datetime.datetime.fromisoformat(timestamp_str)
                current_time = datetime.datetime.now()

                # Check if the cache is still valid (less than one day old)
                expiration_time = timestamp + datetime.timedelta(days=1)

                if current_time <= expiration_time:
                    # If the cache is still valid, parse the result from JSON and return
                    return json.loads(cached_result_json)
                else:
                    # If the cache has expired, remove it from the database
                    self.cursor.execute('DELETE FROM search_cache WHERE search_key = ?', (search_key,))
                    self.conn.commit()

        except sqlite3.Error as e:
            print("Error while retrieving cached result:", e)  # Debugging statement
            raise e

        return None  # Return None if no cached result found

def save_search_result(self, search_key, result):
    try:
        # Get the current timestamp
        current_time = datetime.datetime.now()

        # Insert or replace the search key, result, and timestamp into the search_cache table
        self.cursor.execute('INSERT OR REPLACE INTO search_cache (search_key, result, timestamp) VALUES (?, ?, ?)',
                            (search_key.lower(), json.dumps(result), current_time))
        self.conn.commit()
    except sqlite3.Error as e:
        print("Error while saving search result:", e)  # Debugging statement
        raise e


def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                image_url TEXT
            )
        ''')

        # Create the search_cache table with a timestamp column
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS search_cache (
                        search_key TEXT PRIMARY KEY,
                        result TEXT,
                        timestamp TIMESTAMP
                    )
                ''')

        self.conn.commit()