
##Hypergraph representation

It would be extremely nice to have a HyperGraph class similar
to other network classes in networkx.

However, I still don't have a really good idea of representing
hypergraphs. Probably the best way would be to store nodes and
hyperedges and add other info as some kind of surplus?

My current idea is to inherit after networkx Graph class and provide
similar interface. Basically what it does now is representing hypergraph
as clique on nodes adjacency level (I suspect that multigraph approach
would be better) and as graph of hyper edges.

I need to write more methods and think about this multigraph approach
because it sounds pretty intersting!

##Networkx tutorial thoughts

It was a very simple tutorial!


##Hypergraphs and matroids paper

What is incidence matrix?

Oh, this paper wasn't really good. But it used the book:
Berge-Holland hypergraphs and it looks promising

I have this idea of writing a series of blogposts about
hypergraphs using this book as reference material to understand
it better and promote hypergraphs as a whole. Cool!

##Materials about markov chains from UW

It looks really promising!

Równanie Chapmana-Kołmogorowa - I have no idea, but when I was checking it
with octave it didn't hold!


##Diffusion on markov chains

I really have this specific uncertainty about it. The best way to be sure
is to check it. I'm reading now the ipython notebook on markov chains.

##Time to get wiser?

I downloaded a book about markov chains.

![markov chains](home/att/random_walk_mc.jpeg)

The article/lecture was helpful! It has a theorem with choosing the one element
and powering matrix, yay.

I'll check it with my case. It prooves this theorem with
degree of the node and it's stationary distribution pi!

It should be the case with my hyperedges "degree",
it's easy to check.


It's again a few days/weeks later

##21-04-2014 Tests in hypergraph repository

I think that I should think more about what I do here. There is a lack
of design. It's a bit too much bottom up work.

I have some distinct modules and notebooks. And this is awesome.

I would like to work more on those notebooks to make them tell
complete stories. It's important for my research. I don't want to realize
that, "well, I haven't thought about all those corner cases, and it was
a premature generalization". It's important to think!

To ensure good design and that my software works - I want to introduce
testing to the system.

Tests don't have to be too complicated. I think that python nose
would be good enough.

But what do I want to test? Probably it would be awesome to have every module
tested. I also have those "demo modules" and notebooks. And they should
work well.


