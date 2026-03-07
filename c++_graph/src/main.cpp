#include <print>

#include "graph.h"

int main() {
    auto graph = Graph();
    auto res1 = graph.add_vertex(1);
    if (!res1) {
        std::println("Error: {}", res1.error());
    }
    auto res2 = graph.add_vertex(1);
    if (!res2) {
        std::println("Error: {}", res2.error());
    }
    auto res3 = graph.add_edge(1, 1, 2, 0);
    if (!res3) {
        std::println("Error: {}", res3.error());
    }
    auto res4 = graph.add_vertex(3);
    if (!res4) {
        std::println("Error: {}", res4.error());
    }

    int counter = 0;
    for (VertexIterator it = graph.vertex_iterator_begin(); it != graph.vertex_iterator_end(); ++it) {
        if (counter) {
            std::print(" -> ");
        }
        std::print("{}", *it);
        counter++;
    }
    std::println();

}