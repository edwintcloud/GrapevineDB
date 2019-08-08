from daemoniker import Daemonizer
from database import Database
from pickle import load, dump
from pathlib import Path
from datetime import datetime
from time import sleep
import sys

db = {}


def open_db(db, db_file="data/db.p"):
    db_path = Path(db_file)
    try:
        # if database file exists, load it into memory
        if db_path.exists():
            db = load(db_path.open(mode="rb"))
            print("Database loaded from file!")
        # otherwise, create the db file
        else:
            db_path.parent.mkdir()
            db_path.touch()
            dump(db, db_path.open(mode="wb"))
            print("Database created!")
    except Exception as e:
        print(e)


with Daemonizer() as (is_setup, daemonizer):
    if is_setup:
        # This code is run before daemonization.
        open_db(db)

    # We need to explicitly pass resources to the daemon; other variables
    # may not be correct
    is_parent, db = daemonizer(
        "data/database.pid", db, stdout_goto="data/out.txt"
    )

    if is_parent:
        # Run code in the parent after daemonization
        print("ok")
    else:
        while True:
            # db = Database()
            print("Hello", file="log.txt")
            sleep(0.5)

# We are now daemonized, and the parent just exited.
# code_continues_here()
# print("bingo", file=sys.stderr)
# print("bongo")
# # db = Database()
# sleep(2)

