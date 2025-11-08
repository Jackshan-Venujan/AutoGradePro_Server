"""
Standalone Grading Simulator
Replicates the grading functions from the main project for independent testing.
This file is completely self-contained and doesn't depend on the Django project.
"""

import re
import ollama


class GradingSimulator:
    """
    Simulates all grading methods used in AutoGradePro
    """
    
    def __init__(self, ollama_host=None):
        """
        Initialize the grading simulator
        
        Args:
            ollama_host: Optional Ollama host URL
        """
        self.ollama_host = ollama_host
    
    def grade_one_word(self, student_answer, correct_answer, case_sensitive=False):
        """
        Grade one-word answers with exact matching
        
        Args:
            student_answer: Student's answer
            correct_answer: Correct answer
            case_sensitive: Whether to match case
            
        Returns:
            dict: Grading result with is_correct, score_percentage, explanation
        """
        if not student_answer or not correct_answer:
            return {
                "is_correct": False,
                "score_percentage": 0.0,
                "explanation": "Missing answer"
            }
        
        student_ans = str(student_answer).strip()
        correct_ans = str(correct_answer).strip()
        
        if not case_sensitive:
            student_ans = student_ans.lower()
            correct_ans = correct_ans.lower()
        
        is_correct = student_ans == correct_ans
        
        return {
            "is_correct": is_correct,
            "score_percentage": 100.0 if is_correct else 0.0,
            "explanation": "Exact match" if is_correct else "Not an exact match"
        }
    
    def grade_short_phrase(self, student_answer, correct_answer, question_text=None, 
                          semantic_threshold=0.7):
        """
        Grade short phrases using AI semantic similarity
        
        Args:
            student_answer: Student's answer
            correct_answer: Correct answer
            question_text: Question for context
            semantic_threshold: Minimum confidence for correct
            
        Returns:
            dict: Grading result with is_correct, score_percentage, explanation, confidence
        """
        if not student_answer or not correct_answer:
            return {
                "is_correct": False,
                "score_percentage": 0.0,
                "confidence": 0.0,
                "explanation": "Missing answer"
            }
        
        is_match, confidence = self._check_meaning_with_ollama(
            student_answer, correct_answer, question_text, semantic_threshold
        )
        
        return {
            "is_correct": is_match,
            "score_percentage": confidence * 100,
            "confidence": confidence,
            "explanation": f"Semantic similarity: {confidence:.2f}"
        }
    
    def grade_list(self, student_answer, correct_answer, order_sensitive=False,
                  partial_matching=True, case_sensitive=False):
        """
        Grade list-based answers
        
        Args:
            student_answer: List of student's items
            correct_answer: List of correct items
            order_sensitive: Whether order matters
            partial_matching: Whether to give partial credit
            case_sensitive: Whether to match case
            
        Returns:
            dict: Grading result with is_correct, score_percentage, explanation, matched_items
        """
        if not student_answer or not correct_answer:
            return {
                "is_correct": False,
                "score_percentage": 0.0,
                "matched_items": [],
                "explanation": "Missing answer"
            }
        
        # Normalize lists
        if isinstance(student_answer, str):
            student_list = self._normalize_list_items(student_answer, case_sensitive)
        else:
            student_list = [str(item).strip() for item in student_answer]
            if not case_sensitive:
                student_list = [item.lower() for item in student_list]
        
        if isinstance(correct_answer, str):
            correct_list = self._normalize_list_items(correct_answer, case_sensitive)
        else:
            correct_list = [str(item).strip() for item in correct_answer]
            if not case_sensitive:
                correct_list = [item.lower() for item in correct_list]
        
        if order_sensitive:
            # Order matters - check sequence
            if student_list == correct_list:
                return {
                    "is_correct": True,
                    "score_percentage": 100.0,
                    "matched_items": student_list,
                    "explanation": "Perfect match with correct order"
                }
            elif partial_matching:
                lcs_length = self._longest_common_subsequence(student_list, correct_list)
                score = (lcs_length / len(correct_list)) * 100
                
                return {
                    "is_correct": score >= 100.0,
                    "score_percentage": score,
                    "matched_items": [],
                    "explanation": f"Partial match: {score:.1f}% (order matters)"
                }
            else:
                return {
                    "is_correct": False,
                    "score_percentage": 0.0,
                    "matched_items": [],
                    "explanation": "Lists don't match (order matters)"
                }
        else:
            # Order doesn't matter - use sets
            student_set = set(student_list)
            correct_set = set(correct_list)
            
            matched = student_set.intersection(correct_set)
            
            if student_set == correct_set:
                return {
                    "is_correct": True,
                    "score_percentage": 100.0,
                    "matched_items": list(matched),
                    "explanation": "Perfect match (all items present)"
                }
            elif partial_matching:
                score = (len(matched) / len(correct_set)) * 100
                
                return {
                    "is_correct": score >= 100.0,
                    "score_percentage": score,
                    "matched_items": list(matched),
                    "explanation": f"Partial match: {len(matched)}/{len(correct_set)} items correct"
                }
            else:
                return {
                    "is_correct": False,
                    "score_percentage": 0.0,
                    "matched_items": list(matched),
                    "explanation": "Lists don't match"
                }
    
    def grade_numerical(self, student_answer, correct_answer, range_sensitive=False,
                       tolerance_percent=0, answer_range=None):
        """
        Grade numerical answers
        
        Args:
            student_answer: Student's numerical answer
            correct_answer: Correct numerical answer
            range_sensitive: Whether to use range/tolerance
            tolerance_percent: Tolerance percentage
            answer_range: Dict with min, max, tolerance_percent
            
        Returns:
            dict: Grading result with is_correct, score_percentage, explanation, difference
        """
        try:
            # Clean and convert to float (remove commas and all spaces)
            student_str = str(student_answer).replace(',', '').replace(' ', '')
            correct_str = str(correct_answer).replace(',', '').replace(' ', '')
            
            # Check exact string match first
            if student_str == correct_str:
                return {
                    "is_correct": True,
                    "score_percentage": 100.0,
                    "difference": 0.0,
                    "explanation": f"Exact match: {student_str}"
                }
            
            student_value = float(student_str)
            correct_value = float(correct_str)
            difference = abs(student_value - correct_value)
            
            # Range-based checking
            if range_sensitive:
                if answer_range:
                    min_val = float(answer_range.get("min", float('-inf')))
                    max_val = float(answer_range.get("max", float('inf')))
                    tolerance = answer_range.get("tolerance_percent", tolerance_percent)
                else:
                    min_val = float('-inf')
                    max_val = float('inf')
                    tolerance = tolerance_percent
                
                # Check if value is in range
                if min_val <= student_value <= max_val:
                    return {
                        "is_correct": True,
                        "score_percentage": 100.0,
                        "difference": difference,
                        "explanation": f"Value {student_value} is within range [{min_val}, {max_val}]"
                    }
                
                # Check tolerance if specified
                if tolerance > 0:
                    tolerance_amount = correct_value * (tolerance / 100)
                    lower_bound = correct_value - tolerance_amount
                    upper_bound = correct_value + tolerance_amount
                    
                    if lower_bound <= student_value <= upper_bound:
                        return {
                            "is_correct": True,
                            "score_percentage": 100.0,
                            "difference": difference,
                            "explanation": f"Within {tolerance}% tolerance of {correct_value}"
                        }
                
                return {
                    "is_correct": False,
                    "score_percentage": 0.0,
                    "difference": difference,
                    "explanation": f"Value {student_value} outside acceptable range/tolerance"
                }
            else:
                # Exact match with floating point precision
                epsilon = max(0.0001, abs(correct_value) * 1e-9)
                
                if difference <= epsilon:
                    return {
                        "is_correct": True,
                        "score_percentage": 100.0,
                        "difference": difference,
                        "explanation": f"Exact numerical match: {student_value}"
                    }
                else:
                    return {
                        "is_correct": False,
                        "score_percentage": 0.0,
                        "difference": difference,
                        "explanation": f"Expected {correct_value}, got {student_value} (diff: {difference})"
                    }
        
        except (ValueError, TypeError) as e:
            return {
                "is_correct": False,
                "score_percentage": 0.0,
                "difference": None,
                "explanation": f"Invalid numerical format: {str(e)}"
            }
    
    def _check_meaning_with_ollama(self, student_answer, correct_answer, 
                                   question_text=None, threshold=0.7):
        """
        Use Ollama to check semantic similarity
        
        Returns:
            tuple: (is_match, confidence_score)
        """
        system_prompt = "You are an AI assistant for grading papers. Your task is to compare student answers with correct answers."
        
        if question_text:
            user_prompt = f"Question: {question_text}\n\nStudent Answer: {student_answer}\n\nCorrect Answer: {correct_answer}\n\nAre these answers semantically equivalent? Return a number from 0 to 1 representing the confidence score, where 1 means identical meaning and 0 means completely different meaning. Only return the number."
        else:
            user_prompt = f"Student Answer: {student_answer}\n\nCorrect Answer: {correct_answer}\n\nReturn a number from 0 to 1 representing how similar these answers are in meaning, where 1 means identical and 0 means completely different. Only return the number."
        
        try:
            response = ollama.chat(
                model="qwen2.5:1.5b",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
            )
            
            content = response["message"]["content"].strip()
            
            # Extract number from response
            match = re.search(r'\b([01](?:\.\d+)?|0\.\d+)\b', content)
            if match:
                confidence = float(match.group(1))
            else:
                confidence = 1.0 if "true" in content.lower() else 0.0
            
            return (confidence >= threshold, confidence)
        
        except Exception as e:
            print(f"Error connecting to Ollama: {e}")
            return (False, 0.0)
    
    def _normalize_list_items(self, answer, case_sensitive=False):
        """
        Normalize a list answer string into individual items
        """
        # Detect bullet points or numbered lists
        if re.search(r'\n\s*[-•*]\s+', '\n' + answer) or re.search(r'\n\s*\d+\.\s+', '\n' + answer):
            items = []
            for line in answer.split('\n'):
                match = re.match(r'\s*(?:[-•*]|\d+\.)\s+(.*)', line)
                if match and match.group(1).strip():
                    items.append(match.group(1).strip())
            if items:
                if not case_sensitive:
                    return [item.lower() for item in items]
                return items
        
        # Split on common delimiters
        items = re.split(r'[,;\t\n]+', answer)
        
        # Clean each item
        normalized = []
        for item in items:
            clean = re.sub(r'^\s*[-•*]\s+|^\s*\d+\.\s+', '', item)
            clean = re.sub(r'\s+', ' ', clean).strip()
            if clean:
                normalized.append(clean.lower() if not case_sensitive else clean)
        
        return normalized
    
    def _longest_common_subsequence(self, list1, list2):
        """
        Calculate longest common subsequence length for ordered list comparison
        """
        m, n = len(list1), len(list2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if list1[i-1] == list2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[m][n]


# Convenience function for quick testing
def quick_test():
    """
    Quick test of all grading methods
    """
    grader = GradingSimulator()
    
    print("=== Quick Grading Test ===\n")
    
    # Test one-word
    result = grader.grade_one_word("Paris", "paris", case_sensitive=False)
    print(f"One-Word Test: {result}\n")
    
    # Test numerical
    result = grader.grade_numerical(3.14, 3.14, range_sensitive=False)
    print(f"Numerical Test: {result}\n")
    
    # Test list
    result = grader.grade_list(
        ["Red", "Blue", "Yellow"],
        ["red", "blue", "yellow"],
        order_sensitive=False,
        case_sensitive=False
    )
    print(f"List Test: {result}\n")
    
    print("Note: Short-phrase test requires Ollama running")


if __name__ == "__main__":
    quick_test()
