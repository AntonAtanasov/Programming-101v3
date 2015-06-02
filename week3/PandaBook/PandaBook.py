import json


class PandaAlreadyThere(Exception):
    pass


class PandasAlreadyFriends(Exception):
    pass


class Panda:

    def __init__(self, name, email, gender):
        self.name = name
        self.email = email
        self.gender = gender.lower()

    def __str__(self):
#       message = "Profile for {} ({}). For contacts : {}"
        return "{} - {} - {}".format(self.name, self.gender, self.email)

    def __eq__(self, other):
        return self.name == other.name and self.email == other.email and\
            self.gender == other.gender

    def __repr__(self):
        return "Panda('{}', '{}', '{}')".format(
            self.name(), self.email(), self.gender())

    def to_json(self):
        return self.__repr__()

    def name(self):
        return self.__name

    def email(self):
        return self.__email

    def gender(self):
        return self.__gender

    def isMale(self):
        return self.gender == "male"

    def isFemale(self):
        return self.gender == "female"

    def __hash__(self):
        return hash(self.__str__())


class SocialNetwork:

    def __init__(self, panda):
        self.panda = panda
        self.network = {}

    def __str__(self):
        return str(self.network)

    def __repr__(self):
        return json.dumps(self.network, sort_keys=True)

    def add_panda(self, panda):
        if panda in self.network:
            raise PandaAlreadyThere
        else:
            self.network[panda] = []

    def has_panda(self, panda):
        return panda in self.network

    def make_friends(self, panda, other):
        if self.are_friends(panda, other):
            raise PandasAlreadyFriends

        if not self.has_panda(panda):
            self.add_panda(panda)

        if not self.has_panda(other):
            self.add_panda(other)

        else:
            self.network[panda].append(other)
            self.network[other].append(panda)

    def are_friends(self, panda, other):
        if panda not in self.network or other not in self.network:
                return False
        return panda in self.network[other] and other in self.network[panda]

    def friends_of(self, panda):
        values = self.network[panda]
        if panda in self.network:
            return values
        else:
            return False

    def panda_connections(self, panda):
        print(self.network)
        connections = {}
        q = []
        visited = set()

        q.append((0, panda))
        visited.add(panda)

        while len(q) != 0:
            panda_data = q.pop(0)
            current_level = panda_data[0]
            current_node = panda_data[1]
            print(current_node)
            connections[current_node] = current_level

            for neighbour in self.network[current_node]:
                # print(neighbour)
                if neighbour not in visited:
                    visited.add(neighbour)
                    q.append((current_level + 1, neighbour))

        return connections

    def connection_level(self, panda, other):
        panda_table = self.panda_connections(panda)

        if other not in panda_table:
            return -1

        return panda_table[other]

    def genders_in_network(self, level, gender, panda):
        panda_table = self.panda_connections(panda)
        counter = 0

        for panda in panda_table:
            p_level = panda_table[panda]
            if p_level != 0 and p_level <= level and panda.gender() == gender:
                counter += 1
        return counter

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(self.__repr__())

    @staticmethod
    def load(filename):
        network = SocialNetwork()
        with open(filename, "r") as f:
            contents = f.read()
            json_network = json.loads(contents)

            for panda in json_network:
                for friends in json_network[panda]:
                    p1 = eval(panda)
                    p2 = eval(friends)
                    if not network.are_friends(p1, p2):
                        network.make_friends(p1, p2)
        return network

"""graph = {
    "1": ["2", "3", "5", "10"],
    "2": ["4", "1"],
    "3": ["1", "6"],
    "4": ["2", "5", "6"],
    "5": ["4", "1"],
    "6": ["3", "4", "7"],
    "7": ["6", "8"],
    "8": ["7", "9"],
    "9": ["8", "10"],
    "10": ["9", "1"],
    "11": ["12"],
    "12": ["11"]
}


def bfs(graph, start, end):
    visited = set()
    queue = []
#    path_to[x] = y
#    if we go to x through y
    path_to = {}

    queue.append(start)
    visited.add(start)
    path_to[start] = None
    found = False
    path_length = 0

    while len(queue) != 0:
        current_node = queue.pop(0)
        if current_node == end:
            return True
        for neighbour in graph[current_node]:
            if neighbour not in visited:
                path_to[neighbour] = current_node
                visited.add(neighbour)
                queue.append(neighbour)
    if found:
        while path_to[end] is not None:
            path_length += 1
            end = path_to[end]

    return path_length

result = bfs(graph, "1", "9")

print(json.dumps(result, sort_keys=True, indent=4))
"""
