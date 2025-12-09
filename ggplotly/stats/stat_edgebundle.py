"""
Force-Directed Edge Bundling Statistical Transformation

Based on Holten & Van Wijk (2009) algorithm.
Re-implementation from edgebundleexample with vectorized operations.
"""

import numpy as np
import pandas as pd
from scipy import sparse
from typing import Optional


def _euclidean_distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return np.sqrt(np.sum((p1 - p2) ** 2, axis=-1))


def _edge_length(p1, p2, eps=1e-8):
    """Calculate edge length with epsilon threshold."""
    dist = _euclidean_distance(p1, p2)
    return np.where(dist < eps, eps, dist)


def _edge_as_vector(edges):
    """
    Convert edges to vectors.
    edges: shape (n_edges, 4) where each row is [x1, y1, x2, y2]
    Returns: shape (n_edges, 2) direction vectors
    """
    return edges[:, 2:4] - edges[:, 0:2]


def _angle_compatibility(edges):
    """
    Compute angle compatibility between all pairs of edges (vectorized).
    Returns: (n_edges, n_edges) matrix
    """
    # Get edge vectors
    vectors = _edge_as_vector(edges)  # (n, 2)

    # Compute all pairwise dot products
    dot_products = vectors @ vectors.T  # (n, n)

    # Compute edge lengths
    lengths = np.sqrt((vectors ** 2).sum(axis=1))  # (n,)
    length_products = lengths[:, None] * lengths[None, :]  # (n, n)

    # Avoid division by zero
    length_products = np.where(length_products < 1e-8, 1e-8, length_products)

    return np.abs(dot_products / length_products)


def _scale_compatibility(edges):
    """
    Compute scale compatibility between all pairs of edges (vectorized).
    Returns: (n_edges, n_edges) matrix
    """
    # Compute edge lengths
    p_source = edges[:, 0:2]
    p_target = edges[:, 2:4]
    lengths = _euclidean_distance(p_source, p_target)  # (n,)

    # Create pairwise combinations
    l_i = lengths[:, None]  # (n, 1)
    l_j = lengths[None, :]  # (1, n)

    l_avg = (l_i + l_j) / 2.0
    l_min = np.minimum(l_i, l_j)
    l_max = np.maximum(l_i, l_j)

    return 2.0 / (l_avg / l_min + l_max / l_avg)


def _position_compatibility(edges):
    """
    Compute position compatibility between all pairs of edges (vectorized).
    Returns: (n_edges, n_edges) matrix
    """
    # Compute midpoints
    p_source = edges[:, 0:2]
    p_target = edges[:, 2:4]
    midpoints = (p_source + p_target) / 2.0  # (n, 2)

    # Compute edge lengths
    lengths = _euclidean_distance(p_source, p_target)  # (n,)

    # Compute pairwise distances between midpoints
    mid_diffs = midpoints[:, None, :] - midpoints[None, :, :]
    mid_distances = np.sqrt((mid_diffs ** 2).sum(axis=2))  # (n, n)

    # Average lengths
    l_avg = (lengths[:, None] + lengths[None, :]) / 2.0

    return l_avg / (l_avg + mid_distances)


def _project_point_on_line(point, line):
    """
    Project a point onto a line defined by two endpoints.
    point: (2,) or (n, 2)
    line: (4,) [x1, y1, x2, y2]
    """
    x1, y1, x2, y2 = line
    px, py = point[..., 0], point[..., 1]

    L_sq = (x2 - x1) ** 2 + (y2 - y1) ** 2
    if L_sq < 1e-10:
        return np.array([x1, y1])

    r = ((y1 - py) * (y1 - y2) - (x1 - px) * (x2 - x1)) / L_sq

    proj_x = x1 + r * (x2 - x1)
    proj_y = y1 + r * (y2 - y1)

    return np.stack([proj_x, proj_y], axis=-1)


def _edge_visibility(edge_p, edge_q):
    """Compute visibility between two edges."""
    q_source = edge_q[0:2]
    q_target = edge_q[2:4]

    I0 = _project_point_on_line(q_source, edge_p)
    I1 = _project_point_on_line(q_target, edge_p)

    mid_I = (I0 + I1) / 2.0
    mid_P = (edge_p[0:2] + edge_p[2:4]) / 2.0

    dist_mids = _euclidean_distance(mid_P, mid_I)
    dist_I = _euclidean_distance(I0, I1)

    if dist_I < 1e-8:
        return 0.0

    visibility = 1.0 - 2.0 * dist_mids / dist_I
    return max(0.0, visibility)


