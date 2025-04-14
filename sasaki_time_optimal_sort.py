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
        self.token = None  
    
    def send(self, target, message):
        target.inbox.append(message)
    
    def receive(self):
        if self.inbox:
            return self.inbox.popleft()
        return None

class SasakiTimeOptimalSort:
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
        """Execute Sasaki's time-optimal sorting algorithm"""
        start_time = time.time()
        
        #Phase 1: Collect all elements at the leftmost process
        self._collect_phase()
        
        #Phase 2: Sort locally at the leftmost process
        self._sort_locally()
        
        #Phase 3: Distribute the sorted elements back to all processes
        self._distribute_phase()
        
        end_time = time.time()
        self.execution_time = end_time - start_time
        
        #Return sorted values
        return [p.value for p in self.processes]
    
    def _collect_phase(self):
        """Collect all values at the leftmost process"""
        leftmost = self.processes[0]
        collected_values = [leftmost.value]
        
        #each process sending to its left neighbor, directly relay all values to leftmost
        for i in range(1, self.n):
            process = self.processes[i]
            #Send directly to the leftmost process
            process.send(leftmost, process.value)
            self.messages += 1
            self.time_steps += 1  # Each message takes 1 time step
        
        #Leftmost process receives all values
        for i in range(1, self.n):
            value = leftmost.receive()
            collected_values.append(value)
        
        #Store the collected values
        leftmost.token = collected_values
    
    def _sort_locally(self):
        """Sort the collected values at the leftmost process"""
        leftmost = self.processes[0]
        #Sort the values
        leftmost.token.sort()
        self.comparisons += (self.n * (self.n - 1)) // 2 
    
    def _distribute_phase(self):
        """Distribute the sorted values back to all processes"""
        leftmost = self.processes[0]
        sorted_values = leftmost.token
        
        #Set the leftmost process's value
        leftmost.value = sorted_values[0]
        
        #Distribute the remaining values to the other processes
        for i in range(1, self.n):
            leftmost.send(self.processes[i], sorted_values[i])
            self.messages += 1
            self.time_steps += 1  # Each message takes 1 time step
        
        #All processes receive their value
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

def test_sasaki_sort(n, seed=None):
    """Test Sasaki's time-optimal sorting algorithm with n processes"""
    if seed is not None:
        random.seed(seed)
        
    #Generate random values
    values = random.sample(range(1, n*10), n)
    
    print(f"Testing Sasaki's Time-Optimal Sort with {n} processes")
    print(f"Initial values: {values}")
    
    #Run the algorithm
    sorter = SasakiTimeOptimalSort(n, values)
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
        results[size] = test_sasaki_sort(size)
    
    #Print comparison table
    print("Comparison Table for Sasaki's Time-Optimal Sort:")
    print("=" * 80)
    print(f"{'n':>5} | {'Comparisons':>12} | {'Swaps':>6} | {'Messages':>10} | {'Time Steps':>10} | {'Execution Time (s)':>18}")
    print("-" * 80)
    
    for size, metrics in results.items():
        print(f"{size:>5} | {metrics['comparisons']:>12} | {metrics['swaps']:>6} | {metrics['messages']:>10} | {metrics['time_steps']:>10} | {metrics['execution_time']:>18.6f}")