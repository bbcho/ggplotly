"""
Validation tests to ensure the edge bundling algorithm is working correctly
"""

import numpy as np
import networkx as nx
from edge_bundle import edge_bundle_force


def test_simple_parallel_edges():
    """
    Test with simple parallel edges - they should bundle together.
    """
    print("\n" + "=" * 60)
    print("TEST: Parallel Edges Should Bundle")
    print("=" * 60)

    # Create two parallel edges
    edges_xy = np.array([
        [0, 0, 10, 0],   # Edge 1: horizontal at y=0
        [0, 0.5, 10, 0.5]  # Edge 2: horizontal at y=0.5, very close to edge 1
    ])

    bundled = edge_bundle_force(
        edges_xy,
        K=1.0,
        C=3,
        P=1,
        S=0.1,
        P_rate=2,
        I=20,
        I_rate=2/3,
        compatibility_threshold=0.6
    )

    # Check that edges bundled (middle points should be closer than 0.5)
    edge1 = bundled[bundled['group'] == 0]
    edge2 = bundled[bundled['group'] == 1]

    # Get middle point (closest to index 0.5)
    edge1_middle_idx = (edge1['index'] - 0.5).abs().argmin()
    edge2_middle_idx = (edge2['index'] - 0.5).abs().argmin()
    edge1_middle = edge1.iloc[edge1_middle_idx]
    edge2_middle = edge2.iloc[edge2_middle_idx]

    distance = np.sqrt((edge1_middle['x'] - edge2_middle['x'])**2 +
                      (edge1_middle['y'] - edge2_middle['y'])**2)

    print(f"\nOriginal distance between edges: 0.5")
    print(f"Distance after bundling: {distance:.4f}")

    # The distance should be significantly reduced
    assert distance < 0.4, f"Parallel edges should bundle closer, but distance is {distance}"
    print("✓ PASSED: Parallel edges bundled together")


def test_perpendicular_edges():
    """
    Test with perpendicular edges - they should NOT bundle together.
    """
    print("\n" + "=" * 60)
    print("TEST: Perpendicular Edges Should NOT Bundle")
    print("=" * 60)

    # Create two perpendicular edges
    edges_xy = np.array([
        [0, 5, 10, 5],   # Horizontal edge
        [5, 0, 5, 10]    # Vertical edge
    ])

    bundled = edge_bundle_force(
        edges_xy,
        K=1.0,
        C=3,
        P=1,
        S=0.1,
        P_rate=2,
        I=20,
        I_rate=2/3,
        compatibility_threshold=0.6
    )

    edge1 = bundled[bundled['group'] == 0]
    edge2 = bundled[bundled['group'] == 1]

    # Check that edges stay relatively straight
    # For horizontal edge, y coordinates should not vary much
    edge1_y_std = edge1['y'].std()
    print(f"\nHorizontal edge Y standard deviation: {edge1_y_std:.4f}")

    # For vertical edge, x coordinates should not vary much
    edge2_x_std = edge2['x'].std()
    print(f"Vertical edge X standard deviation: {edge2_x_std:.4f}")

    # Both should be relatively small (edges stay straight)
    assert edge1_y_std < 1.0, f"Horizontal edge bent too much: {edge1_y_std}"
    assert edge2_x_std < 1.0, f"Vertical edge bent too much: {edge2_x_std}"
    print("✓ PASSED: Perpendicular edges did not bundle significantly")


def test_endpoint_preservation():
    """
    Test that edge endpoints are preserved after bundling.
    """
    print("\n" + "=" * 60)
    print("TEST: Endpoints Should Be Preserved")
    print("=" * 60)

    np.random.seed(123)
    n_edges = 10

    # Create random edges
    edges_xy = np.random.rand(n_edges, 4) * 10

    bundled = edge_bundle_force(
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

    # Check that endpoints match
    print("\nChecking endpoint preservation...")
    max_error = 0
    for i in range(n_edges):
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

        if i < 3:  # Print first 3 for verification
            print(f"  Edge {i}: start_error={start_error:.6f}, end_error={end_error:.6f}")

    print(f"\nMaximum endpoint error: {max_error:.6f}")
    assert max_error < 1e-5, f"Endpoints moved too much: {max_error}"
    print("✓ PASSED: All endpoints preserved")


def test_output_structure():
    """
    Test that output has correct structure and data types.
    """
    print("\n" + "=" * 60)
    print("TEST: Output Structure Validation")
    print("=" * 60)

    edges_xy = np.array([
        [0, 0, 5, 5],
        [1, 1, 6, 6]
    ])

    bundled = edge_bundle_force(
        edges_xy,
        K=1.0,
        C=2,
        P=1,
        S=0.05,
        P_rate=2,
        I=5,
        I_rate=2/3,
        compatibility_threshold=0.6
    )

    # Check columns
    assert set(bundled.columns) == {'x', 'y', 'index', 'group'}, \
        f"Unexpected columns: {bundled.columns}"
    print("✓ Correct columns: x, y, index, group")

    # Check data types
    assert bundled['x'].dtype in [np.float64, np.float32], "x should be float"
    assert bundled['y'].dtype in [np.float64, np.float32], "y should be float"
    assert bundled['index'].dtype in [np.float64, np.float32], "index should be float"
    assert bundled['group'].dtype in [np.int64, np.int32], "group should be int"
    print("✓ Correct data types")

    # Check index range
    assert bundled['index'].min() >= 0.0, "index should be >= 0"
    assert bundled['index'].max() <= 1.0, "index should be <= 1"
    print("✓ Index values in [0, 1]")

    # Check groups
    assert bundled['group'].nunique() == 2, "Should have 2 edge groups"
    assert set(bundled['group'].unique()) == {0, 1}, "Groups should be 0 and 1"
    print("✓ Correct number of groups")

    # Check equal points per edge
    counts = bundled.groupby('group').size()
    assert len(counts.unique()) == 1, "All edges should have same number of points"
    print(f"✓ Equal points per edge: {counts.iloc[0]}")

    print("✓ PASSED: Output structure is valid")


def test_performance():
    """
    Test that algorithm completes in reasonable time for moderate graphs.
    """
    print("\n" + "=" * 60)
    print("TEST: Performance Check")
    print("=" * 60)

    import time

    # Create a moderate-sized graph
    n_edges = 50
    np.random.seed(456)
    edges_xy = np.random.rand(n_edges, 4) * 20

    print(f"Testing with {n_edges} edges...")

    start_time = time.time()
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
    elapsed_time = time.time() - start_time

    print(f"\nCompleted in {elapsed_time:.2f} seconds")
    print(f"Time per edge: {elapsed_time / n_edges * 1000:.2f} ms")

    assert elapsed_time < 60, f"Algorithm too slow: {elapsed_time} seconds for {n_edges} edges"
    print("✓ PASSED: Performance acceptable")


def run_all_tests():
    """Run all validation tests."""
    print("\n" + "=" * 60)
    print("RUNNING ALL VALIDATION TESTS")
    print("=" * 60)

    tests = [
        test_output_structure,
        test_endpoint_preservation,
        test_simple_parallel_edges,
        test_perpendicular_edges,
        test_performance
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"\n✗ FAILED: {test_func.__name__}")
            print(f"  Error: {e}")
            failed += 1
        except Exception as e:
            print(f"\n✗ ERROR in {test_func.__name__}: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Passed: {passed}/{passed + failed}")
    print(f"Failed: {failed}/{passed + failed}")

    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! 🎉")
    else:
        print(f"\n⚠️  {failed} test(s) failed")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