def _compute_visibility_batch(edges, candidate_pairs):
    """
    Compute visibility for a batch of candidate edge pairs (vectorized).

    Parameters
    ----------
    edges : np.ndarray
        Shape (n_edges, 4) - [x1, y1, x2, y2] for each edge
    candidate_pairs : np.ndarray
        Shape (n_pairs, 2) - pairs of edge indices to compute

    Returns
    -------
    np.ndarray
        Shape (n_pairs,) - visibility values for each pair
    """
    if len(candidate_pairs) == 0:
        return np.array([])

    i_indices = candidate_pairs[:, 0]
    j_indices = candidate_pairs[:, 1]

    # Get edge data for all pairs
    edges_i = edges[i_indices]  # (n_pairs, 4)
    edges_j = edges[j_indices]  # (n_pairs, 4)

    # Compute visibility i->j
    vis_ij = _visibility_directed_batch(edges_i, edges_j)

    # Compute visibility j->i
    vis_ji = _visibility_directed_batch(edges_j, edges_i)

    # Return minimum
    return np.minimum(vis_ij, vis_ji)


def _visibility_directed_batch(edges_p, edges_q):
    """Compute directed visibility from edges_p to edges_q (vectorized)."""
    # edges_p, edges_q: shape (n_pairs, 4)

    # Extract points
    p_source = edges_p[:, 0:2]  # (n, 2)
    p_target = edges_p[:, 2:4]  # (n, 2)
    q_source = edges_q[:, 0:2]  # (n, 2)
    q_target = edges_q[:, 2:4]  # (n, 2)

    # Project q endpoints onto p
    I0 = _project_points_on_lines_batch(q_source, edges_p)  # (n, 2)
    I1 = _project_points_on_lines_batch(q_target, edges_p)  # (n, 2)

    mid_I = (I0 + I1) / 2.0
    mid_P = (p_source + p_target) / 2.0

    dist_mids = np.sqrt(((mid_P - mid_I) ** 2).sum(axis=1))
    dist_I = np.sqrt(((I0 - I1) ** 2).sum(axis=1))

    # Handle small distances
    visibility = np.where(
        dist_I < 1e-8,
        0.0,
        1.0 - 2.0 * dist_mids / dist_I
    )

    return np.maximum(0.0, visibility)


def _project_points_on_lines_batch(points, lines):
    """
    Project multiple points onto multiple lines (vectorized).

    Parameters
    ----------
    points : np.ndarray
        Shape (n, 2) - points to project
    lines : np.ndarray
        Shape (n, 4) - lines as [x1, y1, x2, y2]

    Returns
    -------
    np.ndarray
        Shape (n, 2) - projected points
    """
    x1 = lines[:, 0]
    y1 = lines[:, 1]
    x2 = lines[:, 2]
    y2 = lines[:, 3]
    px = points[:, 0]
    py = points[:, 1]

    L_sq = (x2 - x1) ** 2 + (y2 - y1) ** 2

    # Handle degenerate lines
    r = np.where(
        L_sq < 1e-10,
        0.0,
        ((y1 - py) * (y1 - y2) - (x1 - px) * (x2 - x1)) / L_sq
    )

    proj_x = x1 + r * (x2 - x1)
    proj_y = y1 + r * (y2 - y1)

    return np.stack([proj_x, proj_y], axis=1)


