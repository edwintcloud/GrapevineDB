from database import Database
from random import shuffle
from time import time as timer

if __name__ == "__main__":
    d = Database()
    try:
        times = {}
        d.wipe()

        # create 10 collections
        start = timer()
        cols = []
        for n in range(10):
            cols.append(d.add(f"collection{n}"))

        #  for each collection create 100 nodes
        nodes = []
        for col in cols:
            for n in range(100):
                nodes.append(col.insert({"num": str(n)}))
        end = timer()
        times["create nodes"] = end - start
        #  create a copy of nodes
        nodes2 = [i for i in nodes]

        # shuffles nodes2
        shuffle(nodes2)

        start = timer()
        #  create FRIENDS_OF associations
        for i in range(0, len(nodes), 10):
            try:
                nodes[i].relate_to(
                    nodes2[i], by="FRIENDS_WITH", bidirectional=True
                )
            except Exception:
                continue

        #  create LIKES associations
        for i in range(0, len(nodes), 2):
            try:
                nodes2[i].relate_to(nodes[i], by="LIKES")
            except Exception:
                continue
        end = timer()
        times["create associations"] = end - start

        # shuffles nodes
        shuffle(nodes)

        start = timer()
        # (problem 2 example)

        indirect_friends = nodes[0].related_difference(
            "FRIENDS_WITH", "FRIENDS_WITH"
        )

        name = nodes[0].data['num']
        end = timer()
        times["related difference"] = end - start
        print(
            f"\n{name} friends have friends that aren't friends with {name}:"
        )
        print(
            "\n".join(
                f"\t{v} friends are friends of {k.data['num']} "
                for k, v in indirect_friends.items()
            )
        )

        # problem 3
        start = timer()
        print("\nAssociations by label:\n")
        for label, edges in d.associations.items():
            print(label)
            for edge in edges:
                print(f"\t{edge[0].data['num']} -> {edge[1].data['num']}")
        end = timer()
        times["associations"] = end - start

        # print times
        for k, v in times.items():
            print(f"{k}: {v*1000:.2f}ms")

        # print database stats
        print(f"\n Number of nodes: {d.num_nodes}")
        print(f"\n Number of associations: {d.num_associations}")
    except Exception as e:
        print(e)
