class HashTable:
    def __init__(self):
        self.table = [[] for _ in range(10)]

    def get_hash(self, key):
        h = 0
        for i in key:
            h += ord(i)
        return h % len(self.table)

    def add(self, key, value):
        h = self.get_hash(key)
        for idx, elem in enumerate(self.table):
            if len(elem) == 2 and elem[0] == key:
                self.table[h][idx] = (key, value)
                return
        self.table[h].append((key, value))

    def get(self, key):
        h = self.get_hash(key)
        for elem in self.table[h]:
            if elem[0] == key:
                return elem[1]

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        return self.add(key, value)
