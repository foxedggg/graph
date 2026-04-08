#include "graph.h"
#include <fstream>
#include <sstream>

VertexIterator::VertexIterator(std::unordered_set<int>::const_iterator it) : it(it) {}
int VertexIterator::operator*() const { return *it; }
VertexIterator& VertexIterator::operator++() { ++it; return *this; }
bool VertexIterator::operator!=(const VertexIterator& other) const { return it != other.it; }

EdgeIterator::EdgeIterator(std::unordered_map<int, int>::const_iterator it) : it(it) {}
int EdgeIterator::operator*() const { return it->first; }
EdgeIterator& EdgeIterator::operator++() { ++it; return *this; }
bool EdgeIterator::operator!=(const EdgeIterator& other) const { return it != other.it; }

EdgeInfoIterator::EdgeInfoIterator(std::unordered_map<std::pair<int, int>, int, pair_hash>::const_iterator it) : it(it) {}
std::tuple<int, int, int> EdgeInfoIterator::operator*() const {
    return {it->first.first, it->first.second, it->second};
}
EdgeInfoIterator& EdgeInfoIterator::operator++() { ++it; return *this; }
bool EdgeInfoIterator::operator!=(const EdgeInfoIterator& other) const { return it != other.it; }

size_t Graph::vertex_count() const {
    return vertex_ids.size();
}

size_t Graph::edge_count() const {
    return edge_info.size();
}

VertexIterator Graph::vertex_iterator_begin() const {
    return VertexIterator(vertex_ids.cbegin());
}

VertexIterator Graph::vertex_iterator_end() const {
    return VertexIterator(vertex_ids.cend());
}

EdgeInfoIterator Graph::edge_info_iterator_begin() const {
    return EdgeInfoIterator(edge_info.cbegin());
}

EdgeInfoIterator Graph::edge_info_iterator_end() const {
    return EdgeInfoIterator(edge_info.cend());
}

std::expected<int, std::string> Graph::get_edge_cost(int source_vertex_id, int target_vertex_id) const {
    if (!vertex_ids.contains(source_vertex_id)) return std::unexpected("ERROR: Invalid source vertex id!");
    if (!vertex_ids.contains(target_vertex_id)) return std::unexpected("ERROR: Invalid target vertex id!");
    if (!edge_info.contains({source_vertex_id, target_vertex_id})) return std::unexpected("ERROR: Edge doesn't exist");

    return edge_info.at({source_vertex_id, target_vertex_id});
}

std::expected<int, std::string> Graph::get_id_degree(int vertex_id) const {
    if (!vertex_ids.contains(vertex_id)) return std::unexpected("ERROR: Invalid vertex id!");
    return in_edges.at(vertex_id).size();
}

std::expected<int, std::string> Graph::get_out_degree(int vertex_id) const {
    if (!vertex_ids.contains(vertex_id)) return std::unexpected("ERROR: Invalid vertex id!");
    return out_edges.at(vertex_id).size();
}

std::expected<EdgeIterator, std::string> Graph::ingoing_edge_iterator_begin(int vertex_id) const {
    if (!vertex_ids.contains(vertex_id)) return std::unexpected("ERROR: Invalid vertex id!");
    return EdgeIterator(in_edges.at(vertex_id).cbegin());
}

std::expected<EdgeIterator, std::string> Graph::ingoing_edge_iterator_end(int vertex_id) const {
    if (!vertex_ids.contains(vertex_id)) return std::unexpected("ERROR: Invalid vertex id!");
    return EdgeIterator(in_edges.at(vertex_id).cend());
}

std::expected<EdgeIterator, std::string> Graph::outgoing_edge_iterator_begin(int vertex_id) const {
    if (!vertex_ids.contains(vertex_id)) return std::unexpected("ERROR: Invalid vertex id!");
    return EdgeIterator(out_edges.at(vertex_id).cbegin());
}

std::expected<EdgeIterator, std::string> Graph::outgoing_edge_iterator_end(int vertex_id) const {
    if (!vertex_ids.contains(vertex_id)) return std::unexpected("ERROR: Invalid vertex id!");
    return EdgeIterator(out_edges.at(vertex_id).cend());
}

std::expected<void, std::string> Graph::set_edge_cost(int source_vertex_id, int target_vertex_id, int new_cost) {
    if (!vertex_ids.contains(source_vertex_id)) return std::unexpected("ERROR: Invalid source vertex id!");
    if (!vertex_ids.contains(target_vertex_id)) return std::unexpected("ERROR: Invalid target vertex id!");
    if (!edge_info.contains({source_vertex_id, target_vertex_id})) return std::unexpected("ERROR: Edge doesn't exist");

    edge_info[{source_vertex_id, target_vertex_id}] = new_cost;
    return {};
}

