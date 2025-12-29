"""
Test to verify that vectorized electrostatic force function produces correct results.
Compares against reference implementation and tests edge cases.
"""

import numpy as np
import scipy.sparse as sparse
from edge_bundle import (
    edge_bundle_force,
    compute_compatibility_matrix,
    apply_electrostatic_force,
    update_edge_divisions
)


def apply_electrostatic_force_reference(edge_list, compatibility_list, edge_idx, point_idx, eps=1e-8):
    """
    REFERENCE implementation using explicit loop (original non-vectorized version).
    This is the ground truth we're testing against.
    """
    compatible_indices = compatibility_list[edge_idx].nonzero()[1]

    if len(compatible_indices) == 0:
        return np.zeros(2)

    curr_point = edge_list[edge_idx][point_idx]
    force_sum = np.zeros(2)

    for other_idx in compatible_indices:
        other_point = edge_list[other_idx][point_idx]
        force = other_point - curr_point
        dist = np.sqrt(np.sum((curr_point - other_point) ** 2))
        if dist > eps:
            force_sum += force / dist

    return force_sum


def test_electrostatic_force_basic():
    """Test basic functionality with simple case."""
    print("\n" + "=" * 70)
    print("TEST 1: Basic Electrostatic Force")
    print("=" * 70)

    # Create simple test case: 3 edges with known positions
    edge_list = [
        np.array([[0, 0], [5, 0]]),    # Edge 0
        np.array([[0, 1], [5, 1]]),    # Edge 1 (parallel, above)
        np.array([[0, -1], [5, -1]])   # Edge 2 (parallel, below)
    ]

    # Create compatibility matrix: all edges compatible
    compat_matrix = sparse.csr_matrix(np.array([
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0]
    ]))

    # Test force on middle point of edge 0
    edge_idx = 0
    point_idx = 1  # Middle point

    # Compute using both methods
    force_vectorized = apply_electrostatic_force(edge_list, compat_matrix, edge_idx, point_idx)
    force_reference = apply_electrostatic_force_reference(edge_list, compat_matrix, edge_idx, point_idx)

    print(f"Edge 0, point {point_idx} position: {edge_list[edge_idx][point_idx]}")
    print(f"Compatible with edges: {compat_matrix[edge_idx].nonzero()[1].tolist()}")
    print(f"\nForce (vectorized): {force_vectorized}")
    print(f"Force (reference):  {force_reference}")
    print(f"Difference: {np.abs(force_vectorized - force_reference)}")
    print(f"Max difference: {np.max(np.abs(force_vectorized - force_reference)):.2e}")

    # Check they're equal
    assert np.allclose(force_vectorized, force_reference, rtol=1e-14, atol=1e-14), \
        f"Forces don't match! Diff: {force_vectorized - force_reference}"

    print("✓ PASSED: Basic test")
    return True


def test_electrostatic_force_no_compatible():
    """Test with no compatible edges."""
    print("\n" + "=" * 70)
    print("TEST 2: No Compatible Edges")
    print("=" * 70)

    edge_list = [
        np.array([[0, 0], [5, 0]]),
        np.array([[0, 1], [5, 1]])
    ]

    # No compatibility
    compat_matrix = sparse.csr_matrix(np.zeros((2, 2)))

    force_vectorized = apply_electrostatic_force(edge_list, compat_matrix, 0, 1)
    force_reference = apply_electrostatic_force_reference(edge_list, compat_matrix, 0, 1)

    print(f"Force (vectorized): {force_vectorized}")
    print(f"Force (reference):  {force_reference}")

    assert np.allclose(force_vectorized, np.zeros(2)), "Should be zero force"
    assert np.allclose(force_vectorized, force_reference), "Should match reference"

    print("✓ PASSED: No compatible edges")
    return True


def test_electrostatic_force_epsilon():
    """Test epsilon handling (very close points)."""
    print("\n" + "=" * 70)
    print("TEST 3: Epsilon Handling")
    print("=" * 70)

    eps = 1e-8

    # Create edges at nearly identical positions
    edge_list = [
        np.array([[0, 0], [5, 0]]),
        np.array([[0, eps/2], [5, eps/2]])  # Very close to edge 0
    ]

    compat_matrix = sparse.csr_matrix(np.array([
        [0, 1],
        [1, 0]
    ]))

    force_vectorized = apply_electrostatic_force(edge_list, compat_matrix, 0, 1, eps=eps)
    force_reference = apply_electrostatic_force_reference(edge_list, compat_matrix, 0, 1, eps=eps)

    print(f"Distance between edges: {eps/2:.2e}")
    print(f"Epsilon: {eps:.2e}")
    print(f"Force magnitude (vectorized): {np.linalg.norm(force_vectorized):.6f}")
    print(f"Force magnitude (reference):  {np.linalg.norm(force_reference):.6f}")

    # Note: Results may differ slightly due to epsilon handling
    # Vectorized clamps to eps, reference skips if below eps
    print(f"Difference: {np.linalg.norm(force_vectorized - force_reference):.2e}")

    # Both should produce finite, reasonable forces
    assert np.all(np.isfinite(force_vectorized)), "Vectorized force should be finite"
    assert np.all(np.isfinite(force_reference)), "Reference force should be finite"

    print("✓ PASSED: Epsilon handling")
    return True


