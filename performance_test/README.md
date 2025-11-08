# AutoGradePro Performance Testing Framework

This is a standalone testing framework to measure and validate the accuracy and performance of all grading methods without modifying the main project.

## Grading Methods Tested

1. **One-Word** - Exact matching with case sensitivity options
2. **Short-Phrase (AI)** - Semantic similarity using Ollama AI
3. **List** - Multiple item matching with order and partial credit options
4. **Numerical** - Number matching with tolerance and range support

## Directory Structure

```
performance_test/
├── README.md                           # This file
├── requirements.txt                    # Test dependencies
├── test_data/                          # Test case data
│   ├── grading_test_cases.json        # Comprehensive test cases
│   └── sample_submissions/            # Sample submission files
├── results/                            # Test results and reports
│   ├── accuracy_report.json           # Detailed accuracy metrics
│   ├── performance_report.json        # Performance metrics
│   └── summary_report.html            # Visual HTML report
├── grading_simulator.py               # Standalone grading functions
├── test_accuracy.py                   # Accuracy testing script
├── test_performance.py                # Performance benchmarking script
└── run_all_tests.py                   # Master test runner
```

## Setup Instructions

1. **Install Dependencies**
   ```bash
   cd performance_test
   pip install -r requirements.txt
   ```

2. **Ensure Ollama is Running** (for AI grading tests)
   ```bash
   ollama serve
   ollama pull qwen2.5:1.5b
   ```

## Running Tests

### Run All Tests (Recommended)
```bash
python run_all_tests.py
```

### Run Individual Tests

**Accuracy Testing:**
```bash
python test_accuracy.py
```

**Performance Testing:**
```bash
python test_performance.py
```

## Test Output

### 1. Console Output
- Real-time test progress
- Pass/Fail indicators
- Timing information

### 2. JSON Reports
- `results/accuracy_report.json` - Detailed accuracy metrics
- `results/performance_report.json` - Performance benchmarks

### 3. HTML Report
- `results/summary_report.html` - Visual report with charts
- Open in any web browser

## Understanding Results

### Accuracy Metrics
- **Pass Rate**: % of correct classifications
- **False Positives**: Incorrect answers marked as correct
- **False Negatives**: Correct answers marked as incorrect
- **Precision**: Accuracy of positive predictions
- **Recall**: Coverage of actual positives

### Performance Metrics
- **Average Response Time**: Mean execution time (ms)
- **Min/Max Times**: Range of execution times
- **Standard Deviation**: Consistency of performance
- **Throughput**: Operations per second

## Expected Results

### One-Word Grading
- **Expected Accuracy**: >99%
- **Expected Avg Time**: <1ms

### Short-Phrase (AI) Grading
- **Expected Accuracy**: >85%
- **Expected Avg Time**: 100-500ms

### List Grading
- **Expected Accuracy**: >95%
- **Expected Avg Time**: <5ms

### Numerical Grading
- **Expected Accuracy**: >99%
- **Expected Avg Time**: <1ms

## Customization

### Adding Test Cases
Edit `test_data/grading_test_cases.json` to add your own test cases.

### Adjusting Thresholds
Modify threshold values in `test_accuracy.py` to change pass/fail criteria.

### Performance Benchmarks
Adjust iteration counts in `test_performance.py` for more thorough testing.

## Troubleshooting

**Issue**: Ollama connection errors
**Solution**: Ensure Ollama is running: `ollama serve`

**Issue**: Module import errors
**Solution**: Install dependencies: `pip install -r requirements.txt`

**Issue**: Permission errors
**Solution**: Run with appropriate permissions or check file paths

## Notes

- This framework is completely independent of the main project
- No database connection required
- Safe to run multiple times
- Results are timestamped to avoid overwriting
