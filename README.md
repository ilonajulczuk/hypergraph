#Hypergraphs are fun!

Code is written in python 3. I use such tools
as [IPython](http://ipython.org/), [numpy](http://www.numpy.org/)
and [networkx](http://networkx.github.io/)
. I write about first two on my
[blog](http://blog.atte.ro/posts/python-for-science.html)..

IPython has a powerful notebook which is amazing for sharing code
and insights and interactive development.
Links to notebooks:

###How can we represent hypergraphs in code?
A very good representation is bipartite graph of nodes and hyperedges.
 Another representation is a graph with hyperedges as nodes connected if
 hyperedges have common nodes. Is it a good representation for our
diffusion problem? Can we use it as a reference model?

- [hypergraphs 1](http://nbviewer.ipython.org/github/atteroTheGreatest/hypergraph/blob/master/notebooks/hypergraphs_1.ipynb?create=1)


###How different are hypergraphs from graphs with cliques?
Cliques are sets of nodes in which every node is connected to every other node.
 They are a bit similar to hypergraphs, but how the nodes are connected
is conceptually different from hypergraphs.

###How are hypergraphs different from graphs with cliques in diffusion simulation with markov chain?

- [hypergraphs vs graphs of cliques - diffusion](http://nbviewer.ipython.org/github/atteroTheGreatest/hypergraph/blob/master/hypergraph/clique_comparison.ipynb?create=1)

