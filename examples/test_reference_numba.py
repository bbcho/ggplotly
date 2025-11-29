#!/usr/bin/env python
"""Run the reference Numba implementation to see what it produces"""

from numba import jitclass, float32, jit, prange, float64, njit
from numba.typed import List
from numba.types import ListType, int16, uint8
import math
import numpy as np
import pandas as pd

# Hyper-parameters from reference
K = 0.1
S_initial = 0.1
P_initial = 1
P_rate = 2
C = 6
I_initial = 90
I_rate = 0.6666667
compatibility_threshold = 0.6
eps = 1e-6

@jitclass([('x', float32), ('y', float32)])
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

@jitclass([('source', Point.class_type.instance_type), ('target', Point.class_type.instance_type)])
class Edge:
    def __init__(self, source, target):
        self.source = source
        self.target = target

ForceFactors = Point

@jit(Point.class_type.instance_type(Edge.class_type.instance_type), nopython=True, nogil=True)
def edge_as_vector(edge):
    return Point(edge.target.x - edge.source.x, edge.target.y - edge.source.y)

@jit(float32(Edge.class_type.instance_type), nopython=True, nogil=True)
def edge_length(edge):
    if (abs(edge.source.x - edge.target.x)) < eps and (abs(edge.source.y - edge.target.y)) < eps:
        return eps
    return math.sqrt(math.pow(edge.source.x - edge.target.x, 2) + math.pow(edge.source.y - edge.target.y, 2))

@jit(float32(Edge.class_type.instance_type, Edge.class_type.instance_type), nopython=True, nogil=True)
def angle_compatibility(edge, oedge):
    v1 = edge_as_vector(edge)
    v2 = edge_as_vector(oedge)
    dot_product = v1.x * v2.x + v1.y * v2.y
    return math.fabs(dot_product / (edge_length(edge) * edge_length(oedge)))

@jit(float32(Edge.class_type.instance_type, Edge.class_type.instance_type), nopython=True, nogil=True)
def scale_compatibility(edge, oedge):
    lavg = (edge_length(edge) + edge_length(oedge)) / 2.0
    return 2.0 / (lavg/min(edge_length(edge), edge_length(oedge)) + max(edge_length(edge), edge_length(oedge))/lavg)

@jit(float32(Point.class_type.instance_type, Point.class_type.instance_type), nopython=True, nogil=True)
def euclidean_distance(source, target):
    return math.sqrt(math.pow(source.x - target.x, 2) + math.pow(source.y - target.y, 2))

@jit(float32(Edge.class_type.instance_type, Edge.class_type.instance_type), nopython=True, nogil=True)
def position_compatibility(edge, oedge):
    lavg = (edge_length(edge) + edge_length(oedge)) / 2.0
    midP = Point((edge.source.x + edge.target.x) / 2.0,
            (edge.source.y + edge.target.y) / 2.0)
    midQ = Point((oedge.source.x + oedge.target.x) / 2.0,
                 (oedge.source.y + oedge.target.y) / 2.0)
    return lavg / (lavg + euclidean_distance(midP, midQ))

@jit(Point.class_type.instance_type(Point.class_type.instance_type, Edge.class_type.instance_type), nopython=True, nogil=True)
def project_point_on_line(point, edge):
    L = math.sqrt(math.pow(edge.target.x - edge.source.x, 2) + math.pow((edge.target.y - edge.source.y), 2))
    r = ((edge.source.y - point.y) * (edge.source.y - edge.target.y) - (edge.source.x - point.x) * (edge.target.x - edge.source.x)) / math.pow(L, 2)
    return Point((edge.source.x + r * (edge.target.x - edge.source.x)),
                 (edge.source.y + r * (edge.target.y - edge.source.y)))

@jit(float32(Edge.class_type.instance_type, Edge.class_type.instance_type), nopython=True, nogil=True)
def edge_visibility(edge, oedge):
    I0 = project_point_on_line(oedge.source, edge)
    I1 = project_point_on_line(oedge.target, edge)
    divisor = euclidean_distance(I0, I1)
    divisor = divisor if divisor != 0 else eps
    midI = Point((I0.x + I1.x) / 2.0, (I0.y + I1.y) / 2.0)
    midP = Point((edge.source.x + edge.target.x) / 2.0,
                 (edge.source.y + edge.target.y) / 2.0)
    return max(0, 1 - 2 * euclidean_distance(midP, midI) / divisor)

@jit(float32(Edge.class_type.instance_type, Edge.class_type.instance_type), nopython=True, nogil=True)
def visibility_compatibility(edge, oedge):
    return min(edge_visibility(edge, oedge), edge_visibility(oedge, edge))

@jit(float32(Edge.class_type.instance_type, Edge.class_type.instance_type), nopython=True)
def are_compatible(edge, oedge):
    score = (angle_compatibility(edge, oedge) * scale_compatibility(edge, oedge) *
             position_compatibility(edge, oedge) * visibility_compatibility(edge, oedge))
    return score >= compatibility_threshold

# Create simple test data
np.random.seed(42)
n_nodes = 20
angles = np.linspace(0, 2*np.pi, n_nodes, endpoint=False)
radius = 1.0

nodes = [(radius * np.cos(a), radius * np.sin(a)) for a in angles]

edge_class = Edge.class_type.instance_type
edges = List.empty_list(edge_class)

# Create 50 edges (not 200, for faster testing)
n_edges_target = 50
while len(edges) < n_edges_target:
    i = np.random.randint(0, n_nodes)
    j = np.random.randint(0, n_nodes)
    if i != j:
        source = Point(float(nodes[i][0]), float(nodes[i][1]))
        target = Point(float(nodes[j][0]), float(nodes[j][1]))
        edges.append(Edge(source, target))

print(f"Created {len(edges)} edges")
print(f"Computing compatibility with threshold={compatibility_threshold}...")

# Compute compatibility
compatibility_list = List()
for _ in edges:
    compatibility_list.append(List.empty_list(int16))

total_edges = len(edges)
for e_idx in range(total_edges - 1):
    for oe_idx in range(e_idx + 1, total_edges):
        if are_compatible(edges[e_idx], edges[oe_idx]):
            compatibility_list[e_idx].append(oe_idx)
            compatibility_list[oe_idx].append(e_idx)

# Print compatibility stats
n_compatible = sum(len(comp_list) for comp_list in compatibility_list)
print(f"Total compatible pairs: {n_compatible // 2}")
print(f"Average compatible neighbors per edge: {n_compatible / len(edges):.1f}")

print("\nReference implementation with threshold=0.6 is very selective!")
print("This is why it doesn't blow up - most edges don't interact.")
