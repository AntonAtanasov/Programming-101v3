from dfs import WalkDFS
import json


class DirectedGraph:

    def __init__(self):
        self.graph = {}

    def __repr__(self):
        l_graph = {}
        for keys in self.graph:
            l_graph[keys] = list(self.graph[keys])
        return json.dumps(l_graph, indent=4, sort_keys=True)

    def __str__(self):
        return self.__repr__()

    def _add_node(self, node):
        self.graph[node] = set()

    def _is_node_in_graph(self, node):
        if node in self.graph:
            return True
        return False

    def add_edge(self, node_a, node_b):
        if not self._is_node_in_graph(node_a):
            self._add_node(node_a)
        if not self._is_node_in_graph(node_b):
            self._add_node(node_b)
        if node_b not in self.graph[node_a]:
            self.graph[node_a].add(node_b)

    def get_neighbors_for(self, node):
        try:
            return self.graph[node]
        except KeyError:
            return False

    def path_between(self, node_a, node_b):
        return WalkDFS.are_connected(node_a, node_b, self.graph)
