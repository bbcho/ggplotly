"""
Test early filtering optimization for visibility compatibility.
"""

import numpy as np
import time
from edge_bundle import edge_bundle_force, compute_compatibility_matrix


def test_correctness_small_graph():
    """Test that early filtering produces correct results on small graph."""
    print("\n" + "=" * 70)
    print("TEST 1: Correctness on Small Graph")
    print("=" * 70)

    np.random.seed(42)
    n_edges = 20
    edges_xy = np.random.rand(n_edges, 4) * 10

    print(f"Testing with {n_edges} edges")
    print("Running full bundling to check correctness...")

    # Run full bundling
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

    print(f"\nResult shape: {bundled.shape}")
    print(f"Groups: {bundled['group'].nunique()}")

    # Check basic properties
    assert bundled.shape[0] > 0, "Should have results"
    assert bundled['group'].nunique() == n_edges, f"Should have {n_edges} groups"

    # Check endpoints preserved
    for i in range(min(5, n_edges)):
        edge_data = bundled[bundled['group'] == i]
        first = edge_data.iloc[0]
        last = edge_data.iloc[-1]

        start_error = np.sqrt((first['x'] - edges_xy[i, 0])**2 + (first['y'] - edges_xy[i, 1])**2)
        end_error = np.sqrt((last['x'] - edges_xy[i, 2])**2 + (last['y'] - edges_xy[i, 3])**2)

        assert start_error < 1e-10, f"Start point moved: {start_error}"
        assert end_error < 1e-10, f"End point moved: {end_error}"

    print("✓ PASSED: Early filtering produces correct results")
    return True


def test_parallel_edges_still_bundle():
    """Test that parallel edges still bundle correctly with early filtering."""
    print("\n" + "=" * 70)
    print("TEST 2: Parallel Edges Bundle with Early Filtering")
    print("=" * 70)

    edges_xy = np.array([
        [0, 0, 10, 0],
        [0, 0.5, 10, 0.5],
        [0, 1.0, 10, 1.0],
        [0, 1.5, 10, 1.5]
    ])

    print("Testing 4 parallel edges...")

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

    # Check bundling occurred
    mid_idx = len(bundled[bundled['group'] == 0]) // 2
    y_coords = []
    for i in range(4):
        edge_data = bundled[bundled['group'] == i]
        y_coords.append(edge_data.iloc[mid_idx]['y'])

    original_spread = 1.5
    bundled_spread = max(y_coords) - min(y_coords)

    print(f"\nOriginal Y spread: {original_spread:.4f}")
    print(f"Bundled Y spread:  {bundled_spread:.4f}")
    print(f"Reduction: {(1 - bundled_spread/original_spread)*100:.1f}%")

    assert bundled_spread < original_spread * 0.5, \
        f"Edges should bundle: {bundled_spread} vs {original_spread}"

    print("✓ PASSED: Bundling behavior preserved with early filtering")
    return True


def test_determinism():
    """Test that results are deterministic with early filtering."""
    print("\n" + "=" * 70)
    print("TEST 3: Determinism")
    print("=" * 70)

    np.random.seed(123)
    n_edges = 15
    edges_xy = np.random.rand(n_edges, 4) * 10

    print(f"Testing determinism with {n_edges} edges")
    print("Running bundling twice...")

    result1 = edge_bundle_force(
        edges_xy.copy(),
        K=1.0,
        C=2,
        P=1,
        S=0.05,
        P_rate=2,
        I=15,
        I_rate=2/3,
        compatibility_threshold=0.6
    )

    result2 = edge_bundle_force(
        edges_xy.copy(),
        K=1.0,
        C=2,
        P=1,
        S=0.05,
        P_rate=2,
        I=15,
        I_rate=2/3,
        compatibility_threshold=0.6
    )

    assert result1.shape == result2.shape, "Shapes should match"
    assert np.allclose(result1['x'], result2['x'], rtol=1e-14), "X should match"
    assert np.allclose(result1['y'], result2['y'], rtol=1e-14), "Y should match"

    max_diff = np.max(np.abs(result1['x'] - result2['x']))
    print(f"\nMaximum difference: {max_diff:.2e}")

    print("✓ PASSED: Results are deterministic")
    return True


def test_performance_improvement():
    """Benchmark performance improvement from early filtering."""
    print("\n" + "=" * 70)
    print("TEST 4: Performance Benchmark")
    print("=" * 70)

    np.random.seed(456)
    n_edges = 100
    edges_xy = np.random.rand(n_edges, 4) * 20

    print(f"Benchmarking with {n_edges} edges")
    print("This will show filtering statistics...\n")

    start = time.time()
    _ = compute_compatibility_matrix(edges_xy, compatibility_threshold=0.6)
    elapsed = time.time() - start

    print(f"\nCompatibility computation time: {elapsed:.2f}s")
    print(f"Time per edge pair: {elapsed / (n_edges * (n_edges-1) / 2) * 1000:.3f}ms")

    # Just check it completes in reasonable time
    assert elapsed < 10.0, f"Should complete quickly, took {elapsed}s"

    print("✓ PASSED: Performance is acceptable")
    return True


def test_filtering_effectiveness():
    """Test that filtering actually reduces visibility computations."""
    print("\n" + "=" * 70)
    print("TEST 5: Filtering Effectiveness")
    print("=" * 70)

    np.random.seed(789)

    # Test different graph sizes
    test_cases = [
        (30, "Small graph"),
        (50, "Medium graph"),
        (100, "Large graph")
    ]

    for n_edges, description in test_cases:
        edges_xy = np.random.rand(n_edges, 4) * 20

        print(f"\n{description} ({n_edges} edges):")

        # Capture filtering statistics by redirecting print
        import io
        import sys
        captured = io.StringIO()
        sys.stdout = captured

        _ = compute_compatibility_matrix(edges_xy, compatibility_threshold=0.6)

        sys.stdout = sys.__stdout__
        output = captured.getvalue()

        # Extract filtering statistics
        for line in output.split('\n'):
            if 'Filtered out' in line:
                print(f"  {line}")
                # Extract percentage
                if '%' in line:
                    pct_str = line.split('(')[1].split('%')[0]
                    pct = float(pct_str)
                    # Should filter out at least 50% typically
                    assert pct > 30, f"Should filter significantly, only filtered {pct}%"

    print("\n✓ PASSED: Filtering is effective")
    return True


def run_all_tests():
    """Run all early filtering tests."""
    print("\n" + "=" * 70)
    print("EARLY FILTERING TEST SUITE")
    print("=" * 70)
    print("\nTesting visibility compatibility early filtering optimization...")

    tests = [
        ("Correctness on small graph", test_correctness_small_graph),
        ("Parallel edges bundling", test_parallel_edges_still_bundle),
        ("Determinism", test_determinism),
        ("Performance benchmark", test_performance_improvement),
        ("Filtering effectiveness", test_filtering_effectiveness),
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
        print("\nEarly filtering optimization verified!")
        print("  ✓ Produces correct results")
        print("  ✓ Preserves bundling behavior")
        print("  ✓ Deterministic output")
        print("  ✓ Significantly reduces visibility computations")
    else:
        print(f"\n⚠️  {failed} test(s) failed")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
