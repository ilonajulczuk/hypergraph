import nose.tools as nt
import hypergraph.generators as generators


def test_uniform_generator():
    number_of_nodes = 10
    number_of_edges = 5
    cardinality = 3
    hu = generators.uniform_hypergraph(number_of_nodes, number_of_edges,
                            cardinality)
    nt.assert_true(hu)
    nt.assert_equals(len(hu.nodes()), number_of_nodes)
    nt.assert_equals(len(hu.hyper_edges()), number_of_edges)
    nt.assert_true(all(len(e) == cardinality for e in hu.hyper_edges()))


def test_generator():
    number_of_nodes = 10
    edges_params = ((2, 3), (3, 4), (4, 8))
    hypergraph = generators.generic_hypergraph(number_of_nodes, edges_params)
    number_of_edges = sum(edge_count for _, edge_count in edges_params)
    nt.assert_equals(number_of_edges, len(hypergraph.hyper_edges()))

