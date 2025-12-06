"""
Test additional vectorizations: DataFrame assembly and spring forces.
"""

import numpy as np
import pandas as pd
from edge_bundle import (
    edge_bundle_force,
    apply_spring_force,
    apply_spring_forces_vectorized
)


def test_spring_force_vectorized_vs_loop():
    """Test that vectorized spring forces match loop version."""
    print("\n" + "=" * 70)
    print("TEST 1: Spring Force Vectorization")
    print("=" * 70)

    # Create test edge with multiple points
    n_points = 10
    edge_points = np.random.rand(n_points, 2) * 10
    kP = 0.5

    print(f"Testing with {n_points} points, kP={kP}")

    # Compute using vectorized version
    forces_vectorized = apply_spring_forces_vectorized(edge_points, kP)

    # Compute using loop (reference)
    forces_reference = np.zeros((n_points, 2))
    for i in range(1, n_points - 1):
        forces_reference[i] = apply_spring_force(edge_points, i, kP)

    print(f"\nVectorized shape: {forces_vectorized.shape}")
    print(f"Reference shape:  {forces_reference.shape}")

    # Check they match
    max_diff = np.max(np.abs(forces_vectorized - forces_reference))
    print(f"Maximum difference: {max_diff:.2e}")

    assert np.allclose(forces_vectorized, forces_reference, rtol=1e-14), \
        f"Forces don't match! Max diff: {max_diff}"

    # Check endpoints are zero
    assert np.allclose(forces_vectorized[0], 0), "First point should have zero force"
    assert np.allclose(forces_vectorized[-1], 0), "Last point should have zero force"

    print("✓ PASSED: Vectorized spring forces match loop version")
    return True


def test_spring_force_edge_cases():
    """Test spring force edge cases."""
    print("\n" + "=" * 70)
    print("TEST 2: Spring Force Edge Cases")
    print("=" * 70)

    kP = 1.0

    # Case 1: Only 2 points (no internal points)
    edge_2_points = np.array([[0, 0], [1, 1]])
    forces = apply_spring_forces_vectorized(edge_2_points, kP)
    assert forces.shape == (2, 2), "Should return correct shape"
    assert np.allclose(forces, 0), "Should be all zeros"
    print("✓ 2-point edge handled correctly")

    # Case 2: 3 points (one internal)
    edge_3_points = np.array([[0, 0], [1, 1], [2, 0]])
    forces = apply_spring_forces_vectorized(edge_3_points, kP)
    assert forces.shape == (3, 2), "Should return correct shape"
    assert np.allclose(forces[0], 0), "First point should be zero"
    assert np.allclose(forces[2], 0), "Last point should be zero"
    assert not np.allclose(forces[1], 0), "Middle point should have force"
    print("✓ 3-point edge handled correctly")

    # Case 3: Straight line (forces should be zero)
    straight_edge = np.array([[0, 0], [1, 0], [2, 0], [3, 0]])
    forces = apply_spring_forces_vectorized(straight_edge, kP)
    # Internal points on straight line should have zero spring force
    assert np.allclose(forces[1], 0, atol=1e-10), "Straight line should have zero forces"
    assert np.allclose(forces[2], 0, atol=1e-10), "Straight line should have zero forces"
    print("✓ Straight line handled correctly")

    print("✓ PASSED: All edge cases handled correctly")
    return True


def test_dataframe_assembly():
    """Test that DataFrame assembly produces correct structure."""
    print("\n" + "=" * 70)
    print("TEST 3: DataFrame Assembly")
    print("=" * 70)

    np.random.seed(789)
    n_edges = 5
    edges_xy = np.random.rand(n_edges, 4) * 10

    print(f"Testing with {n_edges} edges")

    result = edge_bundle_force(
        edges_xy,
        K=1.0,
        C=2,
        P=1,
        S=0.05,
        P_rate=2,
        I=10,
        I_rate=2/3,
        compatibility_threshold=0.6
    )

    print(f"\nResult shape: {result.shape}")
    print(f"Columns: {list(result.columns)}")

    # Check structure
    assert set(result.columns) == {'x', 'y', 'index', 'group'}, "Columns should be correct"
    assert result['group'].nunique() == n_edges, f"Should have {n_edges} groups"

    # Check all groups have same number of points
    group_sizes = result.groupby('group').size()
    assert len(group_sizes.unique()) == 1, "All groups should have same size"

    # Check index ranges from 0 to 1 for each group
    for group_id in range(n_edges):
        group_data = result[result['group'] == group_id]
        indices = group_data['index'].values
        assert np.isclose(indices[0], 0.0), f"Group {group_id} should start at 0"
        assert np.isclose(indices[-1], 1.0), f"Group {group_id} should end at 1"
        assert np.all(np.diff(indices) >= 0), f"Group {group_id} indices should be monotonic"

    # Check data types
    assert result['x'].dtype in [np.float64, np.float32], "x should be float"
    assert result['y'].dtype in [np.float64, np.float32], "y should be float"
    assert result['index'].dtype in [np.float64, np.float32], "index should be float"
    assert result['group'].dtype in [np.int64, np.int32], "group should be int"

    print("✓ PASSED: DataFrame structure is correct")
    return True