def _compute_compatibility_matrix(edges, compatibility_threshold=0.6, verbose=True):
    """
    Compute full compatibility matrix and return as sparse matrix.

    Optimized with early filtering: only computes expensive visibility
    for edge pairs that pass cheap compatibility tests first.
    """
    n = len(edges)

    if verbose:
        print("Computing angle compatibility...")
    angle_compat = _angle_compatibility(edges)

    if verbose:
        print("Computing scale compatibility...")
    scale_compat = _scale_compatibility(edges)

    if verbose:
        print("Computing position compatibility...")
    position_compat = _position_compatibility(edges)

    # Early filtering before expensive visibility computation
    if verbose:
        print("Filtering candidate pairs...")
    candidates = (angle_compat >= compatibility_threshold) & \
                 (scale_compat >= compatibility_threshold) & \
                 (position_compat >= compatibility_threshold)

    # Get candidate pairs as array of indices
    candidate_i, candidate_j = np.where(np.triu(candidates, k=1))
    candidate_pairs = np.column_stack([candidate_i, candidate_j])
    n_candidates = len(candidate_pairs)

    total_pairs = n * (n - 1) // 2
    if verbose:
        print(f"Computing visibility for {n_candidates:,} candidate pairs (out of {total_pairs:,} total)")
        if total_pairs > 0:
            print(f"Filtered out {total_pairs - n_candidates:,} pairs ({(1 - n_candidates/total_pairs)*100:.1f}%)")

    # Compute visibility for all candidate pairs at once (vectorized)
    visibility_compat = np.ones((n, n))

    if n_candidates > 0:
        vis_values = _compute_visibility_batch(edges, candidate_pairs)
        visibility_compat[candidate_i, candidate_j] = vis_values
        visibility_compat[candidate_j, candidate_i] = vis_values

    np.fill_diagonal(visibility_compat, 1.0)

    if verbose:
        print("Computing final compatibility scores...")
    compatibility = angle_compat * scale_compat * position_compat * visibility_compat

    # Apply threshold
    compatibility[compatibility < compatibility_threshold] = 0

    # Zero out diagonal
    np.fill_diagonal(compatibility, 0)

    return sparse.csr_matrix(compatibility)


def _update_edge_divisions(edge_list, P):
    """Update edge divisions to have P+2 points (including endpoints)."""
    new_edge_list = []

    for edge_points in edge_list:
        if P == 1:
            new_points = np.zeros((3, 2))
            new_points[0] = edge_points[0]
            new_points[1] = (edge_points[0] + edge_points[-1]) / 2.0
            new_points[2] = edge_points[-1]
        else:
            segments = edge_points[1:] - edge_points[:-1]
            segment_lengths = np.sqrt((segments ** 2).sum(axis=1))
            total_length = segment_lengths.sum()

            target_segment_length = total_length / (P + 1)

            new_points = np.zeros((P + 2, 2))
            new_points[0] = edge_points[0]
            new_points[-1] = edge_points[-1]

            current_pos = edge_points[0].copy()
            current_segment_idx = 0
            remaining_in_segment = segment_lengths[0]

            for i in range(1, P + 1):
                distance_needed = target_segment_length

                while distance_needed > remaining_in_segment and current_segment_idx < len(edge_points) - 2:
                    distance_needed -= remaining_in_segment
                    current_segment_idx += 1
                    current_pos = edge_points[current_segment_idx].copy()
                    remaining_in_segment = segment_lengths[current_segment_idx]

                if current_segment_idx < len(edge_points) - 1:
                    direction = edge_points[current_segment_idx + 1] - edge_points[current_segment_idx]
                    direction_length = segment_lengths[current_segment_idx]
                    if direction_length > 1e-8:
                        direction = direction / direction_length
                        new_points[i] = current_pos + distance_needed * direction
                        current_pos = new_points[i]
                        remaining_in_segment -= distance_needed
                    else:
                        new_points[i] = current_pos
                else:
                    new_points[i] = edge_points[-1]

        new_edge_list.append(new_points)

    return new_edge_list


def _apply_spring_forces_vectorized(edge_points, kP):
    """Apply spring forces to all internal points at once (vectorized)."""
    n_points = len(edge_points)
    forces = np.zeros((n_points, 2))

    if n_points <= 2:
        return forces

    prev_points = edge_points[:-2]
    curr_points = edge_points[1:-1]
    next_points = edge_points[2:]

    forces[1:-1] = kP * ((prev_points - curr_points) + (next_points - curr_points))

    return forces


