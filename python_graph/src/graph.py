class Graph:
    def __init__(self):
        self._vertex_ids = set()
        self._edge_ids = set()

        # Maps vertex_id to a dictionary of {target: edge_id}
        self._out_edges = {}
        # Maps vertex_id to a dictionary of {source: edge_id}
        self._in_edges = {}
        # Maps edge_id to a dictionary of edge properties: {'source': v1, 'target': v2, 'cost': int}
        self._edge_info = {}

    @property
    def vertex_count(self):
        return len(self._vertex_ids)

    @property
    def vertex_iterator(self):
        return iter(self._vertex_ids)

    def get_edge(self, source_vertex_id: int, target_vertex_id: int) -> int:
        try:
            d = self._out_edges[source_vertex_id]
        except KeyError:
            raise ValueError("ERROR: Invalid source vertex id!")

        try:
            edge = d[target_vertex_id]
        except KeyError:
            raise ValueError("ERROR: Invalid target vertex id!")

        return edge

    def get_id_degree(self, vertex_id: int) -> int:
        try:
            return len(self._in_edges[vertex_id])
        except KeyError:
            raise ValueError("ERROR: Invalid vertex id!")

    def get_out_degree(self, vertex_id: int) -> int:
        try:
            return len(self._out_edges[vertex_id])
        except KeyError:
            raise ValueError("ERROR: Invalid vertex id!")

    def ingoing_edge_iterator(self, vertex_id: int):
        try:
            d = self._in_edges[vertex_id]
        except KeyError:
            raise ValueError("ERROR: Invalid vertex id!")

        return iter(d)

    def outgoing_edge_iterator(self, vertex_id: int):
        try:
            d = self._out_edges[vertex_id]
        except KeyError:
            raise ValueError("ERROR: Invalid vertex id!")

        return iter(d)

    def get_endpoints(self, edge_id) -> tuple[int, int]:
        try:
            d = self._edge_info[edge_id]
        except KeyError:
            raise ValueError("ERROR: Invalid edge id!")

        return d["source"], d["target"]

    def get_edge_cost(self, edge_id: int) -> int:
        try:
            d = self._edge_info[edge_id]
        except KeyError:
            raise ValueError("ERROR: Invalid edge id!")

        return d['cost']

    def set_edge_cost(self, edge_id: int, new_cost: int) -> None:
        try:
            d = self._edge_info[edge_id]
        except KeyError:
            raise ValueError("ERROR: Invalid edge id!")

        d['cost'] = new_cost

    def add_edge(self, edge_id: int, source_vertex_id: int, target_vertex_id: int, cost: int) -> None:
        # if source_vertex_id == target_vertex_id:
        #     raise ValueError("ERROR: Source vertex id and target vertex id cannot be the same!")
        if edge_id in self._edge_ids:
            raise ValueError("ERROR: Invalid edge id!")
        if source_vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid source vertex id!")
        if target_vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid target vertex id!")

        self._edge_info[edge_id] = {'source': source_vertex_id, 'target': target_vertex_id, 'cost': cost}
        self._out_edges[source_vertex_id][target_vertex_id] = edge_id
        self._in_edges[target_vertex_id][source_vertex_id] = edge_id
        self._edge_ids.add(edge_id)

    def remove_edge(self, edge_id) -> None:
        try:
            target = self._edge_info[edge_id]['target']
            source = self._edge_info[edge_id]['source']

            del self._out_edges[source][target]
            del self._in_edges[target][source]
            del self._edge_info[edge_id]
            self._edge_ids.remove(edge_id)

        except KeyError:
            raise ValueError("ERROR: Invalid edge id!")

    def add_vertex(self, vertex_id: int):
        if vertex_id in self._vertex_ids:
            raise ValueError("ERROR: Invalid vertex id!")

        self._vertex_ids.add(vertex_id)
        self._out_edges[vertex_id] = dict()
        self._in_edges[vertex_id] = dict()

    def remove_vertex(self, vertex_id: int):
        if vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid vertex id!")

        for v_id, edge_id in self._in_edges[vertex_id].items():
            del self._out_edges[v_id][vertex_id]
            del self._edge_info[edge_id]
            self._edge_ids.remove(edge_id)


        for v_id, edge_id in self._out_edges[vertex_id].items():
            del self._in_edges[v_id][vertex_id]
            del self._edge_info[edge_id]
            self._edge_ids.remove(edge_id)

        del self._out_edges[vertex_id]
        del self._in_edges[vertex_id]

        self._vertex_ids.remove(vertex_id)

    def save_graph(self, file_name: str):
        v_map = {x: y for y, x in enumerate(self._vertex_ids)}
        lines = [f"{self.vertex_count} {len(self._edge_ids)}\n"]
        for vertex in self.vertex_iterator:
            for edge_id in self._out_edges[vertex].values():
                source = v_map[self._edge_info[edge_id]['source']]
                target = v_map[self._edge_info[edge_id]['target']]
                cost = self._edge_info[edge_id]['cost']
                lines.append(f"{source} {target} {cost}\n")
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
        header_parts = header.split()

        for i in range(int(header_parts[0])):
            self.add_vertex(i)

        for index, line in enumerate(lines):
            parts = line.split()
            self.add_edge(index, int(parts[0]), int(parts[1]), int(parts[2]))

    def clear_graph(self):
        self._vertex_ids = set()
        self._edge_ids = set()
        self._out_edges = {}
        self._in_edges = {}
        self._edge_info = {}


