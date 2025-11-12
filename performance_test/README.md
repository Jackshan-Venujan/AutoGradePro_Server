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
├── PERFORMANCE_TEST_REPORT.md         # 📊 Complete performance evidence report
├── requirements.txt                    # Test dependencies
├── test_data/                          # Test case data
│   ├── grading_test_cases.json        # Comprehensive test cases
│   └── sample_submissions/            # Sample submission files
├── results/                            # Test results and reports
│   ├── accuracy_report.json           # Detailed accuracy metrics
│   ├── performance_report.json        # Performance metrics
│   ├── grading_speed_results.json     # 🚀 Speed test results
│   ├── throughput_results.json        # 📈 Throughput test results
│   ├── concurrent_users_results.json  # 👥 User capacity test results
│   └── summary_report.html            # Visual HTML report
├── grading_simulator.py               # Standalone grading functions
├── test_accuracy.py                   # Accuracy testing script
├── test_performance.py                # Performance benchmarking script
├── test_grading_speed.py              # 🚀 NEW: Grading speed test
├── test_throughput.py                 # 📈 NEW: Concurrent grading test
├── test_concurrent_users.py           # 👥 NEW: User load test
├── run_all_tests.py                   # Master accuracy test runner
└── run_all_performance_tests.py       # 🆕 Master performance test runner
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

### 🆕 Performance Tests (Speed, Throughput, Users)

**Run All Performance Tests (Recommended):**
```bash
python run_all_performance_tests.py
```

**Run Individual Performance Tests:**
```bash
# Test grading speed
python test_grading_speed.py

# Test concurrent grading throughput
python test_throughput.py

# Test concurrent user capacity
python test_concurrent_users.py
```

### Accuracy Tests

**Run All Accuracy Tests:**
```bash
python run_all_tests.py
```

**Run Individual Accuracy Tests:**
```bash
# Test grading accuracy
python test_accuracy.py

# Test performance benchmarks
python test_performance.py
```

## Test Output

### 1. Console Output
- Real-time test progress
- Pass/Fail indicators
- Timing information
- 🆕 Performance metrics (questions/sec, submissions/sec, users/sec)

### 2. JSON Reports

**Accuracy Reports:**
- `results/accuracy_report.json` - Detailed accuracy metrics
- `results/performance_report.json` - Performance benchmarks

**🆕 Performance Reports:**
- `results/grading_speed_results.json` - Speed test results with capacity estimates
- `results/throughput_results.json` - Concurrent grading throughput metrics
- `results/concurrent_users_results.json` - User load test results

### 3. Summary Reports
- `results/summary_report.html` - Visual report with charts
- `PERFORMANCE_TEST_REPORT.md` - 🆕 **Complete performance evidence report**
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

### Accuracy Tests

#### One-Word Grading
- **Expected Accuracy**: >99%
- **Expected Avg Time**: <1ms

#### Short-Phrase (AI) Grading
- **Expected Accuracy**: >85%
- **Expected Avg Time**: 100-500ms

#### List Grading
- **Expected Accuracy**: >95%
- **Expected Avg Time**: <5ms

#### Numerical Grading
- **Expected Accuracy**: >99%
- **Expected Avg Time**: <1ms

### 🆕 Performance Tests (Proven Results)

#### Grading Speed
- **Achieved**: 116,508 questions/second ✅
- **Time per Question**: <0.001 seconds
- **Grade**: 🟢 EXCELLENT

#### Throughput
- **Achieved**: 9,723 submissions/second ✅
- **Daily Capacity**: ~840 million submissions
- **Grade**: 🟢 EXCELLENT

#### Concurrent Users
- **Achieved**: 100+ simultaneous users ✅
- **Success Rate**: 100.0%
- **Grade**: A+ (Production Ready)

*See `PERFORMANCE_TEST_REPORT.md` for complete evidence and detailed metrics*

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
