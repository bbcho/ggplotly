"""
Force-Directed Edge Bundling for Graph Visualization

Based on:
Holten, D., & Van Wijk, J. J. (2009). Force‐directed edge bundling for graph visualization.
Computer Graphics Forum, 28(3), 983-990.
"""

import logging
import numpy as np
import pandas as pd
from typing import Tuple, List, Dict

logger = logging.getLogger(__name__)


class stat_edgebundle:
    """
    Statistical transformation for force-directed edge bundling.

    Parameters
    ----------
    K : float, default=0.1
        Global spring constant controlling bundling strength
        Higher values = tighter bundling
        Range: 0.05 - 0.15 typically

    cycles : int, default=6
        Number of refinement cycles (subdivision iterations)
        Each cycle doubles the number of subdivision points

    subdivision_points_init : int, default=1
        Initial number of subdivision points (P0)
        Final will be P0 * 2^cycles

    compatibility_threshold : float, default=0.1
        Minimum edge compatibility for interaction
        Range: 0.0 - 1.0 (higher = more selective bundling)

    iterations_per_cycle : int, default=90
        Number of force iterations per subdivision cycle
    """

    def __init__(
        self,
        K: float = 0.1,
        cycles: int = 6,
        subdivision_points_init: int = 1,
        compatibility_threshold: float = 0.6,
        iterations_per_cycle: int = 90,
    ):
        self.K = K
        self.cycles = cycles
        self.P_init = subdivision_points_init
        self.compatibility_threshold = compatibility_threshold
        self.iterations_per_cycle = iterations_per_cycle

    def compute_bundling(
        self,
        edges_df: pd.DataFrame,
        nodes_df: pd.DataFrame = None
    ) -> pd.DataFrame:
        """
        Apply force-directed edge bundling to a set of edges.

        Parameters
        ----------
        edges_df : pd.DataFrame
            Must contain columns: ['x', 'y', 'xend', 'yend']
            Optional: ['edge_id', 'weight']

        nodes_df : pd.DataFrame, optional
            Not required for bundling, but can be used for node positions

        Returns
        -------
        pd.DataFrame
            Bundled edges with subdivision points
            Columns: ['edge_id', 'segment', 'x', 'y']
        """
        # Validate input
        required_cols = ['x', 'y', 'xend', 'yend']
        if not all(col in edges_df.columns for col in required_cols):
            raise ValueError(f"edges_df must contain columns: {required_cols}")

        # Add edge_id if not present
        if 'edge_id' not in edges_df.columns:
            edges_df = edges_df.copy()
            edges_df['edge_id'] = range(len(edges_df))

        n_edges = len(edges_df)

        # Initialize subdivision points for each edge (no normalization - work in original space)
        # Start with P_init points between endpoints
        edges = []
        edge_lengths = []
        for idx, row in edges_df.iterrows():
            x_start = row['x']
            y_start = row['y']
            x_end = row['xend']
            y_end = row['yend']

            edge_points = self._initialize_edge(
                (x_start, y_start),
                (x_end, y_end),
                self.P_init
            )
            # Store initial edge length for spring constant calculation
            initial_length = np.linalg.norm(np.array([x_end, y_end]) - np.array([x_start, y_start]))
            edge_lengths.append(initial_length)
            edges.append({
                'edge_id': row['edge_id'],
                'points': edge_points,  # (P+2) x 2 array including endpoints
                'p0': np.array([x_start, y_start]),
                'p1': np.array([x_end, y_end]),
                'initial_length': initial_length
            })

        # Note: K is used directly without scaling (per reference implementation)
        avg_edge_length = np.mean(edge_lengths) if edge_lengths else 1.0
        logger.debug(f"Average edge length: {avg_edge_length:.2f}, using K={self.K}")

        # Precompute edge compatibility matrix
        logger.debug(f"Computing compatibility for {n_edges} edges...")
        compatibility = self._compute_compatibility_matrix(edges)

        # Iterative refinement: progressive subdivision and force application
        P = self.P_init
        I = self.iterations_per_cycle  # Decreases each cycle per reference implementation
        I_rate = 2.0 / 3.0  # Iteration decay rate

        for cycle in range(self.cycles):
            iterations_this_cycle = int(np.ceil(I))
            print(f"Cycle {cycle+1}/{self.cycles}: P={P}, iterations={iterations_this_cycle}")

            # Apply forces iteratively
            step_size = self._get_step_size(cycle)
            for iteration in range(iterations_this_cycle):
                edges = self._apply_forces(edges, compatibility, step_size, self.K)

            # Decrease iterations for next cycle
            I = I * I_rate

            # Double subdivision points for next cycle (except last)
            if cycle < self.cycles - 1:
                P *= 2
                edges = self._subdivide_edges(edges)

        # Convert bundled edges to output format
        result_rows = []
        for edge in edges:
            edge_id = edge['edge_id']
            points = edge['points']
            for seg_idx, point in enumerate(points):
                result_rows.append({
                    'edge_id': edge_id,
                    'segment': seg_idx,
                    'x': point[0],
                    'y': point[1]
                })

        return pd.DataFrame(result_rows)

    def _initialize_edge(
        self,
        p0: Tuple[float, float],
        p1: Tuple[float, float],
        P: int
    ) -> np.ndarray:
        """
        Initialize edge with P subdivision points between endpoints.

        Returns array of shape (P+2, 2) including both endpoints.
        """
        p0 = np.array(p0)
        p1 = np.array(p1)

        # Linear interpolation
        t = np.linspace(0, 1, P + 2)
        points = p0[np.newaxis, :] + t[:, np.newaxis] * (p1 - p0)[np.newaxis, :]

        return points

    def _compute_compatibility_matrix(self, edges: List[Dict]) -> np.ndarray:
        """
        Compute edge compatibility matrix C_e(P,Q) for all edge pairs.

        C_e = C_a * C_s * C_p * C_v
        where:
        - C_a: angle compatibility
        - C_s: scale compatibility
        - C_p: position compatibility
        - C_v: visibility compatibility
        """
        n = len(edges)
        compatibility = np.zeros((n, n))

        for i in range(n):
            for j in range(i+1, n):
                C_e = self._edge_compatibility(edges[i], edges[j])
                compatibility[i, j] = C_e
                compatibility[j, i] = C_e

        # Set diagonal to 0 (no self-interaction)
        np.fill_diagonal(compatibility, 0)

        # Apply threshold
        compatibility[compatibility < self.compatibility_threshold] = 0

        return compatibility

    def _edge_compatibility(self, edge_P: Dict, edge_Q: Dict) -> float:
        """
        Compute compatibility between two edges.

        Returns value in [0, 1] where 1 = fully compatible.
        """
        p0, p1 = edge_P['p0'], edge_P['p1']
        q0, q1 = edge_Q['p0'], edge_Q['p1']

        # Edge vectors
        P_vec = p1 - p0
        Q_vec = q1 - q0

        # Edge lengths
        l_P = np.linalg.norm(P_vec)
        l_Q = np.linalg.norm(Q_vec)

        # Avoid division by zero
        if l_P < 1e-10 or l_Q < 1e-10:
            return 0.0

        # 1. Angle compatibility: C_a = |cos(angle)|
        cos_angle = np.dot(P_vec, Q_vec) / (l_P * l_Q)
        C_a = abs(cos_angle)

        # 2. Scale compatibility: C_s = 2 / (l_avg/l_min + l_max/l_avg)
        l_avg = (l_P + l_Q) / 2
        l_min = min(l_P, l_Q)
        l_max = max(l_P, l_Q)
        C_s = 2.0 / (l_avg / l_min + l_max / l_avg) if l_min > 0 else 0.0

        # 3. Position compatibility: C_p = l_avg / (l_avg + ||m_P - m_Q||)
        m_P = (p0 + p1) / 2  # midpoint of P
        m_Q = (q0 + q1) / 2  # midpoint of Q
        dist_midpoints = np.linalg.norm(m_P - m_Q)
        C_p = l_avg / (l_avg + dist_midpoints)

        # 4. Visibility compatibility: C_v = min(V(P,Q), V(Q,P))
        # V(P,Q) = 1 - 2 * ||m - I_PQ|| / ||P||
        # where I_PQ is projection of Q's midpoint onto P
        V_PQ = self._visibility(p0, p1, m_Q, l_P)
        V_QP = self._visibility(q0, q1, m_P, l_Q)
        C_v = min(V_PQ, V_QP)
        C_v = max(0.0, C_v)  # Clamp to [0, 1]

        # Combined compatibility
        C_e = C_a * C_s * C_p * C_v

        return C_e

    def _visibility(
        self,
        p0: np.ndarray,
        p1: np.ndarray,
        m: np.ndarray,
        length: float
    ) -> float:
        """
        Compute visibility metric V(P,Q).

        Returns visibility in [0, 1] where 1 = fully visible.
        """
        # Project m onto line segment P
        P_vec = p1 - p0
        if length < 1e-10:
            return 0.0

        # Projection parameter t
        t = np.dot(m - p0, P_vec) / (length ** 2)
        t = np.clip(t, 0, 1)  # Clamp to segment

        # Projection point
        I_PQ = p0 + t * P_vec

        # Distance from m to projection
        dist = np.linalg.norm(m - I_PQ)

        # Visibility metric
        V = 1.0 - 2.0 * dist / length

        return V

    def _apply_forces(
        self,
        edges: List[Dict],
        compatibility: np.ndarray,
        step_size: float,
        K: float
    ) -> List[Dict]:
        """
        Apply spring and electrostatic forces to subdivision points.

        Parameters
        ----------
        K : float
            Spring constant controlling bundling strength
        """
        n_edges = len(edges)

        # Update each edge's subdivision points
        for i in range(n_edges):
            points = edges[i]['points']
            P = len(points) - 2  # Number of interior points

            if P == 0:
                continue

            # Calculate forces on interior points (not endpoints)
            forces = np.zeros((P, 2))

            for k in range(1, P + 1):  # k in [1, P], interior points
                p_k = points[k]

                # Spring forces from neighbors on same edge (as per Holten & van Wijk 2009)
                # kP is local spring constant = K / |P| (initial edge length)
                p_prev = points[k - 1]
                p_next = points[k + 1]

                # Calculate per-edge spring constant
                # kP = K / (edge_length * (P+1)) per the reference implementation
                kP = K / (edges[i]['initial_length'] * (P + 1))

                # Spring force: kP * vector sum (unclamped - let physics work naturally)
                spring_vec = (p_prev - p_k) + (p_next - p_k)
                spring_force = kP * spring_vec

                # Electrostatic forces from compatible edges
                electro_force = np.zeros(2)

                for j in range(n_edges):
                    if i == j or compatibility[i, j] == 0:
                        continue

                    # Ensure other edge has same number of points
                    if k >= len(edges[j]['points']):
                        continue

                    q_k = edges[j]['points'][k]
                    diff = q_k - p_k
                    dist = np.linalg.norm(diff)

                    if dist > 1e-10:
                        # Attractive force: diff * (1/dist)
                        electro_force += diff / dist

                # Combined force
                total_force = spring_force + electro_force

                # Clamp total force to prevent extreme displacements
                # Max displacement per iteration should be small fraction of edge length
                max_force = edges[i]['initial_length'] * 0.5
                force_mag = np.linalg.norm(total_force)
                if force_mag > max_force:
                    total_force = total_force * (max_force / force_mag)

                forces[k - 1] = total_force

            # Update positions with step size
            edges[i]['points'][1:-1] += step_size * forces

        return edges

    def _subdivide_edges(self, edges: List[Dict]) -> List[Dict]:
        """
        Double the number of subdivision points on each edge.
        """
        for edge in edges:
            points = edge['points']
            P_old = len(points)
            P_new = 2 * P_old - 1  # New total including endpoints

            # Create new points array
            new_points = np.zeros((P_new, 2))

            # Copy existing points at even indices
            new_points[::2] = points

            # Interpolate midpoints at odd indices
            for i in range(0, P_old - 1):
                new_points[2*i + 1] = (points[i] + points[i + 1]) / 2

            edge['points'] = new_points

        return edges

    def _get_step_size(self, cycle: int) -> float:
        """
        Compute step size for current cycle.

        Step size halves with each cycle: S0=0.1, S1=0.05, S2=0.025, etc.
        """
        # Step size: starts at 0.1 and halves each cycle (per reference implementation)
        return 0.1 / (2 ** cycle)