def test_full_bundling_with_vectorizations():
    """Test complete bundling produces consistent results."""
    print("\n" + "=" * 70)
    print("TEST 4: Full Bundling Consistency (All Vectorizations)")
    print("=" * 70)

    np.random.seed(42)
    n_edges = 15
    edges_xy = np.random.rand(n_edges, 4) * 10

    print(f"Testing full bundling with {n_edges} edges")
    print("Running twice to check determinism...")

    # Run twice
    result1 = edge_bundle_force(
        edges_xy.copy(),
        K=1.0,
        C=3,
        P=1,
        S=0.05,
        P_rate=2,
        I=20,
        I_rate=2/3,
        compatibility_threshold=0.6
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
        compatibility_threshold=0.6
    )

    # Check exact equality
    assert result1.shape == result2.shape, "Shapes should match"
    assert np.allclose(result1['x'], result2['x'], rtol=1e-14), "X should match"
    assert np.allclose(result1['y'], result2['y'], rtol=1e-14), "Y should match"
    assert np.allclose(result1['index'], result2['index'], rtol=1e-14), "Index should match"
    assert np.array_equal(result1['group'], result2['group']), "Group should match"

    max_diff = np.max(np.abs(result1['x'] - result2['x']))
    print(f"\nMaximum coordinate difference: {max_diff:.2e}")
    print("✓ PASSED: Bundling is deterministic")
    return True


def test_parallel_edges_still_bundle():
    """Test that vectorizations don't break bundling behavior."""
    print("\n" + "=" * 70)
    print("TEST 5: Parallel Edges Still Bundle Correctly")
    print("=" * 70)

    # Create highly compatible parallel edges
    edges_xy = np.array([
        [0, 0, 10, 0],
        [0, 0.5, 10, 0.5],
        [0, 1.0, 10, 1.0]
    ])

    print("Testing 3 parallel edges...")

    bundled = edge_bundle_force(
        edges_xy,
        K=1.0,
        C=4,
        P=1,
        S=0.1,
        P_rate=2,
        I=30,
        I_rate=2/3,
        compatibility_threshold=0.5
    )

    # Check bundling occurred
    edge0 = bundled[bundled['group'] == 0]
    edge1 = bundled[bundled['group'] == 1]
    edge2 = bundled[bundled['group'] == 2]

    mid_idx = len(edge0) // 2
    y0 = edge0.iloc[mid_idx]['y']
    y1 = edge1.iloc[mid_idx]['y']
    y2 = edge2.iloc[mid_idx]['y']

    original_spread = 1.0  # Max - min of original Y
    bundled_spread = max(y0, y1, y2) - min(y0, y1, y2)

    print(f"Original Y spread: {original_spread:.4f}")
    print(f"Bundled Y spread:  {bundled_spread:.4f}")
    print(f"Reduction: {(1 - bundled_spread/original_spread)*100:.1f}%")

    # Should reduce spread by at least 50%
    assert bundled_spread < original_spread * 0.5, \
        f"Edges should bundle: {bundled_spread} vs {original_spread}"

    print("✓ PASSED: Bundling behavior preserved")
    return True


def test_performance_comparison():
    """Compare performance with and without spring force vectorization."""
    print("\n" + "=" * 70)
    print("TEST 6: Performance Comparison")
    print("=" * 70)

    import time

    # Test spring force performance
    n_points = 50
    edge_points = np.random.rand(n_points, 2) * 10
    kP = 0.5

    print(f"Testing spring force performance ({n_points} points)")

    # Vectorized version
    n_trials = 1000
    start = time.time()
    for _ in range(n_trials):
        _ = apply_spring_forces_vectorized(edge_points, kP)
    time_vectorized = time.time() - start

    # Loop version
    start = time.time()
    for _ in range(n_trials):
        forces = np.zeros((n_points, 2))
        for i in range(1, n_points - 1):
            forces[i] = apply_spring_force(edge_points, i, kP)
    time_loop = time.time() - start

    speedup = time_loop / time_vectorized

    print(f"\nSpring force performance ({n_trials} trials):")
    print(f"  Vectorized: {time_vectorized:.4f}s")
    print(f"  Loop:       {time_loop:.4f}s")
    print(f"  Speedup:    {speedup:.2f}x")

    assert speedup > 1.0, "Vectorized should be faster"

    if speedup > 1.5:
        print("✓ PASSED: Significant speedup (>1.5x)")
    else:
        print("✓ PASSED: Vectorized is faster")

    return True


def run_all_tests():
    """Run all tests for additional vectorizations."""
    print("\n" + "=" * 70)
    print("ADDITIONAL VECTORIZATIONS TEST SUITE")
    print("=" * 70)
    print("\nTesting DataFrame assembly and spring force vectorizations...")

    tests = [
        ("Spring force vectorization", test_spring_force_vectorized_vs_loop),
        ("Spring force edge cases", test_spring_force_edge_cases),
        ("DataFrame assembly", test_dataframe_assembly),
        ("Full bundling consistency", test_full_bundling_with_vectorizations),
        ("Parallel edges bundling", test_parallel_edges_still_bundle),
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
        print("\nAdditional vectorizations are correct!")
        print("  ✓ DataFrame assembly vectorized")
        print("  ✓ Spring forces vectorized")
        print("  ✓ All behavior preserved")
    else:
        print(f"\n⚠️  {failed} test(s) failed")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
