#include "graph.h"

VertexIterator::VertexIterator(std::set<int>::const_iterator it) {
    this->it = it;
}

int VertexIterator::operator*() const {
    return *it;
}

VertexIterator& VertexIterator::operator++() {
    ++it;
    return *this;
}

bool VertexIterator::operator!=(const VertexIterator& other) const {
    return it != other.it;
}

size_t Graph::vertex_count() const {
    return vertex_ids.size();
}

VertexIterator Graph::vertex_iterator_begin() const {
    return VertexIterator(vertex_ids.cbegin());
}

VertexIterator Graph::vertex_iterator_end() const {
    return VertexIterator(vertex_ids.cend());
}

int Graph::get_edge(int source_vertex_id, int target_vertex_id) {
    auto source_it = out_edges.find(source_vertex_id);
    if (source_it == out_edges.end()) {
        throw std::invalid_argument("Source vertex " + std::to_string(source_vertex_id) + " does not exist.");
    }
    auto target_it = source_it->second.find(target_vertex_id);
    if (target_it == source_it->second.end()) {
        throw std::invalid_argument("Target vertex " + std::to_string(source_vertex_id) + " does not exist.");
    }

    return out_edges[source_vertex_id][target_vertex_id];
}

void Graph::add_vertex(int vertex_id) {
    auto it = vertex_ids.find(vertex_id);
    if (it != vertex_ids.end()) {
        throw std::invalid_argument("Vertex " + std::to_string(vertex_id) + " already exists.");
    }

    vertex_ids.insert(vertex_id);
    out_edges[vertex_id] = std::map<int, int>();
    in_edges[vertex_id] = std::map<int, int>();
}

void Graph::add_edge(int edge_id, int source_vertex_id, int target_vertex_id, int cost) {
    auto edge_it = edge_ids.find(edge_id);
    if (edge_it != edge_ids.end()) {
        throw std::invalid_argument("Edge " + std::to_string(edge_id) + " already exists.");
    }
    auto source_it = vertex_ids.find(source_vertex_id);
    if (source_it == vertex_ids.end()) {
        throw std::invalid_argument("Source vertex " + std::to_string(source_vertex_id) + " does not exist.");
    }
    auto target_it = vertex_ids.find(target_vertex_id);
    if (target_it == vertex_ids.end()) {
        throw std::invalid_argument("Target vertex " + std::to_string(source_vertex_id) + " does not exist.");
    }

    edge_ids.insert(edge_id);
    edge_info[edge_id] = {
        {"source", source_vertex_id},
        {"target", target_vertex_id},
        {"cost", cost},
    };
}