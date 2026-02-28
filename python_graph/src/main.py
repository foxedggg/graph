from graph import Graph

def main():
    graph = Graph()

    graph.load_graph('../../graph1m.txt')
    graph.remove_vertex(888888)
    graph.add_vertex(888888)
    graph.add_edge(4000000, 888888, 888888, 8)
    graph.save_graph('../../test.txt')

if __name__ == '__main__':
    main()
