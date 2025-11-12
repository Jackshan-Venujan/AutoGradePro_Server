"""
Throughput Performance Test
Tests maximum number of submissions that can be graded concurrently.

Run: python test_throughput.py
"""

import sys
import time
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from grading_simulator import GradingSimulator


class ThroughputTest:
    """Test concurrent grading throughput"""
    
    def __init__(self):
        self.results = {
            'metadata': {
                'test_type': 'Throughput Test',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            },
            'test_results': []
        }
    
    def create_submission(self, submission_id, num_questions=10):
        """Create a test submission"""
        submission = {}
        marking_scheme = {}
        
        for i in range(1, num_questions + 1):
            submission[i] = f"Answer {i} for submission {submission_id}"
            marking_scheme[i] = {
                'answer_text': f'Answer {i}',
                'marks': 10,
                'grading_type': 'one-word',
                'case_sensitive': False
            }
        
        return submission, marking_scheme
    
    def grade_one_submission(self, submission_id, submission, marking_scheme):
        """Grade a single submission"""
        grader = GradingSimulator()
        start_time = time.time()
        
        try:
            total_score = 0
            max_score = 0
            
            for q_id in submission:
                if q_id not in marking_scheme:
                    continue
                
                scheme = marking_scheme[q_id]
                student_answer = submission[q_id]
                correct_answer = scheme['answer_text']
                marks = scheme['marks']
                max_score += marks
                
                result = grader.grade_one_word(
                    student_answer, correct_answer,
                    scheme.get('case_sensitive', False)
                )
                
                if result['is_correct']:
                    total_score += marks
            
            elapsed = time.time() - start_time
            
            return {
                'submission_id': submission_id,
                'success': True,
                'time': elapsed,
                'score': total_score,
                'max_score': max_score
            }
        except Exception as e:
            elapsed = time.time() - start_time
            return {
                'submission_id': submission_id,
                'success': False,
                'time': elapsed,
                'error': str(e)
            }
    
    def test_concurrent_grading(self, num_submissions, num_workers, num_questions=10):
        """Test grading multiple submissions concurrently"""
        print(f"\n{'='*70}")
        print(f"Testing: {num_submissions} submissions with {num_workers} workers")
        print(f"         ({num_questions} questions per submission)")
        print(f"{'='*70}")
        
        # Create submissions
        print(f"\nPreparing {num_submissions} submissions...")
        submissions_data = []
        for i in range(1, num_submissions + 1):
            submission, marking_scheme = self.create_submission(i, num_questions)
            submissions_data.append((i, submission, marking_scheme))
        
        # Grade concurrently
        print(f"Grading {num_submissions} submissions with {num_workers} concurrent workers...")
        start_time = time.time()
        results = []
        
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [
                executor.submit(self.grade_one_submission, sid, sub, ms)
                for sid, sub, ms in submissions_data
            ]
            
            for future in as_completed(futures):
                results.append(future.result())
        
        total_time = time.time() - start_time
        
        # Analyze results
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        if successful:
            times = [r['time'] for r in successful]
            avg_time = statistics.mean(times)
            median_time = statistics.median(times)
            min_time = min(times)
            max_time = max(times)
            std_dev = statistics.stdev(times) if len(times) > 1 else 0
        else:
            avg_time = median_time = min_time = max_time = std_dev = 0
        
        throughput = len(successful) / total_time if total_time > 0 else 0
        
        # Print results
        print(f"\n📊 RESULTS:")
        print(f"{'='*70}")
        print(f"✅ Total Submissions: {num_submissions}")
        print(f"✅ Successful: {len(successful)}")
        print(f"❌ Failed: {len(failed)}")
        print(f"⏱️  Total Time: {total_time:.3f} seconds")
        
        if successful:
            print(f"\n📈 Timing Statistics (per submission):")
            print(f"  Average: {avg_time:.3f}s")
            print(f"  Median:  {median_time:.3f}s")
            print(f"  Min:     {min_time:.3f}s")
            print(f"  Max:     {max_time:.3f}s")
            print(f"  Std Dev: {std_dev:.3f}s")
        
        print(f"\n🚀 Throughput:")
        print(f"  {throughput:.2f} submissions/second")
        print(f"  {throughput * 60:.0f} submissions/minute")
        print(f"  {throughput * 3600:.0f} submissions/hour")
        
        # Success rate
        success_rate = (len(successful) / num_submissions * 100) if num_submissions > 0 else 0
        print(f"\n✅ Success Rate: {success_rate:.1f}%")
        
        # Store results
        result = {
            'num_submissions': num_submissions,
            'num_workers': num_workers,
            'num_questions': num_questions,
            'total_time_seconds': round(total_time, 3),
            'successful': len(successful),
            'failed': len(failed),
            'success_rate_percent': round(success_rate, 1),
            'throughput': {
                'per_second': round(throughput, 2),
                'per_minute': round(throughput * 60, 0),
                'per_hour': round(throughput * 3600, 0)
            },
            'timing': {
                'avg_seconds': round(avg_time, 3),
                'median_seconds': round(median_time, 3),
                'min_seconds': round(min_time, 3),
                'max_seconds': round(max_time, 3),
                'std_dev_seconds': round(std_dev, 3)
            }
        }
        
        self.results['test_results'].append(result)
        
        return result
    
    def run_all_tests(self):
        """Run all throughput tests"""
        print("\n" + "="*70)
        print("AUTOGRADEPRO - THROUGHPUT PERFORMANCE TEST")
        print("="*70)
        print("\nMeasuring maximum concurrent grading capacity...")
        
        # Test configurations: (num_submissions, num_workers, num_questions)
        test_configs = [
            (10, 2, 10, "Small Load: 10 submissions, 2 workers"),
            (20, 5, 10, "Medium Load: 20 submissions, 5 workers"),
            (50, 10, 10, "Large Load: 50 submissions, 10 workers"),
        ]
        
        for num_subs, num_workers, num_qs, description in test_configs:
            print(f"\n{'='*70}")
            print(f"Test: {description}")
            print(f"{'='*70}")
            self.test_concurrent_grading(num_subs, num_workers, num_qs)
        
        # Generate summary
        self.generate_summary()
        
        # Save results
        self.save_results()
    
    def generate_summary(self):
        """Generate summary of all tests"""
        print("\n" + "="*70)
        print("THROUGHPUT TEST SUMMARY")
        print("="*70)
        
        print("\n📊 Performance Comparison:")
        print("-" * 70)
        print(f"{'Submissions':<15} {'Workers':<10} {'Success%':<12} {'Throughput/sec':<18} {'Throughput/hour':<15}")
        print("-" * 70)
        
        for result in self.results['test_results']:
            print(f"{result['num_submissions']:<15} "
                  f"{result['num_workers']:<10} "
                  f"{result['success_rate_percent']:<12.1f} "
                  f"{result['throughput']['per_second']:<18.2f} "
                  f"{result['throughput']['per_hour']:<15.0f}")
        
        # Find best throughput
        best_result = max(self.results['test_results'], key=lambda x: x['throughput']['per_second'])
        
        print("\n🏆 Best Performance:")
        print("-" * 70)
        print(f"  Configuration: {best_result['num_submissions']} submissions, {best_result['num_workers']} workers")
        print(f"  Throughput: {best_result['throughput']['per_second']:.2f} submissions/second")
        print(f"  Success Rate: {best_result['success_rate_percent']:.1f}%")
        
        print("\n💡 Capacity Estimates:")
        print("-" * 70)
        max_throughput = best_result['throughput']['per_second']
        print(f"  Maximum sustainable throughput: ~{max_throughput:.2f} submissions/second")
        print(f"  Daily capacity (24h): ~{max_throughput * 3600 * 24:.0f} submissions")
        print(f"  Weekly capacity: ~{max_throughput * 3600 * 24 * 7:.0f} submissions")
        
        print("\n✅ Performance Assessment:")
        print("-" * 70)
        if max_throughput >= 1.0:
            print("  🟢 EXCELLENT: ≥1 submission/second")
        elif max_throughput >= 0.5:
            print("  🟢 VERY GOOD: ≥0.5 submissions/second")
        elif max_throughput >= 0.3:
            print("  🟡 GOOD: ≥0.3 submissions/second")
        elif max_throughput >= 0.1:
            print("  🟡 ACCEPTABLE: ≥0.1 submissions/second")
        else:
            print("  🔴 SLOW: <0.1 submissions/second - optimization needed")
        
        # Store summary
        self.results['summary'] = {
            'max_throughput_per_second': round(max_throughput, 2),
            'best_configuration': {
                'submissions': best_result['num_submissions'],
                'workers': best_result['num_workers']
            },
            'daily_capacity': round(max_throughput * 3600 * 24, 0)
        }
    
    def save_results(self):
        """Save results to JSON file"""
        output_dir = Path(__file__).parent / 'results'
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / 'throughput_results.json'
        
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")


def main():
    """Main entry point"""
    tester = ThroughputTest()
    tester.run_all_tests()
    
    print("\n" + "="*70)
    print("✅ THROUGHPUT TEST COMPLETE")
    print("="*70)


if __name__ == '__main__':
    main()
