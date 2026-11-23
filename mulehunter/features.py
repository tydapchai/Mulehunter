import numpy as np
from .graph import LIMIT


def encode(snapshot):
    nodes, _, features, links, candidate, _ = snapshot
    x = np.zeros((LIMIT, 4), dtype=np.float32)
    x[:len(nodes)] = features
    adjacency = np.zeros((LIMIT, LIMIT), dtype=np.float32)
    for source, target in links:
        adjacency[target, source] = 1
        adjacency[source, target] = 1
    if len(nodes) == 1:
        x[1] = x[0]
        adjacency[1] = adjacency[0]
    return x, adjacency, np.asarray(candidate, dtype=np.float32)
