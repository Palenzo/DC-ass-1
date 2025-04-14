import time
import random
from collections import deque

class Process:
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.inbox = deque()
        self.outbox = deque()
        self.left_neighbor = None
        self.right_neighbor = None
        self.tokens = [] 
    
    def send(self, target, message):
        target.inbox.append(message)
    
    def receive(self):
        if self.inbox:
            return self.inbox.popleft()
        return None

class AlternativeTimeOptimalSort:
    def __init__(self, n, values=None):
        """Initialize n processes with random or specified values"""
        self.n = n
        if values is None:
            self.values = random.sample(range(1, n*10), n)
        else:
            self.values = values[:n]
        
        #Create processes
        self.processes = [Process(i, self.values[i]) for i in range(n)]
        
        #Set up the line network topology
        for i in range(n):
            if i > 0:
                self.processes[i].left_neighbor = self.processes[i-1]
            if i < n-1:
                self.processes[i].right_neighbor = self.processes[i+1]
        
        self.comparisons = 0
        self.swaps = 0
        self.messages = 0
        self.time_steps = 0
    
    def run(self):
        """Execute alternative time-optimal sorting algorithm using parallel merge"""
        start_time = time.time()
        
        #Phase 1: Each process starts with its own value as a sorted list
        for i in range(self.n):
            self.processes[i].tokens = [self.processes[i].value]
        
        #Phase 2: Perform log(n) merge steps
        step_size = 1
        while step_size < self.n:
            self._parallel_merge(step_size)
            step_size *= 2
        
        #Phase 3: Redistribute sorted values
        self._redistribute_values()
        
        end_time = time.time()
        self.execution_time = end_time - start_time
        
        return [p.value for p in self.processes]
    
    def _parallel_merge(self, step_size):
        """Perform one step of parallel merge sorting"""
        self.time_steps += 1
        
        #Each process with rank k where k % (2*step_size) == 0 merges with k+step_size
        for i in range(0, self.n, 2 * step_size):
            if i + step_size < self.n:
                # Send right half of the array to merge
                right_idx = i + step_size
                self.processes[right_idx].send(self.processes[i], self.processes[right_idx].tokens)
                self.messages += 1
        
        #Receive and merge
        for i in range(0, self.n, 2 * step_size):
            if i + step_size < self.n:
                right_idx = i + step_size
                right_tokens = self.processes[i].receive()
                
                #Merge the two sorted arrays
                merged = self._merge(self.processes[i].tokens, right_tokens)
                self.processes[i].tokens = merged
                
                #Clear tokens from the right process as they are now merged into the left process
                self.processes[right_idx].tokens = []
    
    def _merge(self, left, right):
        """Merge two sorted arrays"""
        merged = []
        left_idx, right_idx = 0, 0
        
        while left_idx < len(left) and right_idx < len(right):
            self.comparisons += 1
            if left[left_idx] <= right[right_idx]:
                merged.append(left[left_idx])
                left_idx += 1
            else:
                merged.append(right[right_idx])
                right_idx += 1
        
        #Add remaining elements
        merged.extend(left[left_idx:])
        merged.extend(right[right_idx:])
        
        return merged
    
    def _redistribute_values(self):
        """Redistribute the sorted values from process 0 to all processes"""
        #Get the fully sorted array from the first process
        sorted_values = self.processes[0].tokens
        
        #Set the value for process 0
        self.processes[0].value = sorted_values[0]
        
        #Distribute the remaining values
        for i in range(1, self.n):
            self.processes[0].send(self.processes[i], sorted_values[i])
            self.messages += 1
            self.time_steps += 1
        
        #Each process receives its value
        for i in range(1, self.n):
            self.processes[i].value = self.processes[i].receive()
    
    def get_metrics(self):
        """Return metrics about the algorithm execution"""
        return {
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "messages": self.messages,
            "time_steps": self.time_steps,
            "execution_time": self.execution_time
        }

def test_alternative_sort(n, seed=None):
    """Test the alternative time-optimal sorting algorithm with n processes"""
    if seed is not None:
        random.seed(seed)
        
    #Generate random values
    values = random.sample(range(1, n*10), n)
    
    print(f"Testing Alternative Time-Optimal Sort with {n} processes")
    print(f"Initial values: {values}")
    
    #Run the algorithm
    sorter = AlternativeTimeOptimalSort(n, values)
    sorted_values = sorter.run()
    
    print(f"Sorted values: {sorted_values}")
    print(f"Correctly sorted: {sorted_values == sorted(values)}")
    
    #Print metrics
    metrics = sorter.get_metrics()
    print(f"Comparisons: {metrics['comparisons']}")
    print(f"Swaps: {metrics['swaps']}")
    print(f"Messages exchanged: {metrics['messages']}")
    print(f"Time steps: {metrics['time_steps']}")
    print(f"Execution time: {metrics['execution_time']:.6f} seconds")
    print()
    
    return metrics

if __name__ == "__main__":
    #Set random seed for reproducibility
    random.seed(6)
    
    #Test with different values of n
    test_sizes = [10, 20, 30, 50]
    results = {}
    
    for size in test_sizes:
        results[size] = test_alternative_sort(size)
    
    # Print comparison table
    print("Comparison Table for Alternative Time-Optimal Sort:")
    print("=" * 80)
    print(f"{'n':>5} | {'Comparisons':>12} | {'Swaps':>6} | {'Messages':>10} | {'Time Steps':>10} | {'Execution Time (s)':>18}")
    print("-" * 80)
    
    for size, metrics in results.items():
        print(f"{size:>5} | {metrics['comparisons']:>12} | {metrics['swaps']:>6} | {metrics['messages']:>10} | {metrics['time_steps']:>10} | {metrics['execution_time']:>18.6f}")
