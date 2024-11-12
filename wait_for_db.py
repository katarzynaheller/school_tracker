import time
import psycopg2
from django.db import connections
from django.db.utils import OperationalError

def wait_for_db():
    db_conn = None
    
    while not db_conn:
        try:
            db_conn = connections['default']
            db_conn.cursor()
        except OperationalError:
            print("Database not ready, waiting...")
            time.sleep(1)
        print("Connection with DB established!")


if __name__ == "__main__":
    wait_for_db()
