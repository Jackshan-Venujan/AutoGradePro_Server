# Quick Start Guide - AutoGradePro Performance Testing

## 🚀 Quick Start (3 Steps)

### Windows Users:
```cmd
cd performance_test
run_tests.bat
```

### Linux/Mac Users:
```bash
cd performance_test
chmod +x run_tests.sh
./run_tests.sh
```

### Manual Method:
```bash
cd performance_test
pip install -r requirements.txt
python run_all_tests.py
```

---

## 📋 Prerequisites

1. **Python 3.8+** installed and in PATH
2. **Ollama** running for AI grading tests (optional but recommended)
   ```bash
   ollama serve
   ollama pull qwen2.5:1.5b
   ```

---

## 🧪 What Gets Tested

### ✅ One-Word Grading
- Exact word matching
- Case sensitivity handling
- Special character handling
- **Expected Accuracy**: >99%
- **Expected Speed**: <1ms

### 🤖 Short-Phrase (AI) Grading
- Semantic similarity using Ollama AI
- Context-aware grading
- Paraphrase detection
- **Expected Accuracy**: >85%
- **Expected Speed**: 100-500ms

### 📝 List Grading
- Multi-item matching
- Order sensitivity options
- Partial credit calculation
- **Expected Accuracy**: >95%
- **Expected Speed**: <5ms

### 🔢 Numerical Grading
- Exact number matching
- Tolerance ranges
- Format handling (commas, decimals)
- **Expected Accuracy**: >99%
- **Expected Speed**: <1ms

---

## 📊 Output Reports

After running tests, you'll get:

### 1. Console Output
Real-time test progress with colored indicators:
- ✅ Green = Test passed
- ❌ Red = Test failed
- ⚠️ Yellow = Warning/partial

### 2. JSON Reports
Detailed machine-readable data:
- `results/accuracy_report.json` - All accuracy metrics
- `results/performance_report.json` - All timing data

### 3. HTML Report (Main Report)
Beautiful visual report automatically opens in browser:
- `results/summary_report.html`
- Executive summary
- Detailed metrics per grading type
- Comparison tables
- Performance charts

---

## 🎯 Understanding Results

### Accuracy Metrics Explained

**Accuracy**: Overall correctness percentage
- ≥95% = Excellent ✅
- 85-94% = Good ⚠️
- <85% = Needs Improvement ❌

**Precision**: Of the answers marked correct, how many were actually correct?
- High precision = Few false positives

**Recall**: Of the actually correct answers, how many were marked correct?
- High recall = Few false negatives

**F1 Score**: Harmonic mean of precision and recall
- Balanced measure of accuracy

### Performance Metrics Explained

**Mean Time**: Average execution time per operation

**Median Time**: Middle value (less affected by outliers)

**Std Dev**: Consistency of performance
- Lower = More consistent

**Throughput**: Operations per second
- Higher = Better performance

---

## 🔧 Customization

### Change Number of Iterations
```bash
# Default is 100 iterations
python test_performance.py --iterations 500
```

### Run Only Accuracy Tests
```bash
python test_accuracy.py
```

### Run Only Performance Tests
```bash
python test_performance.py
```

### Add Your Own Test Cases
Edit `test_data/grading_test_cases.json` and add new test cases following the existing format.

---

## 🐛 Troubleshooting

### Issue: "Module not found" errors
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Ollama connection errors
**Solution**: Start Ollama server
```bash
ollama serve
```
Then in another terminal:
```bash
ollama pull qwen2.5:1.5b
```

### Issue: Python not found
**Solution**: Install Python 3.8+ from python.org and add to PATH

### Issue: Permission denied (Linux/Mac)
**Solution**: Make script executable
```bash
chmod +x run_tests.sh
```

---

## 📈 Expected Results Summary

| Grading Method | Accuracy | Avg Speed | Throughput |
|---------------|----------|-----------|------------|
| One-Word      | >99%     | <1ms      | >1000 ops/s |
| Short-Phrase  | >85%     | 100-500ms | 2-10 ops/s  |
| List          | >95%     | <5ms      | >200 ops/s  |
| Numerical     | >99%     | <1ms      | >1000 ops/s |

---

## 💡 Tips

1. **First Run**: The first test run may be slower due to Ollama model loading
2. **AI Tests**: Short-phrase tests take longer due to AI processing
3. **Iterations**: More iterations = more accurate performance data but longer runtime
4. **Ollama**: Ensure Ollama has the model downloaded before running

---

## 📞 Need Help?

If tests fail or results are unexpected:

1. Check that Ollama is running (for AI tests)
2. Verify all dependencies are installed
3. Review the detailed JSON reports for specific failures
4. Check console output for error messages

---

## ✅ Success Criteria

Your grading system is performing well if:

- ✅ All grading types show >95% accuracy (except AI which should be >85%)
- ✅ Response times are under expected thresholds
- ✅ Zero or minimal false positives/negatives
- ✅ Consistent performance (low standard deviation)

---

**Happy Testing! 🎉**
