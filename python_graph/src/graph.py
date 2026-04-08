from collections import deque

class Graph:
    def __init__(self):
        self._vertex_ids = set()

        # Maps vertex_id to a dictionary of {target: cost}
        self._out_edges = {}
        # Maps vertex_id to a dictionary of {source: cost}
        self._in_edges = {}
        # Maps (source_id, vertex_id) to a cost
        self._edge_info = {}

    @property
    def vertex_count(self):
        return len(self._vertex_ids)

    @property
    def edge_count(self):
        return len(self._edge_info)

    def vertex_iterator(self):
        return iter(self._vertex_ids)

    def edge_info_iterator(self):
        for (source_vertex_id, target_vertex_id), cost in self._edge_info.items():
            yield source_vertex_id, target_vertex_id, cost

    def get_edge_cost(self, source_vertex_id: int, target_vertex_id: int) -> int:
        if source_vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid source vertex id!")
        if target_vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid target vertex id!")

        if (source_vertex_id, target_vertex_id) not in self._edge_info:
            raise ValueError("ERROR: Edge doesn't exist")

        return self._edge_info[(source_vertex_id, target_vertex_id)]

    def get_id_degree(self, vertex_id: int) -> int:
        if vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid vertex id!")
        return len(self._in_edges[vertex_id])

    def get_out_degree(self, vertex_id: int) -> int:
        if vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid vertex id!")
        return len(self._out_edges[vertex_id])

    def ingoing_edge_iterator(self, vertex_id: int):
        if vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid vertex id!")
        return iter(self._in_edges[vertex_id])

    def outgoing_edge_iterator(self, vertex_id: int):
        if vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid vertex id!")
        return iter(self._out_edges[vertex_id])

    def set_edge_cost(self, source_vertex_id, target_vertex_id, new_cost: int) -> None:
        if source_vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid source vertex id!")
        if target_vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid target vertex id!")
        if (source_vertex_id, target_vertex_id) not in self._edge_info:
            raise ValueError("ERROR: Edge doesn't exist")

        self._edge_info[(source_vertex_id, target_vertex_id)] = new_cost

    def add_edge(self, source_vertex_id: int, target_vertex_id: int, cost: int) -> None:
        if source_vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid source vertex id!")
        if target_vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid target vertex id!")
        if (source_vertex_id, target_vertex_id) in self._edge_info:
            raise ValueError("ERROR: Edge already exist")

        self._out_edges[source_vertex_id][target_vertex_id] = cost
        self._in_edges[target_vertex_id][source_vertex_id] = cost

        self._edge_info[(source_vertex_id, target_vertex_id)] = cost

    def remove_edge(self, source_vertex_id, target_vertex_id) -> None:
        if source_vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid source vertex id!")
        if target_vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid target vertex id!")
        if (source_vertex_id, target_vertex_id) not in self._edge_info:
            raise ValueError("ERROR: Edge doesn't exist")

        del self._out_edges[source_vertex_id][target_vertex_id]
        del self._in_edges[target_vertex_id][source_vertex_id]

        del self._edge_info[(source_vertex_id, target_vertex_id)]

    def add_vertex(self, vertex_id: int):
        if vertex_id in self._vertex_ids:
            raise ValueError("ERROR: Vertex already exist")

        self._vertex_ids.add(vertex_id)
        self._out_edges[vertex_id] = dict()
        self._in_edges[vertex_id] = dict()

    def remove_vertex(self, vertex_id: int):
        if vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Vertex doesn't exist")

        for v_id in self._in_edges[vertex_id]:
            del self._out_edges[v_id][vertex_id]
            del self._edge_info[(v_id, vertex_id)]

        for v_id in self._out_edges[vertex_id]:
            del self._in_edges[v_id][vertex_id]
            del self._edge_info[(vertex_id, v_id)]

        del self._out_edges[vertex_id]
        del self._in_edges[vertex_id]

        self._vertex_ids.remove(vertex_id)

    def save_graph(self, file_name: str):
        lines = [f"{self.vertex_count} {len(self._edge_info)}\n"]
        for (source_vertex_id, target_vertex_id), cost in self._edge_info.items():
            lines.append(f"{source_vertex_id} {target_vertex_id} {cost}\n")
        with open(file_name, 'w') as f:
            f.writelines(lines)


    def load_graph(self, file_name: str):
        try:
            with open(file_name, 'r') as f:
                header = f.readline().strip()
                lines = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_name} is not found")

        self.clear_graph()

        for line in lines:
            parts = line.split()
            if parts[0] not in self._vertex_ids:
                self.add_vertex(int(parts[0]))
            if parts[1] not in self._vertex_ids:
                self.add_vertex(int(parts[1]))

            self.add_edge(int(parts[0]), int(parts[1]), int(parts[2]))

        header_parts = header.split()
        if int(header_parts[0]) != len(self._vertex_ids):
            raise ValueError("ERROR: Couldn't load right number of vertexes")
        if int(header_parts[1]) != len(self._edge_info):
            raise ValueError("ERROR: Couldn't load right number of edges")

    def clear_graph(self):
        self._vertex_ids = set()
        self._out_edges = {}
        self._in_edges = {}
        self._edge_info = {}


    def copy(self):
        new_graph = Graph()

        for vertex_id in self.vertex_iterator():
            new_graph.add_vertex(vertex_id)

        for (source_vertex_id, target_vertex_id), cost in self._edge_info.items():
            new_graph.add_edge(source_vertex_id, target_vertex_id, cost)

        return new_graph

    def bfs(self, source_vertex_id, target_vertex_id):
        if source_vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid source vertex id!")
        if target_vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid target vertex id!")
        visited = {target_vertex_id}
        queue = deque([target_vertex_id])

        parent = {target_vertex_id: None}

        while len(queue) != 0:
            vertex_id = queue.pop()
            if vertex_id == source_vertex_id:
                break
            for v in self.ingoing_edge_iterator(vertex_id):
                if v in visited:
                    continue
                parent[v] = vertex_id
                queue.appendleft(v)
                visited.add(v)

        if source_vertex_id not in parent:
            return None

        path = []
        v = source_vertex_id
        while v is not None:
            path.append(v)
            v = parent[v]

        return path

