# Performance Time Test - Quick Start Guide

## Overview

This folder contains tools to measure **real production grading performance** from your actual API, not simulations.

## Quick Setup (5 minutes)

### Step 1: Add Timing to Backend

Option A - Use the timed views directly:

```python
# In Server/api/urls.py
from performance_time_test.timed_views import TimedGradeSubmissionView, SingleAnswerGradingView

urlpatterns = [
    # ... existing urls ...
    path('grade-timed/<int:assignment_id>/', TimedGradeSubmissionView.as_view(), name='grade-timed'),
    path('grade-single/', SingleAnswerGradingView.as_view(), name='grade-single'),
]
```

Option B - Just add timing to your existing view:

```python
# In Server/api/views.py - Add to your existing GradeSubmissionView
import time

def update(self, request, *args, **kwargs):
    start_time = time.time()
    
    # ... your existing grading code ...
    
    processing_time_ms = (time.time() - start_time) * 1000
    logger.info(f"⏱️  Grading took {processing_time_ms:.2f}ms")
    
    return Response({
        'scores': scores,
        'processing_time_ms': round(processing_time_ms, 2)
    })
```

### Step 2: Add Performance Logger to Frontend

```javascript
// In your main App.js or dashboard component
import { PerformanceLogger } from '../performance_time_test/performance_logger_component';

function App() {
  return (
    <div>
      {/* Your existing components */}
      <PerformanceLogger />
    </div>
  );
}
```

### Step 3: Update Your API Calls

```javascript
// Replace your existing grading API call
import { gradeAnswerWithTiming } from '../performance_time_test/grading_api_with_timing';

// Instead of:
// const result = await gradeAnswer(answerData);

// Use:
const result = await gradeAnswerWithTiming(answerData);
```

### Step 4: Collect Data

1. **Start your Django server**
   ```bash
   cd Server
   python manage.py runserver
   ```

2. **Start your React frontend**
   ```bash
   cd Client
   npm start
   ```

3. **Grade assignments normally**
   - The Performance Logger will appear in bottom-right corner
   - It will automatically collect timing data as you grade

4. **Export metrics**
   - Click "📥 Export Metrics" button
   - Save the JSON file

### Step 5: Analyze Results

```bash
cd performance_time_test
python collect_metrics.py path/to/exported_metrics.json
```

This will:
- Calculate statistics (mean, median, std dev, etc.)
- Generate an HTML report
- Provide text for your abstract

## Quick Test (Without Frontend)

Run this in your browser console while grading:

```javascript
// Run a quick performance test
window.runPerformanceTest()
```

This will:
- Test all question types
- Display timing in console
- Auto-populate the Performance Logger

## What You'll Get

### Console Output:
```
📊 PERFORMANCE ANALYSIS
====================================================
📝 One-Word Matching
  Mean:    0.45ms
  Median:  0.42ms
  Samples: 50

📋 List Comparison
  Mean:    2.34ms
  Median:  2.21ms
  Samples: 30

🔢 Numerical Validation
  Mean:    0.67ms
  Median:  0.63ms
  Samples: 25

🤖 AI Semantic Analysis
  Mean:    2.35s (2345.67ms)
  Median:  2.21s
  Samples: 15
====================================================
```

### HTML Report:
Beautiful report with charts and statistics (opens in browser)

### Abstract Text:
Ready-to-use text for your research paper

## Tips

✅ **Collect at least 20-30 samples per question type** for statistical validity

✅ **Test with real student submissions** for accurate results

✅ **Note your hardware** (CPU, RAM, Ollama model) in your paper

❌ **Don't use Chrome DevTools network timing** (includes too much overhead)

❌ **Don't cherry-pick results** (report the actual measured performance)

## Troubleshooting

**Performance Logger not appearing?**
- Check browser console for errors
- Make sure the component is imported correctly
- Verify CSS is loaded

**No timing data collected?**
- Check that `window.logGrading` is available
- Verify API responses include `processing_time_ms`
- Open browser console to see logs

**Short-phrase grading fails?**
- Make sure Ollama is running: `ollama serve`
- Verify model is installed: `ollama pull qwen2.5:1.5b`

## For Your Abstract

Report these metrics:

```
The automated grading system demonstrates efficient performance:
- One-word matching: <1ms average
- List comparison: 1-5ms average  
- Numerical validation: <1ms average
- AI semantic analysis: 2-5 seconds average*

*Using Ollama qwen2.5:1.5b on [specify hardware]
```

## Need Help?

Check the main README.md in this folder for detailed documentation.
