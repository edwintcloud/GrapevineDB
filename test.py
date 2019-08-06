from database import Database

if __name__ == "__main__":
    d = Database()
    try:
        d.add_collection("tests1s2")
        print(d)
        for collection_name in d.collections:
            d.remove_collection(collection_name)
        print(d)
    except Exception as e:
        print(e)
