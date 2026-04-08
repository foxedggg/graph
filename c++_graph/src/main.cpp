#include <iostream>
#include <string>
#include <random>
#include <vector>
#include <algorithm>
#include <stdexcept>
#include "graph.h"

int read_int(const std::string& prompt) {
    std::string line;
    std::cout << prompt;
    if (!std::getline(std::cin, line)) {
        exit(0);
    }
    size_t pos;
    int val = std::stoi(line, &pos);
    if (pos != line.length() && line[pos] != ' ' && line[pos] != '\r') {
        throw std::invalid_argument("Invalid literal for int");
    }
    return val;
}

void generate_random_graph(Graph& graph, int n, int m) {
    if (m > n * n) {
        std::cout << "Error: Too many edges (" << m << ") for " << n << " vertices. Maximum is " << n * n << ".\n";
        return;
    }

    graph.clear_graph();
    for (int i = 0; i < n; ++i) {
        graph.add_vertex(i);
    }

    std::vector<std::pair<int, int>> all_possible_edges;
    all_possible_edges.reserve(n * n);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            all_possible_edges.emplace_back(i, j);
        }
    }

    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(all_possible_edges.begin(), all_possible_edges.end(), g);

    for (int i = 0; i < m; ++i) {
        int u = all_possible_edges[i].first;
        int v = all_possible_edges[i].second;
        int cost = std::uniform_int_distribution<>(1, 100)(g);
        graph.add_edge(u, v, cost);
    }

    std::cout << "Successfully generated a random graph with " << n << " vertices and " << m << " edges.\n";
}

void print_menu() {
    std::cout << "\n==============================\n";
    std::cout << "         GRAPH MENU\n";
    std::cout << "==============================\n";
    std::cout << "1. Add Vertex\n";
    std::cout << "2. Remove Vertex\n";
    std::cout << "3. Add Edge\n";
    std::cout << "4. Remove Edge\n";
    std::cout << "5. Generate Random Graph\n";
    std::cout << "6. Print Graph Information\n";
    std::cout << "7. Save Graph to File\n";
    std::cout << "8. Load Graph from File\n";
    std::cout << "9. Get Vertex In-Degree\n";
    std::cout << "10. Get Vertex Out-Degree\n";
    std::cout << "11. Exit\n";
    std::cout << "==============================\n";
}

int main() {
    Graph graph;
    std::string choice;

    while (true) {
        print_menu();
        std::cout << "Enter your choice (1-11): ";
        if (!std::getline(std::cin, choice)) break;

        if (choice == "1") {
            try {
                int v_id = read_int("Enter the new vertex ID: ");
                auto res = graph.add_vertex(v_id);
                if (!res) std::cout << "-> " << res.error() << "\n";
                else std::cout << "-> Vertex " << v_id << " added successfully.\n";
            } catch (...) { std::cout << "-> invalid input. Please enter valid integers.\n"; }
        }
        else if (choice == "2") {
            try {
                int v_id = read_int("Enter the vertex ID to remove: ");
                auto res = graph.remove_vertex(v_id);
                if (!res) std::cout << "-> " << res.error() << "\n";
                else std::cout << "-> Vertex " << v_id << " removed successfully.\n";
            } catch (...) { std::cout << "-> invalid input. Please enter valid integers.\n"; }
        }
        else if (choice == "3") {
            try {
                int source = read_int("Enter the source vertex ID: ");
                int target = read_int("Enter the target vertex ID: ");
                int cost = read_int("Enter the edge cost: ");
                auto res = graph.add_edge(source, target, cost);
                if (!res) std::cout << "-> " << res.error() << "\n";
                else std::cout << "-> Added edge from " << source << " to " << target << " with cost " << cost << ".\n";
            } catch (...) { std::cout << "-> invalid input. Please enter valid integers.\n"; }
        }
        else if (choice == "4") {
            try {
                int source = read_int("Enter the source vertex ID: ");
                int target = read_int("Enter the target vertex ID: ");
                auto res = graph.remove_edge(source, target);
                if (!res) std::cout << "-> " << res.error() << "\n";
                else std::cout << "-> Edge from " << source << " to " << target << " removed successfully.\n";
            } catch (...) { std::cout << "-> invalid input. Please enter valid integers.\n"; }
        }
        else if (choice == "5") {
            try {
                int n = read_int("Enter the number of vertices (n): ");
                int m = read_int("Enter the number of edges (m): ");
                generate_random_graph(graph, n, m);
            } catch (...) { std::cout << "-> Invalid input. Please enter valid integers.\n"; }
        }
        else if (choice == "6") {
            std::cout << "\n--- Graph Details ---\n";
            std::cout << "Total vertices: " << graph.vertex_count() << "\n";
            std::cout << "Total edges: " << graph.edge_count() << "\n";

            std::cout << "Vertices: [";
            bool first = true;
            for (auto it = graph.vertex_iterator_begin(); it != graph.vertex_iterator_end(); ++it) {
                if (!first) std::cout << ", ";
                std::cout << *it;
                first = false;
            }
            std::cout << "]\nEdges:\n";

            int edge_count = 0;
            for (auto it = graph.edge_info_iterator_begin(); it != graph.edge_info_iterator_end(); ++it) {
                auto [s, t, c] = *it;
                std::cout << "  " << s << " -> " << t << " (Cost: " << c << ")\n";
                edge_count++;
            }
            if (edge_count == 0) {
                std::cout << "  No edges in the graph.\n";
            }
        }
        else if (choice == "7") {
            std::cout << "Enter the filename to save the graph to (e.g., graph.txt): ";
            std::string filename;
            std::getline(std::cin, filename);
            auto res = graph.save_graph(filename);
            if (!res) std::cout << "-> Error saving graph: " << res.error() << "\n";
            else std::cout << "-> Graph successfully saved to " << filename << ".\n";
        }
        else if (choice == "8") {
            std::cout << "Enter the filename to load the graph from (e.g., graph.txt): ";
            std::string filename;
            std::getline(std::cin, filename);
            auto res = graph.load_graph(filename);
            if (!res) std::cout << "-> " << res.error() << "\n";
            else std::cout << "-> Graph successfully loaded from " << filename << ".\n";
        }
        else if (choice == "9") {
            try {
                int v_id = read_int("Enter the vertex ID: ");
                auto res = graph.get_id_degree(v_id);
                if (!res) std::cout << "-> " << res.error() << "\n";
                else std::cout << "-> Vertex " << v_id << " has an in-degree of " << res.value() << ".\n";
            } catch (...) { std::cout << "-> invalid input. Please enter valid integers.\n"; }
        }
        else if (choice == "10") {
            try {
                int v_id = read_int("Enter the vertex ID: ");
                auto res = graph.get_out_degree(v_id);
                if (!res) std::cout << "-> " << res.error() << "\n";
                else std::cout << "-> Vertex " << v_id << " has an out-degree of " << res.value() << ".\n";
            } catch (...) { std::cout << "-> invalid input. Please enter valid integers.\n"; }
        }
        else if (choice == "11") {
            std::cout << "Exiting program.\n";
            break;
        }
        else {
            std::cout << "-> Invalid choice. Please select an option from 1 to 11.\n";
        }
    }

    return 0;
}