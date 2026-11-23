from collections import defaultdict, deque
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Transfer:
    transaction_id: str
    source_account: str
    target_account: str
    amount: float
    currency: str
    timestamp: float


WINDOW = 3600
LIMIT = 32


class History:
    def __init__(self):
        self.edges = defaultdict(deque)

    def add(self, event):
        for node in dict.fromkeys((event.source_account, event.target_account)):
            self.edges[node].append(event)

    def adjacent(self, node, timestamp):
        edges = self.edges[node]
        while edges and edges[0].timestamp < timestamp - WINDOW:
            edges.popleft()
        return sorted((edge for edge in edges if timestamp - WINDOW <= edge.timestamp < timestamp),
                      key=lambda edge: (edge.timestamp, edge.transaction_id))[-LIMIT:]


def inspect(event, adjacent, fast_only_when_clean=False, adjacent_many=None):
    source, target, now = event.source_account, event.target_account, event.timestamp
    roots = list(dict.fromkeys((source, target)))
    nodes = roots.copy()
    cache = {}

    def prefetch(items):
        if adjacent_many:
            missing = list(dict.fromkeys(node for node in items if node not in cache))
            if missing:
                cache.update(adjacent_many(missing, now))

    def neighbors(node):
        if node not in cache:
            cache[node] = adjacent(node, now)
        return cache[node]

    prefetch(roots)
    outgoing = [edge for edge in neighbors(source) if edge.source_account == source]
    incoming = [edge for edge in neighbors(target) if edge.target_account == target]
    hits = []
    if len({target, *(edge.target_account for edge in outgoing)}) >= 3:
        hits.append("fan_out")
    if len({source, *(edge.source_account for edge in incoming)}) >= 3:
        hits.append("fan_in")
    next_nodes = {edge.target_account for edge in neighbors(target) if edge.source_account == target}
    if source not in next_nodes:
        prefetch(next_nodes)
    if source in next_nodes or any(
        edge.source_account == node and edge.target_account == source
        for node in next_nodes for edge in neighbors(node)
    ):
        hits.append("cycle")
    if any(edge.target_account == source and now - edge.timestamp <= 60
           for edge in neighbors(source)):
        hits.append("pass_through")
    if not hits and fast_only_when_clean:
        edges = {edge.transaction_id: edge for node in roots for edge in neighbors(node)}
        return roots, list(edges.values()), [], [], [], hits
    edges = {}
    for depth in range(2):
        prefetch(nodes)
        for node in nodes.copy():
            for edge in neighbors(node):
                edges[edge.transaction_id] = edge
                if depth == 0:
                    for endpoint in (edge.source_account, edge.target_account):
                        if endpoint not in nodes and len(nodes) < LIMIT:
                            nodes.append(endpoint)
    node_features = []
    for node in nodes:
        history = neighbors(node)
        inbound = [edge for edge in history if edge.target_account == node]
        outbound = [edge for edge in history if edge.source_account == node]
        node_features.append([
            math.log1p(len(inbound)), math.log1p(len(outbound)),
            math.log1p(sum(edge.amount for edge in inbound if edge.currency == event.currency)),
            math.log1p(sum(edge.amount for edge in outbound if edge.currency == event.currency)),
        ])
    index = {node: position for position, node in enumerate(nodes)}
    links = [(index[edge.source_account], index[edge.target_account])
             for edge in edges.values()
             if edge.source_account in index and edge.target_account in index]
    candidate = [math.log1p(event.amount), *(float(rule in hits)
                 for rule in ("fan_out", "fan_in", "cycle", "pass_through"))]
    return nodes, list(edges.values()), node_features, links, candidate, hits
