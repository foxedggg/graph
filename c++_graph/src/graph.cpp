#include "graph.h"

// Vertex iterator
VertexIterator::VertexIterator(std::unordered_set<int>::const_iterator it) {
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

// Edge iterator
EdgeIterator::EdgeIterator(std::unordered_map<int, int>::const_iterator it) {
    this->it = it;
}

int EdgeIterator::operator*() const {
    return it->first;
}

EdgeIterator& EdgeIterator::operator++() {
    ++it;
    return *this;
}

bool EdgeIterator::operator!=(const EdgeIterator& other) const {
    return it != other.it;
}

// Graph

size_t Graph::vertex_count() const {
    return vertex_ids.size();
}

std::expected<int, std::string> Graph::get_in_degree(int vertex_id) {
    if (!in_edges.contains(vertex_id)) {
        return std::unexpected("Invalid vertex id");
    }
    return in_edges[vertex_id].size();
}

std::expected<int, std::string> Graph::get_out_degree(int vertex_id) {
    if (!out_edges.contains(vertex_id)) {
        return std::unexpected("Invalid vertex id");
    }
    return out_edges[vertex_id].size();
}

VertexIterator Graph::vertex_iterator_begin() const {
    return VertexIterator(vertex_ids.cbegin());
}

VertexIterator Graph::vertex_iterator_end() const {
    return VertexIterator(vertex_ids.cend());
}

std::expected<int, std::string> Graph::get_edge(int source_vertex_id, int target_vertex_id) {
    if (!out_edges.contains(source_vertex_id)) {
        return std::unexpected("Source vertex " + std::to_string(source_vertex_id) + " does not exist.");
    }
    if (!out_edges[source_vertex_id].contains(target_vertex_id)) {
        return std::unexpected("Target vertex " + std::to_string(source_vertex_id) + " does not exist.");
    }
    return out_edges[source_vertex_id][target_vertex_id];
}

std::expected<Graph::end_points, std::string> Graph::get_endpoints(int edge_id) {
    if (!edge_info.contains(edge_id)) {
        return std::unexpected("Edge " + std::to_string(edge_id) + " does not exist.");
    }
    return Graph::end_points{edge_info[edge_id]["source"], edge_info[edge_id]["target"]};
}

std::expected<void, std::string> Graph::add_vertex(int vertex_id) {
    if (vertex_ids.contains(vertex_id)) {
        return std::unexpected("Vertex " + std::to_string(vertex_id) + " already exists.");
    }

    vertex_ids.insert(vertex_id);
    out_edges[vertex_id];
    in_edges[vertex_id];

    return {};
}

std::expected<void, std::string> Graph::add_edge(int edge_id, int source_vertex_id, int target_vertex_id, int cost) {
    if (edge_ids.contains(edge_id)) {
        return std::unexpected("Edge " + std::to_string(edge_id) + " already exists.");
    }
    if (!vertex_ids.contains(source_vertex_id)) {
        return std::unexpected("Source vertex " + std::to_string(source_vertex_id) + " does not exist.");
    }
    if (!vertex_ids.contains(target_vertex_id)) {
        return std::unexpected("Target vertex " + std::to_string(target_vertex_id) + " does not exist.");
    }

    edge_ids.insert(edge_id);
    edge_info[edge_id] = {
        {"source", source_vertex_id},
        {"target", target_vertex_id},
        {"cost", cost},
    };
    return {};
}