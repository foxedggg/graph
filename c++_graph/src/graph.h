#pragma once

#include <unordered_set>
#include <unordered_map>
#include <string>
#include <utility>
#include <expected>
#include <vector>
#include <tuple>

struct pair_hash {
    template <class T1, class T2>
    std::size_t operator () (const std::pair<T1, T2> &p) const {
        auto h1 = std::hash<T1>{}(p.first);
        auto h2 = std::hash<T2>{}(p.second);
        return h1 ^ (h2 << 1); // Combine hashes
    }
};

class VertexIterator {
private:
    std::unordered_set<int>::const_iterator it;
public:
    explicit VertexIterator(std::unordered_set<int>::const_iterator it);
    int operator*() const;
    VertexIterator& operator++();
    bool operator!=(const VertexIterator& other) const;
};

class EdgeIterator {
private:
    std::unordered_map<int, int>::const_iterator it;
public:
    explicit EdgeIterator(std::unordered_map<int, int>::const_iterator it);
    int operator*() const;
    EdgeIterator& operator++();
    bool operator!=(const EdgeIterator& other) const;
};

class EdgeInfoIterator {
private:
    std::unordered_map<std::pair<int, int>, int, pair_hash>::const_iterator it;
public:
    explicit EdgeInfoIterator(std::unordered_map<std::pair<int, int>, int, pair_hash>::const_iterator it);
    std::tuple<int, int, int> operator*() const; // returns (source, target, cost)
    EdgeInfoIterator& operator++();
    bool operator!=(const EdgeInfoIterator& other) const;
};

class Graph {
    using edges_map = std::unordered_map<int, std::unordered_map<int, int>>;
    using edge_info_map = std::unordered_map<std::pair<int, int>, int, pair_hash>;
    using file_name = std::string;

private:
    std::unordered_set<int> vertex_ids;
    edges_map out_edges;
    edges_map in_edges;
    edge_info_map edge_info;

public:
    Graph() = default;

    [[nodiscard]] size_t vertex_count() const;
    [[nodiscard]] size_t edge_count() const;

    VertexIterator vertex_iterator_begin() const;
    VertexIterator vertex_iterator_end() const;

    EdgeInfoIterator edge_info_iterator_begin() const;
    EdgeInfoIterator edge_info_iterator_end() const;

    [[nodiscard]] std::expected<int, std::string> get_edge_cost(int source_vertex_id, int target_vertex_id) const;
    [[nodiscard]] std::expected<int, std::string> get_id_degree(int vertex_id) const;
    [[nodiscard]] std::expected<int, std::string> get_out_degree(int vertex_id) const;

    [[nodiscard]] std::expected<EdgeIterator, std::string> ingoing_edge_iterator_begin(int vertex_id) const;
    [[nodiscard]] std::expected<EdgeIterator, std::string> ingoing_edge_iterator_end(int vertex_id) const;

    [[nodiscard]] std::expected<EdgeIterator, std::string> outgoing_edge_iterator_begin(int vertex_id) const;
    [[nodiscard]] std::expected<EdgeIterator, std::string> outgoing_edge_iterator_end(int vertex_id) const;

    std::expected<void, std::string> set_edge_cost(int source_vertex_id, int target_vertex_id, int new_cost);
    std::expected<void, std::string> add_edge(int source_vertex_id, int target_vertex_id, int cost);
    std::expected<void, std::string> remove_edge(int source_vertex_id, int target_vertex_id);
    std::expected<void, std::string> add_vertex(int vertex_id);
    std::expected<void, std::string> remove_vertex(int vertex_id);

    std::expected<void, std::string> save_graph(file_name f) const;
    std::expected<void, std::string> load_graph(file_name f);
    void clear_graph();

    Graph copy() const;
};