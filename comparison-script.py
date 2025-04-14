import time
import random
import matplotlib.pyplot as plt
import numpy as np
from odd_even_transposition_sort import OddEvenTranspositionSort
from sasaki_time_optimal_sort import SasakiTimeOptimalSort
from alternative_time_optimal_sort import AlternativeTimeOptimalSort

def run_comparison(test_sizes=[10, 20, 30, 50], seed=42):
    """Run comparison of all three algorithms with different process counts"""
    random.seed(seed)
    
    #Store results for each algorithm
    odd_even_results = {}
    sasaki_results = {}
    alternative_results = {}
    
    #For each test size
    for size in test_sizes:
        print(f"\nRunning comparison for n = {size}")
        print("=" * 60)
        
        #Generate the same random values for all algorithms
        values = random.sample(range(1, size*10), size)
        
        #Run Odd-Even Transposition Sort
        print("\nOdd-Even Transposition Sort:")
        sorter = OddEvenTranspositionSort(size, values.copy())
        sorted_values = sorter.run()
        print(f"Correctly sorted: {sorted_values == sorted(values)}")
        odd_even_results[size] = sorter.get_metrics()
        
        #Run Sasaki's Time-Optimal Sort
        print("\nSasaki's Time-Optimal Sort:")
        sorter = SasakiTimeOptimalSort(size, values.copy())
        sorted_values = sorter.run()
        print(f"Correctly sorted: {sorted_values == sorted(values)}")
        sasaki_results[size] = sorter.get_metrics()
        
        #Run Alternative Time-Optimal Sort
        print("\nAlternative Time-Optimal Sort:")
        sorter = AlternativeTimeOptimalSort(size, values.copy())
        sorted_values = sorter.run()
        print(f"Correctly sorted: {sorted_values == sorted(values)}")
        alternative_results[size] = sorter.get_metrics()
    
    #Print comprehensive comparison table
    print("\nComprehensive Comparison Table:")
    print("=" * 120)
    print(f"{'n':>5} | {'Algorithm':^25} | {'Comparisons':>12} | {'Swaps':>6} | {'Messages':>10} | {'Time Steps':>10} | {'Execution Time (s)':>18}")
    print("-" * 120)
    
    for size in test_sizes:
        #Odd-Even
        metrics = odd_even_results[size]
        print(f"{size:>5} | {'Odd-Even Transposition':^25} | {metrics['comparisons']:>12} | {metrics['swaps']:>6} | {metrics['messages']:>10} | {metrics['time_steps']:>10} | {metrics['execution_time']:>18.6f}")
        
        #Sasaki
        metrics = sasaki_results[size]
        print(f"{size:>5} | {'Sasaki Time-Optimal':^25} | {metrics['comparisons']:>12} | {metrics['swaps']:>6} | {metrics['messages']:>10} | {metrics['time_steps']:>10} | {metrics['execution_time']:>18.6f}")
        
        #Alternative
        metrics = alternative_results[size]
        print(f"{size:>5} | {'Alternative Time-Optimal':^25} | {metrics['comparisons']:>12} | {metrics['swaps']:>6} | {metrics['messages']:>10} | {metrics['time_steps']:>10} | {metrics['execution_time']:>18.6f}")
        
        #Add separator between size groups
        if size != test_sizes[-1]:
            print("-" * 120)
    
    plot_comparisons(test_sizes, odd_even_results, sasaki_results, alternative_results)
    
    return odd_even_results, sasaki_results, alternative_results

def plot_comparisons(test_sizes, odd_even_results, sasaki_results, alternative_results):
    """Create comparison charts for the algorithms"""
    metrics = ['time_steps', 'messages', 'comparisons', 'execution_time']
    titles = ['Time Steps', 'Messages Exchanged', 'Comparisons', 'Execution Time (s)']
    
    plt.figure(figsize=(20, 15))
    
    for i, (metric, title) in enumerate(zip(metrics, titles), 1):
        plt.subplot(2, 2, i)
        
        x = np.arange(len(test_sizes))
        width = 0.25
        
        odd_even_values = [odd_even_results[size][metric] for size in test_sizes]
        sasaki_values = [sasaki_results[size][metric] for size in test_sizes]
        alternative_values = [alternative_results[size][metric] for size in test_sizes]
        
        plt.bar(x - width, odd_even_values, width, label='Odd-Even')
        plt.bar(x, sasaki_values, width, label='Sasaki')
        plt.bar(x + width, alternative_values, width, label='Alternative')
        
        plt.title(title)
        plt.xlabel('Number of Processes')
        plt.ylabel(title)
        plt.xticks(x, test_sizes)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('algorithm_comparison.png')
    plt.close()

if __name__ == "__main__":
    test_sizes = [10, 20, 30, 50]
    run_comparison(test_sizes)
