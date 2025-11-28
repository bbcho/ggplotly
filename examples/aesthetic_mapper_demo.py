"""
Demonstration of the refactored aesthetic mapping system.

This example shows how the new AestheticMapper provides clearer,
more maintainable color and aesthetic handling.
"""

import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ggplotly import *

# Create sample data
df = pd.DataFrame({
    'x': range(1, 11),
    'y': [2, 4, 3, 5, 7, 6, 8, 10, 9, 11],
    'category': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B'],
    'size_var': [10, 20, 15, 25, 30, 20, 15, 25, 20, 30]
})

print("Example 1: Color mapped to categorical variable")
print("=" * 60)
p1 = ggplot(df, aes(x='x', y='y', color='category')) + \
     geom_point(size=15) + \
     ggtitle("Color Aesthetic Mapped to Category")
print("✓ Created plot with color aesthetic mapping")

print("\nExample 2: Fill mapped to categorical variable")
print("=" * 60)
p2 = ggplot(df, aes(x='x', y='y', fill='category')) + \
     geom_point(size=15) + \
     ggtitle("Fill Aesthetic Mapped to Category")
print("✓ Created plot with fill aesthetic mapping")

print("\nExample 3: Literal color value")
print("=" * 60)
p3 = ggplot(df, aes(x='x', y='y')) + \
     geom_point(color='red', size=15) + \
     ggtitle("Literal Color Value")
print("✓ Created plot with literal color value")

print("\nExample 4: Color mapped with custom size")
print("=" * 60)
p4 = ggplot(df, aes(x='x', y='y', color='category')) + \
     geom_point(size=20, alpha=0.7) + \
     ggtitle("Color + Custom Size + Alpha")
print("✓ Created plot with multiple aesthetic properties")

print("\nExample 5: Group aesthetic")
print("=" * 60)
p5 = ggplot(df, aes(x='x', y='y', group='category')) + \
     geom_line() + \
     ggtitle("Grouped Lines")
print("✓ Created plot with group aesthetic")

# This should raise a clear error (can't map both color and fill to columns)
print("\nExample 6: Error case - both color and fill mapped to columns")
print("=" * 60)
try:
    p6 = ggplot(df, aes(x='x', y='y', color='category', fill='category')) + \
         geom_point()
    p6.draw()
    print("✗ Should have raised an error!")
except ValueError as e:
    print(f"✓ Correctly raised error: {e}")

print("\nExample 7: Valid - color mapped, fill as literal")
print("=" * 60)
p7 = ggplot(df, aes(x='x', y='y', color='category')) + \
     geom_point(fill='lightblue', size=15) + \
     ggtitle("Color Mapped, Fill Literal")
print("✓ Created plot with color mapped and fill literal")

print("\n" + "=" * 60)
print("All examples completed successfully!")
print("The new AestheticMapper provides:")
print("  • Clear distinction between column references and literal values")
print("  • Better error messages when invalid combinations are used")
print("  • More maintainable and testable code")
print("  • Consistent behavior across all geoms")