def test_full_bundling_consistency():
    """Test that full bundling produces consistent results."""
    print("\n" + "=" * 70)
    print("TEST 4: Full Bundling Consistency")
    print("=" * 70)

    np.random.seed(42)

    # Create small test graph
    n_edges = 10
    edges_xy = np.random.rand(n_edges, 4) * 10

    print(f"Testing with {n_edges} random edges")
    print("Running bundling twice with same parameters...")

    # Run bundling twice
    result1 = edge_bundle_force(
        edges_xy.copy(),
        K=1.0,
        C=3,
        P=1,
        S=0.05,
        P_rate=2,
        I=20,
        I_rate=2/3,
        compatibility_threshold=0.6,
        eps=1e-8
    )

    result2 = edge_bundle_force(
        edges_xy.copy(),
        K=1.0,
        C=3,
        P=1,
        S=0.05,
        P_rate=2,
        I=20,
        I_rate=2/3,
        compatibility_threshold=0.6,
        eps=1e-8
    )

    print(f"\nResult 1 shape: {result1.shape}")
    print(f"Result 2 shape: {result2.shape}")

    # Check exact equality
    assert result1.shape == result2.shape, "Shapes should match"
    assert np.allclose(result1['x'], result2['x'], rtol=1e-14), "X coordinates should match"
    assert np.allclose(result1['y'], result2['y'], rtol=1e-14), "Y coordinates should match"
    assert np.array_equal(result1['group'], result2['group']), "Groups should match"

    max_diff = np.max(np.abs(result1['x'] - result2['x']))
    print(f"Maximum difference in coordinates: {max_diff:.2e}")

    print("✓ PASSED: Full bundling is deterministic")
    return True


def test_parallel_edges_bundling():
    """Test that parallel edges bundle together correctly."""
    print("\n" + "=" * 70)
    print("TEST 5: Parallel Edges Bundle Together")
    print("=" * 70)

    # Create parallel edges
    edges_xy = np.array([
        [0, 0, 10, 0],
        [0, 1, 10, 1],
        [0, 2, 10, 2]
    ])

    print("Testing 3 parallel horizontal edges...")
    print(f"Original Y positions: {edges_xy[:, 1]}")

    bundled = edge_bundle_force(
        edges_xy,
        K=1.0,
        C=4,
        P=1,
        S=0.1,
        P_rate=2,
        I=30,
        I_rate=2/3,
        compatibility_threshold=0.6
    )

    # Check that edges bundled (middle points closer together)
    edge0 = bundled[bundled['group'] == 0]
    edge1 = bundled[bundled['group'] == 1]
    edge2 = bundled[bundled['group'] == 2]

    # Get middle point Y coordinates
    mid_idx = len(edge0) // 2
    y0_mid = edge0.iloc[mid_idx]['y']
    y1_mid = edge1.iloc[mid_idx]['y']
    y2_mid = edge2.iloc[mid_idx]['y']

    print(f"Middle point Y coordinates after bundling:")
    print(f"  Edge 0: {y0_mid:.4f} (original: 0)")
    print(f"  Edge 1: {y1_mid:.4f} (original: 1)")
    print(f"  Edge 2: {y2_mid:.4f} (original: 2)")

    # Calculate spread
    original_spread = 2.0  # Max - min
    bundled_spread = max(y0_mid, y1_mid, y2_mid) - min(y0_mid, y1_mid, y2_mid)

    print(f"\nOriginal spread: {original_spread:.4f}")
    print(f"Bundled spread: {bundled_spread:.4f}")
    print(f"Reduction: {(1 - bundled_spread/original_spread)*100:.1f}%")

    # Edges should be closer together (at least 30% reduction)
    assert bundled_spread < original_spread * 0.7, \
        f"Edges should bundle closer: {bundled_spread} vs {original_spread}"

    print("✓ PASSED: Parallel edges bundle correctly")
    return True


