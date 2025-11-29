#!/usr/bin/env python
"""Test to understand the component clamping behavior"""

import numpy as np

# Simulate a point with neighbors
p_k = np.array([0.0, 0.0])      # Current point at origin
p_prev = np.array([-0.5, -0.5])  # Previous point lower-left
p_next = np.array([0.5, 0.5])    # Next point upper-right

# Spring vector without clamping
spring_vec = (p_prev - p_k) + (p_next - p_k)
print(f"Spring vector (no clamp): {spring_vec}")
# Expected: [-0.5, -0.5] + [0.5, 0.5] = [0, 0] - balanced, no force

# With component clamping (reference implementation)
x = p_prev[0] - p_k[0] + p_next[0] - p_k[0]
x = x if x >= 0 else 0.0
y = p_prev[1] - p_k[1] + p_next[1] - p_k[1]
y = y if y >= 0 else 0.0
spring_vec_clamped = np.array([x, y])
print(f"Spring vector (clamped):  {spring_vec_clamped}")
# With clamping: x=0, y=0 - same result when balanced

print("\n--- Test 2: Unbalanced case ---")
p_k = np.array([0.5, 0.5])       # Current point
p_prev = np.array([0.0, 0.0])    # Previous at origin
p_next = np.array([1.0, 1.0])    # Next upper-right

spring_vec = (p_prev - p_k) + (p_next - p_k)
print(f"Spring vector (no clamp): {spring_vec}")
# Expected: [-0.5, -0.5] + [0.5, 0.5] = [0, 0] - balanced

x = p_prev[0] - p_k[0] + p_next[0] - p_k[0]
x = x if x >= 0 else 0.0
y = p_prev[1] - p_k[1] + p_next[1] - p_k[1]
y = y if y >= 0 else 0.0
spring_vec_clamped = np.array([x, y])
print(f"Spring vector (clamped):  {spring_vec_clamped}")

print("\n--- Test 3: Point pushed left (negative force) ---")
p_k = np.array([1.0, 0.5])       # Current point pushed right
p_prev = np.array([0.0, 0.0])    # Previous at origin
p_next = np.array([1.0, 1.0])    # Next upper-right

spring_vec = (p_prev - p_k) + (p_next - p_k)
print(f"Spring vector (no clamp): {spring_vec}")
# Expected: [-1.0, -0.5] + [0.0, 0.5] = [-1.0, 0.0] - pull left

x = p_prev[0] - p_k[0] + p_next[0] - p_k[0]
x = x if x >= 0 else 0.0
y = p_prev[1] - p_k[1] + p_next[1] - p_k[1]
y = y if y >= 0 else 0.0
spring_vec_clamped = np.array([x, y])
print(f"Spring vector (clamped):  {spring_vec_clamped}")
# With clamping: x=0 (clamped from -1.0), y=0 - NO RESTORING FORCE!
print("^ This is the problem: can't pull back to the left!")
