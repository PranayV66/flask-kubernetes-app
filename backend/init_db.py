import psycopg2
import os

def init_db():
    conn = psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST', 'localhost'),
        database=os.environ.get('POSTGRES_DB', 'mydb'),
        user=os.environ.get('POSTGRES_USER', 'user'),
        password=os.environ.get('POSTGRES_PASSWORD', 'password')
    )
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            value INTEGER NOT NULL
        );
    ''')
    cur.execute('DELETE FROM items;')
    cur.execute('INSERT INTO items (name, value) VALUES (%s, %s);', ('Item 1', 100))
    cur.execute('INSERT INTO items (name, value) VALUES (%s, %s);', ('Item 2', 200))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    init_db()
