"""
Example Usage - Grading Simulator Demo
Shows how to use the grading simulator for quick tests
"""

from grading_simulator import GradingSimulator

def print_result(title, result):
    """Pretty print a result"""
    print(f"\n{title}")
    print("=" * 60)
    for key, value in result.items():
        if key != "all_times_ms":  # Skip raw timing data
            print(f"  {key}: {value}")


def main():
    """Run example grading tests"""
    print("\n" + "="*60)
    print("AutoGradePro Grading Simulator - Example Usage")
    print("="*60)
    
    # Initialize the grader
    grader = GradingSimulator()
    
    # ========== Example 1: One-Word Grading ==========
    print("\n\n📝 Example 1: One-Word Grading")
    print("-" * 60)
    
    result = grader.grade_one_word(
        student_answer="Paris",
        correct_answer="paris",
        case_sensitive=False
    )
    print_result("Test: 'Paris' vs 'paris' (case insensitive)", result)
    
    result = grader.grade_one_word(
        student_answer="Au",
        correct_answer="au",
        case_sensitive=True
    )
    print_result("Test: 'Au' vs 'au' (case sensitive)", result)
    
    # ========== Example 2: List Grading ==========
    print("\n\n📋 Example 2: List Grading")
    print("-" * 60)
    
    result = grader.grade_list(
        student_answer=["Red", "Blue", "Yellow"],
        correct_answer=["red", "blue", "yellow"],
        order_sensitive=False,
        partial_matching=True,
        case_sensitive=False
    )
    print_result("Test: Primary colors (order doesn't matter)", result)
    
    result = grader.grade_list(
        student_answer=["Spring", "Summer", "Fall", "Winter"],
        correct_answer=["Spring", "Summer", "Fall", "Winter"],
        order_sensitive=True,
        partial_matching=True,
        case_sensitive=False
    )
    print_result("Test: Seasons in order (order matters)", result)
    
    result = grader.grade_list(
        student_answer=["Red", "Blue"],
        correct_answer=["Red", "Blue", "Yellow"],
        order_sensitive=False,
        partial_matching=True,
        case_sensitive=False
    )
    print_result("Test: Partial credit (2 out of 3 correct)", result)
    
    # ========== Example 3: Numerical Grading ==========
    print("\n\n🔢 Example 3: Numerical Grading")
    print("-" * 60)
    
    result = grader.grade_numerical(
        student_answer=4,
        correct_answer=4,
        range_sensitive=False
    )
    print_result("Test: Exact match (4 = 4)", result)
    
    result = grader.grade_numerical(
        student_answer=3.15,
        correct_answer=3.14,
        range_sensitive=True,
        tolerance_percent=1
    )
    print_result("Test: Within 1% tolerance (3.15 vs 3.14)", result)
    
    result = grader.grade_numerical(
        student_answer=100,
        correct_answer=100,
        range_sensitive=True,
        answer_range={"min": 99, "max": 101, "tolerance_percent": 0}
    )
    print_result("Test: Range [99-101], answer=100", result)
    
    result = grader.grade_numerical(
        student_answer="78.5",
        correct_answer=78.5,
        range_sensitive=True,
        tolerance_percent=1
    )
    print_result("Test: String to number (78.5)", result)
    
    # ========== Example 4: Short Phrase (AI) Grading ==========
    print("\n\n🤖 Example 4: Short-Phrase (AI) Grading")
    print("-" * 60)
    print("NOTE: This requires Ollama to be running!")
    print("Starting Ollama tests...\n")
    
    try:
        result = grader.grade_short_phrase(
            student_answer="Plants convert sunlight into energy",
            correct_answer="Photosynthesis is the process where plants convert sunlight into energy",
            question_text="What is photosynthesis?",
            semantic_threshold=0.7
        )
        print_result("Test: Photosynthesis answer (paraphrased)", result)
        
        result = grader.grade_short_phrase(
            student_answer="AI mimics human thinking",
            correct_answer="Artificial intelligence is the simulation of human intelligence by machines",
            question_text="Define artificial intelligence",
            semantic_threshold=0.7
        )
        print_result("Test: AI definition (simplified)", result)
        
    except Exception as e:
        print(f"\n❌ AI grading failed: {e}")
        print("Make sure Ollama is running: ollama serve")
        print("And the model is installed: ollama pull qwen2.5:1.5b")
    
    # ========== Example 5: Complex List (String Input) ==========
    print("\n\n📝 Example 5: List from String Input")
    print("-" * 60)
    
    result = grader.grade_list(
        student_answer="Red, Blue, Yellow",  # Comma-separated string
        correct_answer=["Red", "Blue", "Yellow"],
        order_sensitive=False,
        partial_matching=True,
        case_sensitive=False
    )
    print_result("Test: Comma-separated list", result)
    
    result = grader.grade_list(
        student_answer="1. Red\n2. Blue\n3. Yellow",  # Numbered list
        correct_answer=["Red", "Blue", "Yellow"],
        order_sensitive=False,
        partial_matching=True,
        case_sensitive=False
    )
    print_result("Test: Numbered list format", result)
    
    # ========== Summary ==========
    print("\n\n" + "="*60)
    print("✅ Example demonstrations complete!")
    print("="*60)
    print("\nYou can use these methods in your own code:")
    print("  - grade_one_word(): For exact word matching")
    print("  - grade_short_phrase(): For AI semantic similarity")
    print("  - grade_list(): For multiple item answers")
    print("  - grade_numerical(): For number-based answers")
    print("\nSee grading_simulator.py for full documentation.")
    print()


if __name__ == "__main__":
    main()
