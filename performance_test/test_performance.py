"""
Performance Benchmarking Script
Measures execution time, throughput, and resource usage of grading methods.
Tests under various loads and with different data sizes.
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime
from statistics import mean, stdev, median
import gc

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from grading_simulator import GradingSimulator

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    class Fore:
        CYAN = GREEN = YELLOW = RED = ""
    class Style:
        RESET_ALL = ""


class PerformanceTester:
    """
    Performance benchmarking for all grading methods
    """
    
    def __init__(self, iterations=100):
        """
        Initialize performance tester
        
        Args:
            iterations: Number of iterations for each test
        """
        self.iterations = iterations
        self.grader = GradingSimulator()
        self.results = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "iterations": iterations
            },
            "one_word": {},
            "short_phrase": {},
            "list": {},
            "numerical": {}
        }
    
    def benchmark_function(self, func, *args, **kwargs):
        """
        Benchmark a function with multiple iterations
        
        Returns:
            dict: Performance metrics
        """
        times = []
        
        # Warm-up run
        func(*args, **kwargs)
        
        # Timed runs
        for _ in range(self.iterations):
            gc.collect()  # Clean up before each run
            
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            
            times.append((end - start) * 1000)  # Convert to ms
        
        return {
            "mean_ms": mean(times),
            "median_ms": median(times),
            "std_dev_ms": stdev(times) if len(times) > 1 else 0,
            "min_ms": min(times),
            "max_ms": max(times),
            "total_time_s": sum(times) / 1000,
            "operations_per_second": 1000 / mean(times) if mean(times) > 0 else 0,
            "all_times_ms": times
        }
    
    def test_one_word_performance(self):
        """Benchmark one-word grading"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print("Benchmarking One-Word Grading")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        test_cases = [
            ("Paris", "Paris", False),
            ("PARIS", "paris", False),
            ("London", "Paris", False),
            ("Au", "Au", True),
        ]
        
        for student, correct, case_sens in test_cases:
            print(f"Testing: '{student}' vs '{correct}' (case_sensitive={case_sens})")
            
            metrics = self.benchmark_function(
                self.grader.grade_one_word,
                student, correct, case_sens
            )
            
            print(f"  Mean: {metrics['mean_ms']:.4f} ms")
            print(f"  Median: {metrics['median_ms']:.4f} ms")
            print(f"  Ops/sec: {metrics['operations_per_second']:.0f}")
            print()
            
            self.results["one_word"][f"{student}_vs_{correct}"] = metrics
        
        # Calculate aggregate metrics
        all_times = []
        for test_data in self.results["one_word"].values():
            all_times.extend(test_data["all_times_ms"])
        
        self.results["one_word"]["aggregate"] = {
            "mean_ms": mean(all_times),
            "median_ms": median(all_times),
            "std_dev_ms": stdev(all_times) if len(all_times) > 1 else 0,
            "min_ms": min(all_times),
            "max_ms": max(all_times)
        }
    
    def test_short_phrase_performance(self):
        """Benchmark short-phrase AI grading"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print("Benchmarking Short-Phrase (AI) Grading")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}Note: This test uses Ollama AI and will be slower{Style.RESET_ALL}\n")
        
        # Use fewer iterations for AI tests
        original_iterations = self.iterations
        self.iterations = min(10, self.iterations)
        
        test_cases = [
            (
                "Plants convert sunlight into energy",
                "Photosynthesis is the process where plants convert sunlight into energy",
                "What is photosynthesis?"
            ),
            (
                "AI mimics human thinking",
                "Artificial intelligence is the simulation of human intelligence by machines",
                "Define artificial intelligence"
            ),
        ]
        
        for student, correct, question in test_cases:
            print(f"Testing: '{student[:50]}...'")
            
            try:
                metrics = self.benchmark_function(
                    self.grader.grade_short_phrase,
                    student, correct, question, 0.7
                )
                
                print(f"  Mean: {metrics['mean_ms']:.2f} ms")
                print(f"  Median: {metrics['median_ms']:.2f} ms")
                print(f"  Ops/sec: {metrics['operations_per_second']:.2f}")
                print()
                
                test_key = f"phrase_{len(self.results['short_phrase']) + 1}"
                self.results["short_phrase"][test_key] = metrics
            
            except Exception as e:
                print(f"  {Fore.RED}Error: {e}{Style.RESET_ALL}\n")
                self.results["short_phrase"]["error"] = str(e)
        
        # Restore original iterations
        self.iterations = original_iterations
        
        # Calculate aggregate if we have results
        if len(self.results["short_phrase"]) > 0 and "error" not in self.results["short_phrase"]:
            all_times = []
            for key, test_data in self.results["short_phrase"].items():
                if isinstance(test_data, dict) and "all_times_ms" in test_data:
                    all_times.extend(test_data["all_times_ms"])
            
            if all_times:
                self.results["short_phrase"]["aggregate"] = {
                    "mean_ms": mean(all_times),
                    "median_ms": median(all_times),
                    "std_dev_ms": stdev(all_times) if len(all_times) > 1 else 0,
                    "min_ms": min(all_times),
                    "max_ms": max(all_times)
                }
    
    def test_list_performance(self):
        """Benchmark list grading"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print("Benchmarking List Grading")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        test_cases = [
            (["Red", "Blue", "Yellow"], ["Red", "Blue", "Yellow"], False, True),
            (["Blue", "Red", "Yellow"], ["Red", "Blue", "Yellow"], False, True),
            (["Spring", "Summer", "Fall", "Winter"], ["Spring", "Summer", "Fall", "Winter"], True, True),
            (["Africa", "Asia", "Europe", "North America", "South America"], 
             ["Africa", "Asia", "Europe", "North America", "South America"], False, True),
        ]
        
        for student, correct, order_sens, partial in test_cases:
            print(f"Testing: {len(student)} items (order_sensitive={order_sens})")
            
            metrics = self.benchmark_function(
                self.grader.grade_list,
                student, correct, order_sens, partial, False
            )
            
            print(f"  Mean: {metrics['mean_ms']:.4f} ms")
            print(f"  Median: {metrics['median_ms']:.4f} ms")
            print(f"  Ops/sec: {metrics['operations_per_second']:.0f}")
            print()
            
            test_key = f"list_{len(student)}_items_order_{order_sens}"
            self.results["list"][test_key] = metrics
        
        # Calculate aggregate metrics
        all_times = []
        for test_data in self.results["list"].values():
            all_times.extend(test_data["all_times_ms"])
        
        self.results["list"]["aggregate"] = {
            "mean_ms": mean(all_times),
            "median_ms": median(all_times),
            "std_dev_ms": stdev(all_times) if len(all_times) > 1 else 0,
            "min_ms": min(all_times),
            "max_ms": max(all_times)
        }
    
    def test_numerical_performance(self):
        """Benchmark numerical grading"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print("Benchmarking Numerical Grading")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        test_cases = [
            (4, 4, False, 0, None),
            (3.14, 3.14, True, 1, None),
            (100, 100, True, 0, {"min": 99, "max": 101, "tolerance_percent": 0}),
            (78.5, 78.5, True, 1, None),
        ]
        
        for student, correct, range_sens, tolerance, answer_range in test_cases:
            print(f"Testing: {student} vs {correct} (range_sensitive={range_sens})")
            
            metrics = self.benchmark_function(
                self.grader.grade_numerical,
                student, correct, range_sens, tolerance, answer_range
            )
            
            print(f"  Mean: {metrics['mean_ms']:.4f} ms")
            print(f"  Median: {metrics['median_ms']:.4f} ms")
            print(f"  Ops/sec: {metrics['operations_per_second']:.0f}")
            print()
            
            test_key = f"{student}_vs_{correct}"
            self.results["numerical"][test_key] = metrics
        
        # Calculate aggregate metrics
        all_times = []
        for test_data in self.results["numerical"].values():
            all_times.extend(test_data["all_times_ms"])
        
        self.results["numerical"]["aggregate"] = {
            "mean_ms": mean(all_times),
            "median_ms": median(all_times),
            "std_dev_ms": stdev(all_times) if len(all_times) > 1 else 0,
            "min_ms": min(all_times),
            "max_ms": max(all_times)
        }
    
    def generate_report(self):
        """Generate performance report"""
        print(f"\n\n{Fore.CYAN}{'='*60}")
        print("PERFORMANCE BENCHMARK REPORT")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        print(f"Iterations per test: {self.iterations}")
        print()
        
        for grading_type in ["one_word", "short_phrase", "list", "numerical"]:
            data = self.results[grading_type]
            
            if "aggregate" not in data:
                continue
            
            agg = data["aggregate"]
            
            print(f"\n{Fore.YELLOW}{grading_type.upper().replace('_', ' ')}:{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}Mean Time: {agg['mean_ms']:.4f} ms{Style.RESET_ALL}")
            print(f"  Median Time: {agg['median_ms']:.4f} ms")
            print(f"  Std Dev: {agg['std_dev_ms']:.4f} ms")
            print(f"  Min Time: {agg['min_ms']:.4f} ms")
            print(f"  Max Time: {agg['max_ms']:.4f} ms")
            
            if agg['mean_ms'] > 0:
                ops_per_sec = 1000 / agg['mean_ms']
                print(f"  {Fore.CYAN}Throughput: {ops_per_sec:.0f} operations/second{Style.RESET_ALL}")
        
        # Save to JSON
        output_path = Path(__file__).parent / "results" / "performance_report.json"
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n{Fore.GREEN}✓ Detailed results saved to: {output_path}{Style.RESET_ALL}\n")
        
        return self.results
    
    def run_all_tests(self):
        """Run all performance benchmarks"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print("AutoGradePro Performance Testing Framework")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        print(f"Iterations: {self.iterations}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        try:
            self.test_one_word_performance()
            self.test_numerical_performance()
            self.test_list_performance()
            
            print(f"\n{Fore.YELLOW}Starting AI performance tests (this may take a while)...{Style.RESET_ALL}")
            self.test_short_phrase_performance()
            
            return self.generate_report()
        
        except KeyboardInterrupt:
            print(f"\n\n{Fore.RED}Testing interrupted by user{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"\n\n{Fore.RED}Error during testing: {e}{Style.RESET_ALL}")
            import traceback
            traceback.print_exc()
            return None


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Performance testing for AutoGradePro grading methods")
    parser.add_argument("--iterations", type=int, default=100, help="Number of iterations per test (default: 100)")
    
    args = parser.parse_args()
    
    tester = PerformanceTester(iterations=args.iterations)
    results = tester.run_all_tests()
    
    if results:
        print(f"\n{Fore.GREEN}✓ All benchmarks completed successfully!{Style.RESET_ALL}\n")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
