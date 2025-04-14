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
    
    def send(self, target, message):
        target.inbox.append(message)
    
    def receive(self):
        if self.inbox:
            return self.inbox.popleft()
        return None

class OddEvenTranspositionSort:
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
        """Execute the odd-even transposition sort algorithm"""
        start_time = time.time()
        
        #For a line of n processes, we need at most n phases
        for phase in range(self.n):
            self.time_steps += 1
            
            #Odd phase: processes with odd indices compare with right neighbor
            self._run_phase(1)
            
            self.time_steps += 1
            
            #Even phase: processes with even indices compare with right neighbor
            self._run_phase(0)
        
        end_time = time.time()
        self.execution_time = end_time - start_time
        
        #Return sorted values
        return [p.value for p in self.processes]
    
    def _run_phase(self, start_idx):
        """Run a phase of the algorithm starting from start_idx"""
        for i in range(start_idx, self.n - 1, 2):
            self._compare_and_swap(i, i + 1)
    
    def _compare_and_swap(self, left_idx, right_idx):
        """Compare values between two adjacent processes and swap if necessary"""
        left_process = self.processes[left_idx]
        right_process = self.processes[right_idx]
        
        #Left process sends its value to right process
        left_process.send(right_process, left_process.value)
        self.messages += 1
        
        #Right process sends its value to left process
        right_process.send(left_process, right_process.value)
        self.messages += 1
        
        #Both processes receive values
        left_received = left_process.receive()
        right_received = right_process.receive()
        
        #Compare values
        self.comparisons += 1
        if left_received > right_received:
            #Swap values
            left_process.value = right_received
            right_process.value = left_received
            self.swaps += 1
    
    def get_metrics(self):
        """Return metrics about the algorithm execution"""
        return {
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "messages": self.messages,
            "time_steps": self.time_steps,
            "execution_time": self.execution_time
        }

def test_odd_even_sort(n, seed=None):
    """Test the odd-even transposition sort algorithm with n processes"""
    if seed is not None:
        random.seed(seed)
        
    #Generate random values
    values = random.sample(range(1, n*10), n)
    
    print(f"Testing Odd-Even Transposition Sort with {n} processes")
    print(f"Initial values: {values}")
    
    #Run the algorithm
    sorter = OddEvenTranspositionSort(n, values)
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
        results[size] = test_odd_even_sort(size)
    
    #Print comparison table
    print("Comparison Table for Odd-Even Transposition Sort:")
    print("=" * 80)
    print(f"{'n':>5} | {'Comparisons':>12} | {'Swaps':>6} | {'Messages':>10} | {'Time Steps':>10} | {'Execution Time (s)':>18}")
    print("-" * 80)
    
    for size, metrics in results.items():
        print(f"{size:>5} | {metrics['comparisons']:>12} | {metrics['swaps']:>6} | {metrics['messages']:>10} | {metrics['time_steps']:>10} | {metrics['execution_time']:>18.6f}")