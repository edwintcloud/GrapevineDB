from pickle import load, dump
from pathlib import Path
from datetime import datetime
from functools import wraps


class Database:
    def __init__(self, db_file="data/db.p"):
        self.db_path = Path(db_file)
        self.db = {}
        try:
            # if database file exists, load it into memory
            if self.db_path.exists():
                self.db = load(self.db_path.open(mode="rb"))
                print(f"{self._current_dt}: Database loaded from file!")
            # otherwise, create the db file
            else:
                self.db_path.parent.mkdir()
                self.db_path.touch()
                dump(self.db, self.db_path.open(mode="wb"))
                print(f"{self._current_dt}: Database created!")
        except Exception as e:
            print(e)

    def __str__(self):
        return str(self.db)

    def __iter__(self):
        return iter(self.db.items())

    @property
    def collections(self):
        return list(self.db.keys())

    @property
    def _current_dt(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # pylint: disable=no-self-argument,not-callable,no-member
    def _save_on_update(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            result = f(self, *args, **kwargs)
            # after function call, save db to file
            dump(self.db, self.db_path.open(mode="wb"))
            print(
                "{}: {} caused database to be saved to disk.".format(
                    self._current_dt, f.__name__
                )
            )
            return result

        return wrapper

    @_save_on_update
    def add_collection(self, collection_name):

        # collection name must be at least 6 characters
        if len(collection_name) < 6:
            raise Exception(
                "collection name must be at least 6 characters in length"
            )

        # collection must not already exist
        if collection_name in self.db:
            raise Exception("collection already exists in database")

        # create the collection
        self.db[collection_name] = {}

    @_save_on_update
    def remove_collection(self, collection_name):

        # collection must exist in db
        if collection_name not in self.db:
            raise Exception("collection not found in database")

        # remove the collection
        del self.db[collection_name]