def _apply_electrostatic_forces_all_points(edge_list, compatible_indices_list, edge_idx, n_points, weights=None, eps=1e-8):
    """
    Apply electrostatic forces to all internal points of an edge at once.

    Following the FDEB paper (Holten & Van Wijk 2009), the electrostatic force
    is the sum of unit direction vectors toward compatible edge points.

    Parameters
    ----------
    edge_list : list of np.ndarray
        List of edge point arrays
    compatible_indices_list : list of np.ndarray
        Pre-computed compatible edge indices for each edge
    edge_idx : int
        Index of the current edge
    n_points : int
        Number of points in the edge
    weights : np.ndarray, optional
        Normalized edge weights. Heavier edges attract more strongly.
    eps : float
        Small value to avoid division by zero
    """
    compatible_indices = compatible_indices_list[edge_idx]

    # Pre-allocate result for all internal points
    forces = np.zeros((n_points, 2))

    if len(compatible_indices) == 0:
        return forces

    edge_points = edge_list[edge_idx]

    # Get weights for compatible edges (default to 1.0)
    if weights is not None:
        compat_weights = weights[compatible_indices, np.newaxis]  # (n_compat, 1)
    else:
        compat_weights = 1.0

    # Process all internal points (1 to n_points-1)
    for i in range(1, n_points - 1):
        curr_point = edge_points[i]
        other_points = np.array([edge_list[idx][i] for idx in compatible_indices])

        diff = other_points - curr_point
        dists = np.linalg.norm(diff, axis=1, keepdims=True)
        dists = np.maximum(dists, eps)

        # Sum of unit direction vectors toward compatible points, weighted by edge weight
        forces[i] = (compat_weights * diff / dists).sum(axis=0)

    return forces


def _precompute_compatible_indices(compatibility_matrix, n_edges):
    """Pre-compute compatible indices for each edge to avoid repeated sparse lookups."""
    compatible_indices_list = []
    for i in range(n_edges):
        indices = compatibility_matrix[i].nonzero()[1]
        compatible_indices_list.append(indices)
    return compatible_indices_list


