import torch
from torch import nn

try:
    from torch_geometric.nn import DenseSAGEConv
except ImportError:
    class DenseSAGEConv(nn.Module):
        """Mean aggregation with the same weights as PyG DenseSAGEConv."""

        def __init__(self, channels, output):
            super().__init__()
            self.lin_rel = nn.Linear(channels, output, bias=False)
            self.lin_root = nn.Linear(channels, output)

        def forward(self, features, adjacency):
            mean = (adjacency @ features) / adjacency.sum(-1, keepdim=True).clamp_min(1)
            return self.lin_rel(mean) + self.lin_root(features)


class GraphSAGE(nn.Module):
    def __init__(self):
        super().__init__()
        self.first = DenseSAGEConv(4, 32)
        self.second = DenseSAGEConv(32, 32)
        self.head = nn.Sequential(nn.Linear(69, 32), nn.ReLU(), nn.Linear(32, 1))

    def forward(self, features, adjacency, candidate):
        embedding = self.first(features, adjacency).relu()
        embedding = self.second(embedding, adjacency).relu()
        return self.head(torch.cat((embedding[:, 0], embedding[:, 1], candidate), dim=1))


class Calibrated(nn.Module):
    def __init__(self, model, slope, intercept):
        super().__init__()
        self.model = model
        self.register_buffer("slope", torch.tensor(slope))
        self.register_buffer("intercept", torch.tensor(intercept))

    def forward(self, features, adjacency, candidate):
        logits = self.model(features, adjacency, candidate)
        return (logits * self.slope + self.intercept).sigmoid()
