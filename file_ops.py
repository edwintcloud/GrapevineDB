from pickle import load, dump
from pathlib import Path
from datetime import datetime
from functools import wraps


class FileOps:
    """
    FileOps holds methods used to persist the database to a file.
    """

    def __init__(self, path="data"):
        """
        Initialize a FileOps object.

        Returns:
            (FileOps): The initialized FileOps object.
        """
        self.db_path = Path(path)
        self.nodes_path = self.db_path.joinpath("nodes.p")
        self.collections_path = self.db_path.joinpath("collections.p")
        self.nodes = {}
        self.collections = {}
        try:
            # if database file exists, load it into memory
            if not self.db_path.exists():
                self.db_path.mkdir()
                self.nodes_path.touch()
                self.collections_path.touch()
                print(f"{self.current_dt}: Database created!")
            else:
                self.nodes = load(self.nodes_path.open(mode="rb"))
                self.collections = load(self.collections_path.open(mode="rb"))
                print(f"{self.current_dt}: Database loaded from file!")

        except Exception as e:
            print(e)

    @property
    def current_dt(self):
        """
        Return the current datatime as a formatted str.

        Returns:
            (str): The current datetime as a formatted str.
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # pylint: disable=no-self-argument,not-callable,no-member
    def save_on_update(f):
        """
        Save binary representation of database objects to respective files in
        the instance db_path. This function is used as a decorator to wrap
        other functions in subclasses that inherit from FileOps.

        Returns:
            (any): The resulting return from the functon wrapped by this
            decorator.
        """

        @wraps(f)
        def wrapper(self, *args, **kwargs):
            result = f(self, *args, **kwargs)
            # after function call, save db to file
            dump(self.file.nodes, self.file.nodes_path.open(mode="wb"))
            dump(
                self.file.collections,
                self.file.collections_path.open(mode="wb"),
            )
            # print(
            #     "{}: {}.{} caused database to be saved to disk.".format(
            #         self.current_dt, type(self).__name__, f.__name__
            #     )
            # )
            return result

        return wrapper