class stat_edgebundle:
    """
    Statistical transformation for force-directed edge bundling.

    Transforms edge data (x, y, xend, yend) into bundled paths using
    the Holten & Van Wijk (2009) algorithm.

    Parameters
    ----------
    K : float, default=1.0
        Spring constant controlling edge stiffness (resists bundling).
    E : float, default=1.0
        Electrostatic constant controlling bundling attraction strength.
        Higher values increase bundling, lower values decrease it.
    C : int, default=6
        Number of iteration cycles
    P : int, default=1
        Initial number of edge subdivisions
    S : float, default=0.04
        Initial step size
    P_rate : int, default=2
        Rate of subdivision increase per cycle
    I : int, default=50
        Initial iterations per cycle
    I_rate : float, default=2/3
        Rate of iteration decrease per cycle
    compatibility_threshold : float, default=0.6
        Threshold for edge compatibility (0-1)
    verbose : bool, default=True
        Print progress messages

    Examples
    --------
    >>> stat = stat_edgebundle(compatibility_threshold=0.6)
    >>> bundled = stat.compute(edges_df)

    >>> # With edge weights
    >>> stat = stat_edgebundle()
    >>> bundled = stat.compute(edges_df, weights=edges_df['weight'])
    """

    def __init__(
        self,
        K: float = 1.0,
        E: float = 1.0,
        C: int = 6,
        P: int = 1,
        S: float = 0.04,
        P_rate: int = 2,
        I: int = 50,
        I_rate: float = 2/3,
        compatibility_threshold: float = 0.6,
        verbose: bool = True
    ):
        self.K = K
        self.E = E
        self.C = C
        self.P = P
        self.S = S
        self.P_rate = P_rate
        self.I = I
        self.I_rate = I_rate
        self.compatibility_threshold = compatibility_threshold
        self.verbose = verbose

        # Cache for computed results
        self._cached_result = None
        self._cached_data_hash = None

    def _compute_data_hash(self, data: pd.DataFrame, weights: Optional[np.ndarray] = None) -> int:
        """Compute a hash of the input data for cache invalidation."""
        weight_hash = weights.tobytes() if weights is not None else b''
        return hash((
            data.shape,
            data['x'].values.tobytes(),
            data['y'].values.tobytes(),
            data['xend'].values.tobytes(),
            data['yend'].values.tobytes(),
            weight_hash,
        ))

    def _normalize_weights(self, weights: np.ndarray) -> np.ndarray:
        """
        Normalize weights to [0.5, 1.5] range.

        This preserves relative differences while preventing extreme values
        from dominating the force simulation.
        """
        w_min, w_max = weights.min(), weights.max()
        if w_max - w_min < 1e-8:
            # All weights are the same, return uniform weights
            return np.ones_like(weights)
        return 0.5 + (weights - w_min) / (w_max - w_min)

    def compute(self, data: pd.DataFrame, weights: Optional[np.ndarray] = None) -> pd.DataFrame:
        """
        Apply edge bundling transformation.

        Parameters
        ----------
        data : pd.DataFrame
            Must contain columns: x, y, xend, yend
        weights : np.ndarray, optional
            Edge weights. Heavier edges attract compatible edges more strongly,
            causing them to bundle toward high-traffic routes. Weights are
            normalized to [0.5, 1.5] range internally.

        Returns
        -------
        pd.DataFrame
            Bundled edge paths with columns: x, y, index, group
        """
        # Validate input
        required = ['x', 'y', 'xend', 'yend']
        missing = [col for col in required if col not in data.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        # Convert weights to numpy array if provided
        if weights is not None:
            weights = np.asarray(weights, dtype=np.float64)
            if len(weights) != len(data):
                raise ValueError(f"weights length ({len(weights)}) must match data length ({len(data)})")

        # Check cache
        data_hash = self._compute_data_hash(data, weights)
        if self._cached_result is not None and self._cached_data_hash == data_hash:
            if self.verbose:
                print("Using cached bundling result")
            return self._cached_result

        # Normalize weights if provided
        normalized_weights = None
        if weights is not None:
            normalized_weights = self._normalize_weights(weights)
            if self.verbose:
                print(f"Using edge weights (range: {weights.min():.2f} - {weights.max():.2f})")

        # Convert to numpy array format
        edges_xy = np.column_stack([
            data['x'].values,
            data['y'].values,
            data['xend'].values,
            data['yend'].values
        ])

        result = self._bundle_edges(edges_xy, normalized_weights)

        # Cache the result
        self._cached_result = result
        self._cached_data_hash = data_hash

        return result

    def _bundle_edges(self, edges_xy: np.ndarray, weights: Optional[np.ndarray] = None) -> pd.DataFrame:
        """Core bundling algorithm."""
        n_edges = len(edges_xy)
        eps = 1e-8

        if self.verbose:
            print(f"Bundling {n_edges} edges...")

        # Initialize edge subdivision list
        edge_list = [np.array([edge[0:2], edge[2:4]]) for edge in edges_xy]

        # First division
        P = self.P
        if self.verbose:
            print(f"Initial edge division (P={P})...")
        edge_list = _update_edge_divisions(edge_list, P)

        # Compute compatibility matrix
        compatibility_matrix = _compute_compatibility_matrix(
            edges_xy, self.compatibility_threshold, self.verbose
        )
        if self.verbose:
            print(f"Compatibility matrix: {compatibility_matrix.nnz} compatible pairs")

        # Pre-compute compatible indices once (avoids repeated sparse matrix lookups)
        compatible_indices_list = _precompute_compatible_indices(compatibility_matrix, n_edges)

        # Main bundling loop
        S = self.S
        I = self.I

        for cycle in range(self.C):
            if self.verbose:
                print(f"Cycle {cycle + 1}/{self.C}: I={int(I)}, P={P}, S={S:.4f}")

            for _ in range(int(I)):
                forces_list = []
                for e_idx in range(n_edges):
                    edge_points = edge_list[e_idx]
                    n_points = len(edge_points)

                    edge_len = _edge_length(edge_points[0], edge_points[-1], eps)
                    kP = self.K / (edge_len * (P + 1))

                    spring_forces = _apply_spring_forces_vectorized(edge_points, kP)
                    electro_forces = _apply_electrostatic_forces_all_points(
                        edge_list, compatible_indices_list, e_idx, n_points, weights, eps
                    )

                    forces = S * (spring_forces + self.E * electro_forces)
                    forces_list.append(forces)

                for e_idx in range(n_edges):
                    edge_list[e_idx] = edge_list[e_idx] + forces_list[e_idx]

            # Prepare for next cycle
            if cycle < self.C - 1:
                S = S / 2.0
                P = P * self.P_rate
                I = int(I * self.I_rate)
                if self.verbose:
                    print(f"Updating subdivisions (new P={P})...")
                edge_list = _update_edge_divisions(edge_list, P)

        # Assemble output dataframe
        if self.verbose:
            print("Assembling output...")
        segments = len(edge_list[0])
        index_values = np.linspace(0, 1, segments)

        all_x = np.concatenate([edge[:, 0] for edge in edge_list])
        all_y = np.concatenate([edge[:, 1] for edge in edge_list])
        all_index = np.tile(index_values, n_edges)
        all_group = np.repeat(np.arange(n_edges), segments)

        result_df = pd.DataFrame({
            'x': all_x,
            'y': all_y,
            'index': all_index,
            'group': all_group
        })

        if self.verbose:
            print("Done!")
        return result_df
