from database import Database

if __name__ == "__main__":
    d = Database()
    try:
        d.add_collection("tests1s2")
        print(d)
        for collection_name in d.collections:
            d.remove_collection(collection_name)
        print(d)
        d.add_collection("users")
        result1 = d.insert(
            "users", {"name": "edwin", "email": "swewd@gmail.com"}
        )
        result2 = d.insert("users", {"name": "cloud", "email": "jj@gmail.com"})
        print("User1: {}".format(d.get("users", result1["id"])))
        print("User2: {}".format(d.get("users", result2["id"])))
        d.associate("users", result1["id"], result2["id"], "likes")
    except Exception as e:
        print(e)
