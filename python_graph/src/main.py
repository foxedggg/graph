import random
import itertools
import heapq
from graph import Graph


class ImplicitBridgeGraph:
    """
    An implicit representation of the Bridge and Torch state-space graph.
    Matches the interface needed for shortest-path searches (yielding neighbors).

    State representation: (left_side_tuple, right_side_tuple, torch_is_left)
    - left_side_tuple: tuple of integers (identifiers for people on the left side)
    - right_side_tuple: tuple of integers (identifiers for people on the right side)
    - torch_is_left: 1 if torch is on the left, 0 if on the right.
    """

    def __init__(self, people_times: dict):
        self.times = people_times

    def outgoing_edge_iterator(self, state):
        left, right, torch_is_left = state
        left_list, right_list = list(left), list(right)
        edges = []

        if torch_is_left == 1:
            # Torch is on left -> 1 or 2 people must move to right
            for i in range(len(left_list)):
                for j in range(i, len(left_list)):
                    p1, p2 = left_list[i], left_list[j]

                    new_left = left_list[:]
                    new_left.remove(p1)
                    if p1 != p2:
                        new_left.remove(p2)

                    new_right = right_list[:]
                    new_right.append(p1)
                    if p1 != p2:
                        new_right.append(p2)

                    new_state = (tuple(sorted(new_left)), tuple(sorted(new_right)), 0)
                    edges.append(new_state)
        else:
            # Torch is on right -> exactly 1 person must move back to left
            for i in range(len(right_list)):
                p = right_list[i]

                new_right = right_list[:]
                new_right.remove(p)

                new_left = left_list[:]
                new_left.append(p)

                new_state = (tuple(sorted(new_left)), tuple(sorted(new_right)), 1)
                edges.append(new_state)

        return iter(edges)

    def get_edge_cost(self, state1, state2) -> int:
        """Derive the time taken to transition between two states."""
        left1 = set(state1[0])
        left2 = set(state2[0])

        # Identify who crossed the bridge (symmetric difference between the two left states)
        moved = left1 ^ left2
        if not moved:
            return 0
        return max(self.times[p] for p in moved)


