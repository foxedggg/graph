import random
import itertools
from graph import Graph


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
    print("\n" + "=" * 30)
    print("         GRAPH MENU")
    print("=" * 30)
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
    print("11. BFS")
    print("12. Exit")
    print("=" * 30)


def main():
    graph = Graph()

    while True:
        print_menu()
        choice = input("Enter your choice (1-12): ")

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
            print("Exiting program.")
            break

        else:
            print("-> Invalid choice. Please select an option from 1 to 13.")

if __name__ == '__main__':
    main()