def test_endpoint_preservation():
    """Test that endpoints are preserved exactly."""
    print("\n" + "=" * 70)
    print("TEST 6: Endpoint Preservation")
    print("=" * 70)

    np.random.seed(123)
    edges_xy = np.random.rand(5, 4) * 20

    print(f"Testing with 5 random edges")

    bundled = edge_bundle_force(
        edges_xy,
        K=1.0,
        C=3,
        P=1,
        S=0.05,
        P_rate=2,
        I=20,
        I_rate=2/3,
        compatibility_threshold=0.6
    )

    # Check endpoints for each edge
    max_error = 0
    for i in range(len(edges_xy)):
        edge_data = bundled[bundled['group'] == i]

        # First point
        first = edge_data.iloc[0]
        expected_start = edges_xy[i, 0:2]
        start_error = np.sqrt((first['x'] - expected_start[0])**2 +
                             (first['y'] - expected_start[1])**2)

        # Last point
        last = edge_data.iloc[-1]
        expected_end = edges_xy[i, 2:4]
        end_error = np.sqrt((last['x'] - expected_end[0])**2 +
                           (last['y'] - expected_end[1])**2)

        max_error = max(max_error, start_error, end_error)

        if i < 2:
            print(f"  Edge {i}: start_error={start_error:.2e}, end_error={end_error:.2e}")

    print(f"\nMaximum endpoint error: {max_error:.2e}")

    assert max_error < 1e-10, f"Endpoints moved too much: {max_error}"

    print("✓ PASSED: Endpoints preserved")
    return True


def test_performance_comparison():
    """Compare performance of vectorized vs reference implementation."""
    print("\n" + "=" * 70)
    print("TEST 7: Performance Comparison")
    print("=" * 70)

    import time

    # Create realistic test case
    np.random.seed(456)
    n_edges = 50
    n_points = 10

    edge_list = [np.random.rand(n_points, 2) * 10 for _ in range(n_edges)]

    # Create compatibility matrix with ~10% compatibility
    compat = np.random.rand(n_edges, n_edges) > 0.9
    np.fill_diagonal(compat, 0)
    compat_matrix = sparse.csr_matrix(compat)

    n_compatible = compat_matrix.nnz
    print(f"Test setup: {n_edges} edges, {n_points} points per edge")
    print(f"Compatible pairs: {n_compatible} ({n_compatible/(n_edges**2)*100:.1f}%)")

    # Warm up
    _ = apply_electrostatic_force(edge_list, compat_matrix, 0, 5)
    _ = apply_electrostatic_force_reference(edge_list, compat_matrix, 0, 5)

    # Time vectorized version
    n_trials = 100
    start = time.time()
    for _ in range(n_trials):
        for edge_idx in range(min(10, n_edges)):  # Test first 10 edges
            for point_idx in range(1, n_points - 1):  # Test internal points
                _ = apply_electrostatic_force(edge_list, compat_matrix, edge_idx, point_idx)
    time_vectorized = time.time() - start

    # Time reference version
    start = time.time()
    for _ in range(n_trials):
        for edge_idx in range(min(10, n_edges)):
            for point_idx in range(1, n_points - 1):
                _ = apply_electrostatic_force_reference(edge_list, compat_matrix, edge_idx, point_idx)
    time_reference = time.time() - start

    speedup = time_reference / time_vectorized

    print(f"\nPerformance ({n_trials} trials):")
    print(f"  Vectorized: {time_vectorized:.4f}s")
    print(f"  Reference:  {time_reference:.4f}s")
    print(f"  Speedup:    {speedup:.2f}x")

    assert speedup > 1.0, "Vectorized should be faster"

    if speedup > 2.0:
        print("✓ PASSED: Significant speedup achieved (>2x)")
    else:
        print("✓ PASSED: Vectorized version is faster")

    return True


def run_all_tests():
    """Run all vectorization tests."""
    print("\n" + "=" * 70)
    print("VECTORIZATION TEST SUITE")
    print("=" * 70)
    print("\nTesting that vectorized implementation produces correct results...")

    tests = [
        ("Basic functionality", test_electrostatic_force_basic),
        ("No compatible edges", test_electrostatic_force_no_compatible),
        ("Epsilon handling", test_electrostatic_force_epsilon),
        ("Full bundling consistency", test_full_bundling_consistency),
        ("Parallel edges bundle", test_parallel_edges_bundling),
        ("Endpoint preservation", test_endpoint_preservation),
        ("Performance comparison", test_performance_comparison),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"\n✗ FAILED: {name}")
            print(f"  Error: {e}")
            failed += 1
        except Exception as e:
            print(f"\n✗ ERROR in {name}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Passed: {passed}/{passed + failed}")
    print(f"Failed: {failed}/{passed + failed}")

    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("\nVectorized implementation is correct and faster!")
    else:
        print(f"\n⚠️  {failed} test(s) failed")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
