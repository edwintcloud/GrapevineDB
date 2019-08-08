from database import Database

if __name__ == "__main__":
    d = Database()
    try:

        # remove all data for fresh start
        d.wipe()

        # add arbitrary nodes
        apple = d.insert({"Name": "Apple", "Category": "Technology"})
        the_beatles = d.insert(
            {"Name": "The Beatles", "Category": "Musician/Band"}
        )
        coca_cola = d.insert({"Name": "Coca-Cola", "Category": "Food/Drink"})

        # add users collection
        c = d.add("users")

        # add users
        mary = c.insert({"Name": "Mary", "Gender": "F", "Age": "26"})
        francis = c.insert({"Name": "Francis", "Gender": "F", "Age": "31"})
        john = c.insert({"Name": "John", "Gender": "M", "Age": "28"})

        # associate users with each other
        mary.relate_to(john, by="FRIENDS_WITH", bidirectional=True)
        mary.relate_to(francis, by="FRIENDS_WITH", bidirectional=True)

        # associate users to arbitrary nodes
        mary.relate_to(apple, by="LIKES")
        john.relate_to(coca_cola, by="LIKES")
        john.relate_to(the_beatles, by="LIKES")
        francis.relate_to(the_beatles, by="LIKES")

        # print data
        print(f"{str(d)}\n")

        # list all of Mary's friends (problem 1)
        friends_of_mary = mary.related_by("FRIENDS_WITH")
        print("Friends of Mary:")
        for friend in friends_of_mary:
            print(f"\t{friend.data['Name']}")

        # list things Mary's friends like but she doesn't yet (problem 2)
        suggested_likes = mary.related_difference("FRIENDS_WITH", "LIKES")
        print("\nMary's Friends Like These But Mary Doesn't:")
        print(
            "\n".join(
                f"\t{v} friends like {k.data['Name']}"
                for k, v in suggested_likes.items()
            )
        )

        # list friends of John's friends that are not yet friends of John
        # (problem 2)
        indirect_friends = john.related_difference(
            "FRIENDS_WITH", "FRIENDS_WITH"
        )
        print("\nJohn's friends have friends that aren't friends with John:")
        print(
            "\n".join(
                f"\t{v} friends are friends of {k.data['Name']} "
                for k, v in indirect_friends.items()
            )
        )

        # list all the associations in database by label (problem 3)
        # Friends_With: Mary -> Francis, Francis -> Mary
        # LIKES: John -> The Beatles, John -> Coca-Cola
        print("\nAssociations by label:\n")
        for label, edges in d.associations.items():
            print(label)
            for edge in edges:
                print(f"\t{edge[0].data['Name']} -> {edge[1].data['Name']}")

        # print database stats
        print(f"\n Number of nodes: {d.num_nodes}")
        print(f"\n Number of associations: {d.num_associations}")

    except Exception as e:
        print(e)
