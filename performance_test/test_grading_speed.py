"""
Grading Speed Performance Test
Tests how fast the system can grade individual submissions of different sizes.

Run: python test_grading_speed.py
"""

import sys
import time
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from grading_simulator import GradingSimulator


class GradingSpeedTest:
    """Test grading speed for different submission sizes"""
    
    def __init__(self):
        self.grader = GradingSimulator()
        self.results = {
            'metadata': {
                'test_type': 'Grading Speed',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            },
            'test_results': []
        }
    
    def create_test_submission(self, num_questions):
        """Create a test submission with specified number of questions"""
        submission = {}
        marking_scheme = {}
        
        for i in range(1, num_questions + 1):
            # Mix of question types
            if i % 4 == 1:
                # One-word question
                submission[i] = "Paris"
                marking_scheme[i] = {
                    'question_text': f'Question {i}',
                    'answer_text': 'Paris',
                    'marks': 10,
                    'grading_type': 'one-word',
                    'case_sensitive': False
                }
            elif i % 4 == 2:
                # Numerical question
                submission[i] = "42"
                marking_scheme[i] = {
                    'question_text': f'Question {i}',
                    'answer_text': '42',
                    'marks': 10,
                    'grading_type': 'numerical',
                    'range_sensitive': False
                }
            elif i % 4 == 3:
                # List question
                submission[i] = "Red, Blue, Yellow"
                marking_scheme[i] = {
                    'question_text': f'Question {i}',
                    'answer_text': 'Red, Blue, Yellow',
                    'marks': 10,
                    'grading_type': 'list',
                    'order_sensitive': False,
                    'partial_matching': True,
                    'case_sensitive': False
                }
            else:
                # Short phrase (without AI for speed)
                submission[i] = "Answer text"
                marking_scheme[i] = {
                    'question_text': f'Question {i}',
                    'answer_text': 'Answer text',
                    'marks': 10,
                    'grading_type': 'one-word',  # Using one-word for faster testing
                    'case_sensitive': False
                }
        
        return submission, marking_scheme
    
    def grade_submission(self, submission, marking_scheme):
        """Grade a submission and return score and time"""
        total_score = 0
        max_score = 0
        
        for q_id in submission:
            if q_id not in marking_scheme:
                continue
            
            scheme = marking_scheme[q_id]
            student_answer = submission[q_id]
            correct_answer = scheme['answer_text']
            grading_type = scheme['grading_type']
            marks = scheme['marks']
            
            max_score += marks
            
            # Grade based on type
            if grading_type == 'one-word':
                result = self.grader.grade_one_word(
                    student_answer, correct_answer, 
                    scheme.get('case_sensitive', False)
                )
                if result['is_correct']:
                    total_score += marks
            
            elif grading_type == 'numerical':
                result = self.grader.grade_numerical(
                    student_answer, correct_answer,
                    scheme.get('range_sensitive', False),
                    scheme.get('tolerance_percent', 0),
                    scheme.get('range', None)
                )
                if result['is_correct']:
                    total_score += marks
            
            elif grading_type == 'list':
                result = self.grader.grade_list(
                    student_answer, correct_answer,
                    scheme.get('order_sensitive', False),
                    scheme.get('partial_matching', True),
                    scheme.get('case_sensitive', False)
                )
                if result['is_correct']:
                    total_score += marks
                elif result.get('score_percentage', 0) > 0:
                    # Partial credit
                    total_score += marks * (result['score_percentage'] / 100)
        
        return total_score, max_score
    
    def test_size(self, num_questions, test_name):
        """Test grading speed for a specific submission size"""
        print(f"\n{'='*70}")
        print(f"Testing: {test_name} ({num_questions} questions)")
        print(f"{'='*70}")
        
        # Create submission
        submission, marking_scheme = self.create_test_submission(num_questions)
        
        # Grade and measure time
        start_time = time.time()
        total_score, max_score = self.grade_submission(submission, marking_scheme)
        elapsed_time = time.time() - start_time
        
        # Calculate metrics
        time_per_question = elapsed_time / num_questions
        percentage = (total_score / max_score * 100) if max_score > 0 else 0
        
        # Print results
        print(f"✅ Questions Graded: {num_questions}")
        print(f"✅ Score: {total_score:.1f}/{max_score} ({percentage:.1f}%)")
        print(f"⏱️  Total Time: {elapsed_time:.3f} seconds")
        print(f"⏱️  Time per Question: {time_per_question:.3f} seconds")
        print(f"🚀 Questions per Second: {num_questions/elapsed_time:.2f}")
        
        # Store results
        result = {
            'test_name': test_name,
            'num_questions': num_questions,
            'total_time_seconds': round(elapsed_time, 3),
            'time_per_question_seconds': round(time_per_question, 3),
            'questions_per_second': round(num_questions/elapsed_time, 2),
            'score': round(total_score, 1),
            'max_score': max_score,
            'percentage': round(percentage, 1)
        }
        
        self.results['test_results'].append(result)
        
        return result
    
    def run_all_tests(self):
        """Run all grading speed tests"""
        print("\n" + "="*70)
        print("AUTOGRADEPRO - GRADING SPEED PERFORMANCE TEST")
        print("="*70)
        print("\nMeasuring how fast the system can grade submissions...")
        
        # Test different submission sizes
        test_sizes = [
            (10, "Small Submission"),
            (25, "Medium Submission"),
            (50, "Large Submission"),
            (100, "Extra Large Submission"),
        ]
        
        for num_questions, test_name in test_sizes:
            self.test_size(num_questions, test_name)
        
        # Generate summary
        self.generate_summary()
        
        # Save results
        self.save_results()
    
    def generate_summary(self):
        """Generate summary of all tests"""
        print("\n" + "="*70)
        print("GRADING SPEED SUMMARY")
        print("="*70)
        
        print("\n📊 Performance by Submission Size:")
        print("-" * 70)
        print(f"{'Size':<20} {'Questions':<12} {'Total Time':<15} {'Per Question':<15} {'Q/s':<10}")
        print("-" * 70)
        
        for result in self.results['test_results']:
            print(f"{result['test_name']:<20} "
                  f"{result['num_questions']:<12} "
                  f"{result['total_time_seconds']:<15.3f} "
                  f"{result['time_per_question_seconds']:<15.3f} "
                  f"{result['questions_per_second']:<10.2f}")
        
        # Calculate average time per question
        avg_time_per_q = sum(r['time_per_question_seconds'] for r in self.results['test_results']) / len(self.results['test_results'])
        
        print("\n💡 Key Metrics:")
        print("-" * 70)
        print(f"Average Time per Question: {avg_time_per_q:.3f} seconds")
        
        # Extrapolate capacity
        print("\n🚀 Estimated Grading Capacity (single thread):")
        print("-" * 70)
        submissions_per_hour = {}
        for size in [10, 25, 50, 100]:
            result = next((r for r in self.results['test_results'] if r['num_questions'] == size), None)
            if result:
                time_per_submission = result['total_time_seconds']
                if time_per_submission > 0:
                    per_hour = 3600 / time_per_submission
                    per_day = per_hour * 24
                    submissions_per_hour[size] = per_hour
                    print(f"  {size:3d} question submissions: ~{per_hour:6.0f}/hour, ~{per_day:7.0f}/day")
                else:
                    submissions_per_hour[size] = 999999
                    print(f"  {size:3d} question submissions: Extremely fast (< 1ms)")
        
        print("\n✅ Performance Assessment:")
        print("-" * 70)
        if avg_time_per_q < 0.1:
            print("  🟢 EXCELLENT: <0.1s per question")
        elif avg_time_per_q < 0.5:
            print("  🟢 VERY GOOD: <0.5s per question")
        elif avg_time_per_q < 1.0:
            print("  🟡 GOOD: <1.0s per question")
        elif avg_time_per_q < 3.0:
            print("  🟡 ACCEPTABLE: <3.0s per question")
        else:
            print("  🔴 SLOW: >3.0s per question - optimization needed")
        
        # Store summary
        self.results['summary'] = {
            'avg_time_per_question': round(avg_time_per_q, 3),
            'capacity_per_hour': {str(k): round(v, 0) for k, v in submissions_per_hour.items()}
        }
    
    def save_results(self):
        """Save results to JSON file"""
        output_dir = Path(__file__).parent / 'results'
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / 'grading_speed_results.json'
        
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")


def main():
    """Main entry point"""
    tester = GradingSpeedTest()
    tester.run_all_tests()
    
    print("\n" + "="*70)
    print("✅ GRADING SPEED TEST COMPLETE")
    print("="*70)


if __name__ == '__main__':
    main()
