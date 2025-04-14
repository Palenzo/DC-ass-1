# Distributed Sorting Algorithms Implementation

This project implements three distributed sorting algorithms for a line network:
1. Odd-Even Transposition Algorithm
2. Sasaki's Time-Optimal Algorithm
3. An Alternative Time-Optimal Algorithm

## Requirements
- Python 3.6 or higher
- matplotlib (for visualization, optional)
- numpy (for visualization, optional)

## File Structure
- odd_even_transposition_sort.py: Implementation of the Odd-Even Transposition Sort
- sasaki_time_optimal_sort.py: Implementation of Sasaki's Time-Optimal Sort
- alternative_time_optimal_sort.py: Implementation of the Alternative Time-Optimal Sort
- comparison.py: Script to compare all three algorithms
- README.txt: This file

## Compilation & Execution Instructions

As these are Python scripts, no compilation is needed.

### Running Individual Algorithms

1. To run the Odd-Even Transposition Sort:
```
python odd_even_transposition_sort.py
```

2. To run Sasaki's Time-Optimal Sort:
```
python sasaki_time_optimal_sort.py
```

3. To run the Alternative Time-Optimal Sort:
```
python alternative_time_optimal_sort.py
```

### Running Comparison of All Algorithms

To run all algorithms and generate a comparison:
```

pip install matplotlib numpy
python comparison.py
```

This will:
- Run all three algorithms with n = 10, 20, 30, and 50 processes
- Print detailed metrics for each algorithm
- Generate a comparison table in the console
- Create visualization charts (if matplotlib is installed)

## Time and Space Complexity Analysis

### Odd-Even Transposition Sort
- Time Complexity: O(n²) time steps
  - n phases, each with 2 time steps for odd/even comparisons
- Space Complexity: O(n)
  - Each process stores its own value and has a small constant overhead

### Sasaki's Time-Optimal Sort
- Time Complexity: O(n) time steps
  - O(n) steps to collect all values
  - O(n log n) local comparisons at one node (not counted in time steps)
  - O(n) steps to distribute the values
- Space Complexity: O(n)
  - First process temporarily stores all n values

### Alternative Time-Optimal Sort
- Time Complexity: O(n) time steps
  - O(log n) merge steps
  - Each merge step requires O(1) parallel communication
  - Final distribution takes O(n) steps
- Space Complexity: O(n)
  - Each process may temporarily store up to n values during merging

## Performance Metrics

The implementation tracks and reports:
1. Number of comparisons
2. Number of swaps
3. Number of messages exchanged
4. Number of time steps
5. Actual execution time

## Algorithm Details

### Odd-Even Transposition Sort
This algorithm alternates between comparing and swapping odd-indexed and even-indexed adjacent pairs. In a distributed setting, this translates to communication rounds where processes communicate with their neighbors.

### Sasaki's Time-Optimal Sort
This algorithm achieves the theoretical minimum time complexity by:
1. Collecting all values at the leftmost process
2. Sorting them locally
3. Distributing the sorted values back to all processes

### Alternative Time-Optimal Sort
This algorithm uses a parallel merge sort approach:
1. Each process starts with its own sorted list of length 1
2. In O(log n) steps, these are merged in parallel
3. The sorted array is redistributed to all processes

Each algorithm implements the basic primitive operations (send, receive, compute) as specified in the requirements.

#Final Result:

Comprehensive Comparison Table:
========================================================================================================================
    n |         Algorithm         |  Comparisons |  Swaps |   Messages | Time Steps | Execution Time (s)
------------------------------------------------------------------------------------------------------------------------
   10 |  Odd-Even Transposition   |           90 |     20 |        180 |         20 |           0.000000
   10 |    Sasaki Time-Optimal    |           45 |      0 |         18 |         18 |           0.000000
   10 | Alternative Time-Optimal  |           25 |      0 |         18 |         13 |           0.000000
------------------------------------------------------------------------------------------------------------------------
   20 |  Odd-Even Transposition   |          380 |    180 |        760 |         40 |           0.000000
   20 |    Sasaki Time-Optimal    |          190 |      0 |         38 |         38 |           0.000000
   20 | Alternative Time-Optimal  |           68 |      0 |         38 |         24 |           0.000000
------------------------------------------------------------------------------------------------------------------------
   30 |  Odd-Even Transposition   |          870 |    390 |       1740 |         60 |           0.001001
   30 |    Sasaki Time-Optimal    |          435 |      0 |         58 |         58 |           0.000000
   30 | Alternative Time-Optimal  |          111 |      0 |         58 |         34 |           0.000000
------------------------------------------------------------------------------------------------------------------------
   50 |  Odd-Even Transposition   |         2450 |   1150 |       4900 |        100 |           0.001999
   50 |    Sasaki Time-Optimal    |         1225 |      0 |         98 |         98 |           0.000000
   50 | Alternative Time-Optimal  |          222 |      0 |         98 |         55 |           0.000000
