class WalkDFS:

    @staticmethod
    def are_connected(start, end, graph):
        visited = set()
        queue = []
        path_to = {}
        queue.append(start)
        visited.add(start)
        path_to[start] = None
        found = False

        while len(queue) != 0:
            current_node = queue.pop(0)
            if current_node == end:
                found = True
                return found

            for neighbour in graph[current_node]:
                if neighbour not in visited:
                    path_to[neighbour] = current_node
                    visited.add(neighbour)
                    queue.append(neighbour)
        return False
