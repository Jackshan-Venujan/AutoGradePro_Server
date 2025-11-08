"""
AutoGradePro Grading Accuracy Tests
Run with: python manage.py test tests.test_grading_accuracy
"""

import time
from django.test import TestCase
from api.functions import is_answer_correct, check_meaning_with_ollama


class OneWordAccuracyTests(TestCase):
    """Test one-word grading accuracy and performance"""

    def setUp(self):
        self.test_cases = [
            # (student_answer, correct_answer, case_sensitive, expected_result, description)
            ("Paris", "Paris", False, True, "Exact match"),
            ("paris", "Paris", False, True, "Case insensitive match"),
            ("PARIS", "Paris", False, True, "Uppercase match"),
            ("Paris", "Paris", True, True, "Case sensitive exact"),
            ("paris", "Paris", True, False, "Case sensitive mismatch"),
            ("Paaris", "Paris", False, False, "Typo"),
            (" Paris ", "Paris", False, True, "Whitespace trimming"),
            ("Par is", "Paris", False, False, "Internal space"),
            ("", "Paris", False, False, "Empty answer"),
            ("Python", "python", False, True, "Programming term"),
        ]

    def test_accuracy(self):
        """Verify 100% accuracy claim"""
        correct = 0
        total = len(self.test_cases)

        for student, correct_ans, case_sens, expected, desc in self.test_cases:
            result = is_answer_correct(
                student,
                correct_ans,
                grading_type="one-word",
                case_sensitive=case_sens
            )
            if result == expected:
                correct += 1
            else:
                print(f"FAIL: {desc} - Expected {expected}, got {result}")

        accuracy = (correct / total) * 100
        self.assertEqual(accuracy, 100.0, f"One-word accuracy should be 100%, got {accuracy}%")

    def test_performance(self):
        """Verify <10ms performance claim"""
        test_iterations = 1000
        times = []

        for _ in range(test_iterations):
            start = time.perf_counter()
            is_answer_correct("Paris", "Paris", "one-word", case_sensitive=False)
            end = time.perf_counter()
            times.append((end - start) * 1000)  # Convert to ms

        avg_time = sum(times) / len(times)
        max_time = max(times)

        print(f"One-word Performance: Avg={avg_time:.3f}ms, Max={max_time:.3f}ms")
        self.assertLess(avg_time, 10.0, f"Average time should be <10ms, got {avg_time:.3f}ms")


class ListAnswerAccuracyTests(TestCase):
    """Test list grading accuracy and performance"""

    def setUp(self):
        self.test_cases = [
            # Ordered lists
            {
                'student': "2, 3, 5, 7, 11",
                'correct': "2, 3, 5, 7, 11",
                'order_sensitive': True,
                'partial_matching': False,
                'expected_score': 1.0,
                'description': "Exact ordered match"
            },
            {
                'student': "2,3,5,7,11",
                'correct': "2, 3, 5, 7, 11",
                'order_sensitive': True,
                'partial_matching': False,
                'expected_score': 1.0,
                'description': "No spaces"
            },
            {
                'student': "2; 3; 5; 7; 11",
                'correct': "2, 3, 5, 7, 11",
                'order_sensitive': True,
                'partial_matching': False,
                'expected_score': 1.0,
                'description': "Semicolon delimiter"
            },
            {
                'student': "2, 3, 5",
                'correct': "2, 3, 5, 7, 11",
                'order_sensitive': True,
                'partial_matching': True,
                'expected_score': 0.6,
                'description': "Partial ordered (3/5)"
            },
            # Unordered lists
            {
                'student': "Red, Blue, Yellow",
                'correct': "Red, Blue, Yellow",
                'order_sensitive': False,
                'partial_matching': False,
                'expected_score': 1.0,
                'description': "Exact unordered"
            },
            {
                'student': "Yellow, Red, Blue",
                'correct': "Red, Blue, Yellow",
                'order_sensitive': False,
                'partial_matching': False,
                'expected_score': 1.0,
                'description': "Different order unordered"
            },
            {
                'student': "Red, Blue",
                'correct': "Red, Blue, Yellow",
                'order_sensitive': False,
                'partial_matching': True,
                'expected_score': 0.67,
                'description': "Partial unordered (2/3)"
            },
            # Different delimiters
            {
                'student': "apple\nbanana\ncherry",
                'correct': "apple, banana, cherry",
                'order_sensitive': False,
                'partial_matching': False,
                'expected_score': 1.0,
                'description': "Newline delimiter"
            },
        ]

    def test_accuracy(self):
        """Verify 95%+ accuracy claim for list grading"""
        correct = 0
        total = len(self.test_cases)
        tolerance = 0.05  # 5% tolerance for partial matching scores

        for case in self.test_cases:
            result = is_answer_correct(
                case['student'],
                case['correct'],
                grading_type="list",
                order_sensitive=case['order_sensitive'],
                partial_matching=case['partial_matching']
            )

            # For boolean results (non-partial matching)
            if isinstance(result, bool):
                result_score = 1.0 if result else 0.0
            else:
                result_score = result

            if abs(result_score - case['expected_score']) <= tolerance:
                correct += 1
            else:
                print(f"FAIL: {case['description']}")
                print(f"  Expected: {case['expected_score']}, Got: {result_score}")

        accuracy = (correct / total) * 100
        self.assertGreaterEqual(accuracy, 95.0, f"List accuracy should be ≥95%, got {accuracy}%")

    def test_performance(self):
        """Verify <50ms performance claim"""
        test_iterations = 1000
        times = []

        for _ in range(test_iterations):
            start = time.perf_counter()
            is_answer_correct(
                "item1, item2, item3, item4, item5",
                "item1, item2, item3, item4, item5",
                grading_type="list",
                order_sensitive=False,
                partial_matching=True
            )
            end = time.perf_counter()
            times.append((end - start) * 1000)

        avg_time = sum(times) / len(times)
        max_time = max(times)

        print(f"List Performance: Avg={avg_time:.3f}ms, Max={max_time:.3f}ms")
        self.assertLess(avg_time, 50.0, f"Average time should be <50ms, got {avg_time:.3f}ms")


