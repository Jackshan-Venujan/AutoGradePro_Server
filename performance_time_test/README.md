# Performance Time Test - Real Production Timing Measurement

This folder contains tools to measure **actual grading performance** from real API calls, not simulations.

## Purpose

Collect scientifically valid performance metrics suitable for your abstract/research paper by measuring:
- Server-side processing time (algorithm performance)
- Network overhead
- Statistics by question type (one-word, list, numerical, short-phrase)

## Files

### Backend (Django API)
- `timed_views.py` - Enhanced API views with detailed timing
- `timed_functions.py` - Grading functions with performance instrumentation
- `performance_logger.py` - Utility for logging and aggregating metrics

### Frontend (React/JavaScript)
- `performance_logger_component.jsx` - React component for displaying real-time metrics
- `grading_api_with_timing.js` - API client with timing measurements
- `performance_logger.css` - Styling for the performance logger UI

### Data Collection
- `collect_metrics.py` - Script to aggregate and analyze collected metrics
- `export_metrics.html` - Standalone page to visualize metrics

## Setup Instructions

### 1. Backend Setup (Django)

Add timing to your existing grading views:

```python
# In Server/api/views.py
from performance_time_test.timed_views import TimedGradeSubmissionView

# Or patch your existing view with timing
```

### 2. Frontend Setup (React)

```javascript
// Import the performance logger
import { PerformanceLogger } from './performance_time_test/performance_logger_component';
import { gradeAnswerWithTiming } from './performance_time_test/grading_api_with_timing';

// Add to your component
<PerformanceLogger />
```

### 3. Collect Data

1. Start your Django server
2. Open your React frontend
3. Grade real assignments (various question types)
4. Watch the Performance Logger component
5. Click "Export Metrics" to download JSON data

### 4. Generate Report

```bash
cd performance_time_test
python collect_metrics.py path/to/exported_metrics.json
```

## Expected Output

```
📊 Performance Metrics Report
====================================================
One-Word Matching:
  Average: 0.45 ms
  Min: 0.21 ms
  Max: 1.23 ms
  Count: 50

List Comparison:
  Average: 2.34 ms
  Min: 1.12 ms
  Max: 4.56 ms
  Count: 30

Numerical Validation:
  Average: 0.67 ms
  Min: 0.34 ms
  Max: 1.89 ms
  Count: 25

Short-Phrase (AI):
  Average: 2345.67 ms (2.35 seconds)
  Min: 1876.23 ms
  Max: 3456.78 ms
  Count: 15
====================================================
```

## For Your Abstract

Use these metrics to report:
- Algorithm performance (server-side timing)
- Scalability characteristics
- Question type breakdown

**Do NOT report:**
- Browser network timing (includes too much overhead)
- End-to-end UI response time

## Notes

- Short-phrase grading requires Ollama to be running
- Times vary based on hardware specifications
- Collect at least 20-30 samples per question type for statistical validity
- Report both average and range (min-max) in your abstract
