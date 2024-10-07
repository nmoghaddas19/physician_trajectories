import json

i = 6601
filepath = 'NETS 5116 project/data/card/cardiology3/' + str(i) + '.json'
with open(filepath, 'r') as f:
    data = json.load(f)
print(data)
edge_count= 0
institutions = set()
data.get(str(i)).get('training').items() #get('1').keys()
for keys, vals in data.get(str(i)).get('training').items():
    institutions.add(list(vals.keys())[0])
    edge_count = edge_count + 1
for line in data.get(str(i)).get('hospital').items():
    institutions.add(line)
    edge_count = edge_count + 1
    #print(list(vals.keys())[0])


#def count_edges():
    import networkx as nx
    G = nx.Graph()
    edge_count = 0
    institutions = set()
    errors = 0
    while i <= 38970:
        i = i + 1
        if  i <= 6547:
            # count edges in cardiology12
            try:
                filepath = 'NETS 5116 project/data/card/cardiology12/' + str(i) + '.json'
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if data.get(str(i)).get('training'):
                        for keys, vals in data.get(str(i)).get('training').items():
                            institutions.add(list(vals.keys())[0])
                            edge_count = edge_count + 1
                            G.add_edge(i, list(vals.keys())[0])
                        for line in data.get(str(i)).get('hospital'):
                            institutions.add(line)
                            edge_count = edge_count + 1
                            G.add_edge(i, line)
            except Exception as e:
                errors = errors + 1
        elif i <= 10047:
            # count edges in cardiology3
            try:
                filepath = 'NETS 5116 project/data/card/cardiology3/' + str(i) + '.json'
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if data.get(str(i)).get('training'):
                        for keys, vals in data.get(str(i)).get('training').items():
                            institutions.add(list(vals.keys())[0])
                            edge_count = edge_count + 1
                            G.add_edge(i, list(vals.keys())[0])
                        for line in data.get(str(i)).get('hospital'):
                            institutions.add(line)
                            edge_count = edge_count + 1
                            G.add_edge(i, line)
            except Exception as e:
                errors = errors + 1
        elif i <= 15047:
            # count edges in cardiology4
            try:
                filepath = 'NETS 5116 project/data/card/cardiology4/' + str(i) + '.json'
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if data.get(str(i)).get('training'):
                        for keys, vals in data.get(str(i)).get('training').items():
                            institutions.add(list(vals.keys())[0])
                            edge_count = edge_count + 1
                            G.add_edge(i, list(vals.keys())[0])
                        for line in data.get(str(i)).get('hospital'):
                            institutions.add(line)
                            edge_count = edge_count + 1
                            G.add_edge(i, line)
            except Exception as e:
                errors = errors + 1
        elif i <= 26047:
            # count edges in cardiology5
            try:
                filepath = 'NETS 5116 project/data/card/cardiology5/' + str(i) + '.json'
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if data.get(str(i)).get('training'):
                        for keys, vals in data.get(str(i)).get('training').items():
                            institutions.add(list(vals.keys())[0])
                            edge_count = edge_count + 1
                            G.add_edge(i, list(vals.keys())[0])
                        for line in data.get(str(i)).get('hospital'):
                            institutions.add(line)
                            edge_count = edge_count + 1
                            G.add_edge(i, line)
            except Exception as e:
                errors = errors + 1
        else:
            # count edges in cardiology6
            try:
                filepath = 'NETS 5116 project/data/card/cardiology6/' + str(i) + '.json'
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if data.get(str(i)).get('training'):
                        for keys, vals in data.get(str(i)).get('training').items():
                            institutions.add(list(vals.keys())[0])
                            edge_count = edge_count + 1
                            G.add_edge(i, list(vals.keys())[0])
                        for line in data.get(str(i)).get('hospital'):
                            institutions.add(line)
                            edge_count = edge_count + 1
                            G.add_edge(i, line)
            except Exception as e:
                errors = errors + 1

count_edges()

nx.number_connected_components(G)

nx.transitivity(G) # makes sense because its bipartite so theres no triangles

degrees = dict(nx.degree(G))

min(degrees.values())

# find hubs
# plot degree dist
# calc clustering, centrality etc, maybe graph distances between specialties
# randomize

import matplotlib.pyplot as plt
import numpy as np


def degree_distribution(G, number_of_bins=15, log_binning=True, density=True, directed=False):
    """
    Given a degree sequence, return the y values (probability) and the
    x values (support) of a degree distribution that you're going to plot.

    Parameters
    ----------
    G (nx.Graph):
        the network whose degree distribution to calculate

    number_of_bins (int):
        length of output vectors

    log_binning (bool):
        if you are plotting on a log-log axis, then this is useful

    density (bool):
        whether to return counts or probability density (default: True)
        Note: probability densities integrate to 1 but do not sum to 1.

    directed (bool or str):
        if False, this assumes the network is undirected. Otherwise, the
        function requires an 'in' or 'out' as input, which will create the
        in- or out-degree distributions, respectively.

    Returns
    -------
    bins_out, probs (np.ndarray):
        probability density if density=True node counts if density=False; binned edges

    """

    # Step 0: Do we want the directed or undirected degree distribution?
    if directed:
        if directed == 'in':
            k = list(dict(G.in_degree()).values())  # get the in degree of each node
        elif directed == 'out':
            k = list(dict(G.out_degree()).values())  # get the out degree of each node
        else:
            out_error = "Help! if directed!=False, the input needs to be either 'in' or 'out'"
            print(out_error)
            # Question: Is this the correct way to raise an error message in Python?
            #           See "raise" function...
            return out_error
    else:
        k = list(dict(G.degree()).values())  # get the degree of each node

    # Step 1: We will first need to define the support of our distribution
    kmax = np.max(k)  # get the maximum degree
    kmin = 0  # let's assume kmin must be 0

    # Step 2: Then we'll need to construct bins
    if log_binning:
        # array of bin edges including rightmost and leftmost
        bins = np.logspace(0, np.log10(kmax + 1), number_of_bins + 1)
    else:
        bins = np.linspace(0, kmax + 1, num=number_of_bins + 1)

    # Step 3: Then we can compute the histogram using numpy
    probs, _ = np.histogram(k, bins, density=density)

    # Step 4: Return not the "bins" but the midpoint between adjacent bin
    #         values. This is a better way to plot the distribution.
    bins_out = bins[1:] - np.diff(bins) / 2.0

    return bins_out, probs
x, y = degree_distribution(G)

fig, ax = plt.subplots(1,1,figsize=(3,2.5),dpi=200)

ax.loglog(x, y,'o', color='firebrick', alpha=0.8,  ms = 4)

ax.set_xlabel(r"$k$",fontsize='large')
ax.set_ylabel(r"$P(k)$",fontsize='large')
ax.grid(linewidth=0.7, color='#999999', alpha=0.15, linestyle='-')
ax.set_title('Degree Distribution')
plt.show(block=True)
