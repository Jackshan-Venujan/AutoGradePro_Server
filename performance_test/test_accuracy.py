"""
Accuracy Testing Script
Tests all grading methods against comprehensive test cases to measure accuracy.
Generates detailed reports with metrics like precision, recall, false positives/negatives.
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from colorama import Fore, Style, init

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from grading_simulator import GradingSimulator

# Initialize colorama for colored output
init(autoreset=True)


class AccuracyTester:
    """
    Comprehensive accuracy testing for all grading methods
    """
    
    def __init__(self, test_data_path):
        """
        Initialize the accuracy tester
        
        Args:
            test_data_path: Path to test cases JSON file
        """
        self.test_data_path = Path(test_data_path)
        self.grader = GradingSimulator()
        
        # Load test cases
        with open(self.test_data_path, 'r') as f:
            self.test_data = json.load(f)
        
        # Results storage
        self.results = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "test_file": str(self.test_data_path)
            },
            "one_word": {
                "total": 0,
                "correct_predictions": 0,
                "false_positives": 0,
                "false_negatives": 0,
                "true_positives": 0,
                "true_negatives": 0,
                "execution_times": [],
                "test_details": []
            },
            "short_phrase": {
                "total": 0,
                "correct_predictions": 0,
                "within_threshold": 0,
                "false_positives": 0,
                "false_negatives": 0,
                "execution_times": [],
                "confidence_scores": [],
                "test_details": []
            },
            "list": {
                "total": 0,
                "correct_predictions": 0,
                "false_positives": 0,
                "false_negatives": 0,
                "partial_credit_cases": 0,
                "execution_times": [],
                "score_distribution": [],
                "test_details": []
            },
            "numerical": {
                "total": 0,
                "correct_predictions": 0,
                "false_positives": 0,
                "false_negatives": 0,
                "true_positives": 0,
                "true_negatives": 0,
                "execution_times": [],
                "test_details": []
            }
        }
    
    def test_one_word(self):
        """Test one-word grading accuracy"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"Testing One-Word Grading")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        test_cases = self.test_data.get("one_word", {}).get("test_cases", [])
        
        for test_case in test_cases:
            test_id = test_case["id"]
            question = test_case["question"]
            correct_answer = test_case["correct_answer"]
            case_sensitive = test_case.get("case_sensitive", False)
            
            print(f"{Fore.YELLOW}Test {test_id}: {question}{Style.RESET_ALL}")
            print(f"Correct Answer: {correct_answer}")
            print(f"Case Sensitive: {case_sensitive}\n")
            
            for test_input in test_case["test_inputs"]:
                student_answer = test_input["student_answer"]
                expected_correct = test_input["expected_correct"]
                reason = test_input["reason"]
                
                # Time the grading
                start_time = time.perf_counter()
                result = self.grader.grade_one_word(
                    student_answer, correct_answer, case_sensitive
                )
                end_time = time.perf_counter()
                
                execution_time = (end_time - start_time) * 1000  # Convert to ms
                
                # Analyze result
                is_correct = result["is_correct"]
                match = is_correct == expected_correct
                
                # Update statistics
                self.results["one_word"]["total"] += 1
                self.results["one_word"]["execution_times"].append(execution_time)
                
                if match:
                    self.results["one_word"]["correct_predictions"] += 1
                    
                    if expected_correct:
                        self.results["one_word"]["true_positives"] += 1
                    else:
                        self.results["one_word"]["true_negatives"] += 1
                else:
                    if is_correct and not expected_correct:
                        self.results["one_word"]["false_positives"] += 1
                    elif not is_correct and expected_correct:
                        self.results["one_word"]["false_negatives"] += 1
                
                # Store detailed result
                self.results["one_word"]["test_details"].append({
                    "test_id": test_id,
                    "student_answer": student_answer,
                    "expected_correct": expected_correct,
                    "actual_correct": is_correct,
                    "match": match,
                    "reason": reason,
                    "execution_time_ms": execution_time
                })
                
                # Print result
                status_icon = f"{Fore.GREEN}✓" if match else f"{Fore.RED}✗"
                print(f"  {status_icon} '{student_answer}' -> {is_correct} "
                      f"(Expected: {expected_correct}) - {reason} [{execution_time:.4f}ms]{Style.RESET_ALL}")
            
            print()
    
    def test_short_phrase(self):
        """Test short-phrase AI grading accuracy"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"Testing Short-Phrase (AI) Grading")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        test_cases = self.test_data.get("short_phrase", {}).get("test_cases", [])
        
        for test_case in test_cases:
            test_id = test_case["id"]
            question = test_case["question"]
            correct_answer = test_case["correct_answer"]
            semantic_threshold = test_case.get("semantic_threshold", 0.7)
            
            print(f"{Fore.YELLOW}Test {test_id}: {question}{Style.RESET_ALL}")
            print(f"Correct Answer: {correct_answer}")
            print(f"Semantic Threshold: {semantic_threshold}\n")
            
            for test_input in test_case["test_inputs"]:
                student_answer = test_input["student_answer"]
                expected_min = test_input.get("expected_score_min", semantic_threshold)
                expected_max = test_input.get("expected_score_max", 1.0)
                reason = test_input["reason"]
                
                # Time the grading
                start_time = time.perf_counter()
                result = self.grader.grade_short_phrase(
                    student_answer, correct_answer, question, semantic_threshold
                )
                end_time = time.perf_counter()
                
                execution_time = (end_time - start_time) * 1000  # Convert to ms
                
                # Analyze result
                confidence = result["confidence"]
                is_correct = result["is_correct"]
                within_expected_range = expected_min <= confidence <= expected_max
                
                # Update statistics
                self.results["short_phrase"]["total"] += 1
                self.results["short_phrase"]["execution_times"].append(execution_time)
                self.results["short_phrase"]["confidence_scores"].append(confidence)
                
                if within_expected_range:
                    self.results["short_phrase"]["correct_predictions"] += 1
                
                if is_correct:
                    self.results["short_phrase"]["within_threshold"] += 1
                    if expected_min < semantic_threshold:
                        self.results["short_phrase"]["false_positives"] += 1
                else:
                    if expected_min >= semantic_threshold:
                        self.results["short_phrase"]["false_negatives"] += 1
                
                # Store detailed result
                self.results["short_phrase"]["test_details"].append({
                    "test_id": test_id,
                    "student_answer": student_answer,
                    "confidence": confidence,
                    "is_correct": is_correct,
                    "expected_range": [expected_min, expected_max],
                    "within_expected": within_expected_range,
                    "reason": reason,
                    "execution_time_ms": execution_time
                })
                
                # Print result
                status_icon = f"{Fore.GREEN}✓" if within_expected_range else f"{Fore.YELLOW}~"
                print(f"  {status_icon} Confidence: {confidence:.2f} "
                      f"(Expected: {expected_min:.2f}-{expected_max:.2f}) "
                      f"- {reason} [{execution_time:.2f}ms]{Style.RESET_ALL}")
            
            print()
    
    def test_list(self):
        """Test list grading accuracy"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"Testing List Grading")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        test_cases = self.test_data.get("list", {}).get("test_cases", [])
        
        for test_case in test_cases:
            test_id = test_case["id"]
            question = test_case["question"]
            correct_answer = test_case["correct_answer"]
            order_sensitive = test_case.get("order_sensitive", False)
            partial_matching = test_case.get("partial_matching", True)
            case_sensitive = test_case.get("case_sensitive", False)
            
            print(f"{Fore.YELLOW}Test {test_id}: {question}{Style.RESET_ALL}")
            print(f"Correct Answer: {correct_answer}")
            print(f"Order Sensitive: {order_sensitive}, Partial Matching: {partial_matching}\n")
            
            for test_input in test_case["test_inputs"]:
                student_answer = test_input["student_answer"]
                expected_correct = test_input["expected_correct"]
                expected_score = test_input.get("expected_score", 100 if expected_correct else 0)
                reason = test_input["reason"]
                
                # Time the grading
                start_time = time.perf_counter()
                result = self.grader.grade_list(
                    student_answer, correct_answer, order_sensitive, 
                    partial_matching, case_sensitive
                )
                end_time = time.perf_counter()
                
                execution_time = (end_time - start_time) * 1000  # Convert to ms
                
                # Analyze result
                is_correct = result["is_correct"]
                score = result["score_percentage"]
                score_tolerance = 5  # Allow 5% tolerance for rounding
                score_match = abs(score - expected_score) <= score_tolerance
                
                # Update statistics
                self.results["list"]["total"] += 1
                self.results["list"]["execution_times"].append(execution_time)
                self.results["list"]["score_distribution"].append(score)
                
                if score_match:
                    self.results["list"]["correct_predictions"] += 1
                
                if 0 < score < 100:
                    self.results["list"]["partial_credit_cases"] += 1
                
                if is_correct and not expected_correct:
                    self.results["list"]["false_positives"] += 1
                elif not is_correct and expected_correct:
                    self.results["list"]["false_negatives"] += 1
                
                # Store detailed result
                self.results["list"]["test_details"].append({
                    "test_id": test_id,
                    "student_answer": student_answer,
                    "expected_correct": expected_correct,
                    "actual_correct": is_correct,
                    "expected_score": expected_score,
                    "actual_score": score,
                    "score_match": score_match,
                    "matched_items": result["matched_items"],
                    "reason": reason,
                    "execution_time_ms": execution_time
                })
                
                # Print result
                status_icon = f"{Fore.GREEN}✓" if score_match else f"{Fore.YELLOW}~"
                print(f"  {status_icon} Score: {score:.1f}% "
                      f"(Expected: {expected_score}%) "
                      f"- {reason} [{execution_time:.4f}ms]{Style.RESET_ALL}")
            
            print()
    
    def test_numerical(self):
        """Test numerical grading accuracy"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"Testing Numerical Grading")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        test_cases = self.test_data.get("numerical", {}).get("test_cases", [])
        
        for test_case in test_cases:
            test_id = test_case["id"]
            question = test_case["question"]
            correct_answer = test_case["correct_answer"]
            range_sensitive = test_case.get("range_sensitive", False)
            tolerance_percent = test_case.get("tolerance_percent", 0)
            answer_range = test_case.get("range", None)
            
            print(f"{Fore.YELLOW}Test {test_id}: {question}{Style.RESET_ALL}")
            print(f"Correct Answer: {correct_answer}")
            if range_sensitive:
                print(f"Tolerance: {tolerance_percent}%")
                if answer_range:
                    print(f"Range: {answer_range}")
            print()
            
            for test_input in test_case["test_inputs"]:
                student_answer = test_input["student_answer"]
                expected_correct = test_input["expected_correct"]
                reason = test_input["reason"]
                
                # Time the grading
                start_time = time.perf_counter()
                result = self.grader.grade_numerical(
                    student_answer, correct_answer, range_sensitive,
                    tolerance_percent, answer_range
                )
                end_time = time.perf_counter()
                
                execution_time = (end_time - start_time) * 1000  # Convert to ms
                
                # Analyze result
                is_correct = result["is_correct"]
                match = is_correct == expected_correct
                
                # Update statistics
                self.results["numerical"]["total"] += 1
                self.results["numerical"]["execution_times"].append(execution_time)
                
                if match:
                    self.results["numerical"]["correct_predictions"] += 1
                    
                    if expected_correct:
                        self.results["numerical"]["true_positives"] += 1
                    else:
                        self.results["numerical"]["true_negatives"] += 1
                else:
                    if is_correct and not expected_correct:
                        self.results["numerical"]["false_positives"] += 1
                    elif not is_correct and expected_correct:
                        self.results["numerical"]["false_negatives"] += 1
                
                # Store detailed result
                self.results["numerical"]["test_details"].append({
                    "test_id": test_id,
                    "student_answer": student_answer,
                    "expected_correct": expected_correct,
                    "actual_correct": is_correct,
                    "match": match,
                    "difference": result.get("difference"),
                    "reason": reason,
                    "execution_time_ms": execution_time
                })
                
                # Print result
                status_icon = f"{Fore.GREEN}✓" if match else f"{Fore.RED}✗"
                diff_str = f" (diff: {result.get('difference', 'N/A')})" if result.get('difference') is not None else ""
                print(f"  {status_icon} {student_answer} -> {is_correct} "
                      f"(Expected: {expected_correct}) - {reason}{diff_str} [{execution_time:.4f}ms]{Style.RESET_ALL}")
            
            print()
    
    def calculate_metrics(self):
        """Calculate accuracy metrics for each grading type"""
        for grading_type in ["one_word", "short_phrase", "list", "numerical"]:
            data = self.results[grading_type]
            
            if data["total"] == 0:
                continue
            
            # Calculate basic metrics
            if grading_type in ["one_word", "numerical"]:
                tp = data.get("true_positives", 0)
                tn = data.get("true_negatives", 0)
                fp = data.get("false_positives", 0)
                fn = data.get("false_negatives", 0)
                
                # Accuracy
                data["accuracy"] = (tp + tn) / data["total"] * 100 if data["total"] > 0 else 0
                
                # Precision
                data["precision"] = tp / (tp + fp) * 100 if (tp + fp) > 0 else 0
                
                # Recall
                data["recall"] = tp / (tp + fn) * 100 if (tp + fn) > 0 else 0
                
                # F1 Score
                if data["precision"] + data["recall"] > 0:
                    data["f1_score"] = 2 * (data["precision"] * data["recall"]) / (data["precision"] + data["recall"])
                else:
                    data["f1_score"] = 0
            
            elif grading_type == "list":
                data["accuracy"] = data["correct_predictions"] / data["total"] * 100
                data["partial_credit_rate"] = data["partial_credit_cases"] / data["total"] * 100
            
            elif grading_type == "short_phrase":
                data["accuracy"] = data["correct_predictions"] / data["total"] * 100
                data["threshold_pass_rate"] = data["within_threshold"] / data["total"] * 100
                if data["confidence_scores"]:
                    data["avg_confidence"] = sum(data["confidence_scores"]) / len(data["confidence_scores"])
                    data["min_confidence"] = min(data["confidence_scores"])
                    data["max_confidence"] = max(data["confidence_scores"])
            
            # Performance metrics
            if data["execution_times"]:
                data["avg_execution_time_ms"] = sum(data["execution_times"]) / len(data["execution_times"])
                data["min_execution_time_ms"] = min(data["execution_times"])
                data["max_execution_time_ms"] = max(data["execution_times"])
                
                # Calculate standard deviation
                avg = data["avg_execution_time_ms"]
                variance = sum((x - avg) ** 2 for x in data["execution_times"]) / len(data["execution_times"])
                data["std_dev_execution_time_ms"] = variance ** 0.5
    
    def generate_report(self):
        """Generate comprehensive accuracy report"""
        self.calculate_metrics()
        
        print(f"\n\n{Fore.CYAN}{'='*60}")
        print(f"ACCURACY & PERFORMANCE REPORT")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        for grading_type in ["one_word", "short_phrase", "list", "numerical"]:
            data = self.results[grading_type]
            
            if data["total"] == 0:
                continue
            
            print(f"\n{Fore.YELLOW}{grading_type.upper().replace('_', ' ')}:{Style.RESET_ALL}")
            print(f"  Total Tests: {data['total']}")
            
            if grading_type in ["one_word", "numerical"]:
                print(f"  {Fore.GREEN}Accuracy: {data['accuracy']:.2f}%{Style.RESET_ALL}")
                print(f"  Precision: {data['precision']:.2f}%")
                print(f"  Recall: {data['recall']:.2f}%")
                print(f"  F1 Score: {data['f1_score']:.2f}")
                print(f"  True Positives: {data['true_positives']}")
                print(f"  True Negatives: {data['true_negatives']}")
                print(f"  {Fore.RED}False Positives: {data['false_positives']}{Style.RESET_ALL}")
                print(f"  {Fore.RED}False Negatives: {data['false_negatives']}{Style.RESET_ALL}")
            
            elif grading_type == "list":
                print(f"  {Fore.GREEN}Accuracy: {data['accuracy']:.2f}%{Style.RESET_ALL}")
                print(f"  Partial Credit Cases: {data['partial_credit_cases']}")
                print(f"  Partial Credit Rate: {data['partial_credit_rate']:.2f}%")
            
            elif grading_type == "short_phrase":
                print(f"  {Fore.GREEN}Range Accuracy: {data['accuracy']:.2f}%{Style.RESET_ALL}")
                print(f"  Threshold Pass Rate: {data['threshold_pass_rate']:.2f}%")
                print(f"  Average Confidence: {data.get('avg_confidence', 0):.2f}")
                print(f"  Confidence Range: [{data.get('min_confidence', 0):.2f}, {data.get('max_confidence', 0):.2f}]")
            
            print(f"\n  {Fore.CYAN}Performance:{Style.RESET_ALL}")
            print(f"  Average Time: {data['avg_execution_time_ms']:.4f} ms")
            print(f"  Min Time: {data['min_execution_time_ms']:.4f} ms")
            print(f"  Max Time: {data['max_execution_time_ms']:.4f} ms")
            print(f"  Std Dev: {data['std_dev_execution_time_ms']:.4f} ms")
            print()
        
        # Save to JSON
        output_path = Path(__file__).parent / "results" / "accuracy_report.json"
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n{Fore.GREEN}✓ Detailed results saved to: {output_path}{Style.RESET_ALL}\n")
        
        return self.results
    
    def run_all_tests(self):
        """Run all accuracy tests"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"AutoGradePro Accuracy Testing Framework")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        print(f"Test Data: {self.test_data_path}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        try:
            self.test_one_word()
            self.test_numerical()
            self.test_list()
            
            print(f"\n{Fore.YELLOW}Note: Running AI tests (may take longer)...{Style.RESET_ALL}")
            self.test_short_phrase()
            
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
    test_data_path = Path(__file__).parent / "test_data" / "grading_test_cases.json"
    
    if not test_data_path.exists():
        print(f"{Fore.RED}Error: Test data file not found: {test_data_path}{Style.RESET_ALL}")
        return 1
    
    tester = AccuracyTester(test_data_path)
    results = tester.run_all_tests()
    
    if results:
        print(f"\n{Fore.GREEN}✓ All tests completed successfully!{Style.RESET_ALL}\n")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
