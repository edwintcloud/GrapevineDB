from database import Database

if __name__ == "__main__":
    d = Database()
    try:

        # print data
        print(f"{str(d)}\n")

        d.wipe()

        # migrate json file into db
        d.migrate("migrations/test_migration.json")

        # print data
        print(f"{str(d)}\n")

        # print database stats
        print(f"\n Number of nodes: {d.num_nodes}")
        print(f"\n Number of associations: {d.num_associations}")

    except Exception as e:
        print(e)
