from collections import deque


class Graph:
    def __init__(self):
        self._vertex_ids = set()
        # Maps vertex_id to a dictionary of {target: cost}
        self._out_edges = {}
        # Maps vertex_id to a dictionary of {source: cost}
        self._in_edges = {}
        # Maps (source_id, target_id) to a cost
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
        for v_id in list(self._in_edges[vertex_id].keys()):
            del self._out_edges[v_id][vertex_id]
            del self._edge_info[(v_id, vertex_id)]
        for v_id in list(self._out_edges[vertex_id].keys()):
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
            if not parts:
                continue
            if int(parts[0]) not in self._vertex_ids:
                self.add_vertex(int(parts[0]))
            if int(parts[1]) not in self._vertex_ids:
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

    def _print_matrix(self, name: str, matrix: list, idx_to_v: dict, is_predecessor: bool = False):
        """Prints a 2D matrix nicely formatted with vertex ID headers/rows."""
        n = len(matrix)
        print(f"\n--- {name} ---")

        # Print header row with target vertex IDs
        header = "    |" + "".join(f"{str(idx_to_v[i]):>5}" for i in range(n))
        print(header)
        print("----+" + "-" * (n * 5))

        for i in range(n):
            row_str = []
            for val in matrix[i]:
                if val == float('inf'):
                    row_str.append(f"{'INF':>5}")
                elif is_predecessor:
                    # Convert matrix indices back to actual vertex IDs for readability
                    if val == -1:
                        row_str.append(f"{'NIL':>5}")
                    else:
                        row_str.append(f"{idx_to_v[val]:>5}")
                else:
                    row_str.append(f"{val:>5}")

            # Print row label (source vertex ID) and data
            print(f"{str(idx_to_v[i]):>3} |" + "".join(row_str))

    def matrix_mult_lowest_cost_walk(self, source_vertex_id: int, target_vertex_id: int,
                                     show_intermediate: bool = False):
        """
        Finds a lowest cost walk between two vertices using the Matrix Multiplication Algorithm.
        Detects negative cycles. Can optionally print intermediate matrices.
        Returns (cost, path) or a string if a cycle is found.
        """
        if source_vertex_id not in self._vertex_ids or target_vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid vertex ID.")

        vertices = list(self.vertex_iterator())
        n = len(vertices)

        # Mapping real vertex ids to matrix indices (0 to n-1)
        v_to_idx = {v: i for i, v in enumerate(vertices)}
        idx_to_v = {i: v for i, v in enumerate(vertices)}
        INF = float('inf')

        # Initialize the weight matrix W and predecessor matrix P
        W = [[INF] * n for _ in range(n)]
        P = [[-1] * n for _ in range(n)]

        for i in range(n):
            W[i][i] = 0

        for s, t, c in self.edge_info_iterator():
            s_i, t_i = v_to_idx[s], v_to_idx[t]
            W[s_i][t_i] = c
            P[s_i][t_i] = s_i

        # Helper function to extend shortest paths by 1 edge
        def extend_shortest_paths(L_prev, P_prev):
            new_L = [[INF] * n for _ in range(n)]
            new_P = [row[:] for row in P_prev]
            for i in range(n):
                for j in range(n):
                    new_L[i][j] = L_prev[i][j]
                    for k in range(n):
                        if L_prev[i][k] + W[k][j] < new_L[i][j]:
                            new_L[i][j] = L_prev[i][k] + W[k][j]
                            new_P[i][j] = P_prev[k][j]
            return new_L, new_P

        # L^{1} is exactly W
        L = [row[:] for row in W]

        # Print the initial matrices if requested
        if show_intermediate:
            print("\n" + "=" * 40)
            print("INITIAL MATRICES (Path length = 1)")
            print("=" * 40)
            self._print_matrix("L^1 (Distances)", L, idx_to_v)
            self._print_matrix("P^1 (Predecessors)", P, idx_to_v, is_predecessor=True)

        # Iterate to compute up to L^{n-1}
        for m in range(2, n):
            L, P = extend_shortest_paths(L, P)

            # Print the intermediate matrices at each step if requested
            if show_intermediate:
                print("\n" + "=" * 40)
                print(f"INTERMEDIATE MATRICES (Path length \u2264 {m})")
                print("=" * 40)
                self._print_matrix(f"L^{m} (Distances)", L, idx_to_v)
                self._print_matrix(f"P^{m} (Predecessors)", P, idx_to_v, is_predecessor=True)

        # One final iteration to check for negative cycles
        L_next, _ = extend_shortest_paths(L, P)
        for i in range(n):
            for j in range(n):
                if L_next[i][j] < L[i][j]:
                    return "Negative cost cycle detected!"

        s_i, t_i = v_to_idx[source_vertex_id], v_to_idx[target_vertex_id]

        # No path case
        if L[s_i][t_i] == INF:
            return None, []

        # Reconstruct path using the Predecessor matrix
        path = []
        curr = t_i
        while curr != s_i and curr != -1:
            path.append(idx_to_v[curr])
            curr = P[s_i][curr]

        if curr == -1:
            return None, []

        path.append(idx_to_v[s_i])
        path.reverse()

        return L[s_i][t_i], path

    def count_min_cost_walks(self, source_vertex_id: int, target_vertex_id: int) -> int:
        """
        Given a graph with costs and NO negative cost cycles, finds the number 
        of distinct walks of minimum cost between two vertices.
        """
        if source_vertex_id not in self._vertex_ids or target_vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid vertex ID.")

        n = self.vertex_count
        dist = {v: float('inf') for v in self.vertex_iterator()}
        dist[source_vertex_id] = 0

        # Step 1: Bellman-Ford to find shortest distance from source to all nodes.
        for _ in range(n - 1):
            for s, t, c in self.edge_info_iterator():
                if dist[s] != float('inf') and dist[s] + c < dist[t]:
                    dist[t] = dist[s] + c

        if dist[target_vertex_id] == float('inf'):
            return 0  # No path exists

        # Step 2: Use Memoized DFS to count valid paths on the DAG formed by shortest paths
        memo = {}

        def dfs(u):
            if u == target_vertex_id:
                return 1
            if u in memo:
                return memo[u]

            total_walks = 0
            for v in self.outgoing_edge_iterator(u):
                cost = self.get_edge_cost(u, v)
                # Ensure the edge (u, v) is part of a minimum cost path
                if dist[u] + cost == dist[v]:
                    total_walks += dfs(v)

            memo[u] = total_walks
            return total_walks

        return dfs(source_vertex_id)

    def count_walks_dag(self, source_vertex_id: int, target_vertex_id: int) -> int:
        """
        Given a Directed Acyclic Graph (DAG), finds the number of distinct 
        walks between a pair of vertices. Raises error if cycle exists.
        """
        if source_vertex_id not in self._vertex_ids or target_vertex_id not in self._vertex_ids:
            raise ValueError("ERROR: Invalid vertex ID.")

        memo = {}
        visiting = set()  # Needed for cycle detection

        def dfs(u):
            if u in visiting:
                raise ValueError("ERROR: The provided graph is not a DAG. Cycle detected.")
            if u == target_vertex_id:
                return 1
            if u in memo:
                return memo[u]

            visiting.add(u)
            total_walks = 0
            for v in self.outgoing_edge_iterator(u):
                total_walks += dfs(v)

            visiting.remove(u)
            memo[u] = total_walks
            return total_walks

        return dfs(source_vertex_id)