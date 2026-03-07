#pragma once

#include <unordered_set>
#include <unordered_map>
#include <string>
#include <utility>
#include <expected>


class VertexIterator
{
private:
    std::unordered_set<int>::const_iterator it;
public:
    explicit VertexIterator(std::unordered_set<int>::const_iterator it);
    int operator*() const;
    VertexIterator& operator++();
    bool operator!=(const VertexIterator& other) const;

};

class EdgeIterator
{
private:
    std::unordered_map<int, int>::const_iterator it;
public:
    explicit EdgeIterator(std::unordered_map<int, int>::const_iterator it);
    int operator*() const;
    EdgeIterator& operator++();
    bool operator!=(const EdgeIterator& other) const;
};

class Graph {
    using edges_map = std::unordered_map<int, std::unordered_map<int, int>>;
    using edge_info_map = std::unordered_map<int, std::unordered_map<std::string, int>>;
    using end_points = std::pair<int, int>;
    using file_name = std::string;
private:
    std::unordered_set<int> vertex_ids;
    std::unordered_set<int> edge_ids;
    edges_map out_edges;
    edges_map in_edges;
    edge_info_map edge_info;

public:
    Graph() = default;

    size_t vertex_count() const;
    std::expected<int, std::string> get_in_degree(int vertex_id);
    std::expected<int, std::string> get_out_degree(int vertex_id);
    VertexIterator vertex_iterator_begin() const;
    VertexIterator vertex_iterator_end() const;

    std::expected<int, std::string> get_edge(int source_vertex_id, int target_vertex_id);
    std::expected<end_points, std::string> get_endpoints(int edge_id);
    std::expected<EdgeIterator, std::string> ingoing_edge_iterator_begin(int vertex_id);
    std::expected<EdgeIterator, std::string> ingoing_edge_iterator_end(int vertex_id);
    std::expected<EdgeIterator, std::string> outgoing_edge_iterator_begin(int vertex_id);
    std::expected<EdgeIterator, std::string> outgoing_edge_iterator_end(int vertex_id);
    std::expected<int, std::string> get_edge_cost(int edge_id);
    std::expected<void, std::string> set_edge_cost(int edge_id, int cost);
    std::expected<void, std::string> add_edge(int edge_id, int source_vertex_id, int target_vertex_id, int cost);
    std::expected<void, std::string> remove_edge(int edge_id);
    std::expected<void, std::string> add_vertex(int vertex_id);

    std::expected<void, std::string> remove_vertex(int vertex_id);
    void save_graph(file_name f);
    std::expected<void, std::string> load_graph(file_name f);
    void clear_graph();
};