def solve_bridge_and_torch():
    """Reads times and solves using a lowest cost path search."""
    try:
        n = int(input("Enter number of people crossing (up to 20): "))
        if n < 1 or n > 20:
            print("Invalid number of people.")
            return

        people_times = {}
        for i in range(n):
            time = int(input(f"Enter crossing time for person {i + 1}: "))
            people_times[i] = time

        # Instantiate implicit graph matching lab interface
        graph = ImplicitBridgeGraph(people_times)

        # Initial State: Everyone on left, Torch on left (1)
        start_state = (tuple(sorted(people_times.keys())), (), 1)

        # Dijkstra's Algorithm
        dist = {start_state: 0}
        pq = [(0, start_state)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist.get(u, float('inf')):
                continue

            left, right, torch = u
            if len(left) == 0:  # Target: Everyone moved off the left side
                print(f"-> Minimum time required for all to cross: {d}")
                return

            # Explore valid moves using the graph interface
            for v in graph.outgoing_edge_iterator(u):
                cost = graph.get_edge_cost(u, v)
                if dist.get(u, float('inf')) + cost < dist.get(v, float('inf')):
                    dist[v] = dist[u] + cost
                    heapq.heappush(pq, (dist[v], v))

        print("-> No solution found.")
    except ValueError:
        print("-> Invalid numeric input.")


def generate_random_graph(graph: Graph, n: int, m: int):
    if m > n * n:
        print(f"Error: Too many edges ({m}) for {n} vertices. Maximum is {n * n}.")
        return
    graph.clear_graph()
    for i in range(n):
        graph.add_vertex(i)
    all_possible_edges = list(itertools.product(range(n), repeat=2))
    chosen_edges = random.sample(all_possible_edges, m)
    for u, v in chosen_edges:
        cost = random.randint(1, 100)
        graph.add_edge(u, v, cost)
    print(f"Successfully generated a random graph with {n} vertices and {m} edges.")


def print_menu():
    print("\n" + "=" * 35)
    print("         GRAPH MENU")
    print("=" * 35)
    print("1. Add Vertex")
    print("2. Remove Vertex")
    print("3. Add Edge")
    print("4. Remove Edge")
    print("5. Generate Random Graph")
    print("6. Print Graph Information")
    print("7. Save Graph to File")
    print("8. Load Graph from File")
    print("9. Get Vertex In-Degree")
    print("10. Get Vertex Out-Degree")
    print("11. BFS Path")
    print("12. Lowest Cost Walk (Matrix Mult)")
    print("13. Count Min Cost Walks (No Neg Cycle)")
    print("14. Count Distinct Walks in DAG")
    print("15. Solve Bridge & Torch Problem")
    print("16. Exit")
    print("=" * 35)


def main():
    graph = Graph()
    while True:
        print_menu()
        choice = input("Enter your choice (1-16): ")
        if choice == '1':
            try:
                v_id = int(input("Enter the new vertex ID: "))
                graph.add_vertex(v_id)
                print(f"-> Vertex {v_id} added successfully.")
            except ValueError as e:
                print(f"-> {e}")
        elif choice == '2':
            try:
                v_id = int(input("Enter the vertex ID to remove: "))
                graph.remove_vertex(v_id)
                print(f"-> Vertex {v_id} removed successfully.")
            except ValueError as e:
                print(f"-> {e}")
        elif choice == '3':
            try:
                source = int(input("Enter the source vertex ID: "))
                target = int(input("Enter the target vertex ID: "))
                cost = int(input("Enter the edge cost: "))
                graph.add_edge(source, target, cost)
                print(f"-> Added edge from {source} to {target} with cost {cost}.")
            except ValueError as e:
                print(f"-> {e}")
        elif choice == '4':
            try:
                source = int(input("Enter the source vertex ID: "))
                target = int(input("Enter the target vertex ID: "))
                graph.remove_edge(source, target)
                print(f"-> Edge from {source} to {target} removed successfully.")
            except ValueError as e:
                print(f"-> {e}")
        elif choice == '5':
            try:
                n = int(input("Enter the number of vertices (n): "))
                m = int(input("Enter the number of edges (m): "))
                generate_random_graph(graph, n, m)
            except ValueError:
                print("-> Invalid input. Please enter valid integers.")
        elif choice == '6':
            print(f"\n--- Graph Details ---")
            print(f"Total vertices: {graph.vertex_count}")
            print(f"Total edges: {graph.edge_count}")
            print(f"Vertices: {list(graph.vertex_iterator())}")
            print("Edges:")
            edge_count = 0
            for s, t, c in graph.edge_info_iterator():
                print(f"  {s} -> {t} (Cost: {c})")
                edge_count += 1
            if edge_count == 0:
                print("  No edges in the graph.")
        elif choice == '7':
            filename = input("Enter the filename to save the graph to (e.g., graph.txt): ")
            try:
                graph.save_graph(filename)
                print(f"-> Graph successfully saved to {filename}.")
            except Exception as e:
                print(f"-> Error saving graph: {e}")
        elif choice == '8':
            filename = input("Enter the filename to load the graph from (e.g., graph.txt): ")
            try:
                graph.load_graph(filename)
                print(f"-> Graph successfully loaded from {filename}.")
            except FileNotFoundError as e:
                print(f"-> {e}")
            except Exception as e:
                print(f"-> Error loading graph: {e}")
        elif choice == '9':
            try:
                v_id = int(input("Enter the vertex ID: "))
                degree = graph.get_id_degree(v_id)
                print(f"-> Vertex {v_id} has an in-degree of {degree}.")
            except ValueError as e:
                print(f"-> {e}")
        elif choice == '10':
            try:
                v_id = int(input("Enter the vertex ID: "))
                degree = graph.get_out_degree(v_id)
                print(f"-> Vertex {v_id} has an out-degree of {degree}.")
            except ValueError as e:
                print(f"-> {e}")
        elif choice == '11':
            try:
                source = int(input("Enter the source vertex ID: "))
                target = int(input("Enter the target vertex ID: "))
                path = graph.bfs(source, target)
                if path is None:
                    print("No path found")
                else:
                    print(path)
            except ValueError as e:
                print(f"-> {e}")
        elif choice == '12':
            try:
                source = int(input("Enter the source vertex ID: "))
                target = int(input("Enter the target vertex ID: "))

                # Ask the user if they want to see the intermediate matrix steps
                show_int_input = input("Show intermediate matrices? (y/n): ").strip().lower()
                show_int = (show_int_input == 'y')

                res = graph.matrix_mult_lowest_cost_walk(source, target, show_intermediate=show_int)

                print("\n--- Final Result ---")
                if isinstance(res, str):
                    print(f"-> {res}")
                elif res is None or not res[1]:
                    print("-> No path found.")
                else:
                    cost, path = res
                    print(f"-> Lowest cost: {cost} | Path: {path}")
            except ValueError as e:
                print(f"-> {e}")
        elif choice == '13':
            try:
                source = int(input("Enter the source vertex ID: "))
                target = int(input("Enter the target vertex ID: "))
                walks = graph.count_min_cost_walks(source, target)
                print(f"-> Number of distinct minimum cost walks: {walks}")
            except ValueError as e:
                print(f"-> {e}")
        elif choice == '14':
            try:
                source = int(input("Enter the source vertex ID: "))
                target = int(input("Enter the target vertex ID: "))
                walks = graph.count_walks_dag(source, target)
                print(f"-> Number of distinct walks (DAG): {walks}")
            except ValueError as e:
                print(f"-> {e}")
        elif choice == '15':
            solve_bridge_and_torch()
        elif choice == '16':
            print("Exiting program.")
            break
        else:
            print("-> Invalid choice. Please select an option from 1 to 16.")


if __name__ == '__main__':
    main()