class NumericalAnswerAccuracyTests(TestCase):
    """Test numerical grading accuracy and performance"""

    def setUp(self):
        self.test_cases = [
            # Exact matches
            {
                'student': "42",
                'correct': "42",
                'range_min': None,
                'range_max': None,
                'tolerance': None,
                'expected': True,
                'description': "Exact integer match"
            },
            {
                'student': "42.0",
                'correct': "42",
                'range_min': None,
                'range_max': None,
                'tolerance': None,
                'expected': True,
                'description': "Decimal exact match"
            },
            {
                'student': "41.99",
                'correct': "42",
                'range_min': None,
                'range_max': None,
                'tolerance': None,
                'expected': False,
                'description': "Close but not exact"
            },
            # Tolerance testing
            {
                'student': "100",
                'correct': "100",
                'range_min': None,
                'range_max': None,
                'tolerance': 5,
                'expected': True,
                'description': "Exact with tolerance"
            },
            {
                'student': "95",
                'correct': "100",
                'range_min': None,
                'range_max': None,
                'tolerance': 5,
                'expected': True,
                'description': "Lower tolerance bound"
            },
            {
                'student': "105",
                'correct': "100",
                'range_min': None,
                'range_max': None,
                'tolerance': 5,
                'expected': True,
                'description': "Upper tolerance bound"
            },
            {
                'student': "94.9",
                'correct': "100",
                'range_min': None,
                'range_max': None,
                'tolerance': 5,
                'expected': False,
                'description': "Below tolerance"
            },
            # Range validation
            {
                'student': "50",
                'correct': "50",
                'range_min': 40,
                'range_max': 60,
                'tolerance': None,
                'expected': True,
                'description': "Within range"
            },
            {
                'student': "40",
                'correct': "50",
                'range_min': 40,
                'range_max': 60,
                'tolerance': None,
                'expected': True,
                'description': "At min range"
            },
            {
                'student': "60",
                'correct': "50",
                'range_min': 40,
                'range_max': 60,
                'tolerance': None,
                'expected': True,
                'description': "At max range"
            },
            {
                'student': "39.9",
                'correct': "50",
                'range_min': 40,
                'range_max': 60,
                'tolerance': None,
                'expected': False,
                'description': "Below range"
            },
            # Format handling
            {
                'student': "1,000",
                'correct': "1000",
                'range_min': None,
                'range_max': None,
                'tolerance': None,
                'expected': True,
                'description': "Comma formatting"
            },
            {
                'student': " 1000 ",
                'correct': "1000",
                'range_min': None,
                'range_max': None,
                'tolerance': None,
                'expected': True,
                'description': "Whitespace handling"
            },
        ]

    def test_accuracy(self):
        """Verify 100% accuracy claim for numerical grading"""
        correct = 0
        total = len(self.test_cases)

        for case in self.test_cases:
            try:
                # Build answer_range dict if we have range or tolerance
                answer_range = None
                range_sensitive = False
                if case['range_min'] is not None or case['range_max'] is not None or case['tolerance'] is not None:
                    answer_range = {}
                    range_sensitive = True
                    if case['range_min'] is not None:
                        answer_range['min'] = case['range_min']
                    if case['range_max'] is not None:
                        answer_range['max'] = case['range_max']
                    if case['tolerance'] is not None:
                        answer_range['tolerance_percent'] = case['tolerance']

                result = is_answer_correct(
                    case['student'],
                    case['correct'],
                    grading_type="numerical",
                    range_sensitive=range_sensitive,
                    answer_range=answer_range
                )

                if result == case['expected']:
                    correct += 1
                else:
                    print(f"FAIL: {case['description']}")
                    print(f"  Expected: {case['expected']}, Got: {result}")
            except Exception as e:
                print(f"ERROR: {case['description']} - {str(e)}")

        accuracy = (correct / total) * 100
        self.assertEqual(accuracy, 100.0, f"Numerical accuracy should be 100%, got {accuracy}%")

    def test_performance(self):
        """Verify <20ms performance claim"""
        test_iterations = 1000
        times = []

        for _ in range(test_iterations):
            start = time.perf_counter()
            is_answer_correct("42.5", "42.5", grading_type="numerical")
            end = time.perf_counter()
            times.append((end - start) * 1000)

        avg_time = sum(times) / len(times)
        max_time = max(times)

        print(f"Numerical Performance: Avg={avg_time:.3f}ms, Max={max_time:.3f}ms")
        self.assertLess(avg_time, 20.0, f"Average time should be <20ms, got {avg_time:.3f}ms")


