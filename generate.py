####
# A little hack that generates treemap data (suitable for visualization in D3.js)
# from the value size of Redis string keys
####

config = {
    "host": "localhost",
    "port": 6379,
    "db": 0
}


import redis
import json


class TreeMapper(object):

    def connect(self):
        self.redis = redis.StrictRedis(host=config["host"], port=config["port"], db=config["db"])
        return self.redis

    def getSize(self, key):
        if self.redis.type(key) != 'string':
            # TODO: get something for these sizes somehow
            return 0

        return self.redis.strlen(key)

    # probably important TODO: use SCAN instead of KEYS
    # also TODO: recurse into hashes / lists
    def getAllKeys(self):
        return self.redis.keys("*")

    def updateTree(self, key, size):
        if type(self.tree) is not dict:
            # TODO: something more sensible
            raise RuntimeError

        segments = key.split(":")

        # relies on Python passing dicts by reference
        parent = self.tree

        for i, name in enumerate(segments):
            # first, check the parent and see if it has a matching child at this level
            new_child = None

            for child in parent['children']:
                if child['name'] == name:
                    new_child = child

            if new_child is None:
                new_child = {
                    "name": name,
                    "children": []
                }

                if i+1 == len(segments):
                    new_child["value"] = 0
                else:
                    new_child["children"] = []

                # insert into parent's list of children, and assume length matches the index
                parent['children'].append(new_child)

            # if the second-last item (the parent of the item which gets the value) already has a value
            # instead of children, create a new child with that value so it displays properly in the tree
            # (covers the case where both foo:bar and foo:bar:baz are valid Redis keys)
            # TODO: figure out a better way to display this
            if i+1 == len(segments) and "value" in new_child:
                new_child["children"] = []
                new_child["children"].append({
                    "name": "main_key",
                    "value": new_child["value"]
                })
                del new_child["value"]

            # having set up new_child, continue iterating (and TODO: rename these things)
            parent = new_child

        # at the end of that loop, parent should refer to the leaf element
        # representing this item; set the item's value and we're done
        parent["value"] = size

    def loopy(self):
        self.tree = {
            "name": "redis_keys",
            "children": []
        }

        self.connect()

        keys = self.getAllKeys()

        for key in keys:
            size = self.getSize(key)
            self.updateTree(key, size)

        return self.tree


if __name__ == "__main__":
    t = TreeMapper()
    output = t.loopy()

    with open("data.json", "w+") as f:
        json.dump(output, f)

