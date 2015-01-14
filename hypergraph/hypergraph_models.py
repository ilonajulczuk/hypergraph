"""HyperGraph implementation based on networkx Graph"""
import networkx as nx


class HyperGraph(nx.Graph):
    """HyperGraph representing hypergraph. """

    def __init__(self, *args, **kwargs):
        """@todo: to be defined1. """
        super().__init__(*args, **kwargs)
        self.hyperedge = []
        self.hadj = {}

    def add_edge(self, edge, attr_dict=None, **attr):
        """Add an hyperedge between nodes.

        Parameters
        ----------
        edge : list of nodes
            Nodes can be, for example, strings or numbers.
            Nodes must be hashable (and not None) Python objects.
        key : hashable identifier, optional (default=lowest unused integer)
            Used to distinguish multiedges between a pair of nodes.
        attr_dict : dictionary, optional (default= no attributes)
            Dictionary of edge attributes.  Key/value pairs will
            update existing data associated with the edge.
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.

        See Also
        --------
        add_edges_from : add a collection of edges

        Notes
        -----
        To replace/update edge data, use the optional key argument
        to identify a unique edge.  Otherwise a new edge will be created.

        Examples
        --------
        The following all add the edge e=(1,2) to graph G:

        >>> G = nx.Graph()   # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> e = (1, 2, 4)
        >>> G.add_edge(*e)             # single edge as tuple of two nodes
        >>> G.add_edges_from( [(1,2), (1, 2, 3)] ) # add edges from iterable

        Associate data to edges using keywords:

        >>> G.add_edge((1, 2), weight=3)
        >>> G.add_edge((1, 2), weight=4)   # update data for key=0
        >>> G.add_edge((1, 3, 4), weight=7, capacity=15, length=342.7)
        """

        edge = set(edge)
        # set up attribute dict
        if attr_dict is None:
            attr_dict = attr
        else:
            try:
                attr_dict.update(attr)
            except AttributeError:
                raise nx.NetworkXError(
                    "The attr_dict argument must be a dictionary.")
        # add nodes
        for node in edge:
            if node not in self.adj:
                self.adj[node] = {}
                self.node[node] = {}
            for v in set(edge) - set([node]):
                datadict = self.adj[node].get(v, {})
                datadict.update(attr_dict)
                self.adj[node][v] = datadict
                self.adj[v][node] = datadict

        new_edge_index = len(self.hyperedge)
        self.hyperedge.append(set(edge))
        self.hadj[new_edge_index] = {}

        for i, old_edge in enumerate(self.hyperedge):
            if i != new_edge_index:
                self.hadj[i][new_edge_index] = len(edge & old_edge)
                self.hadj[new_edge_index][i] = self.hadj[i][new_edge_index]

    def add_edges_from(self, ebunch, attr_dict=None, **attr):
        """Add all the edges in ebunch.

        Parameters
        ----------
        ebunch : container of edges
            Each edge given in the container will be added to the
            graph. The edges can be arbitrary long collection of nodes.

        attr_dict : dictionary, optional  (default= no attributes)
            Dictionary of edge attributes.  Key/value pairs will
            update existing data associated with each edge.
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.


        See Also
        --------
        add_edge : add a single edge

        Notes
        -----
        Adding the same edge twice has no effect but any edge data
        will be updated when each duplicate edge is added.

        Examples
        --------
        >>> G = nx.Graph()   # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.add_edges_from([(0,1),(1,2)]) # using a list of edge tuples
        >>> e = zip(range(0,3),range(1,4))
        >>> G.add_edges_from(e) # Add the path graph 0-1-2-3

        Associate data to edges

        >>> G.add_edges_from([(1,2),(2,3)], weight=3)
        >>> G.add_edges_from([(3,4),(1,4)], label='WN2898')
        """
        # set up attribute dict
        if attr_dict is None:
            attr_dict = attr
        else:
            try:
                attr_dict.update(attr)
            except AttributeError:
                raise nx.NetworkXError(
                    "The attr_dict argument must be a dictionary.")
        # process ebunch
        for e in ebunch:
            self.add_edge(e, attr_dict=attr_dict)

    def has_edge(self, edge):
        """Return True if the graph has an edge between with nodes.

        Parameters
        ----------
        edge : collection of nodes
            Nodes can be, for example, strings or numbers.

        Returns
        -------
        edge_ind : bool
            True if edge is in the graph, False otherwise.

        Examples
        --------
        Can be called either using arbitrary long collection of nodes.

        >>> G = nx.HyperGraph()
        >>> G.add_path([0, 1, 2, 3])
        >>> G.has_edge(0, 1, 2, 3)
        True
        >>> e = (0, 1, 2, 3)
        >>> G.has_edge(*e)  #  e is a 2-tuple (u,v)
        True

        The following syntax are equivalent:

        >>> G.has_edge(0,1)
        True
        >>> 1 in G[0]  # though this gives KeyError if 0 not in G
        True

        """
        return set(edge) in self.hyperedge

    def hyper_edges(self):
        """Hyper_edges of a hypegraph"""
        return self.hyperedge

    def hyper_edges_iter(self):
        """Return iterator of hyper_edges"""
        for edge in self.hyperedge:
            yield edge

    def remove_edge(self, e):
        """Remove the edge with nodes as in e.

        Parameters
        ----------
        e: collection of nodes
            Remove the edge between nodes in e.

        Raises
        ------
        NetworkXError
            If there isn't such edge as e.

        See Also
        --------
        remove_edges_from : remove a collection of edges

        Examples
        --------
        >>> HG = HyperGraph()   # or DiGraph, etc
        >>> HG.add_nodes([0,1,2,3])
        >>> HG.add_edge((0, 1, 2))
        >>> e = (0, 1, 2)
        >>> HG.remove_edge(*e) # unpacks e from an edge tuple
        >>> e = (2,3,{'weight':7}) # an edge with attribute data
        """
        try:
            self.hyperedge.remove(set(e))
        except ValueError:
            raise nx.NetworkXError("The edge %s is not in the hypergraph" % (e))

    def remove_edges_from(self, ebunch):
        """Remove all edges specified in ebunch.

        Parameters
        ----------
        ebunch: list or container of edge tuples
            Each edge given in the list or container will be removed
            from the graph.

        See Also
        --------
        remove_edge : remove a single edge

        Notes
        -----
        Will fail silently if an edge in ebunch is not in the graph.

        Examples
        --------
        >>> HG = HyperGraph()   # or DiGraph, etc
        >>> HG.add_nodes([0,1,2,3])
        >>> HG.add_edge((0, 1, 2))
        >>> HG.add_edge((1, 3))
        >>> e = (0, 1, 2)
        >>> ebunch=[(0, 1, 2),(1, 3)]
        >>> HG.remove_edges_from(ebunch)
        """
        for e in ebunch:
            self.remove_edge(e)