std::expected<void, std::string> Graph::add_edge(int source_vertex_id, int target_vertex_id, int cost) {
    if (!vertex_ids.contains(source_vertex_id)) return std::unexpected("ERROR: Invalid source vertex id!");
    if (!vertex_ids.contains(target_vertex_id)) return std::unexpected("ERROR: Invalid target vertex id!");
    if (edge_info.contains({source_vertex_id, target_vertex_id})) return std::unexpected("ERROR: Edge already exist");

    out_edges[source_vertex_id][target_vertex_id] = cost;
    in_edges[target_vertex_id][source_vertex_id] = cost;
    edge_info[{source_vertex_id, target_vertex_id}] = cost;

    return {};
}

std::expected<void, std::string> Graph::remove_edge(int source_vertex_id, int target_vertex_id) {
    if (!vertex_ids.contains(source_vertex_id)) return std::unexpected("ERROR: Invalid source vertex id!");
    if (!vertex_ids.contains(target_vertex_id)) return std::unexpected("ERROR: Invalid target vertex id!");
    if (!edge_info.contains({source_vertex_id, target_vertex_id})) return std::unexpected("ERROR: Edge doesn't exist");

    out_edges[source_vertex_id].erase(target_vertex_id);
    in_edges[target_vertex_id].erase(source_vertex_id);
    edge_info.erase({source_vertex_id, target_vertex_id});

    return {};
}

std::expected<void, std::string> Graph::add_vertex(int vertex_id) {
    if (vertex_ids.contains(vertex_id)) return std::unexpected("ERROR: Vertex already exist");

    vertex_ids.insert(vertex_id);
    out_edges[vertex_id] = {};
    in_edges[vertex_id] = {};

    return {};
}

std::expected<void, std::string> Graph::remove_vertex(int vertex_id) {
    if (!vertex_ids.contains(vertex_id)) return std::unexpected("ERROR: Vertex doesn't exist");

    for (const auto& [v_id, cost] : in_edges[vertex_id]) {
        out_edges[v_id].erase(vertex_id);
        edge_info.erase({v_id, vertex_id});
    }

    for (const auto& [v_id, cost] : out_edges[vertex_id]) {
        in_edges[v_id].erase(vertex_id);
        edge_info.erase({vertex_id, v_id});
    }

    out_edges.erase(vertex_id);
    in_edges.erase(vertex_id);
    vertex_ids.erase(vertex_id);

    return {};
}

std::expected<void, std::string> Graph::save_graph(file_name f) const {
    std::ofstream out(f);
    if (!out.is_open()) return std::unexpected("ERROR: Couldn't open file " + f + " for writing");

    out << vertex_count() << " " << edge_count() << "\n";
    for (auto it = edge_info_iterator_begin(); it != edge_info_iterator_end(); ++it) {
        auto [source, target, cost] = *it;
        out << source << " " << target << " " << cost << "\n";
    }

    return {};
}

std::expected<void, std::string> Graph::load_graph(file_name f) {
    std::ifstream in(f);
    if (!in.is_open()) return std::unexpected("File " + f + " is not found");

    std::string header;
    if (!std::getline(in, header)) return std::unexpected("ERROR: File is empty");

    int expected_v_count, expected_e_count;
    std::istringstream hss(header);
    if (!(hss >> expected_v_count >> expected_e_count)) return std::unexpected("ERROR: Invalid header format");

    clear_graph();

    std::string line;
    while (std::getline(in, line)) {
        if (line.empty()) continue;
        std::istringstream liss(line);
        int src, tgt, cost;
        if (liss >> src >> tgt >> cost) {
            if (!vertex_ids.contains(src)) add_vertex(src);
            if (!vertex_ids.contains(tgt)) add_vertex(tgt);
            add_edge(src, tgt, cost);
        }
    }

    if (vertex_ids.size() != static_cast<size_t>(expected_v_count)) return std::unexpected("ERROR: Couldn't load right number of vertexes");
    if (edge_info.size() != static_cast<size_t>(expected_e_count)) return std::unexpected("ERROR: Couldn't load right number of edges");

    return {};
}

void Graph::clear_graph() {
    vertex_ids.clear();
    out_edges.clear();
    in_edges.clear();
    edge_info.clear();
}

Graph Graph::copy() const {
    Graph new_graph;

    for (auto it = vertex_iterator_begin(); it != vertex_iterator_end(); ++it) {
        new_graph.add_vertex(*it);
    }

    for (auto it = edge_info_iterator_begin(); it != edge_info_iterator_end(); ++it) {
        auto [source, target, cost] = *it;
        new_graph.add_edge(source, target, cost);
    }

    return new_graph;
}