#pragma once

#include <set>
#include <map>
#include <string>

using edges_map = std::map<int, std::map<int, int>>;
using edge_info_map = std::map<int, std::map<std::string, int>>;

class VertexIterator
{
private:
    std::set<int>::const_iterator it;
public:
    explicit VertexIterator(std::set<int>::const_iterator it);
    int operator*() const;
    VertexIterator& operator++();
    bool operator!=(const VertexIterator& other) const;

};

class Graph {
private:
    std::set<int> vertex_ids;
    std::set<int> edge_ids;
    edges_map out_edges;
    edges_map in_edges;
    edge_info_map edge_info;

public:
    Graph() = default;

    size_t vertex_count() const;
    VertexIterator vertex_iterator_begin() const;
    VertexIterator vertex_iterator_end() const;
    int get_edge(int source_vertex_id, int target_vertex_id);
    void add_vertex(int vertex_id);
    void add_edge(int edge_id, int source_vertex_id, int target_vertex_id, int cost);
};