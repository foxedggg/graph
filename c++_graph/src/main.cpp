#include <iostream>

#include "graph.h"

int main() {
    auto graph = Graph();
    graph.add_vertex(1);
    graph.add_vertex(2);
    graph.add_edge(1, 1, 2, 0);

    for (VertexIterator it = graph.vertex_iterator_begin(); it != graph.vertex_iterator_end(); ++it) {
        std::cout << " -> " << *it << "\n";
    }

}