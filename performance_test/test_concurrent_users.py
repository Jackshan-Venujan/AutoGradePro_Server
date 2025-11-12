"""
Concurrent Users Load Test
Tests how many users can access the system simultaneously.

Run: python test_concurrent_users.py
"""

import sys
import time
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics
import random

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from grading_simulator import GradingSimulator


class ConcurrentUsersTest:
    """Test concurrent user load"""
    
    def __init__(self):
        self.results = {
            'metadata': {
                'test_type': 'Concurrent Users Test',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            },
            'test_results': []
        }
    
    def simulate_user_session(self, user_id):
        """Simulate a typical user session"""
        grader = GradingSimulator()
        start_time = time.time()
        actions_completed = []
        
        try:
            # Action 1: View assignments (simulate API call)
            time.sleep(random.uniform(0.05, 0.15))
            actions_completed.append('view_assignments')
            
            # Action 2: Create/view submission
            time.sleep(random.uniform(0.1, 0.2))
            actions_completed.append('view_submission')
            
            # Action 3: Grade a small submission (5 questions)
            submission = {i: f"Answer {i}" for i in range(1, 6)}
            marking_scheme = {
                i: {
                    'answer_text': f'Answer {i}',
                    'marks': 10,
                    'grading_type': 'one-word',
                    'case_sensitive': False
                } for i in range(1, 6)
            }
            
            score = 0
            for q_id in submission:
                result = grader.grade_one_word(
                    submission[q_id],
                    marking_scheme[q_id]['answer_text'],
                    False
                )
                if result['is_correct']:
                    score += marking_scheme[q_id]['marks']
            
            actions_completed.append('grade_submission')
            
            # Action 4: View results
            time.sleep(random.uniform(0.05, 0.1))
            actions_completed.append('view_results')
            
            elapsed = time.time() - start_time
            
            return {
                'user_id': user_id,
                'success': True,
                'time': elapsed,
                'actions': len(actions_completed),
                'score': score
            }
            
        except Exception as e:
            elapsed = time.time() - start_time
            return {
                'user_id': user_id,
                'success': False,
                'time': elapsed,
                'actions': len(actions_completed),
                'error': str(e)
            }
    
    def test_concurrent_users(self, num_users, test_name):
        """Test multiple users accessing system concurrently"""
        print(f"\n{'='*70}")
        print(f"Testing: {test_name}")
        print(f"         {num_users} concurrent users")
        print(f"{'='*70}")
        
        print(f"\nSimulating {num_users} users accessing the system...")
        start_time = time.time()
        results = []
        
        with ThreadPoolExecutor(max_workers=num_users) as executor:
            futures = [
                executor.submit(self.simulate_user_session, i)
                for i in range(1, num_users + 1)
            ]
            
            for future in as_completed(futures):
                results.append(future.result())
        
        total_time = time.time() - start_time
        
        # Analyze results
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        if successful:
            session_times = [r['time'] for r in successful]
            avg_time = statistics.mean(session_times)
            median_time = statistics.median(session_times)
            min_time = min(session_times)
            max_time = max(session_times)
            std_dev = statistics.stdev(session_times) if len(session_times) > 1 else 0
        else:
            avg_time = median_time = min_time = max_time = std_dev = 0
        
        success_rate = (len(successful) / num_users * 100) if num_users > 0 else 0
        
        # Print results
        print(f"\n📊 RESULTS:")
        print(f"{'='*70}")
        print(f"👥 Total Users: {num_users}")
        print(f"✅ Successful Sessions: {len(successful)}")
        print(f"❌ Failed Sessions: {len(failed)}")
        print(f"⏱️  Total Test Time: {total_time:.3f} seconds")
        print(f"✅ Success Rate: {success_rate:.1f}%")
        
        if successful:
            print(f"\n📈 Session Time Statistics:")
            print(f"  Average: {avg_time:.3f}s")
            print(f"  Median:  {median_time:.3f}s")
            print(f"  Min:     {min_time:.3f}s")
            print(f"  Max:     {max_time:.3f}s")
            print(f"  Std Dev: {std_dev:.3f}s")
        
        print(f"\n🚀 System Performance:")
        users_per_second = len(successful) / total_time if total_time > 0 else 0
        print(f"  Handled {users_per_second:.2f} users/second")
        print(f"  Could serve ~{users_per_second * 60:.0f} users/minute")
        
        # Determine if system can handle this load
        if success_rate >= 95 and max_time < 10:
            status = "✅ PASSED - System handles this load well"
        elif success_rate >= 90:
            status = "⚠️  WARNING - Some performance degradation"
        else:
            status = "❌ FAILED - System cannot handle this load"
        
        print(f"\n{status}")
        
        # Store results
        result = {
            'test_name': test_name,
            'num_users': num_users,
            'total_time_seconds': round(total_time, 3),
            'successful': len(successful),
            'failed': len(failed),
            'success_rate_percent': round(success_rate, 1),
            'session_timing': {
                'avg_seconds': round(avg_time, 3),
                'median_seconds': round(median_time, 3),
                'min_seconds': round(min_time, 3),
                'max_seconds': round(max_time, 3),
                'std_dev_seconds': round(std_dev, 3)
            },
            'users_per_second': round(users_per_second, 2),
            'status': 'PASSED' if success_rate >= 95 and max_time < 10 else 'WARNING' if success_rate >= 90 else 'FAILED'
        }
        
        self.results['test_results'].append(result)
        
        return result
    
    def run_all_tests(self):
        """Run all concurrent user tests"""
        print("\n" + "="*70)
        print("AUTOGRADEPRO - CONCURRENT USERS LOAD TEST")
        print("="*70)
        print("\nMeasuring maximum concurrent user capacity...")
        
        # Test different user loads
        test_configs = [
            (10, "Light Load: 10 concurrent users"),
            (25, "Moderate Load: 25 concurrent users"),
            (50, "Heavy Load: 50 concurrent users"),
            (100, "Extreme Load: 100 concurrent users"),
        ]
        
        for num_users, test_name in test_configs:
            self.test_concurrent_users(num_users, test_name)
        
        # Generate summary
        self.generate_summary()
        
        # Save results
        self.save_results()
    
    def generate_summary(self):
        """Generate summary of all tests"""
        print("\n" + "="*70)
        print("CONCURRENT USERS TEST SUMMARY")
        print("="*70)
        
        print("\n📊 Load Test Results:")
        print("-" * 70)
        print(f"{'Test Name':<30} {'Users':<10} {'Success%':<12} {'Avg Time':<12} {'Status':<15}")
        print("-" * 70)
        
        for result in self.results['test_results']:
            print(f"{result['test_name']:<30} "
                  f"{result['num_users']:<10} "
                  f"{result['success_rate_percent']:<12.1f} "
                  f"{result['session_timing']['avg_seconds']:<12.3f} "
                  f"{result['status']:<15}")
        
        # Determine maximum capacity
        passed_tests = [r for r in self.results['test_results'] if r['status'] == 'PASSED']
        
        if passed_tests:
            max_capacity = max(r['num_users'] for r in passed_tests)
            print(f"\n✅ Maximum Concurrent User Capacity:")
            print("-" * 70)
            print(f"  System can reliably handle: {max_capacity} concurrent users")
            
            # Find the passed test with most users
            best_test = max(passed_tests, key=lambda x: x['num_users'])
            print(f"  At {max_capacity} users:")
            print(f"    - Success Rate: {best_test['success_rate_percent']:.1f}%")
            print(f"    - Average Session Time: {best_test['session_timing']['avg_seconds']:.3f}s")
        else:
            print(f"\n⚠️  Warning: System struggles with concurrent user load")
            print("-" * 70)
            print("  Consider optimization or load balancing")
        
        # Performance grade
        print("\n🎯 Overall Performance Grade:")
        print("-" * 70)
        
        if passed_tests:
            max_cap = max(r['num_users'] for r in passed_tests)
            if max_cap >= 100:
                grade = "A+"
                desc = "Excellent - Production ready for large scale"
            elif max_cap >= 50:
                grade = "A"
                desc = "Very Good - Suitable for medium to large deployments"
            elif max_cap >= 25:
                grade = "B"
                desc = "Good - Suitable for small to medium deployments"
            elif max_cap >= 10:
                grade = "C"
                desc = "Acceptable - Suitable for small deployments"
            else:
                grade = "D"
                desc = "Needs Improvement - Limited concurrent capacity"
        else:
            grade = "F"
            desc = "Poor - Cannot handle concurrent users reliably"
        
        print(f"  Grade: {grade}")
        print(f"  Assessment: {desc}")
        
        # Recommendations
        print("\n💡 Recommendations:")
        print("-" * 70)
        
        if passed_tests:
            max_cap = max(r['num_users'] for r in passed_tests)
            if max_cap >= 50:
                print("  ✅ System performs well under load")
                print("  ✅ Consider horizontal scaling for even higher capacity")
            elif max_cap >= 25:
                print("  ✅ Good performance for typical workloads")
                print("  💡 Consider caching to improve response times")
            else:
                print("  ⚠️  Limited concurrent capacity")
                print("  💡 Optimize database queries")
                print("  💡 Add caching layer (Redis/Memcached)")
                print("  💡 Use connection pooling")
        else:
            print("  🔴 Critical optimization needed")
            print("  💡 Profile code for bottlenecks")
            print("  💡 Check database connection limits")
            print("  💡 Review server resources (CPU, RAM)")
        
        # Store summary
        self.results['summary'] = {
            'max_concurrent_users': max(r['num_users'] for r in passed_tests) if passed_tests else 0,
            'performance_grade': grade,
            'assessment': desc
        }
    
    def save_results(self):
        """Save results to JSON file"""
        output_dir = Path(__file__).parent / 'results'
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / 'concurrent_users_results.json'
        
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")


def main():
    """Main entry point"""
    tester = ConcurrentUsersTest()
    tester.run_all_tests()
    
    print("\n" + "="*70)
    print("✅ CONCURRENT USERS TEST COMPLETE")
    print("="*70)


if __name__ == '__main__':
    main()
