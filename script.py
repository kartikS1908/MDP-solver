from itertools import product
import itertools

# # Reshape the permutations to m x n grids
m, n = 2, 5  # Replace with the desired dimensions
# # Generate all possible permutations of 0 and 1 for an m x n grid
grid_permutations = list(itertools.product([0, 1], repeat=m * n))
# print(permutations)
# Reshape permutations into m x n arrays
grids = [list(row) for row in grid_permutations]
all_grids = []
# Print the generated grids
for grid in grids:
    print("[")
    for row in range(m):
        print(str(grid[row * n: (row + 1) * n]) + ",")
    print("]")
    print(',')