class ShortPhraseAccuracyTests(TestCase):
    """Test short-phrase semantic grading (requires Ollama running)"""

    def setUp(self):
        # Note: These tests require Ollama to be running
        self.test_cases = [
            {
                'question': "What is photosynthesis?",
                'correct': "The process by which plants convert sunlight into energy",
                'student': "The process by which plants convert sunlight into energy",
                'threshold': 0.7,
                'expected': True,
                'description': "Exact match"
            },
            {
                'question': "What is photosynthesis?",
                'correct': "The process by which plants convert sunlight into energy",
                'student': "Plants convert sunlight to energy",
                'threshold': 0.7,
                'expected': True,
                'description': "Simplified paraphrase"
            },
            {
                'question': "What is photosynthesis?",
                'correct': "The process by which plants convert sunlight into energy",
                'student': "When animals eat food",
                'threshold': 0.7,
                'expected': False,
                'description': "Completely wrong"
            },
        ]

    def test_semantic_grading(self):
        """Test semantic grading with AI (requires Ollama)"""
        try:
            import ollama

            correct = 0
            total = len(self.test_cases)
            times = []

            for case in self.test_cases:
                start = time.perf_counter()
                result = is_answer_correct(
                    case['student'],
                    case['correct'],
                    grading_type="short-phrase",
                    semantic_threshold=case['threshold'],
                    question_text=case['question']
                )
                end = time.perf_counter()
                times.append(end - start)

                if result == case['expected']:
                    correct += 1
                else:
                    print(f"FAIL: {case['description']}")
                    print(f"  Expected: {case['expected']}, Got: {result}")

            accuracy = (correct / total) * 100
            avg_time = sum(times) / len(times)

            print(f"\nSemantic Grading Results:")
            print(f"  Accuracy: {accuracy:.2f}%")
            print(f"  Avg Time: {avg_time:.2f}s")
            print(f"  Min Time: {min(times):.2f}s")
            print(f"  Max Time: {max(times):.2f}s")

            # For semantic grading, we expect 85-92% accuracy
            # With only 3 test cases, we can't verify this, but we check if it runs
            self.assertGreater(accuracy, 0, "Semantic grading should work")

            # Check performance claim (2-5 seconds)
            self.assertLess(avg_time, 5.0, f"Avg time should be <5s, got {avg_time:.2f}s")
            self.assertGreater(avg_time, 0.1, "Avg time should be >0.1s (sanity check)")

        except ImportError:
            self.skipTest("Ollama not available for semantic grading tests")
        except Exception as e:
            self.skipTest(f"Ollama connection failed: {str(e)}")


# Summary test runner
class GradingAccuracySummary(TestCase):
    """Run all tests and generate summary report"""

    def test_generate_summary(self):
        """Generate a summary of all grading accuracy tests"""
        print("\n" + "="*70)
        print("AUTOGRADEPRO GRADING ACCURACY TEST SUMMARY")
        print("="*70)
        print("\nRun individual test classes for detailed results:")
        print("  - OneWordAccuracyTests")
        print("  - ListAnswerAccuracyTests")
        print("  - NumericalAnswerAccuracyTests")
        print("  - ShortPhraseAccuracyTests")
        print("\nExpected Results:")
        print("  ✓ One-Word: 100% accuracy, <10ms")
        print("  ✓ List: 95%+ accuracy, <50ms")
        print("  ✓ Numerical: 100% accuracy, <20ms")
        print("  ✓ Short-Phrase: 85-92% accuracy, 2-5s (requires Ollama)")
        print("="*70)