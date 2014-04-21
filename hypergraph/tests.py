import nose.tools as nt
from hypergraph.generators import uniform_hypergraph


def test_uniform_generator():
    number_of_nodes = 10
    number_of_edges = 5
    cardinality = 3
    hu = uniform_hypergraph(number_of_nodes, number_of_edges,
                            cardinality)
    nt.assert_true(hu)
    nt.assert_equals(len(hu.nodes()), number_of_nodes)
    nt.assert_equals(len(hu.hyper_edges()), number_of_edges)
    nt.assert_true(all(len(e) == cardinality for e in hu.hyper_edges()))

